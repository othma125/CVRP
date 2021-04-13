import random
import threading
import time
from typing import List
from Tools import ListEditor
from InputDatas import inputs
from SplitAuxiliaryGraph import node, acrs, wait


class cvrp_solution:

    def __init__(self, Inputs: inputs, giant_tour: List[int] = None):
        """
        the constructor methode
        if giant_tour is None it generate the self.GiantTour randomly the it launch the split algorithm
        :param Inputs:
        :param giant_tour:
        """
        self.GiantTour: List[int] = RandomGiantTour(Inputs) if giant_tour is None else giant_tour
        self.Split(Inputs)

    def Split(self, Inputs: inputs, lsm: bool = True):
        """
        Split algorithm that clusters the giant tour into feasible routes
        :param Inputs:
        :param lsm:
        :return:
        """
        Length = len(self.GiantTour)
        AuxiliaryGraphNodes = [node(i) for i in range(1 + Length)]
        AuxiliaryGraphNodes[0].PosteriorNode = None
        AuxiliaryGraphNodes[0].Label = 0
        AuxiliaryGraphNodes[0].RouteId = 0
        for i in range(Length):
            while wait(AuxiliaryGraphNodes, i):
                time.sleep(0.0001)
            acrs(Inputs, AuxiliaryGraphNodes, self.GiantTour, i, lsm).start()
        while wait(AuxiliaryGraphNodes, Length):
            time.sleep(0.0001)
        Node: node = AuxiliaryGraphNodes[Length]
        self.TraveledDistance = Node.Label
        self.RoutesCounter: int = Node.RouteId
        self.Routes = [0 for _ in range(Length)]
        self.StartingRouteIndex = []
        self.EndingRouteIndex = [0 for _ in range(self.RoutesCounter)]
        RoutesBordersArray = []
        while True:
            RoutesBordersArray.append(Node)
            Node = Node.PosteriorNode
            if Node is None:
                break
        r = len(RoutesBordersArray) - 1
        route = -1
        i = 0
        while i < Length:
            if i < RoutesBordersArray[r].NodeId:
                self.Routes[self.GiantTour[i]] = route
                self.EndingRouteIndex[route] = i
                i += 1
            else:
                r -= 1
                lsm = RoutesBordersArray[r].LocalSearch
                if lsm is not None:
                    for j in range(len(lsm.GiantTourPortion)):
                        self.GiantTour[j + lsm.FirstBorder] = lsm.GiantTourPortion[j]
                route += 1
                self.StartingRouteIndex.append(i)

    def LocalSearch(self, Inputs: inputs):
        """
        Local search methode tries to improve the current solution by _2opt, insertions, and swap movements
        :param Inputs:
        :return:
        """
        for i in range(len(self.GiantTour) - 1):
            for j in range(i + 1, len(self.GiantTour)):
                if self.Routes[self.GiantTour[i]] != self.Routes[self.GiantTour[j]]:
                    traveled_distance = self.TraveledDistance
                    routes = self.Routes.copy()
                    if self._2OptGain(Inputs, i, j) < 0:
                        ListEditor(i, j).Movement_2opt(self.GiantTour)
                        self.Split(Inputs, False)
                        if self.TraveledDistance > traveled_distance:
                            ListEditor(i, j).Movement_2opt(self.GiantTour)
                            self.TraveledDistance = traveled_distance
                            self.Routes = routes
                        else:
                            continue
                    if self.InsertionGain(Inputs, i, j) < 0:
                        ListEditor(i, j).MovementInsertion(self.GiantTour)
                        self.Split(Inputs, False)
                        if self.TraveledDistance > traveled_distance:
                            ListEditor(i, j).MovementInverseInsertion(self.GiantTour)
                            self.TraveledDistance = traveled_distance
                            self.Routes = routes
                        else:
                            continue
                    if self.InverseInsertionGain(Inputs, i, j) < 0:
                        ListEditor(i, j).MovementInverseInsertion(self.GiantTour)
                        self.Split(Inputs, False)
                        if self.TraveledDistance > traveled_distance:
                            ListEditor(i, j).MovementInsertion(self.GiantTour)
                            self.TraveledDistance = traveled_distance
                            self.Routes = routes
                        else:
                            continue
                    if self.SwapGain(Inputs, i, j) < 0:
                        ListEditor(i, j).MovementSwap(self.GiantTour)
                        self.Split(Inputs, False)
                        if self.TraveledDistance > traveled_distance:
                            ListEditor(i, j).MovementSwap(self.GiantTour)
                            self.TraveledDistance = traveled_distance
                            self.Routes = routes
                        else:
                            continue
                else:
                    gain = self._2OptGain(Inputs, i, j)
                    if gain < 0:
                        ListEditor(i, j).Movement_2opt(self.GiantTour)
                        self.TraveledDistance += gain
                        continue
                    if j == i + 1:
                        continue
                    gain = self.InsertionGain(Inputs, i, j)
                    if gain < 0:
                        ListEditor(i, j).MovementInsertion(self.GiantTour)
                        self.TraveledDistance += gain
                        continue
                    gain = self.InverseInsertionGain(Inputs, i, j)
                    if gain < 0:
                        ListEditor(i, j).MovementInverseInsertion(self.GiantTour)
                        self.TraveledDistance += gain
                        continue
                    gain = self.SwapGain(Inputs, i, j)
                    if gain < 0:
                        ListEditor(i, j).MovementSwap(self.GiantTour)
                        self.TraveledDistance += gain
        self.Split(Inputs)

    def _2OptGain(self, Inputs: inputs, i: int, j: int):
        """
        This methode calculate the traveled distance improvement before doing the _2opt movement
        :param Inputs:
        :param i:
        :param j:
        :return:
        """
        gain: float = 0
        if i == 0 or self.Routes[self.GiantTour[i - 1]] != self.Routes[self.GiantTour[i]]:
            gain += Inputs.DistanceFromDepot(self.GiantTour[j])
            gain -= Inputs.DistanceFromDepot(self.GiantTour[i])
        else:
            gain += Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[j])
            gain -= Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i])
        if j + 1 == len(self.GiantTour) or self.Routes[self.GiantTour[j + 1]] != self.Routes[self.GiantTour[j]]:
            gain += Inputs.DistanceToDepot(self.GiantTour[i])
            gain -= Inputs.DistanceToDepot(self.GiantTour[j])
        else:
            gain += Inputs.Distance(self.GiantTour[i], self.GiantTour[j + 1])
            gain -= Inputs.Distance(self.GiantTour[j], self.GiantTour[j + 1])
        return gain

    def InsertionGain(self, Inputs: inputs, i: int, j: int):
        """
        This methode calculate the traveled distance improvement before doing the insertion movement
        :param Inputs:
        :param i:
        :param j:
        :return:
        """
        if j == i + 1:
            return self._2OptGain(Inputs, i, j)
        gain: float = 0
        if i > 0 and self.Routes[self.GiantTour[i - 1]] == self.Routes[self.GiantTour[i]]:
            gain += Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[j])
            gain += Inputs.Distance(self.GiantTour[j], self.GiantTour[i])
            gain -= Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i])
        else:
            gain += Inputs.DistanceFromDepot(self.GiantTour[j])
            gain += Inputs.Distance(self.GiantTour[j], self.GiantTour[i])
            gain -= Inputs.DistanceFromDepot(self.GiantTour[i])
        if j + 1 < len(self.GiantTour) and self.Routes[self.GiantTour[j + 1]] == self.Routes[self.GiantTour[j]] and \
                self.Routes[self.GiantTour[j - 1]] == self.Routes[self.GiantTour[j]]:
            gain += Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[j + 1])
            gain -= Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[j])
            gain -= Inputs.Distance(self.GiantTour[j], self.GiantTour[j + 1])
        elif (j + 1 == len(self.GiantTour) or self.Routes[self.GiantTour[j + 1]] != self.Routes[self.GiantTour[j]]) and \
                self.Routes[self.GiantTour[j - 1]] == self.Routes[self.GiantTour[j]]:
            gain += Inputs.DistanceToDepot(self.GiantTour[j - 1])
            gain -= Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[j])
            gain -= Inputs.DistanceToDepot(self.GiantTour[j])
        elif j + 1 < len(self.GiantTour) and self.Routes[self.GiantTour[j + 1]] == self.Routes[self.GiantTour[j]] and \
                self.Routes[self.GiantTour[j - 1]] != self.Routes[self.GiantTour[j]]:
            gain += Inputs.DistanceFromDepot(self.GiantTour[j + 1])
            gain -= Inputs.Distance(self.GiantTour[j], self.GiantTour[j + 1])
            gain -= Inputs.DistanceFromDepot(self.GiantTour[j])
        elif (j + 1 == len(self.GiantTour) or self.Routes[self.GiantTour[j + 1]] != self.Routes[self.GiantTour[j]]) and \
                self.Routes[self.GiantTour[j - 1]] != self.Routes[self.GiantTour[j]]:
            gain -= Inputs.DistanceFromDepot(self.GiantTour[j])
            gain += Inputs.DistanceToDepot(self.GiantTour[j])
        return gain

    def InverseInsertionGain(self, Inputs: inputs, i: int, j: int):
        """
        This methode calculate the traveled distance improvement before doing the insertion movement
        :param Inputs:
        :param i:
        :param j:
        :return:
        """
        if j == i + 1:
            return self._2OptGain(Inputs, i, j)
        gain: float = 0
        if j + 1 < len(self.GiantTour) and self.Routes[self.GiantTour[j + 1]] == self.Routes[self.GiantTour[j]]:
            gain += Inputs.Distance(self.GiantTour[j], self.GiantTour[i])
            gain += Inputs.Distance(self.GiantTour[i], self.GiantTour[j + 1])
            gain -= Inputs.Distance(self.GiantTour[j], self.GiantTour[j + 1])
        else:
            gain += Inputs.DistanceToDepot(self.GiantTour[i])
            gain += Inputs.Distance(self.GiantTour[j], self.GiantTour[i])
            gain -= Inputs.DistanceToDepot(self.GiantTour[j])
        if i > 0 and self.Routes[self.GiantTour[i - 1]] == self.Routes[self.GiantTour[i]] \
                and self.Routes[self.GiantTour[i + 1]] == self.Routes[self.GiantTour[i]]:
            gain += Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i + 1])
            gain -= Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i])
            gain -= Inputs.Distance(self.GiantTour[i], self.GiantTour[i + 1])
        elif (i == 0 or self.Routes[self.GiantTour[i - 1]] != self.Routes[self.GiantTour[i]]) and \
                self.Routes[self.GiantTour[i + 1]] == self.Routes[self.GiantTour[i]]:
            gain += Inputs.DistanceFromDepot(self.GiantTour[i + 1])
            gain -= Inputs.Distance(self.GiantTour[i], self.GiantTour[i + 1])
            gain -= Inputs.DistanceFromDepot(self.GiantTour[i])
        elif i > 0 and self.Routes[self.GiantTour[i - 1]] == self.Routes[self.GiantTour[i]] and \
                self.Routes[self.GiantTour[i + 1]] != self.Routes[self.GiantTour[i]]:
            gain += Inputs.DistanceToDepot(self.GiantTour[i - 1])
            gain -= Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i])
            gain -= Inputs.DistanceToDepot(self.GiantTour[i])
        elif (i == 0 or self.Routes[self.GiantTour[i - 1]] != self.Routes[self.GiantTour[i]]) and \
                self.Routes[self.GiantTour[i + 1]] != self.Routes[self.GiantTour[i]]:
            gain -= Inputs.DistanceFromDepot(self.GiantTour[i])
            gain -= Inputs.DistanceToDepot(self.GiantTour[i])
        return gain

    def SwapGain(self, Inputs: inputs, i: int, j: int):
        """
        This methode calculate the traveled distance improvement before doing the swap movement
        :param Inputs:
        :param i:
        :param j:
        :return:
        """
        if j == i + 1:
            return self._2OptGain(Inputs, i, j)
        gain: float = 0
        if j + 1 < len(self.GiantTour) and self.Routes[self.GiantTour[j + 1]] == self.Routes[self.GiantTour[j]] and \
                self.Routes[self.GiantTour[j - 1]] == self.Routes[self.GiantTour[j]]:
            gain += Inputs.Distance(self.GiantTour[i], self.GiantTour[j + 1])
            gain += Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[i])
            gain -= Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[j])
            gain -= Inputs.Distance(self.GiantTour[j], self.GiantTour[j + 1])
        elif (j + 1 == len(self.GiantTour) or self.Routes[self.GiantTour[j + 1]] != self.Routes[self.GiantTour[j]]) and \
                self.Routes[self.GiantTour[j - 1]] == self.Routes[self.GiantTour[j]]:
            gain += Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[i])
            gain += Inputs.DistanceToDepot(self.GiantTour[i])
            gain -= Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[j])
            gain -= Inputs.DistanceToDepot(self.GiantTour[j])
        elif j + 1 < len(self.GiantTour) and self.Routes[self.GiantTour[j + 1]] == self.Routes[self.GiantTour[j]] and \
                self.Routes[self.GiantTour[j - 1]] != self.Routes[self.GiantTour[j]]:
            gain += Inputs.Distance(self.GiantTour[i], self.GiantTour[j + 1])
            gain += Inputs.DistanceFromDepot(self.GiantTour[i])
            gain -= Inputs.Distance(self.GiantTour[j], self.GiantTour[j + 1])
            gain -= Inputs.DistanceFromDepot(self.GiantTour[j])
        elif (j + 1 == len(self.GiantTour) or self.Routes[self.GiantTour[j + 1]] != self.Routes[self.GiantTour[j]]) and \
                self.Routes[self.GiantTour[j - 1]] != self.Routes[self.GiantTour[j]]:
            gain += Inputs.DistanceFromDepot(self.GiantTour[i])
            gain -= Inputs.DistanceFromDepot(self.GiantTour[j])
            gain += Inputs.DistanceToDepot(self.GiantTour[i])
            gain -= Inputs.DistanceToDepot(self.GiantTour[j])

        if i > 0 and self.Routes[self.GiantTour[i - 1]] == self.Routes[self.GiantTour[i]] and self.Routes[self.GiantTour[i + 1]] == self.Routes[self.GiantTour[i]]:
            gain += Inputs.Distance(self.GiantTour[j], self.GiantTour[i + 1])
            gain += Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[j])
            gain -= Inputs.Distance(self.GiantTour[i], self.GiantTour[i + 1])
            gain -= Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i])
        elif (i == 0 or self.Routes[self.GiantTour[i - 1]] != self.Routes[self.GiantTour[i]]) and self.Routes[self.GiantTour[i + 1]] == self.Routes[self.GiantTour[i]]:
            gain += Inputs.Distance(self.GiantTour[j], self.GiantTour[i + 1])
            gain += Inputs.DistanceFromDepot(self.GiantTour[j])
            gain -= Inputs.Distance(self.GiantTour[i], self.GiantTour[i + 1])
            gain -= Inputs.DistanceFromDepot(self.GiantTour[i])
        elif i > 0 and self.Routes[self.GiantTour[i - 1]] == self.Routes[self.GiantTour[i]] and self.Routes[self.GiantTour[i + 1]] != self.Routes[self.GiantTour[i]]:
            gain += Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[j])
            gain += Inputs.DistanceToDepot(self.GiantTour[j])
            gain -= Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i])
            gain -= Inputs.DistanceToDepot(self.GiantTour[i])
        elif (i == 0 or self.Routes[self.GiantTour[i - 1]] != self.Routes[self.GiantTour[i]]) and self.Routes[self.GiantTour[i + 1]] != self.Routes[self.GiantTour[i]]:
            gain -= Inputs.DistanceFromDepot(self.GiantTour[i])
            gain += Inputs.DistanceFromDepot(self.GiantTour[j])
            gain -= Inputs.DistanceToDepot(self.GiantTour[i])
            gain += Inputs.DistanceToDepot(self.GiantTour[j])
        return gain

    def RandomlyExchangeRoutes(self):
        if self.RoutesCounter == 1:
            return
        routes_exchanger = list(range(self.RoutesCounter))
        for r in range(self.RoutesCounter):
            ListEditor(r, random.randint(0, self.RoutesCounter - 1)).MovementSwap(routes_exchanger)
        new_giant_tour: List[int] = []
        for r in routes_exchanger:
            start = self.StartingRouteIndex[r]
            end = self.EndingRouteIndex[r]
            for i in range(end - start + 1):
                new_giant_tour.append(self.GiantTour[start + i])
        self.GiantTour = new_giant_tour

    def Crossover(self, Inputs: inputs, mother, cut_point1: int, cut_point2: int):
        """
        Crossover operation generate a new solution by taking portions form the mother and father solution (self) respecting the cut points
        :param Inputs:
        :param mother:
        :param cut_point1:
        :param cut_point2:
        :return:
        """
        new_giant_tour = [self.GiantTour[i] for i in range(0 if cut_point1 == cut_point2 else cut_point1, cut_point2)]
        k = 0
        for i in range(cut_point2, len(self.GiantTour)):
            if mother.GiantTour[i] not in new_giant_tour:
                if len(new_giant_tour) < len(self.GiantTour) - cut_point1:
                    new_giant_tour.append(mother.GiantTour[i])
                else:
                    new_giant_tour.insert(k, mother.GiantTour[i])
                    k += 1
        for i in range(cut_point2):
            if mother.GiantTour[i] not in new_giant_tour:
                if len(new_giant_tour) < len(self.GiantTour) - cut_point1:
                    new_giant_tour.append(mother.GiantTour[i])
                else:
                    new_giant_tour.insert(k, mother.GiantTour[i])
                    k += 1
        Mutation(new_giant_tour)
        return cvrp_solution(Inputs, new_giant_tour)

    def __str__(self):
        """
        The solution\'s description
        :return:
        """
        txt = f'The solution contains {self.RoutesCounter} routes\n'
        route = 0
        txt += f'The route number {1 + route} contains:\n'
        for gene in self.GiantTour:
            if self.Routes[gene] != route:
                route += 1
                txt += f'The route number {1 + route} contains:\n'
            txt += f'\tCostumer {1 + gene}\n'
        txt += f'Solution\'s cost = {1 + self.TraveledDistance}\n'
        return txt


class crossover_operation(threading.Thread):
    """
    This class make the selection of the parents and the cut points then it generate two child
    """
    def __init__(self, Inputs: inputs, population: list):
        threading.Thread.__init__(self)
        self.Inputs = Inputs
        Length = len(population) - 1
        Half = len(population) // 2
        index_father = random.randint(0, Half)
        self.Father = population[index_father]
        if random.random() < 0.7:
            while True:
                index_mother = random.randint(0, Half)
                if index_mother == index_father:
                    continue
                break
        else:
            index_mother = random.randint(Half + 1, Length)
        self.Mother = population[index_mother]
        Length = len(self.Father.GiantTour) - 1
        self.CutPoint1 = random.randint(0, Length - 1)
        self.CrossoverType = random.random() < 0.3
        if self.CrossoverType:
            self.CutPoint2 = random.randint(self.CutPoint1 + 1, Length)
            self.start()
            self.FirstChild = self.Father.Crossover(self.Inputs, self.Mother, self.CutPoint1, self.CutPoint2)
        else:
            self.start()
            self.FirstChild = self.Father.Crossover(self.Inputs, self.Mother, self.CutPoint1, self.CutPoint1)
        self.FirstChild.LocalSearch(self.Inputs)

    def run(self):
        self.Wait = True
        if self.CrossoverType:
            self.SecondChild = self.Mother.Crossover(self.Inputs, self.Father, self.CutPoint1, self.CutPoint2)
        else:
            self.SecondChild = self.Mother.Crossover(self.Inputs, self.Father, self.CutPoint1, self.CutPoint1)
        self.SecondChild.LocalSearch(self.Inputs)
        self.Wait = False


def GeneticAlgorithm(Inputs: inputs, RunningTime: float):
    """
    Genetic algorithm launched for a selected running time in second then it returns the best solution of the population
    :param Inputs:
    :param RunningTime:
    :return:
    """
    population_length = 10
    start_time = time.time() * 1000
    population = InitialPopulation(Inputs, population_length)
    QuickSort(population, 0, len(population) - 1)
    print(f'\t{population[0].TraveledDistance} after {time.time() * 1000 - start_time} ms')
    while time.time() * 1000 - start_time < RunningTime * 1000:
        if random.random() < 0.8:
            CrossoverOperation = crossover_operation(Inputs, population)
            UpdatePopulation(population, start_time, CrossoverOperation.FirstChild)
            while CrossoverOperation.Wait:
                time.sleep(0.0001)
            UpdatePopulation(population, start_time, CrossoverOperation.SecondChild)
        else:
            new_solution = cvrp_solution(Inputs)
            new_solution.LocalSearch(Inputs)
            UpdatePopulation(population, start_time, new_solution)
    return population[0]


def InitialPopulation(Inputs: inputs, n: int):
    """
    Randomly generated population
    :param Inputs:
    :param n:
    :return:
    """
    population = []
    print('Initial population:')
    for _ in range(n):
        solution = cvrp_solution(Inputs)
        print(solution.TraveledDistance)
        population.append(solution)
    return population


def UpdatePopulation(population: List[cvrp_solution], StartTime: float, solution: cvrp_solution):
    """
    This methode randomly adds a solution to the population then resorts it
    :param population:
    :param StartTime:
    :param solution:
    :return:
    """
    x = len(population) - 1
    if solution.TraveledDistance < population[x].TraveledDistance:
        if solution.TraveledDistance < population[0].TraveledDistance:
            print(f'\t{solution.TraveledDistance} after {time.time() * 1000 - StartTime} ms')
        population[random.randint(len(population) // 2, x)] = solution
        QuickSort(population, 0, x)


def RandomGiantTour(Inputs: inputs):
    """
    This methode randomly generate a giant tour
    :param Inputs:
    :return:
    """
    new_giant_tour = list(range(Inputs.CostumersCounter))
    for i in range(Inputs.CostumersCounter):
        ListEditor(i, random.randint(0, len(new_giant_tour) - 1)).MovementSwap(new_giant_tour)
    return new_giant_tour


def Mutation(giant_tour: List[int]):
    """
    Application of a random _2opt movement on the giant tour
    :param giant_tour:
    :return:
    """
    if random.random() < 0.1:
        i = random.randint(0, len(giant_tour) - 2)
        j = random.randint(i + 1, len(giant_tour) - 1)
        ListEditor(i, j).Movement_2opt(giant_tour)


def QuickSort(population: List[cvrp_solution], x: int, y: int):
    """
    Population's sorting according to the objective function
    :param population:
    :param x:
    :param y:
    :return:
    """
    if x < y:
        p = Partition(population, x, y)
        QuickSort(population, x, p - 1)
        QuickSort(population, p + 1, y)


def Partition(population: List[cvrp_solution], x: int, y: int):
    pivot = population[y].TraveledDistance
    i = x
    for j in range(x, y):
        if population[j].TraveledDistance < pivot:
            ListEditor(i, j).MovementSwap(population)
            i += 1
    ListEditor(i, y).MovementSwap(population)
    return i
