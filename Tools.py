from typing import List


class ListEditor:
    def __init__(self, Id1: int, Id2: int):
        """
        Local search movement between two indexes
        :param Id1:
        :param Id2:
        """
        self.Index1 = Id1
        self.Index2 = Id2

    def MovementSwap(self, li: list):
        if self.Index1 != self.Index2:
            aux = li[self.Index1]
            li[self.Index1] = li[self.Index2]
            li[self.Index2] = aux

    def Movement_2opt(self, li: list):
        if self.Index1 < self.Index2:
            k = self.Index1
            l = self.Index2
            while k < l:
                ListEditor(k, l).MovementSwap(li)
                k += 1
                l -= 1
        else:
            print('_2opt error')
            quit(0)

    def MovementInsertion(self, li: list):
        if self.Index1 < self.Index2:
            aux = li[self.Index2]
            k = self.Index2
            while k > self.Index1:
                li[k] = li[k - 1]
                k -= 1
            li[self.Index1] = aux
        else:
            print('insertion error')
            quit(0)

    def MovementInverseInsertion(self, li: list):
        if self.Index1 < self.Index2:
            aux = li[self.Index1]
            k = self.Index1
            while k < self.Index2:
                li[k] = li[k + 1]
                k += 1
            li[self.Index2] = aux
        else:
            print('inverse insertion error')
            quit(0)


def QuickSort(my_list: List[int], x, y):
    """
    Integer array sorting
    :param my_list:
    :param x:
    :param y:
    :return:
    """
    if x < y:
        p = partition(my_list, x, y)
        QuickSort(my_list, x, p - 1)
        QuickSort(my_list, p + 1, y)


def partition(my_list: List[int], x, y):
    pivot = my_list[y]
    i = x
    for j in range(x, y):
        if my_list[j] < pivot:
            ListEditor(i, j).MovementSwap(my_list)
            i += 1
    ListEditor(i, y).MovementSwap(my_list)
    return i
