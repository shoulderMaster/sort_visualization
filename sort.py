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

    def initialize(self) :
        self.arrDf = self.originalDf.copy()

    def _ascending_compare(self, a, b) :
        #self.plot()
        return a < b

    def _descending_compare(self, a, b) :
        #self.plot()
        return a > b

    def plot(self) :
        x = self.arrDf.index.values.tolist()
        y = [i[0] for i in self.arrDf.values.tolist()]
        if self.rects == None :
            self.fig = plt.figure(figsize=(24, 8))
            self.rects = plt.bar(x, y)
            plt.show(block=False)
        else :
            for rect, height in zip(self.rects, y) :
                rect.set_height(height)
            self.fig.canvas.draw()
        plt.pause(0.000001)

    def swap(self, a_idx, b_idx) :
        if a_idx == b_idx :
            return
        self.plot()
        t_a = self.arrDf.iloc[a_idx].values[0]
        self.arrDf.iloc[a_idx] = self.arrDf.iloc[b_idx].values[0]
        self.arrDf.iloc[b_idx] = t_a

class MergeSort(Sort) :

    def sort(self) :
        self._topDownMerge(0, len(self.arrDf.index.values))
        self.plot()

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
        self.plot()

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


if __name__ == "__main__" :
    sys.setrecursionlimit(100000)
    sorter = FuckingSlowSort(range(100), desc=False)
    sorter.sort()
