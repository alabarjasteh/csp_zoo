# zooSearch.py
##############

import heapq


class SearchProblem:
    def assignVariable(self, var, value):
    def unassignVariable(self, var):
    def isConsistent(self, lastAssignment): 
    def isComplete(self, assignments):
    def isFailed(self): #empty domain
        


def backtrackingSearch(csp):
    return _recursiveBacktracking(csp, minimumRemainingVariable, leastConstrainingValue)

def _recursiveBacktracking(csp, variableSelectionFuction, valueOrderingFuction):
    if csp.isComplete():
        return csp.domains
    var = variableSelectionFuction(csp)
    if var == None:
        print('None var')
    orderedValues = valueOrderingFuction(var, csp)
    for value in orderedValues:
        # if csp.isConsistent(var, value): # valueOrderingFuction just returns consistent values
            csp.assignVariable(var, value)
            result = _recursiveBacktracking(csp, variableSelectionFuction, valueOrderingFuction)
            if not csp.isFailed():
                return result
            csp.unassignVariable(var)
    return {}


def minimumRemainingVariable(csp):
    min = 1000 #a reletively big number
    minVar = None
    for var in csp.variables:
        if not csp.isAssigned[var]:
            remainingDomainSize = len(csp.domains[var])
            if remainingDomainSize < min:
                min = remainingDomainSize
                minVars = var
    return minVar
    
def trivialVariableChoose(csp):
    return first([var for var in csp.variables if not csp.isAssigned[var]])

def leastConstrainingValue(var, csp):
    pq = PriorityQueue()
    domainsLenSum_beforValueAssignment = sum([len(domain) for domain in csp.domains.values()])
    orderedValues = []
    values = csp.domains[var]
    for val in values:
        if csp.isConsistent(var, val):
            csp.assignVariable(var, val)
            domainsLenSum = sum([len(domain) for domain in csp.domains.values()])
            newConstraintsCaused = domainsLenSum_beforValueAssignment - domainsLenSum
            pq.push(val, newConstraintsCaused)
            csp.unassignVariable(var)
    while not pq.isEmpty():
        orderedValues.append(pq.pop())
    return orderedValues


def trivialValueOrdering(var, csp):
    return [val for val in csp.domains[var] if csp.isConsistent(val)]

############ utilities #########

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)