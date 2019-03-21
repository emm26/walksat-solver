#!/usr/bin/python

import sys
import random

# Clases removed

def get_random_interpretation(num_vars):
    """Get a random interpretation for all the variables"""
    interpretation = range(1, num_vars+1)

    for i in xrange(num_vars):
        interpretation[i] *= multiplicator() # 50/50 probability to be - or +

    return interpretation

# Tells if the modified interpretation satisfies the formula.
# A list with the number of falsified literals in each clause for the
# modified interpretation is needed, and the length of each clause.
# If the formula is not safisfied it returns the first unsatisfied clause.
def satisfies(falsified_lit_counters, len_clauses, formula):
    for index, counter in enumerate(falsified_lit_counters):
        if counter == len_clauses[index]:
            return False, formula[index]

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

# Returns a list with the number of falsified literals in each clause
def get_counters_of_falsified_literals(interpretation, formula):
    counters = []

    for clause in formula:
        #clause_length = len(clause)
        current_falsified_literals = 0
        for lit in clause:
            if lit != interpretation[abs(lit)-1]: # falsified literal
                current_falsified_literals += 1

        counters.append(current_falsified_literals)

    return counters

# Caution! the given 'flipped_var' must have the sign that will have in the new interpretation, not the previous one!
# Example: if variable '4' must be flipped to '-4', the given 'flipped_var' parameter must be '-4', not '4' !
def update_falsified_lit_counters_changing_variable_sense(falsified_lit_counters, flipped_var):
    global positive_locs, negative_locs

    #print "Locations pos: ", positive_locs
    #print "Locations neg: ", negative_locs
    variable_position = abs(flipped_var) -1

    if flipped_var > 0:
        for idx in positive_locs[variable_position]: # variable becomes positive, -1 falsified literals
            falsified_lit_counters[idx] -= 1
        for idx in negative_locs[variable_position]: # variable becomes positive, +1 falsified literals
            falsified_lit_counters[idx] += 1
    else:
        for idx in positive_locs[variable_position]: # variable becomes negative, +1 falsified literals
            falsified_lit_counters[idx] += 1
        for idx in negative_locs[variable_position]: # variable becomes negative, -1 falsified literals
            falsified_lit_counters[idx] -= 1

def multiplicator():
    if random.random() < 0.5:
        return 1
    return -1

def flip_a_coin(probability):
    if random.random() < probability:
        return True
    return False



def pick_best_interpretation(random_interpretation, unsatisfied_clause, formula): # treure formula, es pot fer sense !!! (global)
    best_interpretation = None
    least_unsatisfied_clauses = sys.maxint
    for var in unsatisfied_clause:
        current_interpretation = get_interpretation_with_changed_variable_sense(random_interpretation, var)
        current_unsatisfied_clauses = count_unsatisfiable_clauses(current_interpretation, formula)
        if (current_unsatisfied_clauses < least_unsatisfied_clauses):
            least_unsatisfied_clauses = current_unsatisfied_clauses
            best_interpretation = current_interpretation
            best_interp_var = var

    return best_interpretation, best_interp_var, least_unsatisfied_clauses


def solve(formula, len_clauses, num_vars, max_flips = 400, rnd_walk = 0.55, max_restarts = sys.maxint):
#def solve(formula, len_clauses, num_vars, max_flips = 15, rnd_walk = 0.95, max_restarts = 1):

    for _ in xrange(max_restarts):
        random_interpretation = get_random_interpretation(num_vars)
        #print random_interpretation
        falsified_lit_counters = get_counters_of_falsified_literals(random_interpretation, formula) # Added. Update the counters every restart.

        for _ in xrange(max_flips):
            #is_satifiable, unsatisfied_clause = satisfies(random_interpretation, formula)
            is_satifiable, unsatisfied_clause = satisfies(falsified_lit_counters, len_clauses, formula)
            if is_satifiable:
                return random_interpretation

            best_interpretation, best_interp_var, least_unsatisfied_clauses = pick_best_interpretation(random_interpretation, unsatisfied_clause, formula)

            if least_unsatisfied_clauses > 0 and flip_a_coin(rnd_walk):
                random_variable = random.randint(0, len(unsatisfied_clause) - 1)
                flipped_var = unsatisfied_clause[random_variable]
                random_interpretation = get_interpretation_with_changed_variable_sense(random_interpretation, flipped_var)
                #print "Variable flipped first: ", flipped_var
                #print "Before: ", falsified_lit_counters
                update_falsified_lit_counters_changing_variable_sense(falsified_lit_counters, flipped_var)
                #print "After: ", falsified_lit_counters
            else:
                random_interpretation = best_interpretation
                #print "Variable flipped: ", best_interp_var
                update_falsified_lit_counters_changing_variable_sense(falsified_lit_counters, best_interp_var)


    print 's UNSATISFIABLE' # No solution found
    return []


# Functions

def get_cnf_formula(file_name):
    formula = []
    len_clauses = []

    instance = open(file_name, "r")
    for l in instance:
		if l[0] in ["c", "p"]: # pass comments and program line
			if l[0] == "p":
				num_vars = l.split()[2]
			continue

		clause = map(int, l.split())
		clause.pop() # Remove last 0
		formula.append(clause)
		len_clauses.append(len(clause))

    return formula, len_clauses, num_vars

def print_solution(interpretation):
    print 's SATISFIABLE'
    print 'v ' + ' '.join(map(str, interpretation[:])) + ' 0'

# Returns a structure in which for every literal, points to the clauses that have that literal in them.
def get_literal_locations_structure(formula, num_vars):
    positive_literals_locations = [[] for _ in xrange(num_vars)]
    negative_literals_locations = [[] for _ in xrange(num_vars)]

    for cl_index, clause in enumerate(formula):
        #print clause, cl_index
        for literal in clause:
            if literal > 0:
                positive_literals_locations[literal-1].append(cl_index)
            else:
                negative_literals_locations[abs(literal)-1].append(cl_index)

    return positive_literals_locations, negative_literals_locations

if __name__ == '__main__' :
    global positive_locs, negative_locs

    if len(sys.argv) < 2:
        print "Usage: " + sys.argv[0] + " <cnf_file_name> "
        sys.exit()

    cnf_file_name = sys.argv[1]
    formula, len_clauses, num_vars = get_cnf_formula(cnf_file_name)
    positive_locs, negative_locs = get_literal_locations_structure(formula, int(num_vars))

    #print "Num_vars: " + num_vars
    #print formula

	# Solve the problem and get the best solution found
    best_sol = solve(formula, len_clauses, int(num_vars))
    if best_sol:
        print_solution(best_sol)
