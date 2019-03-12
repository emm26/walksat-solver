import sys

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
    print "Num_vars: " + num_vars
    print formula
