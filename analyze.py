import matplotlib
import numpy
import matplotlib.pyplot

backLegSensorValues = numpy.load(r"C:\Users\Nick\mybots\data\backLegSensorValues.npy")
frontLegSensorValues = numpy.load(r"C:\Users\Nick\mybots\data\frontLegSensorValues.npy")
sinMotorVals = numpy.load(r"C:\Users\Nick\mybots\data\sinMotorVals.npy")
backMotorVals = numpy.load(r"C:\Users\Nick\mybots\data\back_motor_vals.npy")
frontMotorVals = numpy.load(r"C:\Users\Nick\mybots\data\front_motor_vals.npy")


matplotlib.pyplot.plot(backMotorVals, label = "Back Leg", linewidth = 3)
matplotlib.pyplot.plot(frontMotorVals, label = "Front Leg", linewidth = 1)


matplotlib.pyplot.legend()
matplotlib.pyplot.show()