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
import sys 

# try to use a sane value here, something that is a 2**n is nice
MaxDetectionHzWindowDefault = 32



class DummyPlatform:
    
    def build(self, _doBurn:bool=False): 
        print("Don't have/can't find amaranth_boards!", file=sys.stderr)

try:
    from amaranth_boards.ice40_hx1k_blink_evn import ICE40HX1KBlinkEVNPlatform as DevPlatform
except ModuleNotFoundError as e:
    DevPlatform = DummyPlatform()