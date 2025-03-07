import numpy
import pyrosim.pyrosim as pyrosim


class SENSOR:
        def __init__(self, linkName): 
            self.linkName = linkName
            self.values =  numpy.zeros(1000)

        def Get_Value(self, i):
            self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
            

        def Save_Sensor_Values(self):
            numpy.save(r"C:\Users\Nick\mybots\data\sensorVals.npy", self.values)
