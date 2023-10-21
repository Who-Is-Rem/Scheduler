"""
In order to keep track of customer widgets and 
know whether or not they overlap
"""

class Graph():
    def __init__(self):
        self.graph = {}

    def occupy(self, col, row, rowspan):
        if col not in self.graph.keys():
            self.graph[col] = list(range(row, row+rowspan))
        else:
            try:
                for r in range(row, row+rowspan):
                    assert r not in self.graph[col]
                self.graph[col].extend(list(range(row, row+rowspan)))
            except:
                raise GraphException
    
    def remove(self, col, row, rowspan):
        try:
            assert col in self.graph.keys()
            for i in range(row, row+rowspan):
                assert i in self.graph[col]
            for i in range(row, row+rowspan):
                self.graph[col].remove(i)
            if self.graph[col] == []:
                self.graph.__delitem__(col)
        except:
            raise GraphException

class GraphException(Exception):
    pass
