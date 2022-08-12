import math


class inputs:
    def __init__(self, file_name: str):
        """
        Input file reader methode
        :param file_name:
        """
        with open("instances\\" + file_name, "r") as file:
            line = file.readline().split()
            self.CostumersCounter: int = int(line[0])
            self.VehicleCapacity: int = int(line[1])
            self.MaxDistanceConstraint: float = float(line[2])
            self.CostumerDemandedAmounts = []
            self.Coordinates = []
            c = False
            for _ in range(self.CostumersCounter + 1):
                line = file.readline().split()
                self.Coordinates.append([float(line[0]), float(line[1])])
                if c:
                    self.CostumerDemandedAmounts.append(int(line[2]))
                else:
                    c = True
        self.MatrixDistance = [[0 for _ in range(self.CostumersCounter + 1)] for _ in range(self.CostumersCounter + 1)]

    def Distance(self, i, j):
        """
        euclidean distance between two sites
        :param i:
        :param j:
        :return:
        """
        if self.MatrixDistance[i + 1][j + 1] == 0 and i != j:
            self.MatrixDistance[i + 1][j + 1] = (self.Coordinates[j + 1][0] - self.Coordinates[i + 1][0]) ** 2 + (
                        self.Coordinates[j + 1][1] - self.Coordinates[i + 1][1]) ** 2
            self.MatrixDistance[i + 1][j + 1] = math.sqrt(self.MatrixDistance[i + 1][j + 1])
        return self.MatrixDistance[i + 1][j + 1]

    def DistanceToDepot(self, i):
        """
        euclidean distance from site i to the depot with index 0
        :param i:
        :return:
        """
        if self.MatrixDistance[i + 1][0] == 0:
            self.MatrixDistance[i + 1][0] = (self.Coordinates[i + 1][0] - self.Coordinates[0][0]) ** 2 + (
                    self.Coordinates[i + 1][1] - self.Coordinates[0][1]) ** 2
            self.MatrixDistance[i + 1][0] = math.sqrt(self.MatrixDistance[i + 1][0])
        return self.MatrixDistance[i + 1][0]

    def DistanceFromDepot(self, i):
        """
        euclidean distance from the depot to site i
        :param i:
        :return:
        """
        if self.MatrixDistance[0][i + 1] == 0:
            self.MatrixDistance[0][i + 1] = (self.Coordinates[0][0] - self.Coordinates[i + 1][0]) ** 2 + (
                    self.Coordinates[0][1] - self.Coordinates[i + 1][1]) ** 2
            self.MatrixDistance[0][i + 1] = math.sqrt(self.MatrixDistance[0][i + 1])
        return self.MatrixDistance[0][i + 1]
