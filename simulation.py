from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim


class SIMULATION:
        def __init__(self, directOrGUI, solutionID): 
            self.solutionID = solutionID
            if directOrGUI == "DIRECT":
                  self.physicsClient = p.connect(p.DIRECT)
            else:
                  self.physicsClient = p.connect(p.GUI)
            self.directOrGUI = directOrGUI
            p.setAdditionalSearchPath(pybullet_data.getDataPath())
            p.setGravity(0,0,-9.8)
            self.world = WORLD()
            self.robot = ROBOT(solutionID)

            
        def Run(self):
              for i in range(1000):
                    p.stepSimulation()
                    self.robot.Sense(i)
                    self.robot.Think()
                    self.robot.Act()
                    

                    if self.directOrGUI == "GUI":
                        time.sleep(1/60)

        def __del__(self):
              p.disconnect()

        def Get_Fitness(self):
              self.robot.Get_Fitness(self.solutionID)
