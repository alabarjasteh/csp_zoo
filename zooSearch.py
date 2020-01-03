# zooSearch.py
#-------------
import util
import heapq


class SearchProblem:
    def assign(self, var, val, assignment):
        """
        assign {var: val} to assignment
        """
    def unassign(self, var, assignment):
        """
        unassign a variable form assinment
        """
        
    def nConflicts(self, var, val, assignment):
        """
        number of conflics
        """

    def assume(self, var, value):
        """
        assume var=value
        """
    
    def restore(self, removals):
        """
        retore the assumption of val=var
        """    

def backtrackingSearch(csp):
    return _recursiveBacktracking({}, csp, mrv, lcv, mac)

def _recursiveBacktracking(assignment, csp, variableSelectionFuction, valueOrderingFuction, inference):
    if len(assignment) == len(csp.variables):
        return assignment
    var = variableSelectionFuction(assignment, csp)
    for val in valueOrderingFuction(var, assignment, csp):
        if csp.nConflicts(var, val, assignment) == 0:
            csp.assign(var, val, assignment)
            removals = csp.assume(var, val)
            if inference(csp, var, val, assignment, removals):
                result = _recursiveBacktracking(assignment, csp, variableSelectionFuction, valueOrderingFuction, inference)
                if result is not None:
                    return result
            csp.restore(removals)
    csp.unassign(var, assignment)
    return None

    
# AC3

def AC3(csp):
    queue = util.Queue()
    if queue.isEmpty():
        [queue.push((Xi, Xj)) for Xi in csp.variables for Xj in csp.neighbours[Xi]]
    while not queue.isEmpty():
        Xi, Xj = queue.pop()
        if revise(csp, Xi, Xj):
            if not csp.domains[Xi]:
                return False
            for Xk in csp.neighbours[Xi]:
                if Xk is Xj:
                    continue
                queue.push((Xk, Xi))
    return True

def revise(csp, Xi, Xj):
    revised = False
    for x in csp.domains[Xi]:
        for y in csp.domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                break
        if not csp.constraints(Xi, x, Xj, y):
            csp.domains[Xi].remove(x)
            revised = True
    return revised



# variable ordering 

def firstUnassignedVariable(assignment, csp):
    """
    A trivial heuristic to return first variable which is not assigned yet
    """
    return util.first([var for var in csp.variables if var not in assignment])

def mrv(assignment, csp):
    """Minimum-remaining-values heuristic."""
    return util.argmin_random_tie([v for v in csp.variables if v not in assignment],
                             key=lambda var: num_legal_values(csp, var, assignment))

def num_legal_values(csp, var, assignment):
    return util.count(csp.nConflicts(var, val, assignment) == 0 for val in csp.domains[var])


# value ordering

def lcv(var, assignment, csp):
    """Least-constraining-values heuristic."""
    if not csp.domains[var]:
        return []
    else:
        return sorted(csp.domains[var], key=lambda val: csp.nConflicts(var, val, assignment))


def trivialValueOrdering(var, assignment, csp):
    return csp.domains[var]



# inferences

def trivialInference(csp, var, value, assignment, removals):
    return True


def forwardChecking(csp, var, value, assignment, removals):
    """Prune neighbour values inconsistent with var=value."""
    for nbr in csp.neighbours[var]:
        if nbr not in assignment:
            for nbrVal in csp.domains[nbr]:
                if not csp.constraints(var, value, nbr, nbrVal):
                    csp.domains[nbr].remove(nbrVal)
            if not csp.domains[nbr]:
                return False
    return True

def mac(csp, var, value, assignment, removals, constraint_propagation=AC3):
    """Maintain arc consistency."""
    return constraint_propagation(csp)

