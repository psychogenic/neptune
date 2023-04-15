'''
Created on Apr 12, 2023

The actual bitfield definitions for the note and proximity sprites.


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
import neptune.notes as notes
from amaranth import Const
from neptune.display.spriteset import SpriteSet, Sprite

        
class NoteSprites(SpriteSet):
    '''
        The detected note display sprite set from A - g, with an "-" for NA.
    '''
        
    def __init__(self):
        
        notebits = [
            Sprite(notes.Scale.NA,     Const(0b00000010)), # -
            Sprite(notes.Scale.A,      Const(0b11101110)), # A
            Sprite(notes.Scale.B,      Const(0b00111110)), # b
            Sprite(notes.Scale.C,      Const(0b10011100)), # C
            Sprite(notes.Scale.D,      Const(0b01111010)), # d
            Sprite(notes.Scale.E,      Const(0b10011110)), # E
            Sprite(notes.Scale.F,      Const(0b10001110)), # F
            Sprite(notes.Scale.G,      Const(0b11110110)), # g
            ]
        
        super().__init__(notebits)
        
class ProximitySprites(SpriteSet):
    '''
        The proximity sprite set
        
        If the 7-seg display is
        ---
        | |
        ---
        | |
        ---
        
        Then the verticals indicate below (low) or above (high) and the 
        horizontals near/far, i.e. 
        
        
        low-far  low-close  high-far high-close  exact
                             ---
                             | |      | |    
                   ---                ---         blank
        | |        | |
        ---
    '''
    
    @classmethod 
    def fieldsToId(cls, exact:bool, high:bool, far:bool):
        # a concat of bits
        # FAR HI EXACT [2 .. 0]
        fid = 0
        if far:
            fid |= (1 << 2)
        if high: 
            fid |= (1 << 1)
        if exact:
            fid |= 1
            
        return fid
    
    def __init__(self):
        proxbits = [
            #                               EXACT   HIGH   FAR
            # off, low, close |-|
            Sprite(
                ProximitySprites.fieldsToId(False, False, False),
                                                               Const(0b00101010)),
            
            # off, low,  far |_|
            Sprite(
                ProximitySprites.fieldsToId(False, False, True),
                                                                Const(0b00111000)),
            # off, high, close
            Sprite(
                ProximitySprites.fieldsToId(False, True, False),
                                                                Const(0b01000110)),
            # off, high, far
            Sprite(
                ProximitySprites.fieldsToId(False, True, True),
                                                                Const(0b11000100)),
            
            # these are all the same
            Sprite(
                ProximitySprites.fieldsToId(True, False, False),
                                                                Const(0b00000001)),
            Sprite(
                ProximitySprites.fieldsToId(True, False, True),
                                                                Const(0b00000001)),
            
            Sprite(
                ProximitySprites.fieldsToId(True, True, False),
                                                                Const(0b00000001)),
            Sprite(
                ProximitySprites.fieldsToId(True, True, True),
                                                                Const(0b00000001)),
            
        ]
        
        super().__init__(proxbits)
        
        