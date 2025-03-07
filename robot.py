from sensor import SENSOR
from motor import MOTOR
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy
import random
import pybullet as p
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c

class ROBOT:
    def __init__(self, solutionID):
        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        os.system(f"del brain{solutionID}.nndf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, i):
        for sensor in self.sensors.values():
            sensor.Get_Value(i)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName, self.robotId)
    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                self.jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[bytes(self.jointName, 'ASCII')].Set_Value(desiredAngle, self.robotId)

    def Think(self):
        self.nn.Update()

    def Get_Fitness(self, solutionID):
        stateOfLink0 = p.getLinkState(self.robotId, 0)
        positionOfLink0 = stateOfLink0[0]
        xCoordinateLink0 = positionOfLink0[0]
        with open(f"mybots/tmp{solutionID}.txt", "w") as file:
            file.write(f"{str(xCoordinateLink0)}")
        os.rename(f"mybots/tmp{solutionID}.txt", f"mybots/fitness{solutionID}.txt")
        print(f"Fitness file created: fitness{solutionID}.txt")