import copy
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class myNode:
    def __init__(self, x, y, _id):
        self.x = x
        self.y = y
        self.id = _id
        self.label = _id.upper()
        self.next = []
        
    def plot(self, ax):
        ax.text(self.x, self.y, self.label, transform=ax.transAxes, fontsize=18, bbox=dict(boxstyle='circle', facecolor='wheat', alpha=1))
        
    def add_child(self, x):
        self.next.append(x)
        
    def remove_child(self, x):
        self.next.remove(x)


class Net:
    def __init__(self, arrays:list):
        self.nodes = dict()
        self.arrays = copy.deepcopy(arrays)
        self.xdim = len(arrays) + 1
        self.ydim = np.zeros(self.xdim, dtype=np.int64)
        self.pivot = pd.DataFrame(columns=['source', 'target', 'linked'], dtype=('str', np.int64))
        for i, array in enumerate(arrays):
            if i:
                try:
                    np.dot(arrays[i-1].values, array.values)
                except:
                    raise ValueError("The dimentions of the matrices %d and %d don't match each other" % (i, i+1))
            self.ydim[i] = array.shape[0]
            self.pivot = pd.concat([self.pivot, array.reset_index().melt(id_vars='source', var_name='target', value_name='linked')])
        self.ydim[i+1] = array.shape[1]
        max_y = 0
        for i in range(self.xdim):
            max_y = max(max_y, self.ydim[i])
        odd = bool(max_y % 2)
        self.pivot = self.pivot.loc[self.pivot['linked']==1, ['source', 'target']].set_index('source')
        self.x_coord = np.linspace(0.05, 0.95, self.xdim)
        self.y_coords = []
        for x in range(self.xdim):
            if odd == bool(self.ydim[x] % 2):
                self.y_coords.append(np.linspace(0.1, 0.9, self.ydim[x]))
            else:
                self.y_coords.append(np.linspace(0.1, 0.9, self.ydim[x] * 2 + 1)[1::2])
            for y in range(self.ydim[x]):
                _id = string.ascii_lowercase[x] + str(y+1)
                self.nodes[_id] = myNode(self.x_coord[x], self.y_coords[x][y], _id)
        for row in range(self.pivot.shape[0]):
            self.nodes[self.pivot.index[row]].next.append(self.nodes[self.pivot.iloc[row]['target']])
            
                
    def plot(self):
        self.fig, self.ax = plt.subplots()
        for i in self.nodes: 
            self.nodes[i].plot(self.ax)
            for nextNode in self.nodes[i].next:
                self.ax.plot([self.nodes[i].x, nextNode.x], [self.nodes[i].y, nextNode.y], 'k-', lw=2, transform=self.ax.transAxes)
        plt.axis('off')
        plt.show()