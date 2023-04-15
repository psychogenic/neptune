/*
    Neptune v1.0.0 for ICE40HX1K Blink evaluation board.
    Copyright (C) 2023 Pat Deegan, https://psychogenic.com

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
*/

module discriminator(note, match_exact, match_high, match_far, clk, rst, edge_count);
  reg \$auto$verilog_backend.cc:2097:dump_module$1  = 0;
  wire \$1 ;
  wire \$10 ;
  wire \$12 ;
  wire [8:0] \$14 ;
  wire [8:0] \$15 ;
  wire [8:0] \$16 ;
  wire [8:0] \$18 ;
  wire [8:0] \$19 ;
  wire [8:0] \$21 ;
  wire [8:0] \$22 ;
  wire [8:0] \$24 ;
  wire [8:0] \$25 ;
  wire [8:0] \$27 ;
  wire [8:0] \$28 ;
  wire \$3 ;
  wire [8:0] \$30 ;
  wire [8:0] \$31 ;
  wire \$33 ;
  wire [5:0] \$35 ;
  wire [5:0] \$36 ;
  wire \$38 ;
  wire [8:0] \$40 ;
  wire [8:0] \$41 ;
  wire \$43 ;
  wire \$45 ;
  wire \$47 ;
  wire \$49 ;
  wire \$5 ;
  wire [3:0] \$7 ;
  wire [3:0] \$8 ;
  input clk;
  wire clk;
  reg [2:0] curNoteIndex = 3'h0;
  reg [2:0] \curNoteIndex$next ;
  reg [2:0] curState = 3'h0;
  reg [2:0] \curState$next ;
  input [7:0] edge_count;
  wire [7:0] edge_count;
  reg inputFreqHigher = 1'h0;
  reg \inputFreqHigher$next ;
  output match_exact;
  reg match_exact = 1'h0;
  reg \match_exact$next ;
  output match_far;
  reg match_far = 1'h0;
  reg \match_far$next ;
  output match_high;
  reg match_high = 1'h0;
  reg \match_high$next ;
  reg [4:0] noMatchCount = 5'h00;
  reg [4:0] \noMatchCount$next ;
  output [2:0] note;
  reg [2:0] note = 3'h0;
  reg [2:0] \note$next ;
  reg [4:0] readingProximityResult = 5'h00;
  reg [4:0] \readingProximityResult$next ;
  input rst;
  wire rst;
  reg [7:0] subtractResult = 8'h00;
  reg [7:0] \subtractResult$next ;
  assign \$10  = noMatchCount ==  5'h1f;
  assign \$12  = subtractResult <=  5'h10;
  assign \$16  = 8'had -  edge_count;
  assign \$1  = subtractResult <=  5'h10;
  assign \$19  = 8'h83 -  edge_count;
  assign \$22  = 8'h6a -  edge_count;
  assign \$25  = 8'h51 -  edge_count;
  assign \$28  = 8'h3f -  edge_count;
  assign \$31  = 8'h31 -  edge_count;
  assign \$33  = curNoteIndex <  3'h6;
  assign \$36  = noMatchCount +  1'h1;
  assign \$38  = subtractResult <=  4'h8;
  assign \$3  = curNoteIndex <  3'h6;
  assign \$41  = 5'h10 -  subtractResult;
  assign \$43  = subtractResult <=  4'h8;
  assign \$45  = readingProximityResult >=  3'h7;
  assign \$47  = readingProximityResult >=  3'h7;
  assign \$49  = readingProximityResult <=  3'h4;
  always @(posedge clk)
    curState <= \curState$next ;
  always @(posedge clk)
    curNoteIndex <= \curNoteIndex$next ;
  always @(posedge clk)
    note <= \note$next ;
  always @(posedge clk)
    subtractResult <= \subtractResult$next ;
  always @(posedge clk)
    noMatchCount <= \noMatchCount$next ;
  always @(posedge clk)
    readingProximityResult <= \readingProximityResult$next ;
  always @(posedge clk)
    inputFreqHigher <= \inputFreqHigher$next ;
  always @(posedge clk)
    match_exact <= \match_exact$next ;
  always @(posedge clk)
    match_far <= \match_far$next ;
  assign \$5  = subtractResult <=  5'h10;
  always @(posedge clk)
    match_high <= \match_high$next ;
  assign \$8  = curNoteIndex +  1'h1;
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$1 ) begin end
    casez (curState)
      
      /* \amaranth.decoding  = "Init/0" */
      3'h0:
          \curState$next  = 3'h1;
      
      /* \amaranth.decoding  = "CalculateDiffFromTarget/1" */
      3'h1:
          \curState$next  = 3'h2;
      
      /* \amaranth.decoding  = "Compare/2" */
      3'h2:
          casez (\$1 )
            
            1'h1:
                \curState$next  = 3'h4;
            
            default:
                \curState$next  = 3'h3;
          endcase
      
      /* \amaranth.decoding  = "MovedToNextCheckBounds/3" */
      3'h3:
          casez (\$3 )
            
            1'h1:
                \curState$next  = 3'h1;
            
            default:
                \curState$next  = 3'h0;
          endcase
      
      /* \amaranth.decoding  = "DetectedValidNote/4" */
      3'h4:
          \curState$next  = 3'h5;
      
      /* \amaranth.decoding  = "DisplayResult/5" */
      3'h5:
          \curState$next  = 3'h0;
      
      /* \amaranth.decoding  = {0{1'b0}} */
      default:
          \curState$next  = 3'h0;
    endcase
    casez (rst)
      1'h1:
          \curState$next  = 3'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$1 ) begin end
    \curNoteIndex$next  = curNoteIndex;
    casez (curState)
      
      /* \amaranth.decoding  = "Init/0" */
      3'h0:
          \curNoteIndex$next  = 3'h0;
      
      /* \amaranth.decoding  = "CalculateDiffFromTarget/1" */
      3'h1:
          /* empty */;
      
      /* \amaranth.decoding  = "Compare/2" */
      3'h2:
          casez (\$5 )
            
            1'h1:
                /* empty */;
            
            default:
                \curNoteIndex$next  = \$8 [2:0];
          endcase
    endcase
    casez (rst)
      1'h1:
          \curNoteIndex$next  = 3'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$1 ) begin end
    \note$next  = note;
    casez (curState)
      
      /* \amaranth.decoding  = "Init/0" */
      3'h0:
          casez (\$10 )
            
            1'h1:
                \note$next  = 3'h0;
          endcase
      
      /* \amaranth.decoding  = "CalculateDiffFromTarget/1" */
      3'h1:
          /* empty */;
      
      /* \amaranth.decoding  = "Compare/2" */
      3'h2:
          casez (\$12 )
            
            1'h1:
                casez (curNoteIndex)
                  3'h0:
                      \note$next  = 3'h6;
                  3'h1:
                      \note$next  = 3'h3;
                  3'h2:
                      \note$next  = 3'h1;
                  3'h3:
                      \note$next  = 3'h5;
                  3'h4:
                      \note$next  = 3'h2;
                  3'h?:
                      \note$next  = 3'h6;
                endcase
          endcase
    endcase
    casez (rst)
      1'h1:
          \note$next  = 3'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$1 ) begin end
    \subtractResult$next  = subtractResult;
    casez (curState)
      
      /* \amaranth.decoding  = "Init/0" */
      3'h0:
          /* empty */;
      
      /* \amaranth.decoding  = "CalculateDiffFromTarget/1" */
      3'h1:
          casez (curNoteIndex)
            3'h0:
                \subtractResult$next  = \$16 [7:0];
            3'h1:
                \subtractResult$next  = \$19 [7:0];
            3'h2:
                \subtractResult$next  = \$22 [7:0];
            3'h3:
                \subtractResult$next  = \$25 [7:0];
            3'h4:
                \subtractResult$next  = \$28 [7:0];
            3'h?:
                \subtractResult$next  = \$31 [7:0];
          endcase
    endcase
    casez (rst)
      1'h1:
          \subtractResult$next  = 8'h00;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$1 ) begin end
    \noMatchCount$next  = noMatchCount;
    casez (curState)
      
      /* \amaranth.decoding  = "Init/0" */
      3'h0:
          /* empty */;
      
      /* \amaranth.decoding  = "CalculateDiffFromTarget/1" */
      3'h1:
          /* empty */;
      
      /* \amaranth.decoding  = "Compare/2" */
      3'h2:
          /* empty */;
      
      /* \amaranth.decoding  = "MovedToNextCheckBounds/3" */
      3'h3:
          casez (\$33 )
            
            1'h1:
                /* empty */;
            
            default:
                \noMatchCount$next  = \$36 [4:0];
          endcase
      
      /* \amaranth.decoding  = "DetectedValidNote/4" */
      3'h4:
          \noMatchCount$next  = 5'h00;
    endcase
    casez (rst)
      1'h1:
          \noMatchCount$next  = 5'h00;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$1 ) begin end
    \readingProximityResult$next  = readingProximityResult;
    casez (curState)
      
      /* \amaranth.decoding  = "Init/0" */
      3'h0:
          /* empty */;
      
      /* \amaranth.decoding  = "CalculateDiffFromTarget/1" */
      3'h1:
          /* empty */;
      
      /* \amaranth.decoding  = "Compare/2" */
      3'h2:
          /* empty */;
      
      /* \amaranth.decoding  = "MovedToNextCheckBounds/3" */
      3'h3:
          /* empty */;
      
      /* \amaranth.decoding  = "DetectedValidNote/4" */
      3'h4:
          casez (\$38 )
            
            1'h1:
                \readingProximityResult$next  = subtractResult[4:0];
            
            default:
                \readingProximityResult$next  = \$41 [4:0];
          endcase
    endcase
    casez (rst)
      1'h1:
          \readingProximityResult$next  = 5'h00;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$1 ) begin end
    \inputFreqHigher$next  = inputFreqHigher;
    casez (curState)
      
      /* \amaranth.decoding  = "Init/0" */
      3'h0:
          /* empty */;
      
      /* \amaranth.decoding  = "CalculateDiffFromTarget/1" */
      3'h1:
          /* empty */;
      
      /* \amaranth.decoding  = "Compare/2" */
      3'h2:
          /* empty */;
      
      /* \amaranth.decoding  = "MovedToNextCheckBounds/3" */
      3'h3:
          /* empty */;
      
      /* \amaranth.decoding  = "DetectedValidNote/4" */
      3'h4:
          casez (\$43 )
            
            1'h1:
                \inputFreqHigher$next  = 1'h1;
            
            default:
                \inputFreqHigher$next  = 1'h0;
          endcase
    endcase
    casez (rst)
      1'h1:
          \inputFreqHigher$next  = 1'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$1 ) begin end
    \match_exact$next  = match_exact;
    casez (curState)
      
      /* \amaranth.decoding  = "Init/0" */
      3'h0:
          /* empty */;
      
      /* \amaranth.decoding  = "CalculateDiffFromTarget/1" */
      3'h1:
          /* empty */;
      
      /* \amaranth.decoding  = "Compare/2" */
      3'h2:
          /* empty */;
      
      /* \amaranth.decoding  = "MovedToNextCheckBounds/3" */
      3'h3:
          /* empty */;
      
      /* \amaranth.decoding  = "DetectedValidNote/4" */
      3'h4:
          /* empty */;
      
      /* \amaranth.decoding  = "DisplayResult/5" */
      3'h5:
          casez (\$45 )
            
            1'h1:
                \match_exact$next  = 1'h1;
            
            default:
                \match_exact$next  = 1'h0;
          endcase
    endcase
    casez (rst)
      1'h1:
          \match_exact$next  = 1'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$1 ) begin end
    \match_far$next  = match_far;
    casez (curState)
      
      /* \amaranth.decoding  = "Init/0" */
      3'h0:
          /* empty */;
      
      /* \amaranth.decoding  = "CalculateDiffFromTarget/1" */
      3'h1:
          /* empty */;
      
      /* \amaranth.decoding  = "Compare/2" */
      3'h2:
          /* empty */;
      
      /* \amaranth.decoding  = "MovedToNextCheckBounds/3" */
      3'h3:
          /* empty */;
      
      /* \amaranth.decoding  = "DetectedValidNote/4" */
      3'h4:
          /* empty */;
      
      /* \amaranth.decoding  = "DisplayResult/5" */
      3'h5:
          casez (\$47 )
            
            1'h1:
                \match_far$next  = 1'h0;
            
            default:
                casez (\$49 )
                  
                  1'h1:
                      \match_far$next  = 1'h1;
                  
                  default:
                      \match_far$next  = 1'h0;
                endcase
          endcase
    endcase
    casez (rst)
      1'h1:
          \match_far$next  = 1'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$1 ) begin end
    \match_high$next  = match_high;
    casez (curState)
      
      /* \amaranth.decoding  = "Init/0" */
      3'h0:
          /* empty */;
      
      /* \amaranth.decoding  = "CalculateDiffFromTarget/1" */
      3'h1:
          /* empty */;
      
      /* \amaranth.decoding  = "Compare/2" */
      3'h2:
          /* empty */;
      
      /* \amaranth.decoding  = "MovedToNextCheckBounds/3" */
      3'h3:
          /* empty */;
      
      /* \amaranth.decoding  = "DetectedValidNote/4" */
      3'h4:
          /* empty */;
      
      /* \amaranth.decoding  = "DisplayResult/5" */
      3'h5:
          \match_high$next  = inputFreqHigher;
    endcase
    casez (rst)
      1'h1:
          \match_high$next  = 1'h0;
    endcase
  end
  assign \$7  = \$8 ;
  assign \$15  = \$16 ;
  assign \$18  = \$19 ;
  assign \$21  = \$22 ;
  assign \$24  = \$25 ;
  assign \$27  = \$28 ;
  assign \$30  = \$31 ;
  assign \$35  = \$36 ;
  assign \$40  = \$41 ;
endmodule

module display(valueProxim, segments, proximitySelect, clk, rst, valueNote);
  reg \$auto$verilog_backend.cc:2097:dump_module$2  = 0;
  wire \$1 ;
  wire \$3 ;
  input clk;
  wire clk;
  wire [7:0] notedisplay_segments;
  reg [2:0] notedisplay_value = 3'h0;
  reg [2:0] \notedisplay_value$next ;
  wire [7:0] proxdisplay_segments;
  reg [2:0] proxdisplay_value = 3'h0;
  reg [2:0] \proxdisplay_value$next ;
  output proximitySelect;
  reg proximitySelect = 1'h0;
  reg \proximitySelect$next ;
  input rst;
  wire rst;
  output [7:0] segments;
  reg [7:0] segments = 8'h00;
  reg [7:0] \segments$next ;
  input [2:0] valueNote;
  wire [2:0] valueNote;
  input [2:0] valueProxim;
  wire [2:0] valueProxim;
  assign \$1  = !  valueNote;
  assign \$3  = ~  proximitySelect;
  always @(posedge clk)
    notedisplay_value <= \notedisplay_value$next ;
  always @(posedge clk)
    proxdisplay_value <= \proxdisplay_value$next ;
  always @(posedge clk)
    segments <= \segments$next ;
  always @(posedge clk)
    proximitySelect <= \proximitySelect$next ;
  notedisplay notedisplay (
    .clk(clk),
    .rst(rst),
    .segments(notedisplay_segments),
    .value(notedisplay_value)
  );
  proxdisplay proxdisplay (
    .clk(clk),
    .rst(rst),
    .segments(proxdisplay_segments),
    .value(proxdisplay_value)
  );
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$2 ) begin end
    \notedisplay_value$next  = valueNote;
    casez (rst)
      1'h1:
          \notedisplay_value$next  = 3'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$2 ) begin end
    \proxdisplay_value$next  = valueProxim;
    casez (rst)
      1'h1:
          \proxdisplay_value$next  = 3'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$2 ) begin end
    casez (proximitySelect)
      
      1'h1:
          casez (\$1 )
            
            1'h1:
                \segments$next  = notedisplay_segments;
            
            default:
                \segments$next  = proxdisplay_segments;
          endcase
      
      default:
          \segments$next  = notedisplay_segments;
    endcase
    casez (rst)
      1'h1:
          \segments$next  = 8'h00;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$2 ) begin end
    \proximitySelect$next  = \$3 ;
    casez (rst)
      1'h1:
          \proximitySelect$next  = 1'h0;
    endcase
  end
endmodule

module edge_detect(\input , \output , rst, clk);
  reg \$auto$verilog_backend.cc:2097:dump_module$3  = 0;
  wire \$1 ;
  wire \$3 ;
  input clk;
  wire clk;
  wire ffsync_syncOut;
  input \input ;
  wire \input ;
  output \output ;
  reg \output  = 1'h0;
  reg \output$next ;
  input rst;
  wire rst;
  reg seenRising = 1'h0;
  reg \seenRising$next ;
  assign \$1  = ~  seenRising;
  assign \$3  = ~  seenRising;
  always @(posedge clk)
    \output  <= \output$next ;
  always @(posedge clk)
    seenRising <= \seenRising$next ;
  ffsync ffsync (
    .clk(clk),
    .\input (\input ),
    .rst(rst),
    .syncOut(ffsync_syncOut)
  );
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$3 ) begin end
    \output$next  = 1'h0;
    casez (ffsync_syncOut)
      
      1'h1:
          casez (\$1 )
            
            1'h1:
                \output$next  = 1'h1;
          endcase
    endcase
    casez (rst)
      1'h1:
          \output$next  = 1'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$3 ) begin end
    \seenRising$next  = seenRising;
    casez (ffsync_syncOut)
      
      1'h1:
          casez (\$3 )
            
            1'h1:
                \seenRising$next  = 1'h1;
          endcase
      
      default:
          \seenRising$next  = 1'h0;
    endcase
    casez (rst)
      1'h1:
          \seenRising$next  = 1'h0;
    endcase
  end
endmodule

module ffsync(\input , rst, syncOut, clk);
  input clk;
  wire clk;
  input \input ;
  wire \input ;
  input rst;
  wire rst;
  reg stage0 = 1'h0;
  wire \stage0$next ;
  reg stage1 = 1'h0;
  wire \stage1$next ;
  output syncOut;
  wire syncOut;
  always @(posedge clk)
    stage0 <= \stage0$next ;
  always @(posedge clk)
    stage1 <= \stage1$next ;
  assign syncOut = stage1;
  assign \stage1$next  = stage0;
  assign \stage0$next  = \input ;
endmodule

module notedisplay(rst, value, segments, clk);
  reg \$auto$verilog_backend.cc:2097:dump_module$4  = 0;
  wire \$1 ;
  input clk;
  wire clk;
  input rst;
  wire rst;
  output [7:0] segments;
  reg [7:0] segments = 8'h00;
  reg [7:0] \segments$next ;
  input [2:0] value;
  wire [2:0] value;
  assign \$1  = value <  4'h8;
  always @(posedge clk)
    segments <= \segments$next ;
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$4 ) begin end
    casez (\$1 )
      
      1'h1:
          casez (value)
            3'h0:
                \segments$next  = 8'h02;
            3'h1:
                \segments$next  = 8'hf6;
            3'h2:
                \segments$next  = 8'hee;
            3'h3:
                \segments$next  = 8'h3e;
            3'h4:
                \segments$next  = 8'h9c;
            3'h5:
                \segments$next  = 8'h7a;
            3'h6:
                \segments$next  = 8'h9e;
            3'h?:
                \segments$next  = 8'h8e;
          endcase
      
      default:
          \segments$next  = 8'h00;
    endcase
    casez (rst)
      1'h1:
          \segments$next  = 8'h00;
    endcase
  end
endmodule

module pin_devinputs_0__clkconf0(devinputs_0__clkconf0__io, devinputs_0__clkconf0__i);
  output devinputs_0__clkconf0__i;
  wire devinputs_0__clkconf0__i;
  inout devinputs_0__clkconf0__io;
  wire devinputs_0__clkconf0__io;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h01)
  ) devinputs_0__clkconf0_0 (
    .D_IN_0(devinputs_0__clkconf0__i),
    .PACKAGE_PIN(devinputs_0__clkconf0__io)
  );
endmodule

module pin_devinputs_0__clkconf1(devinputs_0__clkconf1__io, devinputs_0__clkconf1__i);
  output devinputs_0__clkconf1__i;
  wire devinputs_0__clkconf1__i;
  inout devinputs_0__clkconf1__io;
  wire devinputs_0__clkconf1__io;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h01)
  ) devinputs_0__clkconf1_0 (
    .D_IN_0(devinputs_0__clkconf1__i),
    .PACKAGE_PIN(devinputs_0__clkconf1__io)
  );
endmodule

module pin_devinputs_0__extclk(devinputs_0__extclk__io, devinputs_0__extclk__i);
  output devinputs_0__extclk__i;
  wire devinputs_0__extclk__i;
  inout devinputs_0__extclk__io;
  wire devinputs_0__extclk__io;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h01)
  ) devinputs_0__extclk_0 (
    .D_IN_0(devinputs_0__extclk__i),
    .PACKAGE_PIN(devinputs_0__extclk__io)
  );
endmodule

module pin_devinputs_0__signal(devinputs_0__signal__io, devinputs_0__signal__i);
  output devinputs_0__signal__i;
  wire devinputs_0__signal__i;
  inout devinputs_0__signal__io;
  wire devinputs_0__signal__io;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h01)
  ) devinputs_0__signal_0 (
    .D_IN_0(devinputs_0__signal__i),
    .PACKAGE_PIN(devinputs_0__signal__io)
  );
endmodule

module pin_dualdisp_0__aa(dualdisp_0__aa__io, dualdisp_0__aa__o);
  inout dualdisp_0__aa__io;
  wire dualdisp_0__aa__io;
  input dualdisp_0__aa__o;
  wire dualdisp_0__aa__o;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) dualdisp_0__aa_0 (
    .D_OUT_0(dualdisp_0__aa__o),
    .PACKAGE_PIN(dualdisp_0__aa__io)
  );
endmodule

module pin_dualdisp_0__ab(dualdisp_0__ab__io, dualdisp_0__ab__o);
  inout dualdisp_0__ab__io;
  wire dualdisp_0__ab__io;
  input dualdisp_0__ab__o;
  wire dualdisp_0__ab__o;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) dualdisp_0__ab_0 (
    .D_OUT_0(dualdisp_0__ab__o),
    .PACKAGE_PIN(dualdisp_0__ab__io)
  );
endmodule

module pin_dualdisp_0__ac(dualdisp_0__ac__io, dualdisp_0__ac__o);
  inout dualdisp_0__ac__io;
  wire dualdisp_0__ac__io;
  input dualdisp_0__ac__o;
  wire dualdisp_0__ac__o;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) dualdisp_0__ac_0 (
    .D_OUT_0(dualdisp_0__ac__o),
    .PACKAGE_PIN(dualdisp_0__ac__io)
  );
endmodule

module pin_dualdisp_0__ad(dualdisp_0__ad__io, dualdisp_0__ad__o);
  inout dualdisp_0__ad__io;
  wire dualdisp_0__ad__io;
  input dualdisp_0__ad__o;
  wire dualdisp_0__ad__o;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) dualdisp_0__ad_0 (
    .D_OUT_0(dualdisp_0__ad__o),
    .PACKAGE_PIN(dualdisp_0__ad__io)
  );
endmodule

module pin_dualdisp_0__ae(dualdisp_0__ae__io, dualdisp_0__ae__o);
  inout dualdisp_0__ae__io;
  wire dualdisp_0__ae__io;
  input dualdisp_0__ae__o;
  wire dualdisp_0__ae__o;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) dualdisp_0__ae_0 (
    .D_OUT_0(dualdisp_0__ae__o),
    .PACKAGE_PIN(dualdisp_0__ae__io)
  );
endmodule

module pin_dualdisp_0__af(dualdisp_0__af__io, dualdisp_0__af__o);
  inout dualdisp_0__af__io;
  wire dualdisp_0__af__io;
  input dualdisp_0__af__o;
  wire dualdisp_0__af__o;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) dualdisp_0__af_0 (
    .D_OUT_0(dualdisp_0__af__o),
    .PACKAGE_PIN(dualdisp_0__af__io)
  );
endmodule

module pin_dualdisp_0__ag(dualdisp_0__ag__io, dualdisp_0__ag__o);
  inout dualdisp_0__ag__io;
  wire dualdisp_0__ag__io;
  input dualdisp_0__ag__o;
  wire dualdisp_0__ag__o;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) dualdisp_0__ag_0 (
    .D_OUT_0(dualdisp_0__ag__o),
    .PACKAGE_PIN(dualdisp_0__ag__io)
  );
endmodule

module pin_dualdisp_0__cathode(dualdisp_0__cathode__io, dualdisp_0__cathode__o);
  inout dualdisp_0__cathode__io;
  wire dualdisp_0__cathode__io;
  input dualdisp_0__cathode__o;
  wire dualdisp_0__cathode__o;
  SB_IO #(
    .IO_STANDARD("SB_LVCMOS"),
    .PIN_TYPE(6'h19)
  ) dualdisp_0__cathode_0 (
    .D_OUT_0(dualdisp_0__cathode__o),
    .PACKAGE_PIN(dualdisp_0__cathode__io)
  );
endmodule

module proxdisplay(rst, value, segments, clk);
  reg \$auto$verilog_backend.cc:2097:dump_module$5  = 0;
  wire \$1 ;
  input clk;
  wire clk;
  input rst;
  wire rst;
  output [7:0] segments;
  reg [7:0] segments = 8'h00;
  reg [7:0] \segments$next ;
  input [2:0] value;
  wire [2:0] value;
  assign \$1  = value <  4'h8;
  always @(posedge clk)
    segments <= \segments$next ;
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$5 ) begin end
    casez (\$1 )
      
      1'h1:
          casez (value)
            3'h0:
                \segments$next  = 8'h2a;
            3'h1:
                \segments$next  = 8'h01;
            3'h2:
                \segments$next  = 8'h46;
            3'h3:
                \segments$next  = 8'h01;
            3'h4:
                \segments$next  = 8'h38;
            3'h5:
                \segments$next  = 8'h01;
            3'h6:
                \segments$next  = 8'hc4;
            3'h?:
                \segments$next  = 8'h01;
          endcase
      
      default:
          \segments$next  = 8'h00;
    endcase
    casez (rst)
      1'h1:
          \segments$next  = 8'h00;
    endcase
  end
endmodule

module pulsecounter(clock_config, pulseCount, clk, rst, \input );
  reg \$auto$verilog_backend.cc:2097:dump_module$6  = 0;
  wire [11:0] \$1 ;
  wire \$10 ;
  wire [11:0] \$12 ;
  wire [11:0] \$13 ;
  wire [11:0] \$2 ;
  wire \$4 ;
  wire \$6 ;
  wire \$8 ;
  input clk;
  wire clk;
  reg [10:0] clockCount = 11'h000;
  reg [10:0] \clockCount$next ;
  input [1:0] clock_config;
  wire [1:0] clock_config;
  wire edge_detect_input;
  wire edge_detect_output;
  input \input ;
  wire \input ;
  output [10:0] pulseCount;
  reg [10:0] pulseCount = 11'h000;
  reg [10:0] \pulseCount$next ;
  input rst;
  wire rst;
  reg [10:0] runningPulseCount = 11'h000;
  reg [10:0] \runningPulseCount$next ;
  reg [10:0] singlePeriodClockCount = 11'h000;
  reg [10:0] \singlePeriodClockCount$next ;
  assign \$10  = !  clockCount;
  assign \$13  = runningPulseCount +  1'h1;
  always @(posedge clk)
    clockCount <= \clockCount$next ;
  always @(posedge clk)
    singlePeriodClockCount <= \singlePeriodClockCount$next ;
  always @(posedge clk)
    pulseCount <= \pulseCount$next ;
  always @(posedge clk)
    runningPulseCount <= \runningPulseCount$next ;
  assign \$2  = clockCount +  1'h1;
  assign \$4  = clockCount ==  singlePeriodClockCount;
  assign \$6  = clockCount ==  singlePeriodClockCount;
  assign \$8  = clockCount ==  singlePeriodClockCount;
  edge_detect edge_detect (
    .clk(clk),
    .\input (edge_detect_input),
    .\output (edge_detect_output),
    .rst(rst)
  );
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$6 ) begin end
    \clockCount$next  = \$2 [10:0];
    casez (\$4 )
      
      1'h1:
          \clockCount$next  = 11'h000;
    endcase
    casez (rst)
      1'h1:
          \clockCount$next  = 11'h000;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$6 ) begin end
    casez (clock_config)
      
      2'h0:
          \singlePeriodClockCount$next  = 11'h1f4;
      
      2'h1:
          \singlePeriodClockCount$next  = 11'h3e8;
      
      2'h3:
          \singlePeriodClockCount$next  = 11'h667;
      
      2'h2:
          \singlePeriodClockCount$next  = 11'h7d0;
    endcase
    casez (rst)
      1'h1:
          \singlePeriodClockCount$next  = 11'h000;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$6 ) begin end
    \pulseCount$next  = pulseCount;
    casez (\$6 )
      
      1'h1:
          \pulseCount$next  = runningPulseCount;
    endcase
    casez (rst)
      1'h1:
          \pulseCount$next  = 11'h000;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2097:dump_module$6 ) begin end
    \runningPulseCount$next  = runningPulseCount;
    casez (\$8 )
      
      1'h1:
          /* empty */;
      
      default:
          casez (\$10 )
            
            1'h1:
                casez (edge_detect_output)
                  
                  1'h1:
                      \runningPulseCount$next  = 11'h001;
                  
                  default:
                      \runningPulseCount$next  = 11'h000;
                endcase
            
            default:
                casez (edge_detect_output)
                  
                  1'h1:
                      \runningPulseCount$next  = \$13 [10:0];
                endcase
          endcase
    endcase
    casez (rst)
      1'h1:
          \runningPulseCount$next  = 11'h000;
    endcase
  end
  assign \$1  = \$2 ;
  assign \$12  = \$13 ;
  assign edge_detect_input = \input ;
endmodule

module top(dualdisp_0__af__io, dualdisp_0__ag__io, dualdisp_0__cathode__io, dualdisp_0__aa__io, dualdisp_0__ab__io, dualdisp_0__ac__io, dualdisp_0__ad__io, devinputs_0__signal__io, devinputs_0__clkconf0__io, devinputs_0__clkconf1__io, devinputs_0__extclk__io, dualdisp_0__ae__io);
  wire [1:0] clock_config;
  inout devinputs_0__clkconf0__io;
  wire devinputs_0__clkconf0__io;
  inout devinputs_0__clkconf1__io;
  wire devinputs_0__clkconf1__io;
  inout devinputs_0__extclk__io;
  wire devinputs_0__extclk__io;
  inout devinputs_0__signal__io;
  wire devinputs_0__signal__io;
  wire [7:0] discriminator_edge_count;
  wire discriminator_match_exact;
  wire discriminator_match_far;
  wire discriminator_match_high;
  wire [2:0] discriminator_note;
  wire [7:0] displaySegments;
  wire displaySelect;
  wire display_proximitySelect;
  wire [7:0] display_segments;
  wire [2:0] display_valueNote;
  wire [2:0] display_valueProxim;
  inout dualdisp_0__aa__io;
  wire dualdisp_0__aa__io;
  inout dualdisp_0__ab__io;
  wire dualdisp_0__ab__io;
  inout dualdisp_0__ac__io;
  wire dualdisp_0__ac__io;
  inout dualdisp_0__ad__io;
  wire dualdisp_0__ad__io;
  inout dualdisp_0__ae__io;
  wire dualdisp_0__ae__io;
  inout dualdisp_0__af__io;
  wire dualdisp_0__af__io;
  inout dualdisp_0__ag__io;
  wire dualdisp_0__ag__io;
  inout dualdisp_0__cathode__io;
  wire dualdisp_0__cathode__io;
  wire input_pulses;
  wire pin_devinputs_0__clkconf0_devinputs_0__clkconf0__i;
  wire pin_devinputs_0__clkconf1_devinputs_0__clkconf1__i;
  wire pin_devinputs_0__extclk_devinputs_0__extclk__i;
  wire pin_devinputs_0__signal_devinputs_0__signal__i;
  wire pin_dualdisp_0__aa_dualdisp_0__aa__o;
  wire pin_dualdisp_0__ab_dualdisp_0__ab__o;
  wire pin_dualdisp_0__ac_dualdisp_0__ac__o;
  wire pin_dualdisp_0__ad_dualdisp_0__ad__o;
  wire pin_dualdisp_0__ae_dualdisp_0__ae__o;
  wire pin_dualdisp_0__af_dualdisp_0__af__o;
  wire pin_dualdisp_0__ag_dualdisp_0__ag__o;
  wire pin_dualdisp_0__cathode_dualdisp_0__cathode__o;
  wire pulsecounter_clk;
  wire [1:0] pulsecounter_clock_config;
  wire pulsecounter_input;
  wire [10:0] pulsecounter_pulseCount;
  wire pulsecounter_rst;
  discriminator discriminator (
    .clk(pulsecounter_clk),
    .edge_count(discriminator_edge_count),
    .match_exact(discriminator_match_exact),
    .match_far(discriminator_match_far),
    .match_high(discriminator_match_high),
    .note(discriminator_note),
    .rst(1'h0)
  );
  display display (
    .clk(pulsecounter_clk),
    .proximitySelect(display_proximitySelect),
    .rst(1'h0),
    .segments(display_segments),
    .valueNote(display_valueNote),
    .valueProxim(display_valueProxim)
  );
  pin_devinputs_0__clkconf0 pin_devinputs_0__clkconf0 (
    .devinputs_0__clkconf0__i(pin_devinputs_0__clkconf0_devinputs_0__clkconf0__i),
    .devinputs_0__clkconf0__io(devinputs_0__clkconf0__io)
  );
  pin_devinputs_0__clkconf1 pin_devinputs_0__clkconf1 (
    .devinputs_0__clkconf1__i(pin_devinputs_0__clkconf1_devinputs_0__clkconf1__i),
    .devinputs_0__clkconf1__io(devinputs_0__clkconf1__io)
  );
  pin_devinputs_0__extclk pin_devinputs_0__extclk (
    .devinputs_0__extclk__i(pin_devinputs_0__extclk_devinputs_0__extclk__i),
    .devinputs_0__extclk__io(devinputs_0__extclk__io)
  );
  pin_devinputs_0__signal pin_devinputs_0__signal (
    .devinputs_0__signal__i(pin_devinputs_0__signal_devinputs_0__signal__i),
    .devinputs_0__signal__io(devinputs_0__signal__io)
  );
  pin_dualdisp_0__aa pin_dualdisp_0__aa (
    .dualdisp_0__aa__io(dualdisp_0__aa__io),
    .dualdisp_0__aa__o(pin_dualdisp_0__aa_dualdisp_0__aa__o)
  );
  pin_dualdisp_0__ab pin_dualdisp_0__ab (
    .dualdisp_0__ab__io(dualdisp_0__ab__io),
    .dualdisp_0__ab__o(pin_dualdisp_0__ab_dualdisp_0__ab__o)
  );
  pin_dualdisp_0__ac pin_dualdisp_0__ac (
    .dualdisp_0__ac__io(dualdisp_0__ac__io),
    .dualdisp_0__ac__o(pin_dualdisp_0__ac_dualdisp_0__ac__o)
  );
  pin_dualdisp_0__ad pin_dualdisp_0__ad (
    .dualdisp_0__ad__io(dualdisp_0__ad__io),
    .dualdisp_0__ad__o(pin_dualdisp_0__ad_dualdisp_0__ad__o)
  );
  pin_dualdisp_0__ae pin_dualdisp_0__ae (
    .dualdisp_0__ae__io(dualdisp_0__ae__io),
    .dualdisp_0__ae__o(pin_dualdisp_0__ae_dualdisp_0__ae__o)
  );
  pin_dualdisp_0__af pin_dualdisp_0__af (
    .dualdisp_0__af__io(dualdisp_0__af__io),
    .dualdisp_0__af__o(pin_dualdisp_0__af_dualdisp_0__af__o)
  );
  pin_dualdisp_0__ag pin_dualdisp_0__ag (
    .dualdisp_0__ag__io(dualdisp_0__ag__io),
    .dualdisp_0__ag__o(pin_dualdisp_0__ag_dualdisp_0__ag__o)
  );
  pin_dualdisp_0__cathode pin_dualdisp_0__cathode (
    .dualdisp_0__cathode__io(dualdisp_0__cathode__io),
    .dualdisp_0__cathode__o(pin_dualdisp_0__cathode_dualdisp_0__cathode__o)
  );
  pulsecounter pulsecounter (
    .clk(pulsecounter_clk),
    .clock_config(pulsecounter_clock_config),
    .\input (pulsecounter_input),
    .pulseCount(pulsecounter_pulseCount),
    .rst(1'h0)
  );
  assign pulsecounter_rst = 1'h0;
  assign clock_config = { pin_devinputs_0__clkconf1_devinputs_0__clkconf1__i, pin_devinputs_0__clkconf0_devinputs_0__clkconf0__i };
  assign input_pulses = pin_devinputs_0__signal_devinputs_0__signal__i;
  assign pulsecounter_clk = pin_devinputs_0__extclk_devinputs_0__extclk__i;
  assign pin_dualdisp_0__cathode_dualdisp_0__cathode__o = displaySelect;
  assign pin_dualdisp_0__ag_dualdisp_0__ag__o = displaySegments[1];
  assign pin_dualdisp_0__af_dualdisp_0__af__o = displaySegments[2];
  assign pin_dualdisp_0__ae_dualdisp_0__ae__o = displaySegments[3];
  assign pin_dualdisp_0__ad_dualdisp_0__ad__o = displaySegments[4];
  assign pin_dualdisp_0__ac_dualdisp_0__ac__o = displaySegments[5];
  assign pin_dualdisp_0__ab_dualdisp_0__ab__o = displaySegments[6];
  assign pin_dualdisp_0__aa_dualdisp_0__aa__o = displaySegments[7];
  assign displaySelect = display_proximitySelect;
  assign displaySegments = display_segments;
  assign display_valueProxim = { discriminator_match_far, discriminator_match_high, discriminator_match_exact };
  assign display_valueNote = discriminator_note;
  assign discriminator_edge_count = pulsecounter_pulseCount[7:0];
  assign pulsecounter_clock_config = clock_config;
  assign pulsecounter_input = input_pulses;
endmodule
