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


from amaranth import Signal, Elaboratable, Module, Cat
from amaranth import ClockDomain, ClockSignal, ResetSignal
from amaranth.build import Platform

from neptune.notes import Tuning, StandardGuitarTuning
from neptune.tuner import Neptune


class TinyTapeoutTop(Elaboratable):
    def __init__(self, usingTuning:Tuning=StandardGuitarTuning,
                 samplingDurationSeconds:float = 0.5,
                 inputSynchronizerNumStages:int = 2):
        
        self.tuning = usingTuning
        self.samplingDurationSeconds = samplingDurationSeconds
        self.inputSynchronizerNumStages = inputSynchronizerNumStages
        
        # TT has 8 in, 8 out
        self.io_in = Signal(8)
        self.io_out = Signal(8)
        
    def ports(self):
        return [self.io_in, self.io_out]
    
    

    def elaborate(self, platform:Platform):
        m = Module()
        
        tuner = Neptune(usingTuning=self.tuning, samplingDurationSeconds=self.samplingDurationSeconds, 
                        inputSynchronizerNumStages=self.inputSynchronizerNumStages)
        
        m.submodules.tuner = tuner
        cd_sync = ClockDomain("sync")
        m.domains += cd_sync
 
        # clock and reset
        m.d.comb += [
            ClockSignal("sync").eq(self.io_in[0]),
            ResetSignal("sync").eq(self.io_in[1]),
        ]
        
        # inputs
        m.d.comb += [
            tuner.clock_config.eq(Cat(self.io_in[2], self.io_in[3])),
            tuner.input_pulses.eq(self.io_in[4])    
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


    
    

if __name__ == "__main__":
    # Generate Verilog source for GC4.
    from amaranth.back import verilog
    import os
    top_name = os.environ.get("TOP", "neptune")

    module = TinyTapeoutTop()

    v = verilog.convert(
        module, name=top_name, ports=[module.io_out, module.io_in],
        emit_src=False, strip_internal_attrs=True)
    
    print(v)

        
    
    
    
    