# zooProblem.py
########

import zooSearch

class ZooProblem(zooSearch.SearchProblem):

    def __init__(self, animals, cages, neighbours):
        self.variables = animals    #[lion, ...]
        self.domains = cages        #{lion:[1, 4], ...} domains for each var after imposing unary constraints
        self.neighbours = neighbours #{lion: [leopard, pig], ...}
        self.isAssigned = [False for variable in self.variables] #{lion: True, leopard: False, ...}


    def assignVariable(self, var, value):
        self.domains[var] = value
        self.isAssigned[var] = True

        
    def unassignVariable(self, var):

    def isConsistent(self, lastAssignment):
        ####### Unary Constraints #########
        # lastAssignment: tuple(animal, cage)
        animal = lastAssignment[0]
        cage = lastAssignment[1]
        #check if cage size is ok for that animal
        animalSize = self.animalsSizes[animal]
        cageSize = self.cagesSizes[cage]
        if animalSize > cageSize:
            return False

        ####### Binary Constraints #########

        return True

    def isComplete(self, assignments):
        return all(self.isAssigned)


    def isFailed(self): #empty domain
        




if __name__ == '__main__':
    # instanciate ZooProblem
    # csp = ZooProblem