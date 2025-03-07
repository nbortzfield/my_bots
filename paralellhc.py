import os
import copy
import constants as c
from solution import SOLUTION

class PARALELL_HILL_CLIMBER:
    def __init__(self):
        for i in range(c.populationSize^2):
            if os.path.exists(f"mybots/brain{i}.nndf"):
                os.system(f"del mybots/brain{i}.nndf")
            if os.path.exists(f"mtbots/fitness{i}.txt"):
                os.system(f"del mybots/fitness{i}.txt")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
            self.Print()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Select()

    def Spawn(self):
        self.children = {}
        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Select(self):
        for key in self.parents:
            if self.children[key].fitness < self.parents[key].fitness:
                self.parents[key] = self.children[key]

    def Print(self):
        print()
        for key in self.parents:
            print(f"Parent fitness: {self.parents[key].fitness}, Child fitness: {self.children[key].fitness}")
        print()

    def Show_Best(self):
        best_parent = min(self.parents.values(), key=lambda x: x.fitness)
        best_parent.Start_Simulation("GUI")

    def Evaluate(self, solutions):
        for solution in solutions.values():
            solution.Start_Simulation("DIRECT")
        for solution in solutions.values():
            solution.Wait_For_Simulation_To_End()