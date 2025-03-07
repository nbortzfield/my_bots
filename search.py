import os
from paralellhc import PARALELL_HILL_CLIMBER

for i in range (1):
    #os.system("python3 mybots/generate.py")
    #os.system("python3 mybots/simulate.py")
    phc = PARALELL_HILL_CLIMBER()
    phc.Evolve()
    phc.Show_Best()

