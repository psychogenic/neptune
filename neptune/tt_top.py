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
        self.clkconfig_0 = 2
        self.clkconfig_1 = 3
        self.clkconfig_2 = 4
        self.input_pulses = 5

class TinyTapeoutTop(Elaboratable):
    def __init__(self, usingTuning:Tuning=StandardGuitarTuning,
                 samplingDurationSeconds:float = config.SamplingDurationDefault,
                 inputSynchronizerNumStages:int = config.NumInputSynchronizerStagesDefault):
        
        self.tuning = usingTuning
        self.samplingDurationSeconds = samplingDurationSeconds
        self.inputSynchronizerNumStages = inputSynchronizerNumStages
        
        # TT has 8 in, 8 out, and a bunch of new stuff
        self.ui_in = Signal(8) # dedicated in
        self.uo_out = Signal(8) # dedicated out
        self.uio_in = Signal(8) # bidir, in
        self.uio_out = Signal(8) # bidir, out
        self.uio_oe = Signal(8) # bidir, IOs: Enable path (active high: 0=input, 1=output)
        self.ena = Signal()
        self.clk = Signal()
        self.rst_n = Signal()
        
        
        
        
        
        
        
        
        
        
        # making it public for use in testing
        self.tuner =  Neptune(usingTuning=self.tuning, samplingDurationSeconds=self.samplingDurationSeconds, 
                        inputSynchronizerNumStages=self.inputSynchronizerNumStages)
        
        self.pins = PinLocations()
        
        self.input_pulses = Signal()
        
    def tt_top_public_ports(self):
        return [
            
            
            self.ui_in,
            self.uo_out,
            self.uio_in,
            self.uio_out,
            self.uio_oe,
            self.ena,
            self.clk,
            self.rst_n
        
        
        ]
        
    def ports(self):
        return [self.ui_in, self.uo_out, self.input_pulses, self.clk, self.rst_n]
    
    
    def inputPin(self, idx):
        return self.ui_in[idx]
    
    
    @property 
    def pin_clock(self):
        return self.clk

    @property 
    def pin_reset(self):
        return self.rst_n
    
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
            
            ClockSignal("sync").eq(self.pin_clock),
            ResetSignal("sync").eq(~self.pin_reset),
        ]
        # direct mappings
        m.d.comb += [
            self.uio_oe.eq(0xff), # bidir are all outputs
            self.input_pulses.eq(self.pin_input_pulses),
            self.uio_out.eq(tuner.pulseCount)
        ]

        
        # inputs
        m.d.comb += [
            tuner.clock_config.eq(Cat(self.ui_in[self.pins.clkconfig_0], self.ui_in[self.pins.clkconfig_1], self.ui_in[self.pins.clkconfig_2])),
            tuner.input_pulses.eq(self.input_pulses)    
        ]

        # Output -- all display related
        outputs = Cat(
            tuner.displaySegments[1:],
            tuner.displaySelect
            
        )
        
        output_pins = self.uo_out
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
    m.d.comb += ResetSignal().eq(~rst)
    m.d.comb += [
        Assume(rst), # don't play with reset
        Assume(tttop.ui_in[tttop.pins.clkconfig_0] == 0), # 1 khz clock
        Assume(tttop.ui_in[tttop.pins.clkconfig_1] == 0) # 1 khz clock
    ]
    
    
    numTicksUntilMeasured = math.ceil(1000 * tttop.samplingDurationSeconds) + 25 # approx
    
    hist = History.new(m, numTicksUntilMeasured)
    hist.track(tttop.input_pulses)
    hist.track(tttop.ui_in)
    hist.track(tttop.uo_out)
    
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
                    m.d.comb += Assert(hist.snapshot(tttop.uo_out, len(inputSequence)+numberOfPostSampleTicksForNoteDisplay)[:7] == notesSegs[notes.Scale.E].bits[:7])


    inputSequence = inputSequenceForSignal(tuner, 112)
    
    # giving followedSequence the entire list in one go kills it: max recursion.
    # but break it up a bit, like so, and huzza
    with m.If(hist.followedSequence(tttop.input_pulses, inputSequence[:100], startTick=0)):
        with m.If(hist.followedSequence(tttop.input_pulses, inputSequence[100:200], startTick=100)):
            with m.If(hist.followedSequence(tttop.input_pulses, inputSequence[200:], startTick=200)):
                with m.If(hist.ticks > len(inputSequence) + 25):
                    m.d.comb += Assert(hist.snapshot(tttop.uo_out, len(inputSequence)+numberOfPostSampleTicksForNoteDisplay)[:7] == notesSegs[notes.Scale.A].bits[:7])


                    
    if includeCovers:
        with m.If(hist.ticks > 50):
            m.d.comb += Cover(tttop.uo_out == notesSegs[notes.Scale.G].bits)

    

if __name__ == "__main__":
    # Generate Verilog source for GC4.
    from amaranth.cli import main
    from amaranth.back import verilog
    import os
    top_name = os.environ.get("TOP", "tt_um_psychogenic_neptuneproportional")

    Test = False 
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
            dev, name=top_name, ports=dev.tt_top_public_ports(),
            emit_src=False, strip_internal_attrs=True)
        
        print(v)

        
    
    
    
    
