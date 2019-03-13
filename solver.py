import sys
import random

# Clases removed

def get_random_interpretation(num_vars):
    """Get a random interpretation for all the variables"""
    interpretation = range(1, num_vars+1)

    for i in xrange(num_vars):
        interpretation[i] *= multiplicator() # 50/50 probability to be - or +

    return interpretation

# Tells if the given interpretation satisfies the given formula.
# If the formula is not safisfied it returns the first unsatisfied clause.
def satisfies(interpretation, formula):
    for clause in formula:
        clause_length = len(clause)
        for lit in clause:
            if lit == interpretation[abs(lit)-1]: # satisfies clause
                break
            else:
                clause_length -= 1
        if clause_length == 0: # falsified clause
            return False, clause

    return True, []

# Returns the number of unsatisfied clauses of a formula given an interpretation.
def count_unsatisfiable_clauses(interpretation, formula):
    unsatisfied_clauses = 0

    for clause in formula:
        clause_length = len(clause)
        for lit in clause:
            if lit == interpretation[abs(lit)-1]: # satisfies clause
                break
            else:
                clause_length -= 1
        if clause_length == 0: # falsified clause
            unsatisfied_clauses+=1

    return unsatisfied_clauses

# Given an interpretation an a variable of the interpretation, returns a copy of
# the interpretation with the value of the variable changed. 
def get_interpretation_with_changed_variable_sense(interpretation, variable_to_change):
    new_clause = list(interpretation)
    new_clause[abs(variable_to_change)-1] *= -1
    return new_clause



def multiplicator():
    if random.random() < 0.5:
        return 1
    return -1

def flip_a_coin(probability):
    if random.random() < probability:
        return True
    return False



def solve(formula, num_vars, max_flips = 500, rnd_walk = 0.1, max_restarts = 50):
    """
    random_interpretation = RandomInterpretation(num_vars)
    print "Interpretacio random: " + str(random_interpretation.vars)
    print random_interpretation.satisfies(formula)
    """

    for _ in xrange(max_restarts):
        random_interpretation = get_random_interpretation(num_vars)
        for _ in xrange(max_flips):
            is_satifiable, unsatisfied_clause = satisfies(random_interpretation, formula)
            if is_satifiable:
                return random_interpretation

            best_interpretation = None
            least_unsatisfied_clauses = sys.maxint
            for var in unsatisfied_clause:
                current_interpretation = get_interpretation_with_changed_variable_sense(random_interpretation, var)
                current_unsatisfied_clauses = count_unsatisfiable_clauses(current_interpretation, formula)
                if (current_unsatisfied_clauses < least_unsatisfied_clauses):
                    least_unsatisfied_clauses = current_unsatisfied_clauses
                    best_interpretation = current_interpretation

            #print best_interpretation
            #print least_unsatisfied_clauses

            if least_unsatisfied_clauses > 0 and flip_a_coin(rnd_walk):
                random_variable = random.randint(0, len(unsatisfied_clause) - 1)
                random_interpretation = get_interpretation_with_changed_variable_sense(random_interpretation, unsatisfied_clause[random_variable])
            else:
                random_interpretation = best_interpretation

    return "No solution found"


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

	# Solve the problem and get the best solution found
    best_sol = solve(formula, int(num_vars))
    print best_sol
