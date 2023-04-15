'''
Created on Apr 12, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import math
from amaranth import Signal, Elaboratable, Module, Const
from amaranth.build import Platform
from amaranth.sim import Delay

from neptune.in_clock import ClockOptions, ClockName

from neptune.sims.runner import runSimulator

from neptune.edgedetect import EdgeDetect

class PulseCounter(Elaboratable):
    '''
        PulseCounter... counts pulses.  
        Input pulses are sanitized by an edge detector and then counted for as
        long as specified samplingDurationSeconds, then reported.
        
        The number of clock ticks for this duration depends on clock frequency.
        Clock frequency is configured using the clock_config bits.
        
        
        @see: in_clock for valid clock rates and corresponding bit settings
    '''
    
    def __init__(self, synchronizerNumStages:int=2, 
                 samplingDurationSeconds:float=1.0):
        
        self.samplingDurationSeconds = samplingDurationSeconds
        
        
        # we'll define a clock count register that is big enough to hold
        # the highest possible (valid) clock value
        maxClockCountPossible = ClockOptions.frequencyToTicksOver(ClockOptions.maxFrequencySupported(), 
                                                                  samplingDurationSeconds)
                                                                  
        
        self.maxClocksCount = Const(maxClockCountPossible)
        
        # synch num stages param, for embedded edge detector
        self.synchronizer_num_stages = synchronizerNumStages
        
        
        
        self.input = Signal()
        
        # clock configuration bits
        self.clock_config = Signal(ClockOptions.num_bits_required())
        
        # how many bits can we ever need to count this clock
        self.count_bits = math.ceil(math.log2(maxClockCountPossible + 1))
        
        # output
        # pulse count can at max ever be the highest clock count we can get to
        self.pulseCount = Signal(self.count_bits)
        
        
        
    def ports(self):
        return [self.input, self.output]
    
    def elaborate(self, platform:Platform):
        m = Module()
        
        edgeDetector = EdgeDetect(self.synchronizer_num_stages)
        m.submodules.edge_detect =  edgeDetector
        
        
        singlePeriodClockCount = Signal(self.count_bits) # how many clocks to count for
        clockCount = Signal(self.count_bits) # the running clock count
        runningPulseCount = Signal(self.count_bits) # the running input pulse count from edge detector
        
        # simple wire to tie embedded edge detector input to our input
        # this makes it basically one signal
        m.d.comb += edgeDetector.input.eq(self.input)
        
        # we increment clock count on every singgle tick
        m.d.sync += clockCount.eq(clockCount + 1)
        
        # how long do we keep counting?  Depends on clock config
        with m.Switch(self.clock_config):
            for cset in [ClockName.Clock1KHz, ClockName.Clock2KHz, 
                         ClockName.Clock3277Hz, ClockName.Clock4KHz]:
                with m.Case(cset):
                    m.d.sync += singlePeriodClockCount.eq(ClockOptions.frequencyToTicksOver(ClockOptions.frequencyHz(cset), self.samplingDurationSeconds))
                
        
        # check if we're done counting pulses
        with m.If(clockCount == singlePeriodClockCount):
            # yes we've counted pulses long enough, report result
            m.d.sync += [
                
                    clockCount.eq(0),
                    self.pulseCount.eq(runningPulseCount)
                
                ]
        with m.Else():
            # no, we are still counting pulses
            with m.If(clockCount == 0):
                # actually, we just started a new period, reset pulse count
                with m.If(edgeDetector.output): # but don't miss a beat
                    m.d.sync += runningPulseCount.eq(1)
                with m.Else():
                    m.d.sync += runningPulseCount.eq(0)
                    
            with m.Else():
                # we count any time the edge detector says 1
                with m.If(edgeDetector.output):
                    m.d.sync += runningPulseCount.eq(runningPulseCount + 1)
            
        return m
    
    
def test():
    m = Module() # top
    m.submodules.pulsecounter = dut = PulseCounter(samplingDurationSeconds=1.0)
    
    def clockInput(durationSecs:float, frequencyHz:int):
        periodTime = 1/frequencyHz
        times = math.ceil(durationSecs/periodTime)
        for _ in range(times):
            yield dut.input.eq(1)
            yield Delay(periodTime/2)
            yield dut.input.eq(0)
            yield Delay(periodTime/2)
            
    def countPulsesAt1kHz():
        # set the clock freq bits
        yield dut.clock_config.eq(ClockName.Clock1KHz)
        
        yield from clockInput(2, 110)
        yield from clockInput(1.1, 300)
        yield dut.clock_config.eq(ClockName.Clock2KHz)
        yield from clockInput(2.3, 300)
        yield dut.clock_config.eq(ClockName.Clock4KHz)
        yield from clockInput(4.1, 300)
        yield dut.clock_config.eq(ClockName.Clock3277Hz)
        yield from clockInput(4.1, 300)
        
        
    runSimulator(m, 'pulsecounter', [dut.input, dut.clock_config, dut.pulseCount], 
                 [countPulsesAt1kHz], clockFreq=1e3)


if __name__ == "__main__":
    # allow us to run this directly
    from amaranth.cli import main
    Test = True
    if (Test):
        test()
    else:
        m = Module() # top level
        m.submodules.pulsecounter = dev = PulseCounter()
        main(m, ports=dev.ports())



