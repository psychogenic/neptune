'''
Created on Apr 12, 2023

Contains enums, classes and containers related to the frequencies of interest.

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

from enum import Enum, unique
import math 

class Scale(Enum):
    NA = 0
    G = 1
    A = 2 
    B = 3
    C = 4
    D = 5
    E = 6
    F = 7
    
    def __lt__(self, other):
        return self.value < other.value 
    
    
@unique 
class Accidental(Enum):
    Natural = 0
    Flat = 1
    Sharp = 2

class DetectedNote:
    '''
        Detected note is basically just an association between
            - a Scale.NOTE (Enum) and
            - a frequency (Hz)
        along with some extras for future/debug
    '''
    def __init__(self, name:str, note:Enum, freqHz:float, accidental:Enum=Accidental.Natural):
        self.name = name # e.g. E2
        self.note = note # Scale.E
        self.frequency = freqHz # value in Hz
        self.accidental = accidental # Natural,Flat or sharp
        
        
    def __repr__(self):
        return f'<DetectedNote {self.name} {self.frequency}Hz>'
    
    def __str__(self):
        return f'Note {self.name} ({self.note}) @ {self.frequency}Hz'
    

class Tuning:
    '''
        Tuning is a container of DetectedNotes.
        Its purpose is to hold the set and allow for accessing the notes
        in useful ways (e.g. in a particular order).
    '''
    def __init__(self, notes:list = None):
        self._notes = dict()
        if notes is not None:
            for n in notes:
                self.add(n)
    
    def add(self, note:DetectedNote):
        if note.name in self._notes:
            raise ValueError(f'Note {note.name} already present in this tuning!')
        
        self._notes[note.name] = note
        
    def __len__(self):
        '''
            number of notes in this tuning set
        '''
        return len(self.note_names)
    
    
    
    @property 
    def notes(self) -> list[DetectedNote]:
        return self._notes.values()
    
    @property 
    def note_names(self) -> list[str]:
        return list(self._notes.keys())
    
    @property
    def ascending(self) -> list[DetectedNote]:
        return list(sorted(self._notes.values(), key=lambda n: n.frequency))
    
    @property 
    def descending(self) -> list[DetectedNote]:
        return reversed(self.ascending)
    
    @property
    def lowest(self) -> DetectedNote:
        return self.ascending[0]
    
    @property 
    def highest(self) -> DetectedNote:
        return self.ascending[-1]
    
    
    @property 
    def required_note_bits(self) -> int:
        return math.ceil(math.log2(len(self)))
    
    def __repr__(self):
        names = []
        for n in self.ascending:
            names.append(n.name)
        return f'<Tuning {",".join(names)}>'
    
        

StandardGuitarTuning = Tuning([
        DetectedNote('E2', Scale.E, 82.41),
        DetectedNote('A2', Scale.A, 110.0),
        DetectedNote('D3', Scale.D, 146.83),
        DetectedNote('G3', Scale.G, 196.00),
        DetectedNote('B3', Scale.B, 246.94),
        DetectedNote('E4', Scale.E, 329.63)
    ])

if __name__ == '__main__':
    
    print(f'Standard tuning lowest note: {StandardGuitarTuning.lowest.name}')
    print(f'Standard tuning highest note: {StandardGuitarTuning.highest.name}')
    print('Full set:')
    
    for n in StandardGuitarTuning.ascending:
        print(f'\t{n.name}\t{int(n.frequency)}Hz')
        

