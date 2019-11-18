from rbs import FSAHelperFunctions
from rbs import NealCoverFunctions
from rbs import NeuralCognitiveArchitectureBuilder

class Sudoku6:

    def getBoxIndex(self, x, y):
        boxIndex = 0
        if(x < 4 and y < 3):
            boxIndex = 1
        elif(x > 2 and y < 3):
            boxIndex = 2
        elif(x < 4 and y > 2 and y < 5):
            boxIndex = 3
        elif(x > 2 and y > 2 and y < 5):
            boxIndex = 4
        elif(x < 4 and y > 4):
            boxIndex = 5
        else:
            boxIndex = 6
        return boxIndex

    def setupBoard(self):
        for i in range(1,7):
            self.narc.addFact("Number",(i,))
            self.narc.addFact("X-Axis",(i,))
            self.narc.addFact("Y-Axis",(i,))

            for y in range(1,7):
                boxIndex = self.getBoxIndex(i, y)
                self.narc.addFact("Box", (i, y, boxIndex))
                for n in range(1,7):
                    self.narc.addFact("Item", (i, y, n, boxIndex), False)
                    self.narc.addFact("CantBe", (i, y, n), False)

        self.resetFact = self.narc.addFact("Reset", (), False)

    def __init__(self, sim, simulator):
        self.sim = sim
        self.neal = NealCoverFunctions(simulator, sim)
        self.fsa = FSAHelperFunctions(simulator, sim, self.neal)
        self.narc = NeuralCognitiveArchitectureBuilder(simulator, sim, self.fsa, self.neal).build()

        self.setupBoard()

        self.narc.addRule(
            "StopReset",
            [
                (True, "Reset", (), "f1")
            ],
            [
                ("retract", "f1")
            ]
        )

        self.narc.addRule(
            "ResetItem",
            [
                (True, "Item", ("?x", "?y", "?n", "?b"), "f1"),
                (True, "Reset", (), "f2")
            ],
            [
                ("retract", "f1")
            ]
        )

        self.narc.addRule(
            "ResetCantBe",
            [
                (True, "CantBe", ("?x", "?y", "?n"), "f1"),
                (True, "Reset", (), "f2")
            ],
            [
                ("retract", "f1")
            ]
        )

        self.narc.addRule(
            "CantBeHorizontal",
            [
                (True, "Item", ("?x1", "?y1", "?1", "?"), "1"),
                (True, "X-Axis", ("?x2",), "2"),
                (True, "X-Axis", ("?x3",), "3"),
                (True, "X-Axis", ("?x4",), "4"),
                (True, "X-Axis", ("?x5",), "5"),
                (True, "X-Axis", ("?x6",), "6"),
                ("test", "<>", "?x1", "?x2"),
                ("test", "<>", "?x1", "?x3"),
                ("test", "<>", "?x1", "?x4"),
                ("test", "<>", "?x1", "?x5"),
                ("test", "<>", "?x1", "?x6"),
                ("test", "<", "?x2", "?x3"),
                ("test", "<", "?x3", "?x4"),
                ("test", "<", "?x4", "?x5"),
                ("test", "<", "?x5", "?x6")
            ],
            [
                ("assert", ("CantBe", ("?x2", "?y1", "?1"))),
                ("assert", ("CantBe", ("?x3", "?y1", "?1"))),
                ("assert", ("CantBe", ("?x4", "?y1", "?1"))),
                ("assert", ("CantBe", ("?x5", "?y1", "?1"))),
                ("assert", ("CantBe", ("?x6", "?y1", "?1")))
            ]
        )

        self.narc.addRule(
            "CantBeVertical",
            [
                (True, "Item", ("?x1", "?y1", "?1", "?"), "1"),
                (True, "Y-Axis", ("?y2",), "2"),
                (True, "Y-Axis", ("?y3",), "3"),
                (True, "Y-Axis", ("?y4",), "4"),
                (True, "Y-Axis", ("?y5",), "5"),
                (True, "Y-Axis", ("?y6",), "6"),
                ("test", "<>", "?y1", "?y2"),
                ("test", "<>", "?y1", "?y3"),
                ("test", "<>", "?y1", "?y4"),
                ("test", "<>", "?y1", "?y5"),
                ("test", "<>", "?y1", "?y6"),
                ("test", "<", "?y2", "?y3"),
                ("test", "<", "?y3", "?y4"),
                ("test", "<", "?y4", "?y5"),
                ("test", "<", "?y5", "?y6")
            ],
            [
                ("assert", ("CantBe", ("?x1", "?y2", "?1"))),
                ("assert", ("CantBe", ("?x1", "?y3", "?1"))),
                ("assert", ("CantBe", ("?x1", "?y4", "?1"))),
                ("assert", ("CantBe", ("?x1", "?y5", "?1"))),
                ("assert", ("CantBe", ("?x1", "?y6", "?1")))
            ]
        )

        self.narc.addRule(
            "CantBeBox",
            [
                (True, "Item", ("?x1", "?y1", "?1", "?b"), "1"),
                (True, "Box", ("?x2", "?y1", "?b"), "2"),
                (True, "Box", ("?x3", "?y1", "?b"), "3"),
                (True, "Box", ("?x1", "?y2", "?b"), "4"),
                (True, "Box", ("?x2", "?y2", "?b"), "5"),
                (True, "Box", ("?x3", "?y2", "?b"), "6"),
                ("test", "<", "?x1", "?x2"),
                ("test", "<>", "?x1", "?x3"),
                ("test", "<>", "?x2", "?x3"),
                ("test", "<>", "?y1", "?y2"),
            ],
            [
                ("assert", ("CantBe", ("?x2", "?y1", "?1"))),
                ("assert", ("CantBe", ("?x3", "?y1", "?1"))),
                ("assert", ("CantBe", ("?x1", "?y2", "?1"))),
                ("assert", ("CantBe", ("?x2", "?y2", "?1"))),
                ("assert", ("CantBe", ("?x3", "?y2", "?1")))
            ]
        )

        self.narc.addRule(
            "CellIs",
            [
                (True, "CantBe", ("?x1","?y1", "?1"), "1"),
                (True, "CantBe", ("?x1","?y1", "?2"), "2"),
                (True, "CantBe", ("?x1","?y1", "?3"), "3"),
                (True, "CantBe", ("?x1","?y1", "?4"), "4"),
                (True, "CantBe", ("?x1","?y1", "?5"), "5"),
                (True, "Box", ("?x1", "?y1", "?b"), "6"),
                (True, "Number", ("?6",), "7"),
                ("test", "<>", "?6", "?1"),
                ("test", "<>", "?6", "?2"),
                ("test", "<>", "?6", "?3"),
                ("test", "<>", "?6", "?4"),
                ("test", "<>", "?6", "?5"),
                ("test", "<", "?1", "?2"),
                ("test", "<", "?2", "?3"),
                ("test", "<", "?3", "?4"),
                ("test", "<", "?4", "?5"),                        
            ],
            [
                ("assert", ("Item", ("?x1","?y1","?6", "?b")))
            ]
        )

        self.narc.addRule(
            "BoxCellIs",
            [
                (True, "Box", ("?x1", "?y1", "?b"), "6"),
                (True, "Box", ("?x2", "?y1", "?b"), "7"),
                (True, "Box", ("?x3", "?y1", "?b"), "8"),
                (True, "Box", ("?x1", "?y2", "?b"), "9"),
                (True, "Box", ("?x2", "?y2", "?b"), "10"),
                (True, "CantBe", ("?x1","?y1", "?1"), "1"),
                (True, "CantBe", ("?x2","?y1", "?1"), "2"),
                (True, "CantBe", ("?x3","?y1", "?1"), "3"),
                (True, "CantBe", ("?x1","?y2", "?1"), "4"),
                (True, "CantBe", ("?x2","?y2", "?1"), "5"),
                ("test", "<", "?x1", "?x2"),
                ("test", "<>", "?x3", "?x1"),
                ("test", "<>", "?x3", "?x2"),
                ("test", "<>", "?y1", "?y2"),
            ],
            [
                ("assert", ("Item", ("?x3","?y2","?1", "?b")))
            ]
        )

        self.narc.addRule(
            "RowCellIs",
            [
                (True, "CantBe", ("?x1","?y1", "?1"), "1"),
                (True, "CantBe", ("?x2","?y1", "?1"), "2"),
                (True, "CantBe", ("?x3","?y1", "?1"), "3"),
                (True, "CantBe", ("?x4","?y1", "?1"), "4"),
                (True, "CantBe", ("?x5","?y1", "?1"), "5"),
                (True, "Box", ("?x6","?y1","?b"), "6"),
                ("test","<","?x1","?x2"),
                ("test","<","?x2","?x3"),
                ("test","<","?x3","?x4"),
                ("test","<","?x4","?x5"),
                ("test","<>","?x6","?x1"),
                ("test","<>","?x6","?x2"),
                ("test","<>","?x6","?x3"),
                ("test","<>","?x6","?x4"),
                ("test","<>","?x6","?x5")
            ],
            [
                ("assert", ("Item", ("?x6", "?y1", "?1", "?b")))
            ]
        )

        self.narc.addRule(
            "ColumnCellIs",
            [
                (True, "CantBe", ("?x1","?y1", "?1"), "1"),
                (True, "CantBe", ("?x1","?y2", "?1"), "2"),
                (True, "CantBe", ("?x1","?y3", "?1"), "3"),
                (True, "CantBe", ("?x1","?y4", "?1"), "4"),
                (True, "CantBe", ("?x1","?y5", "?1"), "5"),
                (True, "Box", ("?x1","?y6","?b"), "6"),
                ("test","<","?y1","?y2"),
                ("test","<","?y2","?y3"),
                ("test","<","?y3","?y4"),
                ("test","<","?y4","?y5"),
                ("test","<>","?y6","?y1"),
                ("test","<>","?y6","?y2"),
                ("test","<>","?y6","?y3"),
                ("test","<>","?y6","?y4"),
                ("test","<>","?y6","?y5"),
            ],
            [
                ("assert", ("Item", ("?x1", "?y6", "?1", "?b")))
            ]
        )

        self.narc.addRule(
            "CellCantBe",
            [
                (True, "Item", ("?x1","?y1", "?1", "?b"), "1"),
                (True, "Number", ("?2",), "2"),
                (True, "Number", ("?3",), "3"),
                (True, "Number", ("?4",), "4"),
                (True, "Number", ("?5",), "5"),
                (True, "Number", ("?6",), "6"),
                ("test","<>","?1","?2"),
                ("test","<>","?1","?3"),
                ("test","<>","?1","?4"),
                ("test","<>","?1","?5"),
                ("test","<>","?1","?6"),
                ("test","<","?2","?3"),
                ("test","<","?3","?4"),
                ("test","<","?4","?5"),
                ("test","<","?5","?6")
            ],
            [
                ("assert", ("CantBe", ("?x1", "?y1", "?2"))),
                ("assert", ("CantBe", ("?x1", "?y1", "?3"))),
                ("assert", ("CantBe", ("?x1", "?y1", "?4"))),
                ("assert", ("CantBe", ("?x1", "?y1", "?5"))),
                ("assert", ("CantBe", ("?x1", "?y1", "?6")))
            ]
        )
            
        self.narc.apply()

    def run(self, puzzles):
        runtime = 0
        resetTimes = []
        for p in puzzles:
            puzzleActivationTimes = {'spike_times': [[runtime+5]]}
            puzzleSpikeGen = self.sim.Population(1, self.sim.SpikeSourceArray, puzzleActivationTimes)
            for y,s in enumerate(p):
                for x,i in enumerate(s):
                    if (i <> None):
                        boxIndex = self.getBoxIndex(x+1, y+1)
                        f = self.narc.getFact("Item", (x+1, y+1, i, boxIndex))
                        population = self.narc.exe.getPopulationFromCA(f.caIndex)                        
                        self.fsa.turnOnStateFromSpikeSource(puzzleSpikeGen, population.pop, f.caIndex-population.fromIndex)
                        
            runtime += 600
            resetTimes.append(runtime)
            resetTimes.append(runtime+10)
            runtime += 100

        resetSpikeGen = self.sim.Population(1, self.sim.SpikeSourceArray, {'spike_times': [resetTimes]})
        population = self.narc.exe.getPopulationFromCA(self.resetFact.caIndex)
        self.fsa.turnOnStateFromSpikeSource(resetSpikeGen, population.pop, self.resetFact.caIndex-population.fromIndex)

        self.narc.apply()

        self.sim.run(runtime)

    def printSpikes(self):
        self.narc.printSpikes()

        data = self.narc.get_ca_data()
        pop = self.narc.exe.getPopulationFromCA(self.resetFact.caIndex)
        d = data[pop.pop.label]
        print "RESET AT: {}".format(d.segments[0].spiketrains[self.resetFact.caIndex-pop.fromIndex])
