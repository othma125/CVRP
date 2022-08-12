import itertools
import threading
from typing import List

from InputDatas import inputs
from LocalSearch import Swap, _2Opt, Insertion, InverseInsertion


class route:
    def __init__(self, Inputs: inputs, portion, cost: float, empty_space: int, LSM: bool = True):
        self.GiantTourPortion = portion
        self.Length = len(self.GiantTourPortion)
        self.isImprovedByLSM = LSM
        self.RouteCost: float = self.getRouteCost(Inputs) if cost < 0 else cost
        self.EmptySpaceInVehicle: int = self.getEmptySpace(Inputs) if empty_space < 0 else empty_space

    def getEmptySpace(self, Inputs: inputs) -> int:
        if self.Length == 0:
            return Inputs.VehicleCapacity
        return Inputs.VehicleCapacity - sum(Inputs.CostumerDemandedAmounts[x] for x in self.GiantTourPortion)

    def getRouteCost(self, Inputs: inputs) -> float:
        if self.Length == 0:
            return 0
        return Inputs.DistanceFromDepot(self.GiantTourPortion[0]) + sum(
            Inputs.Distance(x, self.GiantTourPortion[index + 1]) if index + 1 < self.Length else Inputs.DistanceToDepot(
                x) for index, x
            in enumerate(self.GiantTourPortion))

    def getLocalSearchMotion(self, Inputs: inputs, r):
        s1: int = sum(Inputs.CostumerDemandedAmounts[x] for x in self.GiantTourPortion)
        for i in range(self.Length):
            s2: int = 0
            for j in range(r.Length):
                s2 += Inputs.CostumerDemandedAmounts[r.GiantTourPortion[j]]
                if r.EmptySpaceInVehicle + s2 >= s1 and self.EmptySpaceInVehicle + s1 >= s2:
                    lsm = _2Opt(i, j, portion1=self.GiantTourPortion, portion2=r.GiantTourPortion)
                    if lsm.isFeasible(Inputs):
                        return lsm
                # s: int = 0
                # for n in itertools.count(start=0):
                #     if j + n < r.Length:
                #         s += Inputs.CostumerDemandedAmounts[r.GiantTourPortion[j + n]]
                #         if self.EmptySpaceInVehicle >= s:
                #             lsm = Insertion(False, n, i, j, portion1=self.GiantTourPortion.copy(),
                #                              portion2=r.GiantTourPortion.copy())
                #             if lsm.isFeasible(Inputs):
                #                 return lsm
                #             if n > 0:
                #                 lsm = Insertion(True, n, i, j, portion1=self.GiantTourPortion.copy(),
                #                                  portion2=r.GiantTourPortion.copy())
                #                 if lsm.isFeasible(Inputs):
                #                     return lsm
                #         else:
                #             break
                #     else:
                #         break
                # s = 0
                # for n in itertools.count(start=0):
                #     if i - n >= 0:
                #         s += Inputs.CostumerDemandedAmounts[self.GiantTourPortion[i - n]]
                #         if r.EmptySpaceInVehicle >= s:
                #             lsm = InverseInsertion(False, n, i, j, portion1=self.GiantTourPortion.copy(),
                #                                         portion2=r.GiantTourPortion.copy())
                #             if lsm.isFeasible(Inputs):
                #                 return lsm
                #             if n > 0:
                #                 lsm = InverseInsertion(True, n, i, j, portion1=self.GiantTourPortion.copy(),
                #                                             portion2=r.GiantTourPortion.copy())
                #                 if lsm.isFeasible(Inputs):
                #                     return lsm
                #         else:
                #             break
                #     else:
                #         break
                if r.EmptySpaceInVehicle >= Inputs.CostumerDemandedAmounts[self.GiantTourPortion[i]] - \
                        Inputs.CostumerDemandedAmounts[r.GiantTourPortion[j]] and self.EmptySpaceInVehicle >= \
                        Inputs.CostumerDemandedAmounts[r.GiantTourPortion[j]] - \
                        Inputs.CostumerDemandedAmounts[self.GiantTourPortion[i]]:
                    lsm = Swap(i, j, portion1=self.GiantTourPortion.copy(), portion2=r.GiantTourPortion.copy())
                    if lsm.isFeasible(Inputs):
                        return lsm
            s1 -= Inputs.CostumerDemandedAmounts[self.GiantTourPortion[i]]
        return None

    def ImproveByLocalSearch(self, Inputs: inputs, targeted_cost: float) -> None:
        for i in range(self.Length - 1):
            for j in range(self.Length - 1, i, -1):
                lsm = _2Opt(i, j, portion1=self.GiantTourPortion)
                if lsm.isFeasible(Inputs):
                    self.RouteCost += lsm.gain
                    self.isImprovedByLSM = True
                    if self.RouteCost < targeted_cost:
                        return
                if j == i + 1:
                    continue
                # for n in itertools.count(start=0):
                #     if j + n < self.Length:
                #         lsm = Insertion(False, n, i, j, portion1=self.GiantTourPortion)
                #         if lsm.isFeasible(Inputs):
                #             self.RouteCost += lsm.gain
                #             self.isImprovedByLSM = True
                #             if self.RouteCost < targeted_cost:
                #                 return
                #             break
                #         if n > 0:
                #             lsm = Insertion(True, n, i, j, portion1=self.GiantTourPortion)
                #             if lsm.isFeasible(Inputs):
                #                 self.RouteCost += lsm.gain
                #                 self.isImprovedByLSM = True
                #                 if self.RouteCost < targeted_cost:
                #                     return
                #                 break
                #     else:
                #         break
                # for n in itertools.count(start=0):
                #     if i - n >= 0:
                #         lsm = InverseInsertion(False, n, i, j, portion1=self.GiantTourPortion)
                #         if lsm.isFeasible(Inputs):
                #             self.RouteCost += lsm.gain
                #             self.isImprovedByLSM = True
                #             if self.RouteCost < targeted_cost:
                #                 return
                #             break
                #         if n > 0:
                #             lsm = InverseInsertion(True, n, i, j, portion1=self.GiantTourPortion)
                #             if lsm.isFeasible(Inputs):
                #                 self.RouteCost += lsm.gain
                #                 self.isImprovedByLSM = True
                #                 if self.RouteCost < targeted_cost:
                #                     return
                #                 break
                #     else:
                #         break
                lsm = Swap(i, j, portion1=self.GiantTourPortion)
                if lsm.isFeasible(Inputs):
                    self.RouteCost += lsm.gain
                    self.isImprovedByLSM = True
                    if self.RouteCost < targeted_cost:
                        return


class node:
    def __init__(self, i: int):
        """
        Split auxiliary graph node with index i
        :param i:
        """
        self.NodeIndex: int = i
        self.NodeIndexInConnectionWith: int = self.NodeIndex
        self.Label: float = float('inf') if self.NodeIndex > 0 else 0
        self.Posterior: node = None
        self.CostumersCounter: int = 0
        self.Lock = threading.Lock()

    def getLabel(self):
        self.Lock.acquire()
        label = self.Label
        self.Lock.release()
        return label

    def isFeasible(self) -> bool:
        # return self.Posterior is not None
        return self.Posterior is not None and self.CostumersCounter == self.NodeIndex

    def Update(self, Index: int, Posterior, new_label: float, *new_routes) -> None:
        self.Lock.acquire()
        if new_label < self.Label:
            self.Label = new_label
            self.Posterior = Posterior
            self.Routes = []
            self.CostumersCounter = 0
            k: int = 0
            for i, r in enumerate(self.Posterior.Routes):
                self.Routes.append(new_routes[0] if i == Index else r)
                self.CostumersCounter += len(new_routes[0].GiantTourPortion if i == Index else r.GiantTourPortion)
                if i == Index:
                    k += 1
            for i in range(int(Index >= 0), len(new_routes)):
                self.Routes.append(new_routes[i])
                self.CostumersCounter += len(new_routes[i].GiantTourPortion)
        self.Lock.release()

    # def getSkipCondition(self, Inputs: inputs, StartingNode, *stops) -> bool:
    #     if self.isFeasible():
    #         s: float = 0
    #         # self.Lock.acquire()
    #         for r in self.Routes:
    #             portion = []
    #             c = False
    #             for x in r.GiantTourPortion:
    #                 if x in stops:
    #                     c = True
    #                     continue
    #                 portion.append(x)
    #             s += route(Inputs, portion, -1, 0, False).RouteCost if c else r.RouteCost
    #         # self.Lock.release()
    #         return s <= StartingNode.Label
    #     return False

    def getImprovedNode(self, Inputs: inputs):
        for i, r in enumerate(self.Routes):
            for k in range(len(r.GiantTourPortion)):
                for n in itertools.count(start=0):
                    if k - n >= 0 and n + 1 < len(r.GiantTourPortion):
                        lsm = InverseInsertion(False, n, k, 0, portion1=r.GiantTourPortion.copy(), portion2=[])
                        if lsm.isFeasible(Inputs):
                            Node: node = node(self.NodeIndex)
                            Node.Lock = self.Lock
                            Node.Label = self.Label
                            new_route1 = route(Inputs, lsm.GiantTourPortion1, -1, -1)
                            new_route2 = route(Inputs, lsm.GiantTourPortion2, -1, -1)
                            Node.Label += new_route1.RouteCost + new_route2.RouteCost
                            Node.Label -= self.Routes[i].RouteCost
                            Node.Routes = [new_route1 if i == j else r for j, r in enumerate(self.Routes)]
                            Node.Routes.append(new_route2)
                            return Node
                    else:
                        break
        return self


class auxiliary_graph:
    def __init__(self, giant_tour: List[int], lsm: bool, bound: float):
        self.GiantTour = giant_tour
        self.Length: int = len(self.GiantTour)
        self.withLSM = lsm
        # self.BoundingCost = bound
        self.BoundingCost = float('inf')
        self.Nodes = [node(i) for i in range(1 + self.Length)]
        self.ThreadsCounter: int = 0

    def setArcs(self, Inputs: inputs):
        self.Nodes[0].Routes = []
        t = threading.Thread(target=self.run, args=(Inputs, 0,))
        self.ThreadsCounter += 1
        t.start()
        t.join()

    def run(self, Inputs: inputs, NodeIndex: int):
        # if self.withLSM and NodeIndex > 0:
        #     self.Nodes[NodeIndex] = self.Nodes[NodeIndex].getImprovedNode(Inputs)
        StartingNode: node = self.Nodes[NodeIndex]
        FirstCostumer: int = self.GiantTour[NodeIndex]
        EmptySpaceInVehicle: int = Inputs.VehicleCapacity
        TraveledDistance: float = Inputs.DistanceFromDepot(FirstCostumer)
        current_portion = []
        threads_list = []
        for j in itertools.count(start=NodeIndex):
            LastCostumer: int = self.GiantTour[j]
            EmptySpaceInVehicle -= Inputs.CostumerDemandedAmounts[LastCostumer]
            if EmptySpaceInVehicle < 0:
                StartingNode.NodeIndexInConnectionWith = self.Length
                if EndingNode.NodeIndex < self.Length:
                    self.getNewThread(Inputs, EndingNode, threads_list)
                break
            current_portion.append(LastCostumer)
            EndingNode: node = self.Nodes[j + 1]
            TraveledDistance += Inputs.DistanceToDepot(LastCostumer)
            current_route = route(Inputs, current_portion.copy(), TraveledDistance,
                                  EmptySpaceInVehicle, False)
            if self.withLSM:
                if current_route.Length > 2:
                    current_route.ImproveByLocalSearch(Inputs,
                                                       EndingNode.getLabel() - StartingNode.Label if EndingNode.isFeasible() else 0)
                if current_route.RouteCost <= Inputs.MaxDistanceConstraint:
                    EndingNode.Update(-1, StartingNode, StartingNode.Label + current_route.RouteCost, current_route)
                for i, r in enumerate(StartingNode.Routes):
                    if r.EmptySpaceInVehicle >= Inputs.VehicleCapacity - EmptySpaceInVehicle:
                        new_route = route(Inputs, r.GiantTourPortion + current_route.GiantTourPortion, -1,
                                          r.EmptySpaceInVehicle + EmptySpaceInVehicle - Inputs.VehicleCapacity)
                        if new_route.Length > 2:
                            new_route.ImproveByLocalSearch(Inputs,
                                                           EndingNode.getLabel() - StartingNode.Label + r.RouteCost if EndingNode.isFeasible() else 0)
                        if new_route.RouteCost <= Inputs.MaxDistanceConstraint:
                            EndingNode.Update(i, StartingNode, StartingNode.Label + new_route.RouteCost - r.RouteCost,
                                              new_route)
                            break
                for i, r in enumerate(StartingNode.Routes):
                    lsm = r.getLocalSearchMotion(Inputs, current_route)
                    if lsm is None:
                        continue
                    elif len(lsm.GiantTourPortion1) == 0 or len(lsm.GiantTourPortion2) == 0:
                        new_route = route(Inputs, lsm.GiantTourPortion2 if len(
                            lsm.GiantTourPortion1) == 0 else lsm.GiantTourPortion1,
                                          current_route.RouteCost + r.RouteCost + lsm.gain, -1)
                        if new_route.Length > 2:
                            new_route.ImproveByLocalSearch(Inputs, 0)
                        if new_route.RouteCost <= Inputs.MaxDistanceConstraint:
                            EndingNode.Update(i, StartingNode, StartingNode.Label + new_route.RouteCost - r.RouteCost,
                                              new_route)
                            break
                    else:
                        new_route1 = route(Inputs, lsm.GiantTourPortion1, -1, -1)
                        new_route2 = route(Inputs, lsm.GiantTourPortion2,
                                           current_route.RouteCost + r.RouteCost + lsm.gain - new_route1.RouteCost, -1)
                        if new_route1.Length > 2:
                            new_route1.ImproveByLocalSearch(Inputs, 0)
                        if new_route2.Length > 2:
                            new_route2.ImproveByLocalSearch(Inputs, 0)
                        if new_route1.RouteCost <= Inputs.MaxDistanceConstraint and new_route2.RouteCost <= Inputs.MaxDistanceConstraint:
                            EndingNode.Update(i, StartingNode,
                                              StartingNode.Label + new_route1.RouteCost + new_route2.RouteCost - r.RouteCost,
                                              new_route1, new_route2)
                            break
            elif StartingNode.Label >= EndingNode.Label:
                StartingNode.NodeIndexInConnectionWith += 1
                if EndingNode.NodeIndex == self.Length:
                    break
                else:
                    TraveledDistance += Inputs.Distance(LastCostumer, self.GiantTour[EndingNode.NodeIndex])
                    TraveledDistance -= Inputs.DistanceToDepot(LastCostumer)
                    self.getNewThread(Inputs, EndingNode, threads_list)
                    continue
            if TraveledDistance <= Inputs.MaxDistanceConstraint:
                EndingNode.Update(-1, StartingNode, StartingNode.Label + TraveledDistance, current_route)
            if EmptySpaceInVehicle == 0 or current_route.RouteCost > Inputs.MaxDistanceConstraint:
                StartingNode.NodeIndexInConnectionWith = self.Length
                if EndingNode.NodeIndex < self.Length:
                    self.getNewThread(Inputs, EndingNode, threads_list)
                break
            if EndingNode.NodeIndex < self.Length:
                TraveledDistance += Inputs.Distance(LastCostumer, self.GiantTour[EndingNode.NodeIndex])
                TraveledDistance -= Inputs.DistanceToDepot(LastCostumer)
                StartingNode.NodeIndexInConnectionWith += 1
                self.getNewThread(Inputs, EndingNode, threads_list)
            else:
                break
        for t in threads_list:
            t.join()

    def getNewThread(self, Inputs: inputs, Node: node, threads_list) -> None:
        """
        this methode spawn new thread that operate the method run(self, Inputs: Parameters, i: int) when its time comes.
        the created thread is added to threads_list
        :param Inputs:
        :param Node:
        :param threads_list:
        :return:
        """
        for i in range(Node.Posterior.NodeIndex if Node.isFeasible() else 0, Node.NodeIndex):
            if self.Nodes[i].NodeIndexInConnectionWith < Node.NodeIndex:
                return
        Node.Lock.acquire()
        c = self.ThreadsCounter == Node.NodeIndex
        if c:
            self.ThreadsCounter += 1
            if Node.Label < self.BoundingCost:
                t = threading.Thread(target=self.run, args=(Inputs, Node.NodeIndex,))
                t.start()
                threads_list.append(t)
            else:
                Node.NodeIndexInConnectionWith = self.Length
        Node.Lock.release()
        if c and self.ThreadsCounter < self.Length:
            self.getNewThread(Inputs, self.Nodes[self.ThreadsCounter], threads_list)

    def getTraveledDistance(self) -> float:
        return self.getLastNode().Label

    def getRoutesCounter(self) -> bool:
        return len(self.getRoutes())

    def getRoutes(self) -> List[route]:
        return self.getLastNode().Routes

    def getRoute(self, index: int) -> route:
        self.getRoutes()[index]

    def isFeasible(self) -> bool:
        return self.getLastNode().isFeasible()

    def getLastNode(self) -> node:
        return self.Nodes[self.Length]

    def isImprovedByLSM(self) -> bool:
        for r in self.getLastNode().Routes:
            if r.isImprovedByLSM:
                return True
        return False
