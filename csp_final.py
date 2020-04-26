'''
Project #2
Artificial Intelligence Class
Simay Yazicioglu
Fall 2019
'''
import collections
class Cryptarithmetic_Problem:
    def __init__(self):
        self.additional_constraints =[] #stores list of lists which contain equivalent variables
        self.domains_dict = {} #stores the domain for each variable
        self.neighbors_dict ={} #stires the neighbor of each variable
        #initialize domains
        for var in range(1,14):
                self.domains_dict[var] = None
        for var  in self.domains_dict:
            if 9 ==var:
                self.domains_dict[var] = [1]
            elif 1 == var or 5 == var:
                self.domains_dict[var]= [i for i in range(1,10)]
            else: #if variable is 2,3,4,6,7,8,10,11,12,13
                self.domains_dict[var]= [i for i in range(0,10)]
        #set domains for carry outs
        self.domains_dict[-1], self.domains_dict[-2], self.domains_dict[-3] = [0,1] , [0,1] , [0,1]
        #initialize neighbors
        self.initialize_neigbors()

    def initialize_neigbors(self):
        '''initializes the neighbors dictonary
        neighbors dict has variables as keys and their neighbors as dict
        ''' 
        self.neighbors_dict[-1] = [4,8,13,3,7,12, -2]
        self.neighbors_dict[-2] = [-1,3,7,12,2,6,11,-3]
        self.neighbors_dict[-3] = [-2,2,6,11,1,5,10,9]
        self.neighbors_dict[1] =  [-3,5,10,9]
        self.neighbors_dict[2] = [-2,6,11,-3]
        self.neighbors_dict[3] = [-1,7,12,-2]
        self.neighbors_dict[4] = [8,13,-1]
        self.neighbors_dict[5] =  [-3,1,10,9]
        self.neighbors_dict[6] = [-2,2,11,-3]
        self.neighbors_dict[7] = [-1,3,12,-2]
        self.neighbors_dict[8] = [4,13,-1]
        self.neighbors_dict[9] = [-3,5,10,1] 
        self.neighbors_dict[10] =  [-3,1,5,9]
        self.neighbors_dict[11] =  [-2,2,6,-3]
        self.neighbors_dict[12] = [-1,3,7,-2]
        self.neighbors_dict[13] = [4,8,-1]

    def check_additional_constraints(self, assignment):
        '''ensures that every equivalent variable in the assignment has been assigned to the same value
        '''
        for lst in self.additional_constraints:
            s = set(assignment[variable] for variable in lst) 
            #set has to have the length if every value assigned to ther alias variables is the same
            if len(s)!=1:
                return False
        return True

    def check_asignment(self, assignment, var, val):
        '''ensures the constraints for the assignment, before and after assigning val to var
        
        #assigments is a dictioanry. key represnt one variable from (1,..13 and -1, -2, -3) 
        #and value represetns the value
        #1.     x4 + x8= x13 + 10*c1
        #2. c1+ x3 + x7= x12 + 10*c2 
        #3. c2+ x2 + x6= x11 + 10*c3 
        #4. c3 + x1 + x5 = x10 + 10
        #check if varaibales have value
        #if they have, hceck the equation,
        #if they dont go on the other constraint
        #if any of the constraints are violated, return False, else return True
        '''
        alias_lst= []
        if assignment[var] is not None: #already assigned
            return False ,alias_lst
        #check all variables are assgined different values, 
        #apart from carry outs or the variables that are supposed to be equivalent to each other
        #variables that are supposed to be equal to each other are stored in a list in self.additional_constraints
        #if one variable has equivalent variables, we put all of them in alias_lst
        for lst in self.additional_constraints:
            if var  in lst:
                alias_lst = lst[:]
                break
        if var not in (-1,-2,-3): #this constraint doesnt hold for auxilary variables
            for k, v in assignment.items():
                if k not in (-1,-2,-3): 
                    if v ==val and k not in alias_lst:
                    #if they value has been given to some other variable that is not alias of the current variable, return False
                        return False, alias_lst
        #assign the val to var
        assignment[var] = val
        #update every alias with the same val
        for elem in alias_lst:
            if assignment[elem] is not None and assignment[elem]!=val:
                return False, alias_lst
            assignment[elem] = val
        #check the equation constraints
        con1, con2, con3, con4 = True ,  True , True , True
        if assignment[4] is not None and assignment[8] is not None and assignment[13] is not None and assignment[-1] is not None:
            con1= assignment[4] + assignment[8] == assignment[13] + 10*assignment[-1]
        if assignment[-1] is not None and assignment[3] is not None and assignment[7] is not None and assignment[12] is not None and assignment[-2] is not None:
            con2 = assignment[-1] + assignment[3] + assignment[7] == assignment[12] +10* assignment[-2] 
        if assignment[-2] is not None and assignment[2] is not None and assignment[6] is not None and assignment[11] is not None and assignment[-3] is not None:
            con3 = assignment[-2] + assignment[2] + assignment[6] == assignment[11] +10* assignment[-3] 
        if assignment[-3] is not None and assignment[1] is not None and assignment[5] is not None and assignment[10] is not None:
            con4 = assignment[-3] + assignment[1] + assignment[5] == assignment[10] + 10
        check = con1 and con2 and con3 and con4  and self.check_additional_constraints(assignment)
        return check , alias_lst

    def neighbors(self,var1, var2):
        '''returns True if var1 and var2 are neighbors, else false'''
        return var2 in self.neighbors_dict[var1]

    def  degree_heuristics(self, most_constrained_variables, assignments):
        '''returns the variable with the biggest number of unassigned neighbors
            assumes len(most_constrained_variables)>=1
        '''
        #get all unassigned variables 
        all_unassigned_vars =[var for var in assignments if assignments[var] is None ]
        vars_neighbor_nums = []
        #for each variable passed, find the one that has the biggest number of neighbors that are in all_unassigned_vars
        for var in most_constrained_variables:
            num= 0
            for unassigned_var in all_unassigned_vars:
                if self.neighbors(var, unassigned_var):
                    num +=1
            vars_neighbor_nums.append((num, var))
        vars_neighbor_nums.sort() #sort based on number of variables
        return vars_neighbor_nums[-1][1]
        
    def select_unassigned_variable(self, assignments):
        '''implements minimum remaining values algorithm, 
        which calls the degree_heuristics if needed,
        and seelcts and unassigned variable as a result'''
        #get all unassigned variables and already assigned values
        all_unassigned_vars =[var for var in assignments if assignments[var] is None ]
        already_assigned_values = [assignments[var] for var in assignments if assignments[var] is not None and var not in (-1,-2,-3)]
        #find length of the domain for each unassigned variables
        valid_dom_lengths = []
        for var in all_unassigned_vars:
            #find valid lenght for domain of var
            var_domain = self.domains_dict[var]
            var_domain_len = len(var_domain)
            #find how much of the domain values are already assigned
            for domain_value in var_domain:
                if domain_value in already_assigned_values:
                    if var not in (-1,-2,-3):
                        var_domain_len -=1
            valid_dom_lengths.append((var_domain_len, var))
        #find the variable with minimum valid domain length
        valid_dom_lengths.sort() #sort based on var_domain_len
        min_len = valid_dom_lengths[0][0]
        #from the valid domain list, find the couples that have the min len 
        variables_with_min_len =[ (l,var) for l,var in valid_dom_lengths if l==min_len]
        #if there is only one variable with min_len, return that variable
        if len(variables_with_min_len) ==1:
            return variables_with_min_len[0][1]
        #else, do the degree heuristics
        elif len(variables_with_min_len) >1:
            return self.degree_heuristics( [var for (l,var) in variables_with_min_len], assignments)
        else:
            return None

    def assignments_complete(self, assignments):
        '''returns True if assignments are all complete
        ,meaning there is no variable that has been assigned a value yet'''
        for var in assignments:
            if assignments[var] is None:
                return False
        return True

    def order_domain_values(self, var):
        '''returns the domain of a specific variable'''
        return self.domains_dict[var]

    def backtrack(self,assignments):
        '''implements the backtracking algorithm for the given assignments'''
        if self.assignments_complete(assignments):
            return assignments
        var = self.select_unassigned_variable(assignments)
        values = self.order_domain_values(var)
        for value in values:
            if value is not None:
                check, alias_lst =self.check_asignment(assignments, var, value)
                if  not check: #not consistent
                    assignments[var] = None
                    for elem in alias_lst:
                        assignments[elem] = None
                else: # consistent
                    result = self.backtrack(assignments)
                    if result !=  -1: #if result is not failure
                        return result
                    else:
                        assignments[var] = None
                        for elem in alias_lst:
                            assignments[elem] = None
        return -1
                
    def backtrack_search(self):
        '''calls the backtracking algroithm on the empty assignments
        returns solution or failure (-1)'''
        empty_assignments = {-1: None, -2:None, -3:None, 1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None, 10:None, 11:None, 12:None, 13:None}
        return self.backtrack(empty_assignments)

    def update_domains(self):
        '''Makes sure that equivalent variables, stored in self.additional_constraints, have the same domains
        Looks at equivalent variables' domains, and assign the domain that is more constricted (size being less)
        to all of the domains of the equivalent variables
        '''
        for equivalent_lst in self.additional_constraints:
            min_domain_lst = []
            for var in equivalent_lst:
                min_domain_lst.append((len(self.domains_dict[var]),var))
            #sort the min domain lst so fist element is a tuple of
            #(length of the minimum domain of variable, variable)
            min_domain_lst.sort()
            tup = min_domain_lst[0]
            #assign the domain of this variable to every equivalent variable in equivalent lst
            var_with_min_domain = tup[1]
            min_domain= self.domains_dict[var_with_min_domain]
            for var  in equivalent_lst:
                self.domains_dict[var] = min_domain[:]

    def intialize_variables(self, letter_dic):
        '''Builds additional constraints based on which letters are assigned to the which variable
        If same letter is assigned to different variables, those variables are equivalent(or alias)
        and we store those variables in the listself.additional_constraints
        '''
        for lst in letter_dic.values():
            #every variable in each lst represents an additional constraint: they will have to be assigned the same vaue
            if len(lst)>1: #
                self.additional_constraints.append(lst)
        #now that we have additional constraintd, we gotta update the domains of equivalent variables 
        self.update_domains()
    def read_file(self, in_file):
        '''reads the file with name in_file
        returns letter_dict which has a letter as key and a list of variables assigned to that letter
        #letter_dict is for 13 letters, index key'a' represens letter 'a' in the file, 
        #value of each key is the list of variables assosicated with that key
        #for example letter_dict['S']=[5,9] means x5 and x9 have the same value 'S'
        '''
        file = open(in_file, 'r')
        letter_dict = collections.defaultdict(lambda:[])
        #fill the letter dictionary
        index = 1
        for line in file:
            for letter in line.strip():
                if letter in letter_dict:
                    letter_dict[letter].append(index)
                else: 
                    letter_dict[letter] = [index]
                index+=1
        file.close()
        return letter_dict

    def output_result(self, out_file, solution):
        '''Assuming theres is a solution, this function writes the solution into the file 
        The format of the output file is the same as the input file
        '''
        output =open(out_file, 'w')
        for var,value in sorted(solution.items()):
            if var in (-1,-2,-3):
                continue
            if var in (4,8):
                print(value, end='\n', file=output)
            else:
                print(value, end='',file=output)
        output.close()
        
def main():
    crp = Cryptarithmetic_Problem()
    in_file = "Input1.txt" #input file name
    letter_dict =crp.read_file(in_file)
    crp.intialize_variables(letter_dict)
    solution = crp.backtrack_search()
    if solution == -1: #puzzle has no solution
        print("cannot be solved")
    else: #puzzle has solution
        out_file = "Output_of_"+in_file
        crp.output_result(out_file, solution)
        print('SUCCESS!')

main()