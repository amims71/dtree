import json

import pandas as pd
import math
import copy

dataset = pd.read_csv('tennis.csv')
# dataset = pd.read_csv('tennis1.csv')
X = dataset.iloc[:, 1:].values
rownumber = len(X)
colnumber = len(X[0]) - 1
attribute = ['outlook', 'temp', 'humidity', 'wind']


class Node(object):
    def __init__(self):
        self.value = None
        self.decision = None
        self.childs = None

    def findEntropy(self, data, rows):
        yes = 0
        no = 0
        ans = -1
        idx = len(data[0]) - 1
        entropy = 0
        for i in rows:
            if data[i][idx] == 'Yes':
                yes = yes + 1
            else:
                no = no + 1

        x = yes / (yes + no)
        y = no / (yes + no)
        if x != 0 and y != 0:
            entropy = -1 * (x * math.log2(x) + y * math.log2(y))
        if x == 1:
            ans = 1
        if y == 1:
            ans = 0
        return entropy, ans

    def findMaxGain(self, data, rows, columns):
        maxGain = 0
        retidx = -1
        entropy, ans = self.findEntropy(data, rows)
        if entropy == 0:
            return maxGain, retidx, ans

        for idx in columns:
            mydict = {}
            for i in rows:
                key = data[i][idx]
                if key not in mydict:
                    mydict[key] = 1
                else:
                    mydict[key] = mydict[key] + 1
            gain = entropy

            # print(mydict)
            for key in mydict:
                yes = 0
                no = 0
                for k in rows:
                    if data[k][idx] == key:
                        if data[k][-1] == 'Yes':
                            yes = yes + 1
                        else:
                            no = no + 1
                # print(yes, no)
                x = yes / (yes + no)
                y = no / (yes + no)
                # print(x, y)
                if x != 0 and y != 0:
                    gain += (mydict[key] * (x * math.log2(x) + y * math.log2(y))) / rownumber
            # print(gain)
            if gain > maxGain:
                # print("hello")
                maxGain = gain
                retidx = idx

        return maxGain, retidx, ans

    def buildTree(self, data, rows, columns):

        maxGain, idx, ans = self.findMaxGain(X, rows, columns)
        root = Node()
        root.childs = []

        if maxGain == 0:
            if ans == 1:
                root.value = '(Class) = Yes'
            else:
                root.value = '(Class) = No'
            return root

        root.value = attribute[idx]
        mydict = {}
        for i in rows:
            key = data[i][idx]
            if key not in mydict:
                mydict[key] = 1
            else:
                mydict[key] += 1

        newcolumns = copy.deepcopy(columns)
        newcolumns.remove(idx)
        for key in mydict:
            newrows = []
            for i in rows:
                if data[i][idx] == key:
                    newrows.append(i)
            # print(newrows)
            temp = self.buildTree(data, newrows, newcolumns)
            temp.decision = key
            root.childs.append(temp)
        return root

    def traverse(self, root):
        if "--Start--" in root.decision:
            print(root.decision)
        else:
            print("Decision = " + root.decision)

        print("Node = " + root.value)
        n = len(root.childs)
        if n > 0:
            print("It has", n, "children")
        if n > 0:
            for i in range(0, n):
                self.traverse(root.childs[i])

    def calculate(self):
        rows = [i for i in range(0, rownumber)]
        columns = [i for i in range(0, colnumber)]
        root = self.buildTree(X, rows, columns)
        root.decision = '--Start--'
        self.traverse(root)


dt = Node()
dt.calculate()
