import random
import threading
import time
from typing import List
from Tools import Motion
from InputDatas import inputs
from SplitAlgorithm import auxiliary_graph


class heuristic_solution:

    def __init__(self, Inputs: inputs, giant_tour: List[int] = None):
        """
        the constructor methode
        if giant_tour is None it generate the self.GiantTour randomly the it launch the split algorithm
        :param Inputs:
        :param giant_tour:
        """
        self.GiantTour = RandomGiantTour(Inputs.CostumersCounter) if giant_tour is None else giant_tour
        self.TraveledDistance = float('inf')
        # self.Split(Inputs, True)
        self.Split(Inputs, giant_tour is not None or random.random() < 0.1)

    def Split(self, Inputs: inputs, withLSM: bool, bound: float = float('inf')) -> None:
        """
        Split algorithm that clusters the giant tour into feasible routes
        :param bound:
        :type withLSM: bool
        :param withLSM:
        :param Inputs:
        :return:
        """
        self.setGraph(Inputs, withLSM, bound)
        self.setRoutes(Inputs)

    def getGraph(self, Inputs: inputs, withLSM: bool, bound: float) -> auxiliary_graph:
        graph = auxiliary_graph(self.GiantTour, withLSM, bound)
        graph.setArcs(Inputs)
        return graph

    def setGraph(self, Inputs: inputs, withLSM: bool, bound: float) -> None:
        self.AuxiliaryGraph = auxiliary_graph(self.GiantTour, withLSM, bound)
        self.AuxiliaryGraph.setArcs(Inputs)

    def setRoutes(self, Inputs: inputs):
        if self.isFeasible():
            if self.AuxiliaryGraph.isImprovedByLSM() and self.TraveledDistance > self.AuxiliaryGraph.getTraveledDistance():
                self.TraveledDistance = self.AuxiliaryGraph.getTraveledDistance()
                self.GiantTour = [gene for r in self.AuxiliaryGraph.getRoutes() for gene in r.GiantTourPortion]
                # if len(self.GiantTour)<Inputs.CostumersCounter:
                #     print('bug: len(self.GiantTour)<Inputs.CostumersCounter')
                #     quit(0)
                self.Split(Inputs, random.random() < 0.1, min(self.TraveledDistance, self.AuxiliaryGraph.BoundingCost))
            else:
                self.TraveledDistance = self.AuxiliaryGraph.getTraveledDistance()
                self.RoutesCounter = self.AuxiliaryGraph.getRoutesCounter()
                self.Routes = [0 for _ in range(Inputs.CostumersCounter)]
                self.GiantTour = []
                for index, r in enumerate(self.AuxiliaryGraph.getRoutes()):
                    for gene in r.GiantTourPortion:
                        self.GiantTour.append(gene)
                        self.Routes[gene] = index
                # if len(self.GiantTour) < Inputs.CostumersCounter:
                #     print('bug: len(self.GiantTour)<Inputs.CostumersCounter')
                #     quit(0)

    def isFeasible(self) -> bool:
        return self.AuxiliaryGraph is not None and self.AuxiliaryGraph.isFeasible()

    # def LocalSearch(self, Inputs: Parameters):
    #     """
    #     Local search methode tries to improve the current solution by _2opt, insertions, and swap movements
    #     :param Inputs:
    #     :return:
    #     """
    #     traveled_distance = self.TraveledDistance
    #     for i in range(len(self.GiantTour) - 1):
    #         for j in range(i + 1, len(self.GiantTour)):
    #             if self.Routes[self.GiantTour[i]] == self.Routes[self.GiantTour[j]]:
    #                 gain = self._2OptGain(Inputs, i, j)
    #                 if gain < 0:
    #                     Motion(i, j)._2opt(self.GiantTour)
    #                     self.TraveledDistance += gain
    #                     continue
    #                 if j == i + 1:
    #                     continue
    #                 gain = self.InsertionGain(Inputs, i, j)
    #                 if gain < 0:
    #                     Motion(i, j).Insertion(self.GiantTour)
    #                     self.TraveledDistance += gain
    #                     continue
    #                 gain = self.InverseInsertionGain(Inputs, i, j)
    #                 if gain < 0:
    #                     Motion(i, j).InverseInsertion(self.GiantTour)
    #                     self.TraveledDistance += gain
    #                     continue
    #                 gain = self.SwapGain(Inputs, i, j)
    #                 if gain < 0:
    #                     Motion(i, j).Swap(self.GiantTour)
    #                     self.TraveledDistance += gain
    #             else:
    #                 break
    #     if self.TraveledDistance < traveled_distance:
    #         self.Split(Inputs)
    #         # self.LocalSearch(Inputs)
    #
    # def _2OptGain(self, Inputs: Parameters, i: int, j: int):
    #     """
    #     This methode calculate the traveled distance improvement before doing the _2opt movement
    #     :param Inputs:
    #     :param i:
    #     :param j:
    #     :return:
    #     """
    #     gain: float = 0
    #     if i == 0 or self.Routes[self.GiantTour[i - 1]] != self.Routes[self.GiantTour[i]]:
    #         gain += Inputs.DistanceFromDepot(self.GiantTour[j])
    #         gain -= Inputs.DistanceFromDepot(self.GiantTour[i])
    #     else:
    #         gain += Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[j])
    #         gain -= Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i])
    #     if j + 1 == len(self.GiantTour) or self.Routes[self.GiantTour[j + 1]] != self.Routes[self.GiantTour[j]]:
    #         gain += Inputs.DistanceToDepot(self.GiantTour[i])
    #         gain -= Inputs.DistanceToDepot(self.GiantTour[j])
    #     else:
    #         gain += Inputs.Distance(self.GiantTour[i], self.GiantTour[j + 1])
    #         gain -= Inputs.Distance(self.GiantTour[j], self.GiantTour[j + 1])
    #     return gain
    #
    # def InsertionGain(self, Inputs: Parameters, i: int, j: int):
    #     """
    #     This methode calculate the traveled distance improvement before doing the insertion movement
    #     :param Inputs:
    #     :param i:
    #     :param j:
    #     :return:
    #     """
    #     if j == i + 1:
    #         return self._2OptGain(Inputs, i, j)
    #     gain: float = 0
    #     if i > 0 and self.Routes[self.GiantTour[i - 1]] == self.Routes[self.GiantTour[i]]:
    #         gain += Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[j])
    #         gain += Inputs.Distance(self.GiantTour[j], self.GiantTour[i])
    #         gain -= Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i])
    #     else:
    #         gain += Inputs.DistanceFromDepot(self.GiantTour[j])
    #         gain += Inputs.Distance(self.GiantTour[j], self.GiantTour[i])
    #         gain -= Inputs.DistanceFromDepot(self.GiantTour[i])
    #     if j + 1 < len(self.GiantTour) and self.Routes[self.GiantTour[j + 1]] == self.Routes[self.GiantTour[j]] and \
    #             self.Routes[self.GiantTour[j - 1]] == self.Routes[self.GiantTour[j]]:
    #         gain += Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[j + 1])
    #         gain -= Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[j])
    #         gain -= Inputs.Distance(self.GiantTour[j], self.GiantTour[j + 1])
    #     elif (j + 1 == len(self.GiantTour) or self.Routes[self.GiantTour[j + 1]] != self.Routes[self.GiantTour[j]]) and \
    #             self.Routes[self.GiantTour[j - 1]] == self.Routes[self.GiantTour[j]]:
    #         gain += Inputs.DistanceToDepot(self.GiantTour[j - 1])
    #         gain -= Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[j])
    #         gain -= Inputs.DistanceToDepot(self.GiantTour[j])
    #     elif j + 1 < len(self.GiantTour) and self.Routes[self.GiantTour[j + 1]] == self.Routes[self.GiantTour[j]] and \
    #             self.Routes[self.GiantTour[j - 1]] != self.Routes[self.GiantTour[j]]:
    #         gain += Inputs.DistanceFromDepot(self.GiantTour[j + 1])
    #         gain -= Inputs.Distance(self.GiantTour[j], self.GiantTour[j + 1])
    #         gain -= Inputs.DistanceFromDepot(self.GiantTour[j])
    #     elif (j + 1 == len(self.GiantTour) or self.Routes[self.GiantTour[j + 1]] != self.Routes[self.GiantTour[j]]) and \
    #             self.Routes[self.GiantTour[j - 1]] != self.Routes[self.GiantTour[j]]:
    #         gain -= Inputs.DistanceFromDepot(self.GiantTour[j])
    #         gain += Inputs.DistanceToDepot(self.GiantTour[j])
    #     return gain
    #
    # def InverseInsertionGain(self, Inputs: Parameters, i: int, j: int):
    #     """
    #     This methode calculate the traveled distance improvement before doing the insertion movement
    #     :param Inputs:
    #     :param i:
    #     :param j:
    #     :return:
    #     """
    #     if j == i + 1:
    #         return self._2OptGain(Inputs, i, j)
    #     gain: float = 0
    #     if j + 1 < len(self.GiantTour) and self.Routes[self.GiantTour[j + 1]] == self.Routes[self.GiantTour[j]]:
    #         gain += Inputs.Distance(self.GiantTour[j], self.GiantTour[i])
    #         gain += Inputs.Distance(self.GiantTour[i], self.GiantTour[j + 1])
    #         gain -= Inputs.Distance(self.GiantTour[j], self.GiantTour[j + 1])
    #     else:
    #         gain += Inputs.DistanceToDepot(self.GiantTour[i])
    #         gain += Inputs.Distance(self.GiantTour[j], self.GiantTour[i])
    #         gain -= Inputs.DistanceToDepot(self.GiantTour[j])
    #     if i > 0 and self.Routes[self.GiantTour[i - 1]] == self.Routes[self.GiantTour[i]] \
    #             and self.Routes[self.GiantTour[i + 1]] == self.Routes[self.GiantTour[i]]:
    #         gain += Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i + 1])
    #         gain -= Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i])
    #         gain -= Inputs.Distance(self.GiantTour[i], self.GiantTour[i + 1])
    #     elif (i == 0 or self.Routes[self.GiantTour[i - 1]] != self.Routes[self.GiantTour[i]]) and \
    #             self.Routes[self.GiantTour[i + 1]] == self.Routes[self.GiantTour[i]]:
    #         gain += Inputs.DistanceFromDepot(self.GiantTour[i + 1])
    #         gain -= Inputs.Distance(self.GiantTour[i], self.GiantTour[i + 1])
    #         gain -= Inputs.DistanceFromDepot(self.GiantTour[i])
    #     elif i > 0 and self.Routes[self.GiantTour[i - 1]] == self.Routes[self.GiantTour[i]] and \
    #             self.Routes[self.GiantTour[i + 1]] != self.Routes[self.GiantTour[i]]:
    #         gain += Inputs.DistanceToDepot(self.GiantTour[i - 1])
    #         gain -= Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i])
    #         gain -= Inputs.DistanceToDepot(self.GiantTour[i])
    #     elif (i == 0 or self.Routes[self.GiantTour[i - 1]] != self.Routes[self.GiantTour[i]]) and \
    #             self.Routes[self.GiantTour[i + 1]] != self.Routes[self.GiantTour[i]]:
    #         gain -= Inputs.DistanceFromDepot(self.GiantTour[i])
    #         gain -= Inputs.DistanceToDepot(self.GiantTour[i])
    #     return gain
    #
    # def SwapGain(self, Inputs: Parameters, i: int, j: int):
    #     """
    #     This methode calculate the traveled distance improvement before doing the swap movement
    #     :param Inputs:
    #     :param i:
    #     :param j:
    #     :return:
    #     """
    #     if j == i + 1:
    #         return self._2OptGain(Inputs, i, j)
    #     gain: float = 0
    #     if j + 1 < len(self.GiantTour) and self.Routes[self.GiantTour[j + 1]] == self.Routes[self.GiantTour[j]] and \
    #             self.Routes[self.GiantTour[j - 1]] == self.Routes[self.GiantTour[j]]:
    #         gain += Inputs.Distance(self.GiantTour[i], self.GiantTour[j + 1])
    #         gain += Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[i])
    #         gain -= Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[j])
    #         gain -= Inputs.Distance(self.GiantTour[j], self.GiantTour[j + 1])
    #     elif (j + 1 == len(self.GiantTour) or self.Routes[self.GiantTour[j + 1]] != self.Routes[self.GiantTour[j]]) and \
    #             self.Routes[self.GiantTour[j - 1]] == self.Routes[self.GiantTour[j]]:
    #         gain += Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[i])
    #         gain += Inputs.DistanceToDepot(self.GiantTour[i])
    #         gain -= Inputs.Distance(self.GiantTour[j - 1], self.GiantTour[j])
    #         gain -= Inputs.DistanceToDepot(self.GiantTour[j])
    #     elif j + 1 < len(self.GiantTour) and self.Routes[self.GiantTour[j + 1]] == self.Routes[self.GiantTour[j]] and \
    #             self.Routes[self.GiantTour[j - 1]] != self.Routes[self.GiantTour[j]]:
    #         gain += Inputs.Distance(self.GiantTour[i], self.GiantTour[j + 1])
    #         gain += Inputs.DistanceFromDepot(self.GiantTour[i])
    #         gain -= Inputs.Distance(self.GiantTour[j], self.GiantTour[j + 1])
    #         gain -= Inputs.DistanceFromDepot(self.GiantTour[j])
    #     elif (j + 1 == len(self.GiantTour) or self.Routes[self.GiantTour[j + 1]] != self.Routes[self.GiantTour[j]]) and \
    #             self.Routes[self.GiantTour[j - 1]] != self.Routes[self.GiantTour[j]]:
    #         gain += Inputs.DistanceFromDepot(self.GiantTour[i])
    #         gain -= Inputs.DistanceFromDepot(self.GiantTour[j])
    #         gain += Inputs.DistanceToDepot(self.GiantTour[i])
    #         gain -= Inputs.DistanceToDepot(self.GiantTour[j])
    #
    #     if i > 0 and self.Routes[self.GiantTour[i - 1]] == self.Routes[self.GiantTour[i]] and self.Routes[
    #         self.GiantTour[i + 1]] == self.Routes[self.GiantTour[i]]:
    #         gain += Inputs.Distance(self.GiantTour[j], self.GiantTour[i + 1])
    #         gain += Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[j])
    #         gain -= Inputs.Distance(self.GiantTour[i], self.GiantTour[i + 1])
    #         gain -= Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i])
    #     elif (i == 0 or self.Routes[self.GiantTour[i - 1]] != self.Routes[self.GiantTour[i]]) and self.Routes[
    #         self.GiantTour[i + 1]] == self.Routes[self.GiantTour[i]]:
    #         gain += Inputs.Distance(self.GiantTour[j], self.GiantTour[i + 1])
    #         gain += Inputs.DistanceFromDepot(self.GiantTour[j])
    #         gain -= Inputs.Distance(self.GiantTour[i], self.GiantTour[i + 1])
    #         gain -= Inputs.DistanceFromDepot(self.GiantTour[i])
    #     elif i > 0 and self.Routes[self.GiantTour[i - 1]] == self.Routes[self.GiantTour[i]] and self.Routes[
    #         self.GiantTour[i + 1]] != self.Routes[self.GiantTour[i]]:
    #         gain += Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[j])
    #         gain += Inputs.DistanceToDepot(self.GiantTour[j])
    #         gain -= Inputs.Distance(self.GiantTour[i - 1], self.GiantTour[i])
    #         gain -= Inputs.DistanceToDepot(self.GiantTour[i])
    #     elif (i == 0 or self.Routes[self.GiantTour[i - 1]] != self.Routes[self.GiantTour[i]]) and self.Routes[
    #         self.GiantTour[i + 1]] != self.Routes[self.GiantTour[i]]:
    #         gain -= Inputs.DistanceFromDepot(self.GiantTour[i])
    #         gain += Inputs.DistanceFromDepot(self.GiantTour[j])
    #         gain -= Inputs.DistanceToDepot(self.GiantTour[i])
    #         gain += Inputs.DistanceToDepot(self.GiantTour[j])
    #     return gain

    def getTraveledDistance(self, Inputs: inputs):
        return sum(r.getRouteCost(Inputs) for r in self.AuxiliaryGraph.getRoutes())

    def toString(self):
        """
        The solution\'s description
        :return:
        """
        txt = f'The solution contains {self.RoutesCounter} routes\n'
        r: int = 0
        txt += f'The route number {1 + r} contains:\n'
        for gene in self.GiantTour:
            if self.Routes[gene] != r:
                r += 1
                txt += f'The route number {1 + r} contains:\n'
            txt += f'\tCostumer {1 + gene}\n'
        txt += f'Solution\'s cost = {self.TraveledDistance}\n'
        return txt

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
            if i >= len(mother.GiantTour):
                print(i)
                print(len(mother.GiantTour))
                print(len(self.GiantTour))
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
        return heuristic_solution(Inputs, new_giant_tour)


def GeneticAlgorithm(Inputs: inputs, RunningTime: float):
    """
    Genetic algorithm launched for a selected running time in second then it returns the best solution of the population
    :param Inputs:
    :param RunningTime:
    :return:
    """
    population_length = 20
    start_time = time.time() * 1000
    population = InitialPopulation(Inputs, population_length)
    QuickSort(population, 0, len(population) - 1)
    print(f'\t{population[0].TraveledDistance} after {int(time.time() * 1000 - start_time)} ms')
    # quit()
    while time.time() * 1000 - start_time < RunningTime * 1000:
        if random.random() < 0.8:
            crossover_operation(Inputs, population, start_time)
        else:
            while True:
                new_solution = heuristic_solution(Inputs)
                if new_solution.isFeasible():
                    break
            UpdatePopulation(population, start_time, new_solution)
    return population[0]


def InitialPopulation(Inputs: inputs, population_size: int):
    """
    Randomly generated population
    :param Inputs:
    :param n:
    :return:
    """
    population = []
    print('Initial population:')
    for _ in range(population_size):
        while True:
            solution = heuristic_solution(Inputs)
            if solution.isFeasible():
                break
        print(f'{solution.TraveledDistance}')
        population.append(solution)
    return population


def UpdatePopulation(population: List[heuristic_solution], StartTime: float, solution: heuristic_solution):
    """
    This methode randomly adds a solution to the population then resorts it
    :param population:
    :param StartTime:
    :param solution:
    :return:
    """
    x = len(population) - 1
    if solution.isFeasible() and solution.TraveledDistance < population[x].TraveledDistance:
        if solution.TraveledDistance < population[0].TraveledDistance:
            print(f'\t{solution.TraveledDistance} after {int(time.time() * 1000 - StartTime)} ms')
        population[random.randint(len(population) // 2, x)] = solution
        QuickSort(population, 0, x)


def crossover_operation(Inputs: inputs, population, start_time) -> None:
    Length = len(population) - 1
    Half = len(population) // 2
    index_father = random.randint(0, Half)
    Father: heuristic_solution = population[index_father]
    if random.random() < 0.7:
        while True:
            index_mother = random.randint(0, Half)
            if index_mother == index_father:
                continue
            break
    else:
        index_mother = random.randint(Half + 1, Length)
    Mother: heuristic_solution = population[index_mother]
    if random.random() < 0.3:
        CutPoint1 = random.randint(0, len(Father.GiantTour) - 1)
        CutPoint2 = random.randint(CutPoint1, len(Father.GiantTour) - 1)
    else:
        CutPoint1 = CutPoint2 = random.randint(0, len(Father.GiantTour) - 1)
    t = threading.Thread(target=UpdatePopulation,
                         args=(population, start_time, Mother.Crossover(Inputs, Father, CutPoint1, CutPoint2),))
    t.start()
    Child: heuristic_solution = Father.Crossover(Inputs, Mother, CutPoint1, CutPoint2)
    t.join()
    UpdatePopulation(population, start_time, Child)


def RandomGiantTour(n: int):
    """
    This methode randomly generate a giant tour
    :param n:
    :return:
    """
    new_giant_tour = list(range(n))
    for i in range(n):
        Motion(i, random.randint(0, len(new_giant_tour) - 1)).Swap(new_giant_tour)
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
        Motion(i, j)._2opt(giant_tour)


def QuickSort(population: List[heuristic_solution], x: int, y: int):
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


def Partition(population: List[heuristic_solution], x: int, y: int):
    pivot = population[y].TraveledDistance
    i = x
    for j in range(x, y):
        if population[j].TraveledDistance < pivot:
            Motion(i, j).Swap(population)
            i += 1
    Motion(i, y).Swap(population)
    return i
