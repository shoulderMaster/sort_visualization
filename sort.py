#!/home/ckdqja0225/anaconda3/bin/python3 

import pandas as pd
from matplotlib import pyplot as plt
from random import shuffle
import sys
import time

class Sort() :

    def __init__(self, rangeToSort=range(1000), desc=False) :
        listToSort = [i for i in rangeToSort]
        shuffle(listToSort)
        self.originalDf = pd.DataFrame(listToSort)
        self.arrDf = self.originalDf.copy()
        self.fig = None
        self.rects = None

        if desc == True :
            self.compare = self._descending_compare
        else :
            self.compare = self._ascending_compare
        self.plot_init()

    def initialize(self) :
        self.arrDf = self.originalDf.copy()

    def _ascending_compare(self, a, b) :
        #self.plot_update()
        return a < b

    def _descending_compare(self, a, b) :
        #self.plot_update()
        return a > b

    def plot_init(self) :
        x = self.arrDf.index.values.tolist()
        y = [i[0] for i in self.arrDf.values.tolist()]
        if self.rects == None :
            self.fig = plt.figure(figsize=(24, 8))
            self.rects = plt.bar(x, y)
            plt.show(block=False)

    def plot_update(self, idx_list) :
        y = [self.arrDf.values[i][0] for i in idx_list]
        rects = [self.rects[i] for i in idx_list]
        for rect, height in zip(rects, y) :
            rect.set_height(height)
        self.fig.canvas.update()
        plt.pause(0.000001)

    def swap(self, a_idx, b_idx) :
        if a_idx == b_idx :
            return
        t_a = self.arrDf.iloc[a_idx].values[0]
        self.arrDf.iloc[a_idx] = self.arrDf.iloc[b_idx].values[0]
        self.arrDf.iloc[b_idx] = t_a
        self.plot_update([a_idx, b_idx])

class MergeSort(Sort) :

    def sort(self) :
        self._topDownMerge(0, len(self.arrDf.index.values))

    def _topDownMerge(self, start, end) :
        if end-start < 2 :
            return
        else :
            df = self.arrDf
            divider = (end-start+1)//2
            self._topDownMerge(start, start+divider)
            self._topDownMerge(start+divider, end)
            self._merge(start, start+divider, end)
            print(start, end)

    def _merge(self, start, mid, end) :
        df = self.arrDf
        tdf = self.arrDf.copy()

        a_idx = start
        b_idx = mid
        for idx in range(start, end) :
            if (not b_idx < end) or ((a_idx < mid) and self.compare(tdf.iloc[a_idx].values[0], tdf.iloc[b_idx].values[0])) :
                df.iloc[idx] = tdf.iloc[a_idx].values[0]
                a_idx += 1
            else :
                df.iloc[idx] = tdf.iloc[b_idx].values[0]
                b_idx += 1
            self.plot_update([idx])

class FuckingSlowSort(Sort) :

    def sort(self) :
        idx = 0
        size = len(self.arrDf)
        while idx+1 != size :
            t_a = self.arrDf.iloc[idx].values[0]
            t_b = self.arrDf.iloc[idx+1].values[0]
            if not self.compare(t_a, t_b) :
                self.swap(idx, idx+1)
                idx = 0
                continue
            idx += 1


class QuickSort(Sort) :

    def sort(self) :
        self._topDownQuickSort(0, len(self.arrDf.index.values))

    def _topDownQuickSort(self, start, end) :
        if end-start < 2 :
            return
        else :
            pivot_idx = end-1
            pivot_val = self.arrDf.iloc[pivot_idx].values[0]
            leftmost_idx = start
            rightmost_idx = end - 2
            while True :
                leftmost_val = self.arrDf.iloc[leftmost_idx].values[0]
                rightmost_val = self.arrDf.iloc[rightmost_idx].values[0]
                while self.compare(leftmost_val, pivot_val) :
                    leftmost_idx += 1
                    leftmost_val = self.arrDf.iloc[leftmost_idx].values[0]
                while self.compare(pivot_val, rightmost_val) and leftmost_idx < rightmost_idx:
                    rightmost_idx -= 1
                    rightmost_val = self.arrDf.iloc[rightmost_idx].values[0]
                if leftmost_idx < rightmost_idx :
                    self.swap(leftmost_idx, rightmost_idx)
                    leftmost_idx += 1
                    rightmost_idx -= 1
                    continue
                else :
                    break
            self.swap(leftmost_idx, pivot_idx)
            self._topDownQuickSort(start, leftmost_idx)
            self._topDownQuickSort(leftmost_idx+1, end)

class RadixSort(Sort) :

    def __init__(self, rangeToSort=range(1000), desc=False, base=10) :
        super(RadixSort, self).__init__(rangeToSort, desc)
        self.base = base


    def sort(self) :
        maximum_exponent = self.getMaximumExponent()
        self._radixSort(0, len(self.arrDf.index.values), maximum_exponent, current_exponent=0)

    def getMaximumExponent(self) :
        max_val = max([i[0] for i in self.arrDf.values.tolist()])
        exponent = 0
        while not max_val//(self.base**exponent) < 10 :
            exponent += 1
        return exponent


    def _radixSort(self, start, end, maximum_exponent, current_exponent) :
        base = self.base
        divider = base**current_exponent
        if current_exponent > maximum_exponent :
            return
        else :
            countList = [0]*base
            tmpList = [0]*(end-start)
            for i in range(len(tmpList)) :
                remainder = (self.arrDf.iloc[start+i].values[0] // divider) % base
                print(remainder)
                countList[remainder] += 1

            for i in range(1, base) :
                countList[i] = countList[i] + countList[i-1];

            for idx in range(end-start-1, -1, -1) :
                remainder = (self.arrDf.iloc[start+idx].values[0] // divider) % base
                tmpList[countList[remainder]-1] = self.arrDf.iloc[start+idx].values[0]
                countList[remainder] -= 1
                idx -= 1

            for i in range(len(tmpList)) :
                self.arrDf.iloc[start+i] = tmpList[i]
                self.plot_update([i])

            self._radixSort(start, end, maximum_exponent, current_exponent+1)


class HeapSort(Sort) :

    def __init__(self, rangeToSort=range(1000), desc=False) :
        super(HeapSort, self).__init__(rangeToSort, desc)
        self.heapLength = len(self.arrDf.index)

    def sort(self) :
        self.build_heap()
        for idx in range(len(self.arrDf.index)-1, -1, -1) :
            self.arrDf.iloc[idx] = self.pop()
            self.plot_update([idx])

    def build_heap(self) :
        start_idx = self.get_parent_index(self.heapLength-1)
        end_idx = -1
        for node_idx in range(start_idx, end_idx, -1) :
            self.heapify(node_idx)

    def isOutOfSize(self, node_idx) :
        return node_idx >= self.heapLength or node_idx < 0

    def heapify(self, node_idx) :
        print("heapify : " + str(node_idx))
        #parent_index = self.get_parent_index(node_idx)
        left_child_index = self.get_left_child_index(node_idx)
        right_child_index = self.get_right_child_index(node_idx)

        if self.isOutOfSize(left_child_index) or self.isOutOfSize(node_idx) :
            return
        else :
            node_val = self.get_value_with_node_idx(node_idx)
            left_child_val = self.get_value_with_node_idx(left_child_index)

            if self.isOutOfSize(right_child_index) :
                if self.compare(left_child_val, node_val) :
                    return
                else :
                    self.swap(left_child_index, node_idx)
                    self.heapify(left_child_index)
            else :
                right_child_val = self.get_value_with_node_idx(right_child_index)

                if self.compare(left_child_val, node_val) and self.compare(right_child_val, node_val) :
                    return
                else :
                    if self.compare(left_child_val, right_child_val) :
                        self.swap(right_child_index, node_idx)
                        self.heapify(right_child_index)
                    else :
                        self.swap(left_child_index, node_idx)
                        self.heapify(left_child_index)


    def push(self, value) :
        self.arrDf.iloc[self.heapLength][0] = -1
        self.increaseKey(self.heapLength, value)
        self.heapLength += 1

    def increaseKey(self, index, key) :
        if self.heapLength == 0 :
            return
        elif self.get_value_with_node_idx(index) > key :
            return
        else :
            self.arrDf.iloc[index][0] = key
            while( (not isOutOfSize(index))
                    and (not self.compare(
                        self.get_value_with_node_idx(index),
                        self.get_value_with_node_idx(self.get_parent_index(index))))) :
                self.swap(index, self.get_parent_index(index))
                index = self.get_parent_index(index)

    def pop(self) :
        retToVal = self.get_value_with_node_idx(0)
        self.arrDf.iloc[0][0] = self.arrDf.iloc[self.heapLength-1][0]
        self.heapify(0)
        self.heapLength -= 1
        return retToVal

    def get_left_child_index(self, idx) :
        return (idx+1)*2-1

    def get_right_child_index(self, idx) :
        return (idx+1)*2

    def get_parent_index(self, idx) :
        return (idx+1)//2-1

    def get_value_with_node_idx(self, node_idx) :
        print(node_idx, self.arrDf.values[node_idx][0])
        return self.arrDf.values[node_idx][0]



if __name__ == "__main__" :
    sys.setrecursionlimit(100000)
    #sorter = RadixSort(range(300), desc=False, base=10)
    #sorter = MergeSort(range(300), desc=False)
    #sorter = QuickSort(range(300), desc=False)
    sorter = HeapSort(range(300), desc=False)
    sorter.sort()
