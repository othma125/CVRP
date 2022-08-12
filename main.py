from InputDatas import inputs
from Solution import GeneticAlgorithm


if __name__ == '__main__':

    Inputs = inputs("vrpnc1.txt")
    # Inputs = inputs("vrpnc2.txt")
    # Inputs = inputs("vrpnc3.txt")
    # Inputs = inputs("vrpnc4.txt")
    # Inputs = inputs("E101-10c.txt")
    # Inputs = inputs("E031-09h.txt")
    # Inputs = inputs("E484-19k.txt")
    # Inputs = inputs("E241-22k.txt")

    print(GeneticAlgorithm(Inputs, 30).toString())  # running time in seconds
