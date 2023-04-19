'''
Created on Apr 12, 2023


Used to generate verilog suitable for inclusion in TinyTapeout.  Basically means
tying the 8 input and 8 output to appropriate places.

@see: https://tinytapeout.com/

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
from amaranth import ClockDomain, ClockSignal, ResetSignal
from amaranth.build import Platform
from amaranth.asserts import Assert, Assume, Cover

import neptune.neptune_config as config 
from neptune.notes import Tuning, StandardGuitarTuning
from neptune.tuner import Neptune, inputSequenceForSignal
from neptune.testing.history import History

class PinLocations:
    def __init__(self):
        
        self.clk = 0
        self.rst = 1
        self.clkconfig_0 = 2
        self.clkconfig_1 = 3
        self.input_pulses = 4

class TinyTapeoutTop(Elaboratable):
    def __init__(self, usingTuning:Tuning=StandardGuitarTuning,
                 samplingDurationSeconds:float = config.SamplingDurationDefault,
                 inputSynchronizerNumStages:int = config.NumInputSynchronizerStagesDefault):
        
        self.tuning = usingTuning
        self.samplingDurationSeconds = samplingDurationSeconds
        self.inputSynchronizerNumStages = inputSynchronizerNumStages
        
        # TT has 8 in, 8 out
        self.io_in = Signal(8)
        self.io_out = Signal(8)
        
        # making it public for use in testing
        self.tuner =  Neptune(usingTuning=self.tuning, samplingDurationSeconds=self.samplingDurationSeconds, 
                        inputSynchronizerNumStages=self.inputSynchronizerNumStages)
        
        self.pins = PinLocations()
        
        self.input_pulses = Signal()
        self.clock = Signal()
        self.reset = Signal()
        
        
    def ports(self):
        return [self.io_in, self.io_out, self.input_pulses, self.clock]
    
    
    def inputPin(self, idx):
        return self.io_in[idx]
    
    
    @property 
    def pin_clock(self):
        return self.inputPin(self.pins.clk)

    @property 
    def pin_reset(self):
        return self.inputPin(self.pins.rst)
    
    @property 
    def pin_input_pulses(self):
        return self.inputPin(self.pins.input_pulses)

    def elaborate(self, platform:Platform):
        m = Module()
        
        tuner = self.tuner 
        
        m.submodules.tuner = tuner
        cd_sync = ClockDomain("sync")
        m.domains += cd_sync
 
        # clock and reset
        m.d.comb += [
            
            self.input_pulses.eq(self.pin_input_pulses),
            self.clock.eq(self.pin_clock),
            self.reset.eq(self.pin_reset),
            ClockSignal("sync").eq(self.pin_clock),
            ResetSignal("sync").eq(self.pin_reset),
        ]
        
        # inputs
        m.d.comb += [
            tuner.clock_config.eq(Cat(self.io_in[self.pins.clkconfig_0], self.io_in[self.pins.clkconfig_1])),
            tuner.input_pulses.eq(self.input_pulses)    
        ]

        # Output -- all display related
        outputs = Cat(
            tuner.displaySegments[:7],
            tuner.displaySelect
            
        )
        
        output_pins = self.io_out
        assert outputs.shape() == output_pins.shape(), "inconsistent output shape"

        m.d.comb += output_pins.eq(outputs)
        
        return m




def coverAndProve(m:Module, tttop:TinyTapeoutTop, includeCovers:bool=False):
    # Note: I have a condition below that makes the period 0.1s -- so 
    # during testing we only need to count a bit past 100 ticks to see results
    import neptune.display.sprites as sprites
    import neptune.notes as notes
    
    tuner = tttop.tuner
    
    rst = tttop.pin_reset
    m.d.comb += ResetSignal().eq(rst)
    m.d.comb += [
        Assume(~rst), # don't play with reset
        Assume(tttop.io_in[tttop.pins.clkconfig_0] == 0), # 1 khz clock
        Assume(tttop.io_in[tttop.pins.clkconfig_1] == 0) # 1 khz clock
    ]
    
    
    numTicksUntilMeasured = math.ceil(1000 * tttop.samplingDurationSeconds) + 25 # approx
    
    hist = History.new(m, numTicksUntilMeasured)
    hist.track(tttop.input_pulses)
    hist.track(tttop.io_in)
    hist.track(tttop.io_out)
    
    notesSegs = sprites.NoteSprites()
    
    inputSequence = inputSequenceForSignal(tuner, 330)
    #print(len(inputSequence))
    
    numberOfPostSampleTicksForNoteDisplay = 23
    # giving followedSequence the entire list in one go kills it: max recursion.
    # but break it up a bit, like so, and huzza
    with m.If(hist.followedSequence(tttop.input_pulses, inputSequence[:100], startTick=0)):
        with m.If(hist.followedSequence(tttop.input_pulses, inputSequence[100:200], startTick=100)):
            with m.If(hist.followedSequence(tttop.input_pulses, inputSequence[200:], startTick=200)):
                with m.If(hist.ticks > (len(inputSequence) + 25)):
                    m.d.comb += Assert(hist.snapshot(tttop.io_out, len(inputSequence)+numberOfPostSampleTicksForNoteDisplay)[:7] == notesSegs[notes.Scale.E].bits[:7])


    inputSequence = inputSequenceForSignal(tuner, 112)
    
    # giving followedSequence the entire list in one go kills it: max recursion.
    # but break it up a bit, like so, and huzza
    with m.If(hist.followedSequence(tttop.input_pulses, inputSequence[:100], startTick=0)):
        with m.If(hist.followedSequence(tttop.input_pulses, inputSequence[100:200], startTick=100)):
            with m.If(hist.followedSequence(tttop.input_pulses, inputSequence[200:], startTick=200)):
                with m.If(hist.ticks > len(inputSequence) + 25):
                    m.d.comb += Assert(hist.snapshot(tttop.io_out, len(inputSequence)+numberOfPostSampleTicksForNoteDisplay)[:7] == notesSegs[notes.Scale.A].bits[:7])


                    
    if includeCovers:
        with m.If(hist.ticks > 50):
            m.d.comb += Cover(tttop.io_out == notesSegs[notes.Scale.G].bits)

    

if __name__ == "__main__":
    # Generate Verilog source for GC4.
    from amaranth.cli import main
    from amaranth.back import verilog
    import os
    top_name = os.environ.get("TOP", "neptune")

    Test = True 
    if Test:
        samplingDurationSeconds = 0.25
    else:
        samplingDurationSeconds = config.SamplingDurationDefault
        
    dev = TinyTapeoutTop(samplingDurationSeconds=samplingDurationSeconds)
    
    if Test:
        m = Module()
        m.submodules.tt_top = dev 
        coverAndProve(m, dev, includeCovers=True)
        main(m, ports=dev.ports())
    else:
        v = verilog.convert(
            dev, name=top_name, ports=[dev.io_out, dev.io_in],
            emit_src=False, strip_internal_attrs=True)
        
        print(v)

        
    
    
    
    