import itertools
from Tools import Motion
from InputDatas import inputs


class local_search_motion:
    """
    This class manage the local search movements that may be applied on a giant tour portion. this last is systematically selected in the Split algorithm
    """

    def __init__(self, i: int, j: int, **portions):
        self.I: int = i
        self.J: int = j
        self.OnePortion = len(portions) == 1
        self.Border: int = len(portions['portion1'] if self.OnePortion else portions['portion2'])
        self.GiantTourPortion1 = portions['portion1']
        self.GiantTourPortion2 = portions['portion1'] if self.OnePortion else portions['portion2']
        self.gain: float = 0

    def isFeasible(self, Inputs: inputs):
        """
        Only the movement with negative gain is selected
        :param Inputs:
        :return:
        """
        self.setGain(Inputs)
        if self.gain < 0:
            self.Execution()
            return True
        return False

    # def getGain(self, Inputs: Parameters):
    #     self.setGain(Inputs)
    #     return self.gain


class _2Opt(local_search_motion):
    def __init__(self, i: int, j: int, **portions):
        super().__init__(i, j, **portions)
        self.Name: str = 'inverse insertion'

    def Execution(self):
        if self.OnePortion:
            Motion(self.I, self.J)._2opt(self.GiantTourPortion1)
        else:
            l1 = [self.GiantTourPortion1[i] for i in range(self.I)]
            for i in range(self.J, -1, -1):
                l1.append(self.GiantTourPortion2[i])
            l2 = self.GiantTourPortion2[self.J + 1:len(self.GiantTourPortion2)]
            for i in range(self.I, len(self.GiantTourPortion1)):
                l2.insert(0, self.GiantTourPortion1[i])
            self.GiantTourPortion1 = l1
            self.GiantTourPortion2 = l2

    def setGain(self, Inputs: inputs):
        if self.I == 0:
            self.gain += Inputs.DistanceFromDepot(self.GiantTourPortion2[self.J])
            self.gain -= Inputs.DistanceFromDepot(self.GiantTourPortion1[self.I])
        else:
            self.gain += Inputs.Distance(self.GiantTourPortion1[self.I - 1],
                                         self.GiantTourPortion2[self.J])
            self.gain -= Inputs.Distance(self.GiantTourPortion1[self.I - 1],
                                         self.GiantTourPortion1[self.I])
        if self.J + 1 < self.Border:
            self.gain += Inputs.Distance(self.GiantTourPortion1[self.I],
                                         self.GiantTourPortion2[self.J + 1])
            self.gain -= Inputs.Distance(self.GiantTourPortion2[self.J],
                                         self.GiantTourPortion2[self.J + 1])
        else:
            self.gain += Inputs.DistanceToDepot(self.GiantTourPortion1[self.I])
            self.gain -= Inputs.DistanceToDepot(self.GiantTourPortion2[self.J])


class Swap(local_search_motion):
    def __init__(self, i: int, j: int, **portions):
        super().__init__(i, j, **portions)
        self.FirstBorder = len(self.GiantTourPortion1)
        self.Name: str = 'inverse insertion'

    def Execution(self):
        if self.OnePortion:
            Motion(self.I, self.J).Swap(self.GiantTourPortion1)
        else:
            aux: int = self.GiantTourPortion1[self.I]
            self.GiantTourPortion1[self.I] = self.GiantTourPortion2[self.J]
            self.GiantTourPortion2[self.J] = aux

    def setGain(self, Inputs: inputs):
        if self.I == 0:
            self.gain += Inputs.DistanceFromDepot(self.GiantTourPortion2[self.J])
            self.gain -= Inputs.DistanceFromDepot(self.GiantTourPortion1[self.I])
        else:
            self.gain += Inputs.Distance(self.GiantTourPortion1[self.I - 1],
                                         self.GiantTourPortion2[self.J])
            self.gain -= Inputs.Distance(self.GiantTourPortion1[self.I - 1],
                                         self.GiantTourPortion1[self.I])
        if self.I + 1 < self.J and self.OnePortion:
            self.gain += Inputs.Distance(self.GiantTourPortion1[self.J - 1],
                                         self.GiantTourPortion1[self.I])
            self.gain -= Inputs.Distance(self.GiantTourPortion1[self.J - 1],
                                         self.GiantTourPortion1[self.J])
            self.gain += Inputs.Distance(self.GiantTourPortion1[self.J],
                                         self.GiantTourPortion1[self.I + 1])
            self.gain -= Inputs.Distance(self.GiantTourPortion1[self.I],
                                         self.GiantTourPortion1[self.I + 1])
        elif not self.OnePortion:
            self.gain += Inputs.Distance(self.GiantTourPortion2[self.J - 1],
                                         self.GiantTourPortion1[self.I]) if self.J > 0 else Inputs.DistanceFromDepot(
                self.GiantTourPortion1[self.I])
            self.gain -= Inputs.Distance(self.GiantTourPortion2[self.J - 1],
                                         self.GiantTourPortion2[self.J]) if self.J > 0 else Inputs.DistanceFromDepot(
                self.GiantTourPortion2[self.J])
            self.gain += Inputs.Distance(self.GiantTourPortion2[self.J],
                                         self.GiantTourPortion1[
                                             self.I + 1]) if self.I + 1 < self.FirstBorder else Inputs.DistanceToDepot(
                self.GiantTourPortion2[self.J])
            self.gain -= Inputs.Distance(self.GiantTourPortion1[self.I],
                                         self.GiantTourPortion1[
                                             self.I + 1]) if self.I + 1 < self.FirstBorder else Inputs.DistanceToDepot(
                self.GiantTourPortion1[self.I])
        if self.J + 1 < self.Border:
            self.gain += Inputs.Distance(self.GiantTourPortion1[self.I],
                                         self.GiantTourPortion2[self.J + 1])
            self.gain -= Inputs.Distance(self.GiantTourPortion2[self.J],
                                         self.GiantTourPortion2[self.J + 1])
        else:
            self.gain += Inputs.DistanceToDepot(self.GiantTourPortion1[self.I])
            self.gain -= Inputs.DistanceToDepot(self.GiantTourPortion2[self.J])


class Insertion(local_search_motion):
    def __init__(self, with2opt: bool, n: int, i: int, j: int, **portions):
        super().__init__(i, j, **portions)
        self.N: int = n
        self.With2Opt: bool = with2opt
        self.Name: str = 'inverse insertion'

    def Execution(self):
        if self.OnePortion:
            for k in range(self.N + 1):
                Motion(self.I + (0 if self.With2Opt else k), self.J + k).Insertion(self.GiantTourPortion1)
        else:
            for k in range(self.N + 1):
                self.GiantTourPortion1.insert(self.I + (0 if self.With2Opt else k),
                                              self.GiantTourPortion2[self.J + k])
            for _ in range(self.N + 1):
                self.GiantTourPortion2.pop(self.J)

    def setGain(self, Inputs: inputs):
        self.gain -= Inputs.DistanceFromDepot(self.GiantTourPortion1[self.I]) if self.I == 0 else Inputs.Distance(
            self.GiantTourPortion1[self.I - 1], self.GiantTourPortion1[self.I])
        if self.With2Opt:
            self.gain += Inputs.Distance(self.GiantTourPortion2[self.J],
                                         self.GiantTourPortion1[self.I])
            self.gain += Inputs.DistanceFromDepot(
                self.GiantTourPortion2[self.J + self.N]) if self.I == 0 else Inputs.Distance(
                self.GiantTourPortion1[self.I - 1],
                self.GiantTourPortion2[self.J + self.N])
        else:
            self.gain += Inputs.Distance(self.GiantTourPortion2[self.J + self.N],
                                         self.GiantTourPortion1[self.I])
            self.gain += Inputs.DistanceFromDepot(self.GiantTourPortion2[self.J]) if self.I == 0 else Inputs.Distance(
                self.GiantTourPortion1[self.I - 1],
                self.GiantTourPortion2[self.J])
        self.gain -= Inputs.Distance(self.GiantTourPortion2[self.J - 1],
                                     self.GiantTourPortion2[
                                         self.J]) if self.J > 0 or self.OnePortion else Inputs.DistanceFromDepot(
            self.GiantTourPortion2[self.J])
        if self.J + self.N + 1 < self.Border:
            self.gain += Inputs.Distance(self.GiantTourPortion2[self.J - 1],
                                         self.GiantTourPortion2[
                                             self.J + self.N + 1]) if self.J > 0 or self.OnePortion else Inputs.DistanceFromDepot(
                self.GiantTourPortion2[self.J + self.N + 1])
            self.gain -= Inputs.Distance(self.GiantTourPortion2[self.J + self.N],
                                         self.GiantTourPortion2[self.J + self.N + 1])
        else:
            self.gain += Inputs.DistanceToDepot(
                self.GiantTourPortion2[self.J - 1]) if self.J > 0 or self.OnePortion else 0
            self.gain -= Inputs.DistanceToDepot(self.GiantTourPortion2[self.J + self.N])


class InverseInsertion(local_search_motion):
    def __init__(self, with2opt: bool, n: int, i: int, j: int, **portions):
        super().__init__(i, j, **portions)
        self.N: int = n
        self.With2Opt: bool = with2opt
        self.FirstBorder = len(self.GiantTourPortion1)
        self.Name: str = 'inverse insertion'

    def Execution(self):
        if self.OnePortion:
            for k in range(self.N + 1):
                Motion(self.I - k, self.J if self.With2Opt else self.J - k).InverseInsertion(self.GiantTourPortion1)
        else:
            if len(self.GiantTourPortion2) == 0:
                if self.With2Opt:
                    self.GiantTourPortion2 = self.GiantTourPortion1[self.I: self.I - self.N - 1: -1]
                else:
                    self.GiantTourPortion2 = self.GiantTourPortion1[self.I - self.N: self.I + 1]
            else:
                for k in range(self.N + 1):
                    self.GiantTourPortion2.insert(self.J + 1 + (k if self.With2Opt else 0),
                                                  self.GiantTourPortion1[self.I - k])
            for _ in range(self.N + 1):
                self.GiantTourPortion1.pop(self.I - self.N)

    def setGain(self, Inputs: inputs):
        if self.Border == 0:
            if self.With2Opt:
                self.gain += Inputs.DistanceFromDepot(self.GiantTourPortion1[self.I])
                self.gain += Inputs.DistanceToDepot(self.GiantTourPortion1[self.I - self.N])
            else:
                self.gain += Inputs.DistanceToDepot(self.GiantTourPortion1[self.I])
                self.gain += Inputs.DistanceFromDepot(self.GiantTourPortion1[self.I - self.N])
        else:
            self.gain -= Inputs.Distance(self.GiantTourPortion2[self.J], self.GiantTourPortion2[
                self.J + 1]) if self.J + 1 < self.Border else Inputs.DistanceToDepot(
                self.GiantTourPortion2[self.J])
            if self.With2Opt:
                self.gain += Inputs.Distance(self.GiantTourPortion2[self.J], self.GiantTourPortion1[self.I])
                self.gain += Inputs.Distance(self.GiantTourPortion1[self.I - self.N],
                                             self.GiantTourPortion2[self.J + 1]) \
                    if self.J + 1 < self.Border else Inputs.DistanceToDepot(self.GiantTourPortion1[self.I - self.N])
            else:
                self.gain += Inputs.Distance(self.GiantTourPortion2[self.J], self.GiantTourPortion1[self.I - self.N])
                self.gain += Inputs.Distance(self.GiantTourPortion1[self.I],
                                             self.GiantTourPortion2[self.J + 1]) \
                    if self.J + 1 < self.Border else Inputs.DistanceToDepot(self.GiantTourPortion1[self.I])
        self.gain -= Inputs.Distance(self.GiantTourPortion1[self.I],
                                     self.GiantTourPortion1[self.I + 1]) \
            if self.I + 1 < self.FirstBorder or self.OnePortion else Inputs.DistanceToDepot(
            self.GiantTourPortion1[self.I])
        if self.I - self.N == 0:
            self.gain += Inputs.DistanceFromDepot(
                self.GiantTourPortion1[self.I + 1]) if self.I + 1 < self.FirstBorder or self.OnePortion else 0
            self.gain -= Inputs.DistanceFromDepot(self.GiantTourPortion1[self.I - self.N])
        else:
            self.gain += Inputs.Distance(self.GiantTourPortion1[self.I - self.N - 1],
                                         self.GiantTourPortion1[
                                             self.I + 1]) if self.I + 1 < self.FirstBorder or self.OnePortion else Inputs.DistanceToDepot(
                self.GiantTourPortion1[self.I - self.N - 1])
            self.gain -= Inputs.Distance(self.GiantTourPortion1[self.I - self.N - 1],
                                         self.GiantTourPortion1[self.I - self.N])
