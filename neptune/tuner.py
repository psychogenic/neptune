'''
Created on Apr 12, 2023

The main module that glues all the bits together into a 
coherently functioning system.

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
from amaranth import Signal, Elaboratable, Module, Cat
from amaranth import ClockDomain, ClockSignal

from amaranth.build import Platform
from amaranth.build import Pins, Resource, Subsignal, Attrs


from amaranth.sim import Delay

from neptune.discriminator import Discriminator
from neptune.display.display import DualSevenSegmentDisplay
from neptune.notes import Tuning, StandardGuitarTuning
from neptune.pulsecounter import PulseCounter
from neptune.in_clock import ClockOptions, ClockName


from neptune.sims.runner import runSimulator
from neptune.neptune_config import DevPlatform



class Neptune(Elaboratable):
    '''
        Neptune is our tuner/top module.
        
        It is constructed by passing in the Tuning (set of frequencies of 
        interest) and the sampling duration (time to count inputs), and 
        in elaborate() instantiates and ties together all the submodules.
    
    '''
    
    def __init__(self,  
                 usingTuning:Tuning=StandardGuitarTuning,
                 samplingDurationSeconds:float = 1.0,
                 inputSynchronizerNumStages:int = 2):
        
        
        self.tuning = usingTuning
        self.samplingDurationSeconds = samplingDurationSeconds
        self.inputSynchronizerNumStages = inputSynchronizerNumStages
        
        # inputs
        self.input_pulses = Signal()
        self.clock_config = Signal(ClockOptions.num_bits_required())
        
        # outputs
        self.displaySegments = Signal(8)
        self.displaySelect = Signal()
        
        
    def ports(self):
        return [self.input_pulses, self.displaySegments, self.displaySelect]
    

    def elaborate(self, platform:Platform):
        m = Module()
        
        # input -> counter
        inputPulseCounter = PulseCounter(synchronizerNumStages=self.inputSynchronizerNumStages, 
                                         samplingDurationSeconds=self.samplingDurationSeconds)
        
        # counter -> discriminator
        discrim = Discriminator(usingTuning=self.tuning, samplingDurationSeconds=self.samplingDurationSeconds)
        
        # discriminater -> output display
        display = DualSevenSegmentDisplay(self.tuning)
        
        m.submodules.pulsecounter = inputPulseCounter
        m.submodules.discriminator = discrim 
        m.submodules.display = display  
        
        
        # hook everything up with straight-up wires (combinatorial) so 
        # signals go to/from the right places
        m.d.comb += [
            inputPulseCounter.input.eq(self.input_pulses),
            inputPulseCounter.clock_config.eq(self.clock_config),
            discrim.edge_count.eq(inputPulseCounter.pulseCount),
            display.valueNote.eq(discrim.note),
            display.valueProxim.eq(Cat(discrim.match_exact, discrim.match_high, discrim.match_far)),
            self.displaySegments.eq(display.segments),
            self.displaySelect.eq(display.proximitySelect)
            
            ]
        
        
        # can also run this to build/burn and FPGA tester
        self.wireForPlatform(m, platform) 
        
        return m
        
        
    
    def wireForPlatform(self, m:Module, platform:Platform):
        if platform is None or platform.device != 'iCE40HX1K':
            return 
        
        # these values are all specific to the iCE40HX1K dev platform 
        # I'm using.
        pmod1 = ('pmod', 1) # j1
        pmod2 = ('pmod', 6) # j6
        
        platform.add_resources([
           Resource('dualdisp', 0, 
                    # these subsignals are pins 1 and 2 of the PMOD connector
                    # not pins 1,2 of the FPGA (these are mapped in the 
                    # platform definition file), e.g. in ice40_hx1k_blink_evn it's
                    # Connector("pmod",  1, "10  9  8  7 - -  4  3  2  1 - -"), # J1
                    # so pin 10 and 9.
                    Subsignal('ae', Pins('7', conn=pmod1, dir='o')),
                    Subsignal('af', Pins('8', conn=pmod1, dir='o')),
                    Subsignal('ag', Pins('9', conn=pmod1, dir='o')),
                    Subsignal('cathode', Pins('10', conn=pmod1, dir='o')),
                    
                    
                    Subsignal('aa', Pins('7', conn=pmod2, dir='o')),
                    Subsignal('ab', Pins('8', conn=pmod2, dir='o')),
                    Subsignal('ac', Pins('9', conn=pmod2, dir='o')),
                    Subsignal('ad', Pins('10', conn=pmod2, dir='o')),
                    
                    
                    # using the ice blink40, we seem to want SB_LVCMOS,
                    # and seem to have to say it out loud:
                    Attrs(IO_STANDARD="SB_LVCMOS")
                ),
           Resource('devinputs', 0, 
                    Subsignal('signal', Pins('1', conn=pmod1, dir='i')),
                    Subsignal('clkconf0', Pins('2', conn=pmod1, dir='i')),
                    Subsignal('clkconf1', Pins('3', conn=pmod1, dir='i')),
                    Subsignal('extclk', Pins('4', conn=pmod1, dir='i')),
                    # Subsignal('reset', Pins('4', conn=pmod1, dir='i')),
                    
                    # Subsignal('halfclock', Pins('3', conn=pmod1, dir='o')),
                    
                    Attrs(IO_STANDARD="SB_LVCMOS")
                    )
        ])
        
        disppins = platform.request('dualdisp', 0)
        devinputs = platform.request('devinputs', 0)
        
        
        cd_sync = ClockDomain("sync")
        m.domains += cd_sync
 
        m.d.comb += [
                disppins.aa.eq(self.displaySegments[7]),
                disppins.ab.eq(self.displaySegments[6]),
                disppins.ac.eq(self.displaySegments[5]),
                disppins.ad.eq(self.displaySegments[4]),
                disppins.ae.eq(self.displaySegments[3]),
                disppins.af.eq(self.displaySegments[2]),
                disppins.ag.eq(self.displaySegments[1]),
                disppins.cathode.eq(self.displaySelect),
                
                # the inputs
                ClockSignal("sync").eq(devinputs.extclk), 
                ### ResetSignal("sync").eq(self.io_in[1]),
                self.input_pulses.eq(devinputs.signal),
                self.clock_config.eq(Cat(devinputs.clkconf0, devinputs.clkconf1))
                
            ]
        
        


  
def test():
    m = Module() # top
    m.submodules.tuner = dut = Neptune(usingTuning=StandardGuitarTuning, samplingDurationSeconds=0.5)
    
    def toggle_the_input(freqHz, tickCount=300):
        periodSecs = 1/freqHz 
        
        yield Delay(1e-3)
        for _i in range(tickCount):
            yield dut.input_pulses.eq(1)
            yield Delay(periodSecs / 2)
            yield dut.input_pulses.eq(0)
            yield Delay(periodSecs / 2)
            
    def toggle_the_input_for(atFreqHz, forTimeSecs=1.0):
        periodSecs = 1/atFreqHz 
        numClicks =  math.ceil(forTimeSecs/periodSecs) + 1
        for _i in range(numClicks):
            yield dut.input_pulses.eq(1)
            yield Delay(periodSecs / 2)
            yield dut.input_pulses.eq(0)
            yield Delay(periodSecs / 2)
            
        
            
    def testSystem():
        
        yield dut.clock_config.eq(ClockName.Clock1KHz)
        yield Delay(10e-4)
        yield dut.clock_config.eq(ClockName.Clock2KHz)
        yield Delay(10e-4)
        yield dut.clock_config.eq(ClockName.Clock3277Hz)
        yield Delay(10e-4)
        yield dut.clock_config.eq(ClockName.Clock4KHz)
        yield Delay(10e-4)
        yield dut.clock_config.eq(ClockName.Clock1KHz)
        
        yield from toggle_the_input_for(330, 1.0)
        yield from toggle_the_input_for(145, 1.0)
        yield from toggle_the_input_for(154, 1.0)
        yield from toggle_the_input_for(138, 1.0)

    
    runSimulator(m, 'neptune', [dut.input_pulses, dut.displaySegments, dut.displaySelect], [testSystem], clockFreq=1e3)







def build(doBurn:bool=False):
    DevPlatform().build(
            Neptune(usingTuning=StandardGuitarTuning, 
                    samplingDurationSeconds=0.5), 
            do_program=doBurn)


if __name__ == "__main__":
    # allow us to run this directly
    from amaranth.cli import main
    
    doBuild = False
    doBurnAfterBuild = False
    Test = True
    
    if doBuild:
        build(doBurnAfterBuild)
        
    if Test:
        test()
    else:
        m = Module() # top level
        m.submodules.edgedetect = dev = Neptune(usingTuning=StandardGuitarTuning, 
                                                    samplingDurationSeconds=0.5)
        main(m, ports=dev.ports())



