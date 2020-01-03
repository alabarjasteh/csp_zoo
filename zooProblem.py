# zooProblem.py
#--------------
import util
import zooSearch

class ZooProblem(zooSearch.SearchProblem):

    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables    #[cage1, cage2, ...]
        self.domains = domains        #{cage1:[lion, leopard], ...} domains for each var after imposing unary constraints (size)
        self.neighbours = neighbours  #{cage1: [cage2, cage4], ...}
        self.constraints = constraints #constraints(var, val, var2, val2) returns True if (var, val) is consistent with (var2, val2)

    def assign(self, var, val, assignment):
        assignment[var] = val
        
    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def nConflicts(self, var, val, assignment):
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])
        return util.count([conflict(v) for v in self.neighbours[var]]) + util.count([val is assignment[k] for k in assignment.keys() if var is not k])
    

    def assume(self, var, value):
        """
        assume var=value
        """
        removals = [(var, a) for a in self.domains[var] if a != value]
        self.domains[var] = [value]
        return removals
    
    def restore(self, removals):
        for var, a in removals:
            self.domains[var].append(a)
        
if __name__ == '__main__':

    #read input.txt
    with open("input.txt") as f:
        c = f.readlines()
        c = [x.strip() for x in c]
        print("input:", c)
        nVariables = int(c[0][0])
        nNeighbours = int(c[0][2])
        cageSizes = int(c[1])
        animalSizes = int(c[2])

        domains = {i: [] for i in range(nVariables)}
        [domains[i].append(j) for i in range(nVariables) for j in range(nVariables) if not int(c[1][i]) < int(c[2][j])]
        print("domains:   ",domains)
            

        neighbours = {}
        for i in range(3, nNeighbours + 3):
            cage1 = int(c[i][0]) - 1  #input indices started at 1
            cage2 = int(c[i][1]) - 1  #input indices started at 1
            neighbours[cage1] = []
            neighbours[cage2] = []
        for i in range(3, nNeighbours + 3):
            cage1 = int(c[i][0]) - 1  #input indices started at 1
            cage2 = int(c[i][1]) - 1  #input indices started at 1
            neighbours[cage1].append(cage2)
            neighbours[cage2].append(cage1)
        print("neighbours:",neighbours)

        constraintsMatrix = [[] for _ in range(nNeighbours + 3, nNeighbours + 3 + nVariables)]
        for i in range(nVariables):
            for j in range(nVariables):
                constraintsMatrix[i].append(int(c[i + nNeighbours + 3][j]))
        print("constraintsMatrix:", constraintsMatrix)

        def constraints(var, val, var2, val2):
            if var not in neighbours[var2]:
                return True
            else:
                return constraintsMatrix[val][val2]

        
        # solve the problem
        csp = ZooProblem(list(range(nVariables)) , domains, neighbours, constraints)
        result  = zooSearch.backtrackingSearch(csp)
        print("result", result)
