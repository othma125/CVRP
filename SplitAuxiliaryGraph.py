import itertools
import time
import threading
from typing import List
from LocalSearch import Swap, _2Opt, Insertion, InverseInsertion, local_search_movement
from InputDatas import inputs


class node:
    def __init__(self, i):
        """
        Split auxiliary graph node with index i
        :param i:
        """
        self.NodeInProcessWith: int = i
        self.NodeId: int = i
        self.RouteId: int = 0
        self.IsLSMNotNone: bool = False
        self.Label = float('inf')
        self.PosteriorNode = None
        self.LocalSearch = None
        self.ScheduledLabelImprovement = []

    def LabelImproved(self, starting_node, lsm: local_search_movement, new_label: float):
        self.ScheduledLabelImprovement.append(new_label)
        while self.ScheduledLabelImprovement[0] != new_label:
            time.sleep(0.0001)
        if new_label < self.Label:
            self.Label = new_label
            self.LocalSearch = lsm
            self.PosteriorNode = starting_node
            self.RouteId = self.PosteriorNode.RouteId + 1
            self.IsLSMNotNone = not self.IsLSMNotNone and self.LocalSearch is not None
        self.ScheduledLabelImprovement.pop(0)

    def getLabel(self):
        self.ScheduledLabelImprovement.append(-1)
        while self.ScheduledLabelImprovement[0] != -1:
            time.sleep(0.0001)
        label = self.Label
        self.ScheduledLabelImprovement.pop(0)
        return label

    def isLSMNone(self):
        self.ScheduledLabelImprovement.append(-2)
        while self.ScheduledLabelImprovement[0] != -2:
            time.sleep(0.0001)
        c = not self.IsLSMNotNone
        self.ScheduledLabelImprovement.pop(0)
        return c


class acrs(threading.Thread):

    def __init__(self, Inputs: inputs, nodes: List[node], giant_tour: List[int], Id: int, with_lsm: bool):
        """
        Split auxiliary graph arcs that are starting from the node with Id index
        :param i:
        """
        threading.Thread.__init__(self)
        self.InputDatas: inputs = Inputs
        self.Nodes: node = nodes
        self.GiantTour: List[int] = giant_tour
        self.NodeId: int = Id
        self.WithLocalSearch: bool = with_lsm

    def run(self):
        StartingNode: node = self.Nodes[self.NodeId]
        FirstCostumer: int = self.GiantTour[self.NodeId]
        EmptySpaceInVehicle: int = self.InputDatas.VehicleCapacity
        RouteTraveledDistance: float = self.InputDatas.DistanceFromDepot(FirstCostumer)
        for costumer_id in range(self.NodeId, len(self.GiantTour)):
            LastCostumer: int = self.GiantTour[costumer_id]
            if self.InputDatas.CostumerDemandedAmounts[LastCostumer] > EmptySpaceInVehicle:
                StartingNode.NodeInProcessWith = len(self.GiantTour)
                return
            RouteTraveledDistance += self.InputDatas.DistanceToDepot(LastCostumer)
            EndingNode: node = self.Nodes[costumer_id + 1]
            if RouteTraveledDistance <= self.InputDatas.MaxDistance:
                Feasibility = True
                EndingNode.LabelImproved(StartingNode, None, RouteTraveledDistance + StartingNode.Label)
            else:
                Feasibility = False
            if not Feasibility:
                StartingNode.NodeInProcessWith = len(self.GiantTour)
                return
            elif self.WithLocalSearch and EndingNode.isLSMNone():
                ImprovedTraveledDistance = RouteTraveledDistance
                giant_tour_portion = self.GiantTour[self.NodeId: costumer_id + 1]
                lsm = None
                for i in range(self.NodeId, costumer_id):
                    for j in range(costumer_id, i, -1):
                        _2opt = _2Opt(i, j, self.NodeId, costumer_id, giant_tour_portion)
                        if _2opt.isFeasible(self.InputDatas):
                            lsm = _2opt
                            ImprovedTraveledDistance += lsm.gain
                            giant_tour_portion = lsm.GiantTourPortion
                            continue
                        if j == i + 1:
                            continue
                        ins = Insertion(False, 0, i, j, self.NodeId, costumer_id, giant_tour_portion)
                        if ins.isFeasible(self.InputDatas):
                            lsm = ins
                            ImprovedTraveledDistance += lsm.gain
                            giant_tour_portion = lsm.GiantTourPortion
                            continue
                        inv_ins = InverseInsertion(False, 0, i, j, self.NodeId, costumer_id, giant_tour_portion)
                        if inv_ins.isFeasible(self.InputDatas):
                            lsm = inv_ins
                            ImprovedTraveledDistance += lsm.gain
                            giant_tour_portion = lsm.GiantTourPortion
                            continue
                        swp = Swap(i, j, self.NodeId, costumer_id, giant_tour_portion)
                        if swp.isFeasible(self.InputDatas):
                            lsm = swp
                            ImprovedTraveledDistance += lsm.gain
                            giant_tour_portion = lsm.GiantTourPortion
                if lsm is not None:
                    EndingNode.LabelImproved(StartingNode, lsm, ImprovedTraveledDistance + StartingNode.Label)
            if costumer_id + 1 < len(self.GiantTour):
                RouteTraveledDistance += self.InputDatas.Distance(LastCostumer, self.GiantTour[costumer_id + 1])
            RouteTraveledDistance -= self.InputDatas.DistanceToDepot(LastCostumer)
            EmptySpaceInVehicle -= self.InputDatas.CostumerDemandedAmounts[LastCostumer]
            StartingNode.NodeInProcessWith += 1


def wait(nodes: List[node], i):
    """
    Threads orchestration
    :param nodes:
    :param i:
    :return:
    """
    for j in range(len(nodes) - 1, -1, -1):
        if nodes[j].NodeInProcessWith < i:
            return True
    return False
