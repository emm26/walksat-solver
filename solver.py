import sys
import random

# Clases

class RandomInterpretation():
    """An interpretation is an assignment of the possible values to variables"""

    def __init__(self, num_vars):
        self.num_vars = int(num_vars)
        self.vars = None
        self.get_random_interpretation() # al crear l'instancia ja es genera l'interpretacio


    def get_random_interpretation(self):
        """Get a random interpretation for all the variables"""
        self.vars = range(1, self.num_vars+1)

        for i in xrange(self.num_vars):
            self.vars[i] *= multiplicator() # probabilitat 50-50 de ser positiva o negada

    def satisfies(self, formula):
        for clause in formula:
            length = 3 #SEMPRE 3-SAT, MAGIC NUMBER ! (posar llargada clausula)

            for lit in clause:
                if lit == self.vars[abs(lit)-1]: # Satisfies clause:
                    break
                else:
                    length -= 1
            if length == 0: # Falsified clause
                return False

        return True


def multiplicator():
	if random.random() < 0.5:
		return 1
	else:
		return -1

class Solver():
    """docstring for [object Object]."""
    def __init__(self):
        self.probability = 0
        #self.problem = problem
    	#self.best_sol = None
    	#self.best_cost = problem

    def solve(self, formula, num_vars, max_tries = 100, rnd_walk = 0.1, max_restarts = 10):
        random_interpretation = RandomInterpretation(num_vars)
        print "Interpretacio random: " + str(random_interpretation.vars)
        print random_interpretation.satisfies(formula)

# Funcions

def get_cnf_formula(file_name):
    formula = []

    instance = open(file_name, "r")
    for l in instance:
		if l[0] in ["c", "p"]: # Pass comments and program line
			if l[0] == "p":
				num_vars = l.split()[2]
			continue

		clause = map(int, l.split())
		clause.pop() # Remove last 0
		formula.append(clause)


    return formula, num_vars


if __name__ == '__main__' :
    if len(sys.argv) < 2:
        print "Usage: " + sys.argv[0] + " <cnf_file_name> "
        sys.exit()

    cnf_file_name = sys.argv[1]
    formula, num_vars = get_cnf_formula(cnf_file_name)
    #print "Num_vars: " + num_vars
    #print formula

	# Create a solver instance with the problem to solve
    solver = Solver()
	# Solve the problem and get the best solution found
    best_sol = solver.solve(formula, num_vars)
