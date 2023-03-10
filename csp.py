##################################################################################
# It is not allowed to add imports here. Use these two packages and nothing else.
import numpy as np
import typing
##################################################################################


class CSP:
    def __init__(self, grid:np.ndarray, numbers: typing.Set[int], groups: typing.List[typing.List[typing.Tuple[int,int]]],
                 constraints: typing.List[typing.Tuple[int,int]]):
        
        """
        The CSP solver object, containing all information and functions required for the assignment. You do not need to change
        this function.

        :param grid: 2-d numpy array corresponding to the grid that we have to fill in. Empty squares are denoted with 0s.
        :param numbers: The set of numbers that we are allowed to use in order to fill the grid (can be any set of integers)
        :param groups: A list of cell groups (cell groups are lists of location tuples).
        :param constraints: The list of constraints for every group of cells. constraints[i] hold for groups[i]. Every
                            constraint is a tuple of the form (sum_of_elements, max_count_element) where sum_of_elements 
                            indicates what the sum must be of the elements of the given group, and max_count_element indicates
                            the maximum number of times that a number/element may occur in the given group
        """

        self.width = grid.shape[1]
        self.height = grid.shape[0]
        self.numbers = numbers
        self.groups = groups
        self.constraints = constraints
        
        self.grid = grid
        self.cell_to_groups = {(row_idx, col_idx): [] for row_idx in range(self.height) for col_idx in range(self.width)}


    def fill_cell_to_groups(self):
        """
        Function that fills in the self.cell_to_groups datastructure, which maps a cell location (row_idx, col_idx)
        to a list of groups of which it is a member. For example, suppose that cell (0,0) is member of groups 0, 1,
        and 2. Then, self.cell_to_groups[(0,0)] should be equal to [0,1,2]. This function should do this for every cell. 
        If a cell is not a member of any groups, self.cell_to_groups[cell] should be an empty list []. 
        The function does not return anything. 

        Before completing this function, make sure to read the assignment description and study the data structures created
        in the __init__ function above (self.groups and self.cell_to_groups).
        """

        # enumerate to get the index of a group(i) and the coordinates of a group(group)
        for i, group in enumerate(self.groups):
            # get every individual coordinate from the group
            for group2 in group:
                # append the coordinate to the group(i) where it belongs
                self.cell_to_groups[group2].append(i)


    def satisfies_sum_constraint(self, group: typing.List[typing.Tuple[int,int]], sum_constraint: int) -> bool:
        """
        Function that checks whether the given group satisfies the given sum constraint (group smaller or equal 
        than sum). Returns True if the current group satisfies the constraint and False otherwise. 

        :param group: The list of locations [loc1, loc2, loc3,...,locN] that specify the group. Here, every loc is 
                      a tuple (row_idx, col_idx) of indices, specifying the row and column of the cell. 
        :param sum_constraint: The sum_of_elements constraint specifying that the numbers in the given group must
                               sum up to this number. This is None if there is no sum constraint for the given group. 
        """

        sum = 0 
      
        # sum up all values of a group
        for i in group:
            sum += self.grid[i]
          
        # check if the sum satisfies the sum_constraint
        if sum <= sum_constraint:
            return True
        else:
            return False

        # TODO: write this function

        raise NotImplementedError()

    
    def satisfies_count_constraint(self, group: typing.List[typing.Tuple[int,int]], count_constraint: int) -> bool:
        """
        Function that checks whether the given group satisfies the given count constraint.
        Returns True if the current group satisfies the constraint and False otherwise. 
        Recall that the value of 0 indicates an empty cell (0s should not count towards the count constraint).

        :param group: The list of locations [loc1, loc2, loc3,...,locN] that specify the group. Here, every loc is 
                      a tuple (row_idx, col_idx) of indices, specifying the row and column of the cell. 
        :param count_constraint: Integer specifying that a given number cannot occur more than this amount of times. 
                                 This is None if there is no count constraint for the given group. 
        """
        
        # TODO: write this function
        list = []

        for i in group:
            if self.grid[i] != 0:
                list.append(self.grid[i])
        
        for i in list:
            if list.count(i) > count_constraint:
                return False

        return True
        raise NotImplementedError()


    def satisfies_group_constraints(self, group_indices: typing.List[int]) -> bool:
        """
        Function that checks whether the constraints for the given group indices are satisfied.
        Returns True if all relevant constraints are satisfied, False otherwise. Make sure to use functions defined above. 

        :param group_indices: The indices of the groups for which we check all of the constraints 
        """

        # check for every index in i if the sum and count constraints are satisfied.
        for i in group_indices:
            # initially give the variable constraints the boolean False
            constraint = False
            # if both the sum and count constraints are satisfied change the variable constraint to True and continue to the next iteration
            if self.satisfies_sum_constraint(self.groups[i], self.constraints[0][0]) == True and self.satisfies_count_constraint(self.groups[i], self.constraints[0][1]) == True:
                constraint = True
                continue
            # if one of the constraints is not satisfied, break the loop
            break

        # return the outcome
        return constraint

        # TODO: write this function

        raise NotImplementedError()


    def search(self, empty_locations: typing.List[typing.Tuple[int, int]]) -> np.ndarray:
        """
        Recursive exhaustive search function. It tries to fill in the empty_locations with permissible values
        in an attempt to find a valid solution that does not violate any of the constraints. Instead of checking all
        possible constraints after filling in a number, it checks only the relevant group constraints using the 
        self.cell_to_groups data structure. 

        Returns None if there is no solution. Returns the filled in solution (self.grid) otherwise if a solution is found.

        :param empty_locations: list of empty locations that still need a value from self.numbers 
        """

        print("#####################")        
        print(self.grid)
        print(self.constraints)
        print(empty_locations)
        print(self.numbers)
        group_indices = []

        for i in range(len(self.groups)):
            group_indices.append(i)

        if len(empty_locations) == 0:
            return self.grid
        
        location = empty_locations.pop(0)
        print(location)
        for number in self.numbers:
            self.grid[location] = number
            if self.satisfies_group_constraints(group_indices) == False:
                self.grid[location] = 0
                continue
            result = self.search(empty_locations)
            print("success")
            break
        print("end")
        try:
            return result
        except:
            print("none")
            return None

        group_indices=[]
        copy_locations = empty_locations.copy()

        for i in range(len(self.groups)):
            group_indices.append(i)

        if len(copy_locations)==0:
            return self.grid

        location = copy_locations.pop(0)
        for number in self.numbers:
            self.grid[empty_locations[0]] = number
            if self.satisfies_group_constraints(group_indices) == False:
                self.grid[empty_locations[0]] = 0
                continue
            result = self.search(copy_locations)
            break

        try:
            return result
        except:
            return None
        
        # TODO: write this function

        raise NotImplementedError()
    

    def start_search(self):
        """
        Non-recursive function that starts the recursive search function above. It first fills the cell_to_group
        data structure and computes the empty locations. Then, it starts the recursive search procedure. 
        The result is None if there is no solution possible. Otherwise, it returns the grid that is a solution.

        You do not need to change this function.
        """

        self.fill_cell_to_groups()
        empty_locations = [(row_idx, col_idx) for row_idx in range(self.height) for col_idx in range(self.width) if self.grid[row_idx,col_idx]==0]
        return self.search(empty_locations)
    
