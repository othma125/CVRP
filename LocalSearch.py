from typing import List
from Tools import ListEditor
from InputDatas import inputs


class local_search_movement:
    """
    This class manage the local search movements that may be applied between two points on a giant tour portion. this last is systematically selected in the Split algorithm
    """
    def __init__(self, i: int, j: int, first_border: int, second_border: int, giant_tour_portion: List[int]):
        self.I: int = i
        self.J: int = j
        self.FirstBorder: int = first_border
        self.SecondBorder: int = second_border
        self.GiantTourPortion: List[int] = giant_tour_portion


class _2Opt(local_search_movement):
    def __init__(self, i: int, j: int, first_border: int, second_border: int, giant_tour_portion: List[int]):
        super().__init__(i, j, first_border, second_border, giant_tour_portion)
        self.Name = 'inverse insertion'

    def isFeasible(self, Inputs: inputs):
        """
        Only the movement with negative gain is selected
        :param Inputs:
        :return:
        """
        self.Feasibility: bool = True
        self.Gain(Inputs)
        if self.gain < 0:
            self.GiantTourPortion = self.GiantTourPortion.copy()
            ListEditor(self.I - self.FirstBorder, self.J - self.FirstBorder).Movement_2opt(self.GiantTourPortion)
        else:
            self.Feasibility = False
        return self.Feasibility

    def Gain(self, Inputs: inputs):
        self.gain: float = 0
        if self.I == self.FirstBorder:
            self.gain += Inputs.DistanceFromDepot(self.GiantTourPortion[self.J - self.FirstBorder])
            self.gain -= Inputs.DistanceFromDepot(self.GiantTourPortion[self.I - self.FirstBorder])
        else:
            self.gain += Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder - 1],
                                         self.GiantTourPortion[self.J - self.FirstBorder])
            self.gain -= Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder - 1],
                                         self.GiantTourPortion[self.I - self.FirstBorder])
        if self.J == self.SecondBorder:
            self.gain += Inputs.DistanceToDepot(self.GiantTourPortion[self.I - self.FirstBorder])
            self.gain -= Inputs.DistanceToDepot(self.GiantTourPortion[self.J - self.FirstBorder])
        else:
            self.gain += Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder],
                                         self.GiantTourPortion[self.J - self.FirstBorder + 1])
            self.gain -= Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder],
                                         self.GiantTourPortion[self.J - self.FirstBorder + 1])


class Swap(local_search_movement):
    def __init__(self, i: int, j: int, first_border: int, second_border: int, giant_tour_portion: List[int]):
        super().__init__(i, j, first_border, second_border, giant_tour_portion)
        self.Name = 'inverse insertion'

    def isFeasible(self, Inputs: inputs):
        """
        Only the movement with negative gain is selected
        :param Inputs:
        :return:
        """
        self.Feasibility: bool = True
        self.Gain(Inputs)
        if self.gain < 0:
            self.GiantTourPortion = self.GiantTourPortion.copy()
            ListEditor(self.I - self.FirstBorder, self.J - self.FirstBorder).MovementSwap(self.GiantTourPortion)
        else:
            self.Feasibility = False
        return self.Feasibility

    def Gain(self, Inputs: inputs):
        self.gain: float = 0
        if self.I == self.FirstBorder:
            self.gain += Inputs.DistanceFromDepot(self.GiantTourPortion[self.J - self.FirstBorder])
            self.gain -= Inputs.DistanceFromDepot(self.GiantTourPortion[self.I - self.FirstBorder])
        else:
            self.gain += Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder - 1],
                                         self.GiantTourPortion[self.J - self.FirstBorder])
            self.gain -= Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder - 1],
                                         self.GiantTourPortion[self.I - self.FirstBorder])
        if self.I + 1 < self.J:
            self.gain += Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder - 1],
                                         self.GiantTourPortion[self.I - self.FirstBorder])
            self.gain -= Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder - 1],
                                         self.GiantTourPortion[self.J - self.FirstBorder])
            self.gain += Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder],
                                         self.GiantTourPortion[self.I - self.FirstBorder + 1])
            self.gain -= Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder],
                                         self.GiantTourPortion[self.I - self.FirstBorder + 1])
        if self.J == self.SecondBorder:
            self.gain += Inputs.DistanceToDepot(self.GiantTourPortion[self.I - self.FirstBorder])
            self.gain -= Inputs.DistanceToDepot(self.GiantTourPortion[self.J - self.FirstBorder])
        else:
            self.gain += Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder],
                                         self.GiantTourPortion[self.J - self.FirstBorder + 1])
            self.gain -= Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder],
                                         self.GiantTourPortion[self.J - self.FirstBorder + 1])


class Insertion(local_search_movement):
    def __init__(self, with2opt: bool, n: int, i: int, j: int, first_border: int, second_border: int,
                 giant_tour_portion: List[int]):
        super().__init__(i, j, first_border, second_border, giant_tour_portion)
        self.N: int = n
        self.With2Opt: bool = with2opt
        self.Name: str = 'inverse insertion'

    def isFeasible(self, Inputs: inputs):
        """
        Only the movement with negative gain is selected
        :param Inputs:
        :return:
        """
        self.Feasibility: bool = True
        self.Gain(Inputs)
        if self.gain < 0:
            self.GiantTourPortion = self.GiantTourPortion.copy()
            for k in range(self.N + 1):
                if self.With2Opt:
                    ListEditor(self.I - self.FirstBorder, self.J - self.FirstBorder + k).MovementInsertion(
                        self.GiantTourPortion)
                else:
                    ListEditor(self.I - self.FirstBorder + k, self.J - self.FirstBorder + k).MovementInsertion(
                        self.GiantTourPortion)
        else:
            self.Feasibility = False

    def Gain(self, Inputs: inputs):
        self.gain: float = 0
        if self.With2Opt:
            if self.I == self.FirstBorder:
                self.gain += Inputs.DistanceFromDepot(self.GiantTourPortion[self.J + self.N - self.FirstBorder])
                self.gain += Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder],
                                             self.GiantTourPortion[self.I - self.FirstBorder])
                self.gain -= Inputs.DistanceFromDepot(self.GiantTourPortion[self.I - self.FirstBorder])
            else:
                self.gain += Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder - 1],
                                             self.GiantTourPortion[self.J + self.N - self.FirstBorder])
                self.gain += Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder],
                                             self.GiantTourPortion[self.I - self.FirstBorder])
                self.gain -= Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder - 1],
                                             self.GiantTourPortion[self.I - self.FirstBorder])
        else:
            if self.I == self.FirstBorder:
                self.gain += Inputs.DistanceFromDepot(self.GiantTourPortion[self.J - self.FirstBorder])
                self.gain += Inputs.Distance(self.GiantTourPortion[self.J + self.N - self.FirstBorder],
                                             self.GiantTourPortion[self.I - self.FirstBorder])
                self.gain -= Inputs.DistanceFromDepot(self.GiantTourPortion[self.I - self.FirstBorder])
            else:
                self.gain += Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder - 1],
                                             self.GiantTourPortion[self.J - self.FirstBorder])
                self.gain += Inputs.Distance(self.GiantTourPortion[self.J + self.N - self.FirstBorder],
                                             self.GiantTourPortion[self.I - self.FirstBorder])
                self.gain -= Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder - 1],
                                             self.GiantTourPortion[self.I - self.FirstBorder])
        if self.J + self.N == self.SecondBorder:
            self.gain += (Inputs.DistanceToDepot(
                self.GiantTourPortion[self.J - self.FirstBorder - 1]) - Inputs.DistanceToDepot(
                self.GiantTourPortion[self.J + self.N - self.FirstBorder]) - Inputs.Distance(
                self.GiantTourPortion[self.J - self.FirstBorder - 1], self.GiantTourPortion[self.J - self.FirstBorder]))
        else:
            self.gain += Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder - 1],
                                         self.GiantTourPortion[self.J + self.N - self.FirstBorder + 1])
            self.gain -= Inputs.Distance(self.GiantTourPortion[self.J + self.N - self.FirstBorder],
                                         self.GiantTourPortion[self.J + self.N - self.FirstBorder + 1])
            self.gain -= Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder - 1],
                                         self.GiantTourPortion[self.J - self.FirstBorder])


class InverseInsertion(local_search_movement):
    def __init__(self, with2opt: bool, n: int, i: int, j: int, first_border: int, second_border: int,
                 giant_tour_portion: List[int]):
        super().__init__(i, j, first_border, second_border, giant_tour_portion)
        self.N: int = n
        self.With2Opt: bool = with2opt
        self.Name: str = 'inverse insertion'

    def isFeasible(self, Inputs: inputs):
        """
        Only the movement with negative gain is selected
        :param Inputs:
        :return:
        """
        self.Feasibility: bool = True
        self.Gain(Inputs)
        if self.gain < 0:
            self.GiantTourPortion = self.GiantTourPortion.copy()
            for k in range(self.N + 1):
                if self.With2Opt:
                    ListEditor(self.I - self.FirstBorder - k, self.J - self.FirstBorder).MovementInverseInsertion(
                        self.GiantTourPortion)
                else:
                    ListEditor(self.I - self.FirstBorder - k, self.J - self.FirstBorder - k).MovementInverseInsertion(
                        self.GiantTourPortion)
        else:
            self.Feasibility = False

    def Gain(self, Inputs: inputs):
        self.gain: float = 0
        if self.With2Opt:
            if self.J == self.SecondBorder:
                self.gain += Inputs.DistanceToDepot(self.GiantTourPortion[self.I - self.FirstBorder - self.N])
                self.gain += Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder],
                                             self.GiantTourPortion[self.I - self.FirstBorder])
                self.gain -= Inputs.DistanceToDepot(self.GiantTourPortion[self.J - self.FirstBorder])
            else:
                self.gain += Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder],
                                             self.GiantTourPortion[self.I - self.FirstBorder])
                self.gain += Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder - self.N],
                                             self.GiantTourPortion[self.J - self.FirstBorder + 1])
                self.gain -= Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder],
                                             self.GiantTourPortion[self.J - self.FirstBorder + 1])
        else:
            if self.J == self.SecondBorder:
                self.gain += Inputs.DistanceToDepot(self.GiantTourPortion[self.I - self.FirstBorder])
                self.gain += Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder],
                                             self.GiantTourPortion[self.I - self.N - self.FirstBorder])
                self.gain -= Inputs.DistanceToDepot(self.GiantTourPortion[self.J - self.FirstBorder])
            else:
                self.gain += Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder],
                                             self.GiantTourPortion[self.I - self.N - self.FirstBorder])
                self.gain += Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder],
                                             self.GiantTourPortion[self.J - self.FirstBorder + 1])
                self.gain -= Inputs.Distance(self.GiantTourPortion[self.J - self.FirstBorder],
                                             self.GiantTourPortion[self.J - self.FirstBorder + 1])
        if self.I - self.N == self.FirstBorder:
            self.gain += Inputs.DistanceFromDepot(self.GiantTourPortion[self.I - self.FirstBorder + 1])
            self.gain -= Inputs.DistanceFromDepot(self.GiantTourPortion[self.I - self.N - self.FirstBorder])
            self.gain -= Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder],
                                         self.GiantTourPortion[self.I - self.FirstBorder + 1])
        else:
            self.gain += Inputs.Distance(self.GiantTourPortion[self.I - self.N - self.FirstBorder - 1],
                                         self.GiantTourPortion[self.I - self.FirstBorder + 1])
            self.gain -= Inputs.Distance(self.GiantTourPortion[self.I - self.FirstBorder],
                                         self.GiantTourPortion[self.I - self.FirstBorder + 1])
            self.gain -= Inputs.Distance(self.GiantTourPortion[self.I - self.N - self.FirstBorder - 1],
                                         self.GiantTourPortion[self.I - self.N - self.FirstBorder])
