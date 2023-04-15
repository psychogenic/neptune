'''
Created on Feb 27, 2023

Convenience functions for running simulations.

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

DEFAULT_CLOCK_RATEHZ = 1e6

from amaranth.sim import Simulator, Delay, Settle, Tick
from amaranth import Module

def runSimulator(m:Module, baseFileName:str, traces=[], processes=[], clockFreq:int=DEFAULT_CLOCK_RATEHZ, runTimeSecs:float=None):
    s = getSim(m, clockFreq)
    if processes is not None and len(processes):
        for p in processes:
            print ("Adding process %s" % str(p))
            s.add_process(p)
    
    doSimulate(s, baseFileName, runTimeSecs, traces)


def getSim(m:Module, clockFreq:int=DEFAULT_CLOCK_RATEHZ) -> Simulator:
    sim = Simulator(m)
    sim.add_clock(1/clockFreq, domain="sync")
    return sim


    

def doSimulate(sim:Simulator, baseFileName:str, runTimeSecs:float=None, traces=[]):
    print(f"Running {baseFileName} simulation")
    # sim.add_process(process) # or sim.add_sync_process(process), see below
    with sim.write_vcd(f"{baseFileName}.vcd", f"{baseFileName}.gtkw", traces=traces
                       ):
        # sim.run_until(runTimeSecs, run_passive=True)
        if runTimeSecs is not None:
            sim.run_until(runTimeSecs, run_passive=True)
        else:
            sim.run()
    
    print("Done!")
    print(f"gtkwave {baseFileName}.gtkw to see results!")