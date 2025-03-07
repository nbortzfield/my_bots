import pyrosim.pyrosim as pyrosim
import random

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[5, 5, .5], size=[1, 1, 1])
    pyrosim.End()
    
def Generate_Body():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])
    ## Joints should not be in the same spot possibly, since links are not in same spot
    ## Reconsider the posiitoning of the joints and adjust links as needed
    pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [-.5, 0, 1])
    pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [.5, 0, 1])

    ## x, y, z. X runs across the screen, y runs "into" the screen and z runs up and down. Links are spaced on y axis, adjust x to adjust joints on face of link0
    ## Adjust y to adjust joint "depth" in link0, different from z to adjust joint height. Height is the only one I'm fairly certain is correct 
    pyrosim.Send_Cube(name ="BackLeg",pos=[-.5, 0, -.5], size=[1, 1, 1] )
    pyrosim.Send_Cube(name ="FrontLeg",pos=[.5, 0, -.5], size=[1, 1, 1] )
    pyrosim.End()

def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    # Sensor Neurons
    sensor_neurons = [0, 1, 2]  # Neurons for Torso, BackLeg, and FrontLeg
    for i, linkName in enumerate(["Torso", "BackLeg", "FrontLeg"]):
        pyrosim.Send_Sensor_Neuron(name=sensor_neurons[i], linkName=linkName)

    # Motor Neurons
    motor_neurons = [3, 4]  # Neurons for Torso_BackLeg and Torso_FrontLeg joints
    for i, jointName in enumerate(["Torso_BackLeg", "Torso_FrontLeg"]):
        pyrosim.Send_Motor_Neuron(name=motor_neurons[i], jointName=jointName)

    # Fully connected network - Connect each sensor neuron to each motor neuron
    for sensor_neuron in sensor_neurons:
        for motor_neuron in motor_neurons:
            weight = (random.random() * 2) -1
            pyrosim.Send_Synapse(sourceNeuronName=sensor_neuron, targetNeuronName=motor_neuron, weight= weight)

    pyrosim.End()

    

Create_World()
Generate_Body()
Generate_Brain()
