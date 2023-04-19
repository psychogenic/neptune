# neptune
Flexible digital logic hardware frequency discriminator used as an extreeeeeme guitar tuner. 

![Neptune Project](https://raw.githubusercontent.com/psychogenic/neptune/main/img/neptuneproject.jpg)

&copy; 2023 Pat Deegan, [psychogenic.com](https://psychogenic.com)
Released under the GPL, see the LICENSE file for details.

*Neptune* was created to provide

 * a basis for frequency discrimination digital logic projects;
 * a first [TinyTapeout](https://tinytapeout.com/) submission; and 
 * an Amaranth tutorial.

## Design and Walk-through 

The motivation, goals, constraints and design are all covered in
[Python design of a hardware digital tuner on FPGA and ASIC](https://www.youtube.com/watch?v=h9_4jBKhs9k).

A complete walkthrough of the implementation is also available in
[Python to HDL: full Amaranth walkthrough to FPGA and ASIC GDS](https://youtu.be/yJxAX7gCpvQ)

## Requirements

You need [Amaranth](https://amaranth-lang.org/docs/amaranth/latest/intro.html) to do anything of interest. 

 
You'll need the [amaranth-boards](https://github.com/amaranth-lang/amaranth-boards) and probably 
need Yosys and other things to get to FPGAs going, though I've included the verilog for the 
FPGA board I use in verilog/.  

You need [OpenLane](https://github.com/efabless/openlane)
to do ASIC things.  See [my videos](https://www.youtube.com/@PsychogenicTechnologies) 
and [blog](https://inductive-kickback.com/).

## Generating Verilog

Most of the modules contain _main_ blocks that allow you to run it with 
```
python neptune/modulename.py generate -t v
```
to spit out generic Verilog for the module.

The 
	* `neptune/tuner.py`; and
	* `neptune/tt_top.py`
have more specialized functions in their main to produce FPGA and TinyTapeout stuff.  See vids and source.

## Burning to FPGA

Setting the appropriate flags to call build(doBurn=True) in the _main_ of `neptune/tuner.py`, then run that module
with the board plugged in--will burn.  

The platform is selected in `neptune/neptune_config.py` but if you're using
something other than the  iCE40HX1K Blink I'm using, you'll likely need to adjust the wireForPlatform() in tuner.py
somewhat.

## Resources

Other than the [Amaranth docs](https://amaranth-lang.org/docs/amaranth/latest/intro.html) themselves, Robert Baruch put out some amazing content: I first learned to use it while he was [building a 6800 CPU](https://www.youtube.com/playlist?list=PLEeZWGE3PwbbjxV7_XnPSR7ouLR2zjktw) and there's a [more recent project](https://www.youtube.com/playlist?list=PLEeZWGE3PwbZTypHq00G-yEX8TEI95lw4) also using it (both while it was still called nMigen).  Lot of hours, but was much fun.

Finally, there's a nice summary of all those videos in the [Amaranth tutorial](https://github.com/RobertBaruch/amaranth-tutorial) he also put out.



