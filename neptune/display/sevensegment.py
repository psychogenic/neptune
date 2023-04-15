'''
Created on Apr 12, 2023

A 7-segment LED display driver.

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

from amaranth import Elaboratable, Signal, Module
from amaranth.build import Platform

from neptune.display.spriteset import SpriteSet


class SevenSegment(Elaboratable):
    '''
        A 7-segment LED display. 
        
        value is input to determine what is shown;
        segments are the segment wires 0bABCDEFG*
        
        Uses a sprite set to output the display bit field 
        associated with value.
    '''
    
    def __init__(self, spritesContainer:SpriteSet):
        
        self.sprites = spritesContainer
        #inputs 
        self.value = Signal(range(len(spritesContainer)))
        
        # outputs 
        self.segments = Signal(8)
        
    def elaborate(self, platform: Platform):
        
        m = Module()
        
        segMap = self.sprites.toArray()
        
        # if the value is valid, spit the associated bitfield out 
        # on segments
        with m.If(self.value < len(self.sprites)):
            m.d.sync += self.segments.eq(segMap[self.value])
        with m.Else():
            # otherwise, blank it.
            m.d.sync += self.segments.eq(0)
             
        return m
    
        