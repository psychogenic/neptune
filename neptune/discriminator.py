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
import math
from enum import Enum, unique

from amaranth import Elaboratable, Signal, Module, Const, Array, unsigned, ResetSignal
from amaranth.build import Platform
from amaranth.asserts import Assert, Assume, Cover

import neptune.notes as notes
from neptune.notes import Tuning, DetectedNote
import neptune.neptune_config as config
from neptune.testing.history import History


# FSM states
@unique
class DiscriminatorState(Enum):
    PowerUp                 = 0 
    Init                    = 1
    CalculateDiffFromTarget = 2
    Compare                 = 3
    MovedToNextCheckBounds  = 4
    DetectedValidNote       = 5
    DisplayResult           = 6
    
    

    
class Discriminator(Elaboratable):
    '''
        The Discriminator does all the heavy lifting in Neptune: its what tells the 
        difference between frequencies of interest and irrelevant input, and what 
        determines "proximity".
        
        Currently implements functionality through an FSM.
    
    '''
    
    def __init__(self, usingTuning:Tuning, # the set of notes we care about
                 samplingDurationSeconds:float=config.SamplingDurationDefault, # the time over which we're gathering input pulse counts
                 detectionWindowHz:int=config.MaxDetectionHzWindowDefault # the window for "valid" and "close" detection, in Hz
                 ):
        
        self.tuning = usingTuning
        
        self.samplingDurationSeconds = samplingDurationSeconds
        self.detectionWindowHz = detectionWindowHz
        
        # we need to count up at least to whatever the max reportable 
        # frequency is, plus some room above for our detection window
        
        maxFreqHz = self.tuning.highest.frequency
        countJitterHeadroomHz = detectionWindowHz # we only use half this window, but whatever, won't die from extra bits
        
        # everything is specified in Hz however.  If, e.g., we are only sampling 
        # for half a second, then all these values get scaled by half as well,
        # so real maxCount is:
        maxCount = (maxFreqHz + countJitterHeadroomHz) * samplingDurationSeconds
        
        # and for this we need this many bits, tops
        countBits = math.ceil(math.log2(round(maxCount)))
        self.input_bits = countBits
        
        #### INPUT ####
        # edge_count: count of ticks over SAMPLETIME
        self.edge_count = Signal(unsigned(self.input_bits))
        
        #### OUTPUTS ####
        
        # note: the Scale.NOTE detected, if any (or Scale.NA)
        self.note = Signal(self.tuning.required_note_bits)
        
        
        # match_* bits: note match attributes
        # valid when note != Scale.NA
        #    - exact: reported note is considered "spot on"
        #    - high: if not exact, is above target freq
        #    - far:  if not exact, is considered pretty distant
        self.match_exact = Signal()
        self.match_high = Signal()
        self.match_far = Signal()
        
    def ports(self):
        return [self.edge_count, self.note, self.match_exact, self.match_high, self.match_far]
    
    
    @property 
    def detectionWindowSpanCount(self) -> int:
        # detectionWindowHz must be adjusted to account for the 
        # desired sampling duration
        return math.ceil(self.detectionWindowHz * self.samplingDurationSeconds)
    
    @property 
    def detectionWindowMidPoint(self) -> int:
        # midway point of the span is useful for a number of reasons,
        # notably that that is where our target frequency lies
        return (math.ceil(self.detectionWindowSpanCount/2))
    
    

    def expectedCountForNote(self, aNote:DetectedNote) -> int:
        '''
            The pulse count expected based on frequency and sampling time
        '''
        return round(aNote.frequency * self.samplingDurationSeconds)
    
    
    
    def maxCountForNote(self, aNote:DetectedNote) -> int:
        '''
            The maximum "reasonable" count for this note, based on expected plus
            half the proximity detection window (adjusted for sampling time)
        '''
        return self.detectionWindowMidPoint + self.expectedCountForNote(aNote)
    
    
        
    def elaborate(self, platform:Platform):
        m = Module()
        self.elaborateStateMachine(m, platform)
        return m
        
    
    
    def elaborateStateMachine(self, m:Module, platform:Platform):
        
        
        curState = Signal(DiscriminatorState) # FSM current state
        
        maxNoMatchesBeforeErase = 31
        noMatchCount = Signal(range(maxNoMatchesBeforeErase+1))
        
        # during search, we will subtract each target count from actual edge count 
        # the distance may be very large, so the result must have as many bits as the
        # input edge count itself, to ensure we don't wrap
        subtractResult = Signal(unsigned(self.input_bits))
        
        # in cases where the subtraction above is "close enough" -- ie within our
        # detection window span, further processing will occur
        # this smaller value is guaranteed to have a max value equal to the 
        # detection window itself, hence we create a signal with less bits for this
        # distance result
        readingProximityResult = Signal(range(self.detectionWindowSpanCount + 1 ))
        
        inputFreqHigher = Signal()
        
        curNoteIndex = Signal(range(len(self.tuning)))
        m.d.sync += curState.eq(DiscriminatorState.PowerUp)
        
        # these two arrays get used within the actual verilog, so they are Array objects
        
        # the tests we'll be doing, highest frequency first
        TestsDescending = Array(
            list(map(lambda n: Const(self.maxCountForNote(n), unsigned(self.input_bits)), 
                     self.tuning.descending)))
        
        # the notes related to each test, in the same order
        NotesSortedByTestIdx = Array(
            list(map(lambda x: x.note, self.tuning.descending))
            )
        
        
        # the actual FSM dispatcher
        with m.Switch(curState):
            with m.Case(DiscriminatorState.PowerUp):
                m.d.sync += [
                     noMatchCount.eq(0),
                     curState.eq(DiscriminatorState.Init)
                ]
                
            
            # init state
            with m.Case(DiscriminatorState.Init):
                m.d.sync += [
                    curNoteIndex.eq(0), # begin search at start of array
                    curState.eq(DiscriminatorState.CalculateDiffFromTarget) # move into search state
                ]
                
                with m.If(noMatchCount == maxNoMatchesBeforeErase):
                    m.d.sync += self.note.eq(notes.Scale.NA)
                
            # calculation state
            with m.Case(DiscriminatorState.CalculateDiffFromTarget):
                # basically just load difference into subtractResult
                # and move on
                m.d.sync += [
                    subtractResult.eq(TestsDescending[curNoteIndex] - self.edge_count),
                    curState.eq(DiscriminatorState.Compare)
                ]
                
                
                
            with m.Case(DiscriminatorState.Compare):
                # check if difference is smaller than our threshold window
                with m.If(subtractResult <= self.detectionWindowSpanCount):
                    # if it is, we're close enough to call this a valid note
                    m.d.sync += [ 
                        self.note.eq(NotesSortedByTestIdx[curNoteIndex]), # set output note to Scale.XXX
                        curState.eq(DiscriminatorState.DetectedValidNote) # move to processing
                    ]
                with m.Else():
                    # if not, move to next note 
                    m.d.sync += [
                        curNoteIndex.eq(curNoteIndex + 1),
                        curState.eq(DiscriminatorState.MovedToNextCheckBounds)
                    ]
                    
                        
                        
            with m.Case(DiscriminatorState.MovedToNextCheckBounds):
                # didn't match last check
                # make sure current note index is valid first
                with m.If(curNoteIndex < Const(len(self.tuning))):
                    # yep.
                    # we haven't check all in tuning yet, so this current note 
                    # index is valid: do diff calculation
                    m.d.sync += curState.eq(DiscriminatorState.CalculateDiffFromTarget)
                with m.Else():
                    # we're out of bounds, back to init but also make note 
                    # that we've done another full scan without a match
                    m.d.sync += [
                        curState.eq(DiscriminatorState.Init),
                        noMatchCount.eq(noMatchCount + 1)
                    ]
                        
                
                        
            # found a valid note state
            with m.Case(DiscriminatorState.DetectedValidNote):
                # we are close enough to some note to call it "detected" and display something
                #
                # what would be nice is to have a unified set of tests regardless of if we are 
                # off by +ve or -ve amount
                
                # to do this, math will come in handy.
                
                # the situation: subtractResult holds
                # (exactCountForNote + windowHalfSpan) - actualEdgeCount
                # e.g. for 330Hz and 32Hz window
                #  subtractResult = (330 + 15) - actualCount
                #
                #  So if result of subtraction was:
                #  1* windowHalfSpan -> we are exactly on the target note, yayz!
                #  2* [0, windowHalfSpan[ -> we are somewhat above the target note freq (0 is way above, and higher value is closer)
                #  3* ]windowHalfSpan, windowSpan] -> we are somewhat below target note freq (windowSpan is way above, and lower value is closer)
                
                # to get tests unified, we flip the case 3 value by doing
                #    windowSpan - subtractResult
                # such that anything close to target freq (ie windowHalfSpan) stays close to 
                # there, and anything "far away" get's shifted toward 0.  After this
                #   0 <- far away ... higgher closer -> halfspan == target
                # regardless of if we were above or below.
                with m.If(subtractResult <= self.detectionWindowMidPoint):
                    # either on or above target note, our proximity result is simply the subtractResult
                    # note we were higher (or equal)
                    m.d.sync += [
                        readingProximityResult.eq(subtractResult), # proxim value is simply the result of the subtraction
                        inputFreqHigher.eq(1) # remember that measured freq is higher or equal
                    ]
                with m.Else():
                    # we are below target note, so we do that flip using a subtraction
                    # note we were lower
                    m.d.sync += [
                        readingProximityResult.eq(self.detectionWindowSpanCount - subtractResult),
                        inputFreqHigher.eq(0)
                    ]
                
                # move to next state, and reset the noMatchCount
                m.d.sync += [
                    curState.eq(DiscriminatorState.DisplayResult),
                    noMatchCount.eq(0)
                ]
                
            with m.Case(DiscriminatorState.DisplayResult):
                #
                #  Here we take all our processed results and actually 
                # write the output values that are our discriminator reports
                # on matches to the outside world/upper layers.
                
                # At this stage, we have:
                # 
                #  * a readingProximityResult value between 0 and windowHalfSpan
                #    where greater value ==> closer to target
                #  * a inputFreqHigher which tells us if our error is a freq that
                #    is higher than target or not (lower)
                
                
                    
                # we'll use a simple rule for determining proximity:
                #  - anything really close to halfspan -> "exact match"
                #  - otherwise, not exact but any "proximity" less that halfspan/2 is "far away"
                with m.If(readingProximityResult >=  (self.detectionWindowMidPoint - 1)):
                    m.d.sync += [
                        self.match_exact.eq(1),
                        self.match_far.eq(0)
                    ]
                    
                with m.Else():
                    # near or far but not considered an exact match, no matter what
                    m.d.sync +=  self.match_exact.eq(0)
                    
                    with m.If(readingProximityResult <= math.ceil(self.detectionWindowMidPoint/2)):
                        # call this far away
                        m.d.sync += self.match_far.eq(1)
                            
                    with m.Else():
                        # pretty close
                        m.d.sync += self.match_far.eq(0)     
                        
                
                
                # after all this, we'll go back to init.
                # also report if measurement is higher or lower than target
                # by mapping the inputFreqHigher bit directly
                m.d.sync += [
                    curState.eq(DiscriminatorState.Init), # we'll
                    self.match_high.eq(inputFreqHigher)
                ]
                               
            
            with m.Default():
                # catch any weird start-up state, and shunt it 
                # to reset
                m.d.sync += curState.eq(DiscriminatorState.PowerUp)
        

        
        
        
    def elaborateParallel(self, m:Module, platform:Platform):
        
        m.d.sync += self.note.eq(notes.Scale.NA) 
        
        distanceValue = Signal(range(self.detectionWindowHz + 1))
        
        for aNote in self.tuning.descending:
            
            compareCount = Const(self.maxCountForNote(aNote))
            
            subtractResult = Signal(self.input_bits)
            
            m.d.comb += subtractResult.eq(compareCount - self.edge_count)
            with m.If(subtractResult <= self.detectionWindowHz):
                m.d.sync += self.note.eq(aNote.note)
                m.d.comb += distanceValue.eq(subtractResult)
                
        
        # at this stage self.note has NA or a note within window
        # and distanceValue has the last delta value
        
        


def simulate(usingTuning:Tuning, samplingDurationSecs:float=1.0):
    m = Module() # top
    m.submodules.discriminator = dut = Discriminator(usingTuning)
    
    
    def setEdgeCountToFrequency(f:float, deltaVal:int = 0):
        sampledFreq = round(f * samplingDurationSecs)
        yield dut.edge_count.eq(sampledFreq + deltaVal)
            
    def tunerTestWithDelta(deltaVal:int):
        yield Delay(1e-4)
        for aNote in usingTuning.ascending[:1]:
            yield from setEdgeCountToFrequency(aNote.frequency, deltaVal)
            yield Delay(40e-3)
            
    def tunerTestExact():
        yield from tunerTestWithDelta(0) # EXACT
        
    def tunerTest():
        yield from tunerTestWithDelta(0) # EXACT
        yield from tunerTestWithDelta(7) # far + high
        yield from tunerTestWithDelta(4) # high
        yield from tunerTestWithDelta(-4) # low
        yield from tunerTestWithDelta(-7) # far + low 
        
        
    def tunerTestRange():
        baseFreq = 305
        for i in range(0,68,3):
            yield from setEdgeCountToFrequency(baseFreq + i)
            yield Delay(40e-3)
            
        for i in range(0,75,3):
            yield from setEdgeCountToFrequency((baseFreq + 50) - i)
            yield Delay(40e-3)
        
    
            
        
    runSimulator(m, 'discriminator', 
                 [dut.edge_count, dut.note, dut.match_exact, dut.match_far, dut.match_high], 
                 [tunerTest], clockFreq=1e3)



def coverAndProve(m:Module, discrim:Discriminator, includeCovers:bool=False):
    # Note: I have a condition below that makes the period 0.1s -- so 
    # during testing we only need to count a bit past 100 ticks to see results
    rst = Signal()
    m.d.comb += ResetSignal().eq(rst)
    m.d.comb += [
        Assume(~rst), # don't play with reset
    ]
    
    hist = History.new(m, 50)
    hist.track(discrim.edge_count)
    hist.track(discrim.note)
    
    baseFreq = 330
    for freq in range(baseFreq-14, baseFreq + 14):
        with m.If( hist.wasConstant(discrim.edge_count, value=freq, startTick=0, numTicks=6) ):
            with m.If(hist.ticks == 7):
                m.d.comb += Assert(hist.snapshot(discrim.note, 6) == notes.Scale.E)
                
                if freq >= baseFreq:
                    m.d.comb += Assert(discrim.match_high)
                else:
                    m.d.comb += Assert(~discrim.match_high)
                    
                
                if abs(freq - baseFreq) < 2:
                    m.d.comb += Assert(discrim.match_exact)
                else:
                    m.d.comb += Assert(~discrim.match_exact)
                    
                if abs(freq - baseFreq) < (discrim.detectionWindowHz/4):
                    m.d.comb += Assert(~discrim.match_far)
                else:
                    m.d.comb += Assert(discrim.match_far)
                    

    if includeCovers:
        with m.If(hist.wasConstant(discrim.edge_count, value=110, startTick=0, numTicks=20)):
            m.d.comb += Cover((discrim.note == notes.Scale.A) & discrim.match_exact )
        with m.If(hist.wasConstant(discrim.edge_count, value=199, startTick=0, numTicks=20)):
            m.d.comb += Cover((discrim.note == notes.Scale.G))
        
        

def ho():
    m = Module() # top level
    m.submodules.discriminator = dev = Discriminator(notes.StandardGuitarTuning)
    coverAndProve(m, dev) 
    return (m,dev,m.submodules._history)

if __name__ == "__main__":
    # allow us to run this directly
    from amaranth.cli import main
    from neptune.sims.runner import runSimulator, Delay
    doSimulate = False
    Test = True 
    if (doSimulate):
        simulate(notes.StandardGuitarTuning, samplingDurationSecs=1.0)
    else:
        if Test:
            samplingDurationSecs=1.0 
        else:
            samplingDurationSecs=config.SamplingDurationDefault
        m = Module() # top level
        m.submodules.discriminator = dev = Discriminator(notes.StandardGuitarTuning, 
                                                         samplingDurationSeconds=samplingDurationSecs)
        if Test:
            coverAndProve(m, dev, includeCovers=False) 
            
        main(m, ports=dev.ports())