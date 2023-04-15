'''
Created on Apr 12, 2023


Utility classes and containers for 7-segment display "sprites"


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

from amaranth import Array

class Sprite:
    '''
        Sprite - just a way to keep display segment bitfield 
        with an associated name.
        
        Bitfield specified in binary for 7-seg display:
        
        0bABCDEFG*
        
        where * is the "dot" (which won't work in this project)
    '''
    def __init__(self, name:str, fieldVal:int):
        self.name = name 
        self.bits = fieldVal
        
    def __repr__(self):
        return f'<Sprite {str(self.name)}>'
        
class SpriteSet:
    '''
        A set of "sprites" -- just bitfields we display -- that 
        go together, along with some accessor methods to 
        allow set[SOMENAME] to give me the sprite in question,
        as well as a way to get Amaranth Arrays of the bitfields.
    '''
    def __init__(self, fieldsList:list=None):
        self._bitfields = dict()
        
        if fieldsList is not None and len(fieldsList):
            for f in fieldsList:
                self.add(f)
        
    def add(self, bitfield:Sprite, key=None):
        if key is None:
            key = bitfield.name 
            
        self._bitfields[key] = bitfield
        
    def __getitem__(self, k) -> Sprite:
        if k not in self._bitfields:
            raise KeyError(f'No such sprite defined: {str(k)}')
        
        return self._bitfields[k]
    
    def __len__(self) -> int:
        return len(self._bitfields.keys())
    
    
    def toArray(self):
        orderedByKeyList = list(sorted(self._bitfields.values(), key=lambda x: x.name))
        asList = list(map( lambda x: x.bits, orderedByKeyList))
        return Array(asList)
        