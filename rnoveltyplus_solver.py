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
    """Get a random interpretation for all the variables"""
    interpretation = range(1, num_vars + 1)

    for i in xrange(num_vars):
        interpretation[i] *= multiplicator()  # 50/50 probability to be - or +

    return interpretation


def satisfies(interpretation, formula):
    """ Finds out if the given interpretation satisfies the given formula.
        If the formula is not safisfied it returns the first unsatisfied clause """
    for clause in formula:
        clause_length = len(clause)
        for lit in clause:
            if lit == interpretation[abs(lit) - 1]:  # satisfies clause
                break
            else:
                clause_length -= 1
        if clause_length == 0:  # falsified clause
            return False, clause

    return True, []


def count_unsatisfiable_clauses(interpretation, formula):
    """ Returns the number of unsatisfied clauses of a formula given an interpretation """
    unsatisfied_clauses = 0

    for clause in formula:
        clause_length = len(clause)
        for lit in clause:
            if lit == interpretation[abs(lit) - 1]:  # satisfies clause
                break
            else:
                clause_length -= 1
        if clause_length == 0:  # falsified clause
            unsatisfied_clauses += 1

    return unsatisfied_clauses


def get_interpretation_with_changed_variable_sense(interpretation, variable_to_change):
    """ Given an interpretation an a variable of the interpretation, returns a copy of
        the interpretation with the value of the variable changed """
    new_clause = list(interpretation)
    new_clause[abs(variable_to_change) - 1] *= -1
    return new_clause


def multiplicator():
    if random.random() < 0.5:
        return 1
    return -1


def flip_a_coin(probability):
    if random.random() < probability:
        return True
    return False


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


def solve(formula, num_vars, max_flips=4000, rnd_walk=0.55, max_restarts=sys.maxint):
    for _ in xrange(max_restarts):
        random_interpretation = get_random_interpretation(num_vars)
        most_recently_flipped_var = None

        for x in xrange(max_flips):
            is_satifiable, unsatisfied_clause = satisfies(random_interpretation, formula)
            if is_satifiable:
                return random_interpretation

            if x % 150 != 0: # rnovelty
                break_count = []
                for var in unsatisfied_clause:
                    current_interpretation = get_interpretation_with_changed_variable_sense(random_interpretation, var)
                    current_num_of_unsatisfied_clauses = count_unsatisfiable_clauses(current_interpretation, formula)
                    break_count.append(current_num_of_unsatisfied_clauses)

                to_flip_var, num_unsatisfied_clauses_next_flip = rnovelty(unsatisfied_clause, break_count,
                                                                               most_recently_flipped_var)
                best_interpretation = get_interpretation_with_changed_variable_sense(random_interpretation,
                                                                                     to_flip_var)
                most_recently_flipped_var = to_flip_var
                num_unsatisfied_clauses_last_flip = num_unsatisfied_clauses_next_flip

            else: # inject a pure random walk
                to_flip_var_index = random.randint(0, len(unsatisfied_clause) - 1)
                to_flip_var = unsatisfied_clause[to_flip_var_index]
                random_interpretation = get_interpretation_with_changed_variable_sense(random_interpretation,
                                                                                       to_flip_var)
                current_num_of_unsatisfied_clauses = count_unsatisfiable_clauses(random_interpretation, formula)
                most_recently_flipped_var = to_flip_var # in fact, already flipped variable
                num_unsatisfied_clauses_last_flip = current_num_of_unsatisfied_clauses
                continue


            if num_unsatisfied_clauses_last_flip > 0 and flip_a_coin(rnd_walk):
                random_var_index = random.randint(0, len(unsatisfied_clause) - 1)
                random_interpretation = get_interpretation_with_changed_variable_sense(random_interpretation,
                                                                                       unsatisfied_clause
                                                                                       [random_var_index])
            else:
                random_interpretation = best_interpretation

    print("s UNSATISFIABLE")  # no solution found
    return []


def get_cnf_formula(file_name):
    formula = []

    instance = open(file_name, "r")
    for l in instance:
        if l[0] in ["c", "p"]:  # pass comments and program line
            if l[0] == "p":
                num_vars = l.split()[2]
            continue

        clause = map(int, l.split())
        clause.pop()  # remove last 0
        formula.append(clause)

    return formula, num_vars


def print_solution(interpretation):
    print("s SATISFIABLE")
    print("v " + ' '.join(map(str, interpretation[:])) + " 0")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " <cnf_file_name> ")
        sys.exit()

    cnf_file_name = sys.argv[1]
    formula, num_vars = get_cnf_formula(cnf_file_name)

    # Solve the problem and get the best solution found
    best_sol = solve(formula, int(num_vars), int(num_vars) * 35)
    if best_sol:
        print_solution(best_sol)
