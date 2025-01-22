from PIL import Image
from PIL import ImageDraw
import numpy as np
from generate import create_board

class Variable:
    def __init__(self):
        self.i = None
        self.j = None
        self.cannot_go = None

    def set_coordinates(self, i, j):
        self.i = i
        self.j = j

    def return_cannot_come(self, n):
        #Horizontal constraints
        cannot_come = set()
        for x_axis in range(n):
            if x_axis == self.j:
                continue
            cannot_come.add((self.i, x_axis))
        
        #vertical constraints
        for y_axis in range(n):
            if y_axis == self.i:
                continue
            cannot_come.add((y_axis, self.j))
        
        #diagonal constraints
        for i in range(1, n):
            #upper right
            flag = True
            new_i = self.i - i
            new_j = self.j + i
            if new_i >= 0 and new_j < n:
                cannot_come.add((new_i, new_j))
                flag = False
            #lower left
            new_i = self.i + i
            new_j = self.j - i

            if new_i < n and new_j >= 0:
                cannot_come.add((new_i, new_j))
                flag = False
            
            #upper left
            new_i = self.i - i
            new_j = self.j - i
            if new_i >= 0 and new_j >= 0:
                cannot_come.add((new_i, new_j))
                flag = False
            
            #lower right
            new_i = self.i + i
            new_j = self.j + i
            if new_i < n and new_j < n:
                cannot_come.add((new_i, new_j))
                flag = False

            #if flag true, it means it cannot go more towards diagonal
            if flag:
                break
        self.cannot_go = cannot_come

    def __str__(self):
        return str(self.i) + " " + str(self.j)



    #Returns the coordinates other variables cannot be in.
    def cross(self, other_var):
        if self.i is None or self.j is None:
            return False

        if other_var.i is None or other_var.j is None:
            return False
        
        column_difference = abs(self.i - other_var.i)
        row_difference = abs(self.j - other_var.j)

        #horizontal
        if column_difference == 0:
            return True
        
        #vertical
        if row_difference == 0:
            return True
        
        #diagonal
        if column_difference - row_difference == 0:
            return True
        
        #no collision
        return False
        


class Solve:
    def __init__(self, queen_number, side_length):
        self.length = side_length
        self.n = queen_number
        self.domains = {Variable(): {(i, j) for j in range(self.length) for i in range(self.length)} for x in range(queen_number)}
        self.arcs = set(self.domains.keys())
        self.arcs_list = list(self.domains.keys())
        self.dont_go = {}
    
    def solve(self):
        self.ac3()

        the_result = self.backtrack(set())
        if self.n > self.length:
            print("no solution")
            return False
        if the_result:
            self.print(the_result)
            return the_result
        print("no solution")

        return False

    def revise(self, x, y):
        is_revised = False
        for i in self.domains[x].copy():
            x.set_coordinates(i[0], i[1])
            for j in self.domains[y]:
                if i == j:
                    continue
                y.set_coordinates(j[0], j[1])
                if x.cross(y):
                    continue
                break
            else:
                self.domains[x].remove(i)
        x.set_coordinates(None, None)
        y.set_coordinates(None, None)
        return is_revised

    def ac3(self):
        queue = [(x, y) for x in self.domains.keys() for y in self.domains.keys() if x != y]
        while len(queue) != 0:
            x, y = queue.pop(0)
            result = self.revise(x, y)
            if len(self.domains[x]) == 0:
                return False
            if result:
                for neighbors in self.arcs.difference({x, y}):
                    queue.append((y, neighbors))
        return False

    def ordered_domains(self, arc):
        cost_and_value = {}
        for value in self.domains[arc]:
            if value not in self.dont_go.keys():
                arc.set_coordinates(value[0], value[1])
                arc.return_cannot_come(self.n)
                self.dont_go[value] = arc.cannot_go.copy()
                arc.set_coordinates(None, None)
                arc.cannot_go = None
            cost = len(self.dont_go[value])
            if cost in cost_and_value.keys():
                cost_and_value[cost].append(value)
            else:
                cost_and_value[cost] = [value]
        sorted_keys = sorted(cost_and_value)
        domain = []
        for i in sorted_keys:
            for j in cost_and_value[i]:
                domain.append(j)
        return domain

    def consistent(self, assignments, last_value):
        the_constraints = self.dont_go[last_value]
        for arc in assignments:
            if (arc.i, arc.j) == last_value:
                return False
            if (arc.i, arc.j) in the_constraints:
                return False
            
        return True

    def is_complete(self, assignment):
        if len(self.arcs.difference(assignment)) == 0:
            return True

    def select_arc(self, assignment):
        released_arcs = list(self.arcs.difference(assignment))
        return released_arcs[0]


    #create output
    def to_png(self, queens, file = None):
        if file is None:
            return
        create_board(file, self.length, queens)
        




    def backtrack(self, assign):
        if self.is_complete(assign):
            return assign

        arc = self.select_arc(assign)
        sorted_domain = self.ordered_domains(arc)
        for value in sorted_domain:
            result = self.consistent(assign, value)
            if not result:
                continue
            arc.set_coordinates(value[0], value[1])
            assign.add(arc)
            real_result = self.backtrack(assign)
            if real_result:
                return assign
            assign.remove(arc)
            arc.set_coordinates(None, None)
        return False

    def print(self, assignment):
        coordinates = [(arc.i, arc.j) for arc in assignment]
        for i in range(self.length):
            for j in range(self.length):
                if (i, j) in coordinates:
                    print("O", end = "")
                    continue
                print("X", end = "")
            print()
                

solution = Solve(9, 10)

result = solution.solve()
queens = [(arc.j, arc.i) for arc in result]
if result:
    solution.to_png(queens, "queen_problem.png")