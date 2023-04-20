'''
Created on Apr 12, 2023

The actual display we're using, which is a dual 7-segment display with a
switched cathode.

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

from amaranth import Signal, Elaboratable, Module
from amaranth.build import Platform
from amaranth.sim import Delay
from neptune.display.sevensegment import SevenSegment
from neptune.display.sprites import NoteSprites, ProximitySprites
from neptune.sims.runner import runSimulator

import neptune.notes as notes
from neptune.notes import Tuning
class DualSevenSegmentDisplay(Elaboratable):
    
    def __init__(self, usingTuning:Tuning):
        
        # inputs 
        self.valueNote = Signal(usingTuning.required_note_bits)
        self.valueProxim = Signal(3)
        
        # outputs 
        self.segments = Signal(8) # the segments to display, [7:1] on dual-display
        
        self.proximitySelect = Signal() # this is the cathode select, on dual-display
        
        

    def ports(self):
        return [self.valueNote, self.valueProxim, 
                self.segments, self.proximitySelect]
    
    
    
    
    def elaborate(self, platform: Platform):
        
        m = Module()
        
        m.submodules.notedisplay = notedisplay = SevenSegment(NoteSprites())
        m.submodules.proxdisplay = proxdisplay = SevenSegment(ProximitySprites())
        
        m.d.sync += [
            notedisplay.value.eq(self.valueNote),
            proxdisplay.value.eq(self.valueProxim)
        ]
            
        
        m.d.sync += self.proximitySelect.eq(1)
            
        with m.If(self.proximitySelect):
            m.d.sync += self.proximitySelect.eq(0) # flip it
            with m.If(self.valueNote == notes.Scale.NA):
                m.d.sync += self.segments.eq(notedisplay.segments)
            with m.Else():
                m.d.sync += self.segments.eq(proxdisplay.segments)
                
        with m.Else():
            m.d.sync += self.segments.eq(notedisplay.segments)
            

        return m
    
    
    


def test():
    m = Module() # top
    m.submodules.display = dut = DualSevenSegmentDisplay(notes.StandardGuitarTuning)
    
    def displayTest():
        baseDelay = 1e-3
        yield Delay(1e-4)
        # EXACT MATCH
        yield dut.valueProxim.eq(ProximitySprites.fieldsToId(exact=True, high=False, far=False))
        yield dut.valueNote.eq(notes.Scale.A)
        yield Delay(baseDelay)
        
        # OFF LOW CLOSE
        yield dut.valueProxim.eq(ProximitySprites.fieldsToId(exact=False, high=False, far=False))
        yield Delay(baseDelay)
        
        # OFF HIGH CLOSE
        yield dut.valueProxim.eq(ProximitySprites.fieldsToId(exact=False, high=True, far=False))
        yield Delay(baseDelay)
        
        # OFF HIGH FAR
        yield dut.valueProxim.eq(ProximitySprites.fieldsToId(exact=False, high=True, far=True))
        yield Delay(baseDelay)
        
        
        # EXACT E
        yield dut.valueProxim.eq(ProximitySprites.fieldsToId(exact=True, high=False, far=False))
        yield dut.valueNote.eq(notes.Scale.E)
        yield Delay(baseDelay)
        # OFF HIGH CLOSE
        yield dut.valueProxim.eq(ProximitySprites.fieldsToId(exact=False, high=True, far=False))
        yield Delay(baseDelay)
        
        
        
        

    runSimulator(m, 'display', [dut.valueNote, dut.valueProxim, 
                                dut.segments, dut.proximitySelect], [displayTest], clockFreq=20e3)


if __name__ == "__main__":
    # allow us to run this directly
    from amaranth.cli import main
    Test = True
    if (Test):
        test()
    else:
        m = Module() # top level
        m.submodules.dualsevseg = dev = DualSevenSegmentDisplay(notes.StandardGuitarTuning)
        main(m, ports=dev.ports())




