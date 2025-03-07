import pyrosim.pyrosim as pyrosim
import constants as c
import numpy
import pybullet as p
import math

class MOTOR:
        def __init__(self, jointName, robotId): 
            self.jointName = jointName
            self.robotId = robotId
            self.Prepare_To_Act()


        def Prepare_To_Act(self):
            if self.jointName == b'Torso_Backleg':
                self.amplitude = numpy.pi /4
                self.frequency = 10
                self.phaseOffset = numpy.pi
            if self.jointName == b'Torso_Frontleg':
                self.amplitude = numpy.pi /4
                self.frequency = 10
                self.phaseOffset = numpy.pi
            self.motor_vals = (c.amplitude * numpy.sin(c.frequency * numpy.linspace(0, 2 *numpy.pi, 1000))+ c.phaseOffset)
                 
            
        def Set_Value(self, desiredAngle, robotId):
             pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = self.jointName, controlMode = p.POSITION_CONTROL, targetPosition = desiredAngle, maxForce = 50)

        def Save_Sensor_Values(self):
            numpy.save(r"C:\Users\Nick\mybots\data\motorVals.npy", self.motor_vals)

