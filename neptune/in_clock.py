'''
Created on Apr 12, 2023

Two input bits allow us to set the externally-provided clock frequency.
This module defines their values and some utils.


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
from enum import Enum, unique

@unique
class ClockName(Enum):
    Clock1KHz = 0
    Clock2KHz = 1
    Clock4KHz = 2
    Clock3277Hz = 3 # 32.768k / 10
    Clock10KHz = 4
    Clock32KHz = 5 # 32.768k
    Clock40KHz = 6
    Clock60KHz = 7
    
class ClockSetting:
    def __init__(self, clockOpt, freqHz:int):
        self.name = clockOpt 
        self.frequency = math.floor(freqHz)
        

class ClockOptions:
    
    Settings = [
         ClockSetting(ClockName.Clock1KHz, 1000),
         ClockSetting(ClockName.Clock2KHz, 2000),
         ClockSetting(ClockName.Clock4KHz, 4000),
         ClockSetting(ClockName.Clock3277Hz, 3277),
         ClockSetting(ClockName.Clock10KHz, 10000),
         ClockSetting(ClockName.Clock32KHz, 32768),
         ClockSetting(ClockName.Clock40KHz, 40000),
         ClockSetting(ClockName.Clock60KHz, 60000)
        ]
    
    @classmethod 
    def frequencyToTicksOver(cls, freqHz, periodIntervalSeconds:float):
        return math.ceil(freqHz * periodIntervalSeconds)
    
    @classmethod 
    def num_bits_required(cls):
        return math.ceil(math.log2(cls.num()))
    @classmethod 
    def num(cls):
        return len(ClockOptions.Settings)
    
    @classmethod
    def maxFrequencySupported(cls):
        maxFreq = 0
        for cs in ClockOptions.Settings:
            if maxFreq < cs.frequency:
                maxFreq = cs.frequency
        
        return maxFreq
    
    @classmethod 
    def frequencyHz(cls, ckey):
        for cs in ClockOptions.Settings:
            if ckey == cs.name:
                return cs.frequency
            
            if ckey == cs.name.value:
                return cs.frequency
        
        raise ValueError(f'Unknown clock {str(ckey)}')
    
        
            
            
        
