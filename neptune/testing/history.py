'''
Created on Apr 18, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com
'''
from amaranth import Elaboratable, Signal, Module, Array
from amaranth.build import Platform

class RecentPast:
    def __init__(self, s:Signal, maxHistory:int=50):
        self.rose = Signal()
        self.fell = Signal()
        self.rose_trace = Signal(maxHistory)
        self.fell_trace = Signal(maxHistory)
        nsuf = s.name
        self.rose.name = f'rose_{nsuf}'
        self.fell.name = f'fell_{nsuf}'
        self.rose_trace.name = f'rosetrace_{nsuf}'
        self.fell_trace.name = f'felltrace_{nsuf}'

class History(Elaboratable):
    '''
        Track the history of signals of interest.
        
        Weirdly, Past and all my old friends for testing seem to be deprecated and
        I got absolutely 0 love or information from the amaranth guys on how to 
        replace it (other than "use registers" which was super helpful).
        
        So this utility class lets you preserve and observe the history of 
        signals of interest.
        
        @copyright: (C) 2023 Pat Deegan, https://psychogenic.com
        
        Basic attempt to replace Past() functions.  Rather than working backwards,
        you track() signals of interest and then can access their state at any point
        (up to maxHistory), e.g.
        
        hist = History()
        
        hist.track(somesignal)
        
        # ...
        
        # two cycles after somesignal rises, anothersig will be true
        with m.If( (hist.ticks == 3) & 
                    ~hist.snapshot(somesignal, 0) &
                    hist.snapshot(somesignal, 1)):
            m.d.comb += Assert(anothersig == 1)
        
        @note: barely tested, but see the __main__ in discriminator etc to check it 
        in use.
    '''
    @classmethod 
    def new(cls, m:Module, maxHistory:int=50):
        hist = cls(maxHistory)
        m.submodules._history = hist 
        return hist 
    
    def __init__(self, maxHistory:int=50):
        self.registers = Array()
        self.history = Array()
        self.recentPast = Array()
        self.regmap = dict()
        self.maxHistory = maxHistory
        self.ticks = Signal(range(self.maxHistory))
        self.usingRecentPast = False
        
    def track(self, s:Signal):
        '''
            track -- add signal to list of those for which we take snapshots
        '''
        sighist = Signal(len(s)*self.maxHistory)
        regIdx = len(self.registers)
        sighist.name = f'shist_{s.name}'
        self.history.append(sighist)
        self.registers.append(s)
        self.regmap[s.name] = regIdx
        
        self.recentPast.append(RecentPast(s, self.maxHistory))


        
    def snapshot(self, s:Signal, tickIdx:int):
        '''
            snapshot -- get the value of the signal at tick tickIdx
        '''
        return self.history[self.regmap[s.name]][self.sliceStart(s, tickIdx):self.sliceEnd(s, tickIdx)]
        
    def rose(self, s:Signal):
        '''
            rose -- if the signal of interest just went from low to high
        '''
        self.usingRecentPast = True
        return self.recentPast[self.regmap[s.name]].rose
    def fell(self, s:Signal):
        '''
            fell - if the signal of interest just went from high to low
        '''
        self.usingRecentPast = True
        return self.recentPast[self.regmap[s.name]].fell
        
    def ago(self, numTicksBack:int):
        return self.ticks - numTicksBack
    
    @property
    def now(self):
        return self.ticks
    
    def sequence(self, s:Signal, startTick:int, numTicks:int):
        '''
            sequence -- get the value(s) of a signal over multiple ticks, all as one long blob
        '''
        return self.history[self.regmap[s.name]][self.sliceStart(s, startTick):self.sliceEnd(s, startTick+numTicks)]
    
    def wasConstant(self, s:Signal, value:int, startTick:int, numTicks:int):
        '''
            wasConstant
            Returns something you can stick in an m.If() to say
            if this signal had value value for this many ticks, starting at tick x
            then ...
        '''
        vList = [value] * numTicks
        return self.followedSequence(s, vList, startTick, numTicks)
    
    def followedSequence(self, s:Signal, values:list, startTick:int=0, numTicks:int=None):
        '''
            followedSequence
            Similar to above, but rather than being constant, the value is expected 
            to have followed the pattern is the values list.
            
            with m.If(history.followedSequenc(mysignal, [1,2,3,4], startTick=10)):
                # ... and such
        '''
        if numTicks is None or not numTicks:
            numTicks = len(values)
        v = None
        vIdx = 0
        
        endTick = startTick+numTicks
        if startTick >= endTick:
            raise ValueError('Must have at least 1 tick in sequence')
            return 1
        
        for i in range(startTick, startTick+numTicks):
            if v is None:
                v = (self.snapshot(s, i) == values[vIdx])
            else:
                v = v & (self.snapshot(s, i) == values[vIdx])
                
            vIdx += 1
            
        if v is None:
            raise ValueError('History got nothing from snapshot sequence?')
        return v
            
    def elaborate(self, _plat:Platform):
        m = Module()
        m.d.sync += self.ticks.eq(self.ticks + 1)
        for r in range(len(self.registers)):
            for t in range(self.maxHistory):
                with m.If(self.ticks == t):
                    s = self.registers[r]
                    m.d.sync += self.history[r][
                            self.sliceStart(s, t):self.sliceEnd(s, t)].eq(self.registers[r])
                            
                    if self.usingRecentPast and t:
                        prevStep = t - 1
                        with m.If(s):
                            # high 
                            m.d.sync += self.recentPast[r].fell.eq(0)
                            with m.If(~ self.snapshot(s, prevStep)):
                                # and was low: rose
                                m.d.sync += self.recentPast[r].rose_trace[t].eq(1)
                                m.d.sync += self.recentPast[r].rose.eq(1)
                            with m.Else():
                                m.d.sync += self.recentPast[r].rose.eq(0)
                                
                                
                        with m.Else():
                            # low 
                            m.d.sync += self.recentPast[r].rose.eq(0)
                            with m.If(self.snapshot(s, prevStep)):
                                # and was high: fell
                                m.d.sync += self.recentPast[r].fell_trace[t].eq(1)
                                m.d.sync += self.recentPast[r].fell.eq(1)
                            with m.Else():
                                m.d.sync += self.recentPast[r].fell.eq(0)
                                
                            
                    
        
        return m
    
    
        
    def sizeFor(self, s:Signal):
        return len(s)
    
    def sliceStart(self, s:Signal, tickIdx:int):
        ssize = self.sizeFor(s)
        return tickIdx*ssize
        
    def sliceEnd(self, s:Signal, tickIdx:int):
        return self.sliceStart(s, tickIdx) + self.sizeFor(s)
    
    
