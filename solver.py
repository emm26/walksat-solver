import sys
import random

# Clases

class RandomInterpretation():
    """An interpretation is an assignment of the possible values to variables"""

    def __init__(self, num_vars):
        self.num_vars = int(num_vars)
        self.vars = None
        self.get_random_interpretation() # generate a random interp. when creating the instance 

    def get_random_interpretation(self):
        """Get a random interpretation for all the variables"""
        self.vars = range(1, self.num_vars+1)

        for i in xrange(self.num_vars):
            self.vars[i] *= multiplicator() # 50/50 probability to be - or +

    def satisfies(self, formula):
        for clause in formula:
            clause_length = len(clause)
            for lit in clause:
                if lit == self.vars[abs(lit)-1]: # satisfies clause
                    break
                else:
                    length -= 1
            if length == 0: # falsified clause
                return False, clause

        return True, []

    def get_interpretation_with_changed_variable_sense(variable_to_change):
        new_clause = list(self.vars)
        new_clause[abs(variable_to_change)-1] *= -1
        return new_clause

    @staticmethod
    def count_unsatisfiable_clauses(interpretation, formula):
        unsatisfied_clauses = 0

        for clause in formula:
            clause_length = len(clause)
            for lit in clause:
                if lit == self.vars[abs(lit)-1]: # satisfies clause
                    break
                else:
                    length -= 1
            if length == 0: # falsified clause
                unsatisfied_clauses++

        return unsatisfied_clauses


def multiplicator():
	if random.random() < 0.5:
		return 1
    return -1

def flip_a_coin(probability):
    if random.random() < probability:
        return True
    return False

class Solver():
    """docstring for [object Object]."""
    def __init__(self):
        self.probability = 0
        #self.problem = problem
    	#self.best_sol = None
    	#self.best_cost = problem

    def solve(self, formula, num_vars, max_flips = 100, rnd_walk = 0.1, max_restarts = 10):
        """
        random_interpretation = RandomInterpretation(num_vars)
        print "Interpretacio random: " + str(random_interpretation.vars)
        print random_interpretation.satisfies(formula) 
        """

        for i in xrange(max_restarts):
            random_interpretation = RandomInterpretation(num_vars)
            for j in xrange(max_flips):
                is_satifiable, unsatisfied_clause = random_interpretation.satisfies(formula)
                if is_satifiable:
                    return random_interpretation

                best_interpretation = None
                least_unsatisified_clauses = sys.maxint
                for var in unsatisfied_clause:
                    current_interpretation = random_interpretation.get_interpretation_with_changed_variable_sense(var)
                    current_unsatisified_clauses = count_unsatisfiable_clauses(new_interpretation, formula)
                    if (current_unsatisified_clauses < least_unsatisified_clauses):
                        least_unsatisified_clauses = current_unsatisified_clauses
                        best_interpretation = current_interpretation
                if least_unsatisified_clauses > 0 and flip_a_coin(rnd_walk):
                    random_variable = random.randint(0, len(unsatisfied_clause) - 1)
                    random_interpretation = random_interpretation.get_interpretation_with_changed_variable_sense(unsatisfied_clause[random_variable])
                


# Functions

def get_cnf_formula(file_name):
    formula = []

    instance = open(file_name, "r")
    for l in instance:
		if l[0] in ["c", "p"]: # pass comments and program line
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
