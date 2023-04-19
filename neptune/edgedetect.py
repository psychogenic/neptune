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


from amaranth import Signal, Elaboratable, Module, ResetSignal
from amaranth.build import Platform

from amaranth.lib.cdc import FFSynchronizer

from amaranth.sim import Delay
from amaranth.asserts import Assert, Assume, Cover

import neptune.neptune_config as config
from neptune.testing.history import History
from neptune.sims.runner import runSimulator


class EdgeDetect(Elaboratable):
    '''
        EdgeDetect puts out a pulse for 1 clock cycle, on each rising edge.
        
        @note: it uses an FF synchronizer to do this, crossing the clock
                domains (relatively) safely.  May add extra stages, but 
                it is unlikely to be required.
    '''
    
    def __init__(self, numStages:int = config.NumInputSynchronizerStagesDefault):
        # just one input and one output
        self.input = Signal()
        self.output = Signal()
        
        self._numStages = numStages
        
    
    def ports(self):
        return [self.input, self.output]
    
    @property 
    def numStages(self):
        return self._numStages
    
    @property 
    def signalDelayClocks(self):
        return self.numStages + 1
    
    def elaborate(self, platform:Platform):
        m = Module()
        
        # we'll feed the input directly into synchronizer and 
        # take the output locally, as syncOut
        syncOut = Signal()
        # also keep track if we've seen this "high" before
        seenRising = Signal()
        
        # the synchronizer itself
        # add it to the submodules being used
        m.submodules.ffsync  = FFSynchronizer(i=self.input, o=syncOut, 
                                                      stages=self.numStages) 
        
        
        # by default, out output is low
        m.d.sync += self.output.eq(0)
        
        # when the ff sync is high, we may want to send 
        # an ouput pulse, if we haven't done so already
        with m.If(syncOut):
            # is high
            with m.If(~ seenRising):
                # haven't seen this before
                m.d.sync += [
                        seenRising.eq(1),
                        self.output.eq(1)
                    ]
            
        with m.Else():
            # sync out is low, can safely 
            # clear out seenRising so we'll 
            # catch the next transition
            m.d.sync += seenRising.eq(0)
        
            
        return m
    
    
def simulate(m:Module, dut:EdgeDetect):
    
    def clockInput(times:int, frequencyHz:int):
        periodTime = 1/frequencyHz
        for _ in range(times):
            yield dut.input.eq(1)
            yield Delay(periodTime/2)
            yield dut.input.eq(0)
            yield Delay(periodTime/2)
            
    def twoClocks():
        yield Delay(1e-4)
        yield from clockInput(5, 2e3)
        yield Delay(1e-4)
        yield from clockInput(5, 300)
        
    runSimulator(m, 'edge_detect', [dut.input, dut.output], [twoClocks], clockFreq=4e3)


def coverAndProve(m:Module, edgedetect:EdgeDetect, includeCovers:bool=False):

    rst = Signal()
    m.d.comb += ResetSignal().eq(rst)
    #sync = ClockDomain('sync')
    #m.domains += sync
    m.d.comb += Assume(~rst)
    
    hist = History.new(m, 50)
    
    hist.track(edgedetect.input)
    hist.track(edgedetect.output)
    
    with m.If( (hist.ticks > 5) & 
               ~(hist.snapshot(edgedetect.input, 0)) & 
               hist.snapshot(edgedetect.input, 1)):
        m.d.comb += Assert(hist.snapshot(edgedetect.output, 4))
        
        
    if includeCovers:
        # find a way to have output high
        m.d.comb += Cover((hist.ticks > 8) & hist.snapshot(edgedetect.output, 6))
        
        # check what a long input pulse spits out
        m.d.comb += Cover( hist.snapshot(edgedetect.input, 4) & 
                           hist.snapshot(edgedetect.input, 5 ) & 
                           hist.snapshot(edgedetect.input, 6 ) &
                           (hist.ticks > 8) )

 

if __name__ == "__main__":
    # allow us to run this directly
    from amaranth.cli import main
    
    
    m = Module() # top
    m.submodules.edgedetect = dev = EdgeDetect()
    
    
    Sim = False
    Test = True
    if (Sim):
        simulate(m, dev)
    
    else:
        if Test:
            coverAndProve(m, dev)
    
    main(m, ports=dev.ports())




        
