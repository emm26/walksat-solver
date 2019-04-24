#!/usr/bin/python

"""
Please notice the following SAT solver's goal is not to follow correct programming standards
but to be fast. Quickness has been picked over good programming practices.
Many decisions have been taken avoiding good programming practices in order to achieve
a quick solver (such as deleting classes). Again, do not take the following approach as an
example of good coding standards and practices.
Fasten your seat belts
"""

import sys
import random


def get_random_interpretation(num_vars):
    """
    Gets random interpretation for formula by assigning 
    true or false sense to all the variables.
    """
    interpretation = range(1, num_vars + 1)

    for i in xrange(num_vars):
        interpretation[i] *= multiplicator()  # 50/50 probability to be - or +

    return interpretation


def satisfies(falsified_lit_counters, len_clauses, formula):
    """
    Reveals whether the modified interpretation satisfies the formula.
    A list with the number of falsified literals in each clause for the
    modified interpretation is needed, and the length of each clause.
    :return: true and empty list if the interpretation satisfies the formula, 
    false and the first unsatisfied clause if not.
    """
    for index, counter in enumerate(falsified_lit_counters):
        if counter == len_clauses[index]:
            return False, formula[index]

    return True, []


def get_interpretation_with_changed_variable_sense(interpretation, variable_to_change):
    """
    Given an interpretation and a variable of the interpretation, returns a copy of
    the interpretation with the value of the given variable changed.
    """
    new_clause = list(interpretation)
    new_clause[abs(variable_to_change) - 1] *= -1
    return new_clause


def get_counters_of_falsified_literals(interpretation, formula):
    """
    Returns a list with the number of falsified literals in each clause.
    """
    counters = []

    for clause in formula:
        # clause_length = len(clause)
        current_falsified_literals = 0
        for lit in clause:
            if lit != interpretation[abs(lit) - 1]:  # falsified literal
                current_falsified_literals += 1

        counters.append(current_falsified_literals)

    return counters


# Caution! the given 'flipped_var' must have the sign that will have in the new interpretation,
# not the previous one!
# Example: if variable '4' must be flipped to '-4', the given 'flipped_var' parameter
# must be '-4', not '4' !
def update_falsified_lit_counters_changing_variable_sense(falsified_lit_counters, flipped_var):
    global positive_locs, negative_locs

    variable_position = abs(flipped_var) - 1

    if flipped_var > 0:
        for idx in positive_locs[variable_position]:  # variable becomes positive, -1 falsified literals
            falsified_lit_counters[idx] -= 1
        for idx in negative_locs[variable_position]:  # variable becomes positive, +1 falsified literals
            falsified_lit_counters[idx] += 1
    else:
        for idx in positive_locs[variable_position]:  # variable becomes negative, +1 falsified literals
            falsified_lit_counters[idx] += 1
        for idx in negative_locs[variable_position]:  # variable becomes negative, -1 falsified literals
            falsified_lit_counters[idx] -= 1


def count_unsatisfiable_clauses_after_flipping_var(falsified_lit_counters, var):
    new_counters = falsified_lit_counters[:]  # The original counters must not be modified
    # ----- ----- ----- ----- ----- ----- -----
    variable_position = abs(var) - 1

    if var > 0:
        for idx in positive_locs[variable_position]:  # variable becomes positive, -1 falsified literals
            new_counters[idx] -= 1
        for idx in negative_locs[variable_position]:  # variable becomes positive, +1 falsified literals
            new_counters[idx] += 1
    else:
        for idx in positive_locs[variable_position]:  # variable becomes negative, +1 falsified literals
            new_counters[idx] += 1
        for idx in negative_locs[variable_position]:  # variable becomes negative, -1 falsified literals
            new_counters[idx] -= 1
    # ----- ----- ----- ----- ----- ----- -----

    unsatisfied_clauses = 0

    for index, counter in enumerate(new_counters):
        if counter == len(formula[index]):
            unsatisfied_clauses += 1

    return unsatisfied_clauses


def multiplicator():
    if random.random() < 0.5:
        return 1
    return -1


def flip_a_coin(probability):
    if random.random() < probability:
        return True
    return False


def pick_best_interpretation(falsified_lit_counters, unsatisfied_clause):
    least_unsatisfied_clauses = sys.maxint
    for var in unsatisfied_clause:
        current_unsatisfied_clauses = count_unsatisfiable_clauses_after_flipping_var(falsified_lit_counters, int(var) * -1)
        if current_unsatisfied_clauses < least_unsatisfied_clauses:
            least_unsatisfied_clauses = current_unsatisfied_clauses
            best_interpretation_var = var

    return best_interpretation_var, least_unsatisfied_clauses


def rnovelty(variables, break_count, most_recently_flipped_var):
    """
    Applies Rnovelty heuristic
    :param variables: list of variables in an unsatisfied clause
    :param break_count: list of the number of broken clauses if changing
    the sense of the each variable in variables list.
    NOTICE: each element of break_count is mapped to an element in variables
    at the same position in both lists
    :param most_recently_flipped_var: variable last flipped (changed sense)
    :return: the new variable to flip computed by the Rnovelty heuristic
    """

    # compute the variables that have the least break count
    # without considering the most recently flipped variable
    least_break = sys.maxint
    least_break_variables = []
    is_most_recently_flipped_var_in_clause = False

    for i in range(0, len(break_count)):
        if variables[i] == most_recently_flipped_var:  # ignore it
            is_most_recently_flipped_var_in_clause = True
            recently_flipped_pos_in_clause = i
            continue
        elif break_count[i] < least_break:
            least_break = break_count[i]
            least_break_variables = [variables[i]]
        elif break_count[i] == least_break:
            least_break_variables.append(variables[i])

    if is_most_recently_flipped_var_in_clause and least_break - break_count[recently_flipped_pos_in_clause] > 1:
        return variables[recently_flipped_pos_in_clause], break_count[recently_flipped_pos_in_clause]
    else:  # otherwise, pick at random one of the least_break_variables
        return least_break_variables[random.randint(0, len(least_break_variables) - 1)], least_break


def solve(formula, len_clauses, num_vars, max_flips=4000, rnd_walk=0.55, max_restarts=sys.maxint):
    for _ in xrange(max_restarts):
        most_recently_flipped_var = None
        random_interpretation = get_random_interpretation(num_vars)
        # update the counters every restart
        falsified_lit_counters = get_counters_of_falsified_literals(random_interpretation, formula)

        for x in xrange(max_flips):
            is_satisfiable, unsatisfied_clause = satisfies(falsified_lit_counters, len_clauses, formula)
            if is_satisfiable:
                return random_interpretation

            if x % 120 != 0:  # r-novelty
                break_count = []
                for var in unsatisfied_clause:
                    current_num_of_unsatisfied_clauses = count_unsatisfiable_clauses_after_flipping_var(
                        falsified_lit_counters, var)
                    break_count.append(current_num_of_unsatisfied_clauses)

                to_flip_var, num_unsatisfied_clauses_next_flip = rnovelty(unsatisfied_clause, break_count,
                                                                          most_recently_flipped_var)
                best_interpretation = get_interpretation_with_changed_variable_sense(random_interpretation,
                                                                                     to_flip_var)
                most_recently_flipped_var = to_flip_var
                num_unsatisfied_clauses_last_flip = num_unsatisfied_clauses_next_flip
            else:  # inject a pure random walk flip 
                random_variable_index = random.randint(0, len(unsatisfied_clause) - 1)
                to_flip_var = unsatisfied_clause[random_variable_index]
                random_interpretation = get_interpretation_with_changed_variable_sense(random_interpretation,
                                                                                       to_flip_var)
                most_recently_flipped_var = to_flip_var
                update_falsified_lit_counters_changing_variable_sense(falsified_lit_counters, to_flip_var)
                continue

            if num_unsatisfied_clauses_last_flip > 0 and flip_a_coin(rnd_walk):
                random_variable_index = random.randint(0, len(unsatisfied_clause) - 1)
                to_flip_var = unsatisfied_clause[random_variable_index]
                random_interpretation = get_interpretation_with_changed_variable_sense(random_interpretation, to_flip_var)
                most_recently_flipped_var = to_flip_var
                update_falsified_lit_counters_changing_variable_sense(falsified_lit_counters, to_flip_var)
            else:
                random_interpretation = best_interpretation
                update_falsified_lit_counters_changing_variable_sense(falsified_lit_counters, to_flip_var)

    print("s UNSATISFIABLE")  # no solution found
    return []


def get_cnf_formula(file_name):
    formula = []
    len_clauses = []

    instance = open(file_name, "r")
    for l in instance:
        if l[0] in ["c", "p"]:  # pass comments and program line
            if l[0] == "p":
                num_vars = l.split()[2]
            continue

        clause = map(int, l.split())
        clause.pop()  # Remove last 0
        formula.append(clause)
        len_clauses.append(len(clause))

    return formula, len_clauses, num_vars


def print_solution(interpretation):
    print("s SATISFIABLE")
    print("v " + ' '.join(map(str, interpretation[:])) + " 0")


def get_literal_locations_structure(formula, num_vars):
    """
    :return: a structure in which for every literal, points to the clauses
    that have that literal in them.
    """
    positive_literals_locations = [[] for _ in xrange(num_vars)]
    negative_literals_locations = [[] for _ in xrange(num_vars)]

    for cl_index, clause in enumerate(formula):
        for literal in clause:
            if literal > 0:
                positive_literals_locations[literal - 1].append(cl_index)
            else:
                negative_literals_locations[abs(literal) - 1].append(cl_index)

    return positive_literals_locations, negative_literals_locations


if __name__ == '__main__':
    global positive_locs, negative_locs

    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " <cnf_file_name> ")
        sys.exit()

    cnf_file_name = sys.argv[1]
    formula, len_clauses, num_vars = get_cnf_formula(cnf_file_name)
    positive_locs, negative_locs = get_literal_locations_structure(formula, int(num_vars))

    # print("Formula about to be solved:")
    # print(formula)

    best_sol = solve(formula, len_clauses, int(num_vars), 35 * (int(num_vars)))
    if best_sol:
        print_solution(best_sol)
