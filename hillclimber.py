from solution import SOLUTION
import constants as c
import copy

class HILL_CLIMBER:
    def __init__ (self):
        self.parent = SOLUTION()

    def evolve(self):
        self.parent.Evaluate("DIRECT")
        self.Show_Best()
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child
    def Print(self):
        print("child:", self.child.fitness)
        print("Parent:", self.parent.fitness)

    def Show_Best(self):
        self.parent.Evaluate("GUI")