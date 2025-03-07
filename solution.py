import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:
    def __init__(self, ID):
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
        self.myID = ID

    def Create_World(self):
        pyrosim.Start_SDF("mybots/world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[5, 5, .5], size=[1, 1, 1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0, -.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0, .5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -.5, 0], size=[.2, 1, .2])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, .5, 0], size=[.2, 1, .2])
        pyrosim.Send_Cube(name="LeftLeg", pos=[-.5, 0, 0], size=[1, .2, .2])
        pyrosim.Send_Cube(name="RightLeg", pos=[.5, 0, 0], size=[1, .2, .2])

        

        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute", position=[0, -1, 0], jointAxis="1 0 0")
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0, 1, 0], jointAxis="1 0 0")
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute", position=[-1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1, 0, 0], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, 0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, .5], size=[.2, .2, 1])
        
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        sensor_neurons = list(range(c.numSensorNeurons))
        motor_neurons = list(range(c.numSensorNeurons, c.numSensorNeurons + c.numMotorNeurons))

        for i, linkName in enumerate(["Torso", "BackLeg", "FrontLeg", "LeftLeg", "RightLeg", "BackLowerLeg", "FrontLowerLeg", "LeftLowerLeg", "RightLowerLeg"]):
            pyrosim.Send_Sensor_Neuron(name=sensor_neurons[i], linkName=linkName)

        for i, jointName in enumerate(["Torso_BackLeg", "Torso_FrontLeg", "Torso_LeftLeg", "Torso_RightLeg", "BackLeg_BackLowerLeg", 
                                       "FrontLeg_FrontLowerLeg", "LeftLeg_LeftLowerLeg", "RightLeg_RightLowerLeg"]):
            pyrosim.Send_Motor_Neuron(name=motor_neurons[i], jointName=jointName)

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                weight = self.weights[currentRow][currentColumn]
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + c.numSensorNeurons, weight=weight)

        pyrosim.End()

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"start /B python3 mybots/simulate.py {directOrGUI} {self.myID}")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = f"mybots/fitness{self.myID}.txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        with open(fitnessFileName, "r") as file:
            self.fitness = float(file.readline())
        try:
            os.remove(fitnessFileName)
        except FileNotFoundError:
            print(f"Fitness file not found for deletion: {fitnessFileName}")
        except Exception as e:
            print(f"Error deleting fitness file: {fitnessFileName}")
            print(f"Exception: {str(e)}")
    def Mutate(self):
        row = random.randint(0, c.numSensorNeurons -1)
        column = random.randint(0, c.numMotorNeurons -1)
        self.weights[row, column] = np.random.rand() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        
        os.system(f"start /B python3 simulate.py {directOrGUI} {self.myID}")
        
        fitnessFileName = f"mybots/fitness{self.myID}.txt"
        print(f"Waiting for fitness file: {fitnessFileName}")
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        print(f"Fitness file found: {fitnessFileName}")
        
        with open(fitnessFileName, "r") as fitnessFile:
            self.fitness = float(fitnessFile.readline())
        print(f"Fitness value read: {self.fitness}")
        
        try:
            os.remove(fitnessFileName)
            print(f"Fitness file deleted: {fitnessFileName}")
        except FileNotFoundError:
            print(f"Fitness file not found for deletion: {fitnessFileName}")
        except Exception as e:
            print(f"Error deleting fitness file: {fitnessFileName}")
            print(f"Exception: {str(e)}")