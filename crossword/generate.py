import sys
from collections import deque

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generator.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }


    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """

        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]

        for variable, word in assignment.items():

            for k in range(len(word)):

                i = variable.i + (
                    k if variable.direction == Variable.DOWN else 0
                )

                j = variable.j + (
                    k if variable.direction == Variable.ACROSS else 0
                )

                letters[i][j] = word[k]

        return letters


    def print(self, assignment):
        """
        Print crossword assignment to terminal.
        """

        letters = self.letter_grid(assignment)

        for i in range(self.crossword.height):

            for j in range(self.crossword.width):

                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")

            print()


    def save(self, assignment, filename):
        """
        Save crossword assignment to image file.
        """

        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2

        letters = self.letter_grid(assignment)

        img = Image.new(
            "RGBA",
            (
                self.crossword.width * cell_size,
                self.crossword.height * cell_size
            ),
            "black"
        )

        font = ImageFont.truetype(
            "assets/fonts/OpenSans-Regular.ttf",
            80
        )

        draw = ImageDraw.Draw(img)


        for i in range(self.crossword.height):

            for j in range(self.crossword.width):

                rect = [
                    (
                        j * cell_size + cell_border,
                        i * cell_size + cell_border
                    ),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border
                    )
                ]


                if self.crossword.structure[i][j]:

                    draw.rectangle(rect, fill="white")


                    if letters[i][j]:

                        _, _, w, h = draw.textbbox(
                            (0,0),
                            letters[i][j],
                            font=font
                        )

                        draw.text(
                            (
                                rect[0][0] + (cell_size - w)/2,
                                rect[0][1] + (cell_size - h)/2
                            ),
                            letters[i][j],
                            fill="black",
                            font=font
                        )


        img.save(filename)



    def solve(self):
        """
        Enforce node and arc consistency, then solve CSP.
        """

        self.enforce_node_consistency()

        if not self.ac3():
            return None

        return self.backtrack({})



    def enforce_node_consistency(self):
        """
        Remove words with incorrect lengths.
        """

        for var in self.domains:

            for word in self.domains[var].copy():

                if len(word) != var.length:

                    self.domains[var].remove(word)



    def revise(self, x, y):
        """
        Make variable x arc consistent with y.
        """

        revised = False

        overlap = self.crossword.overlaps[x, y]


        if overlap is None:
            return False


        i, j = overlap


        for word_x in self.domains[x].copy():

            found = False


            for word_y in self.domains[y]:

                if word_x[i] == word_y[j]:

                    found = True
                    break


            if not found:

                self.domains[x].remove(word_x)
                revised = True


        return revised



    def ac3(self, arcs=None):
        """
        Enforce arc consistency.
        """

        if arcs is None:

            queue = deque()

            for x in self.crossword.variables:

                for y in self.crossword.neighbors(x):

                    queue.append((x,y))

        else:

            queue = deque(arcs)



        while queue:

            x,y = queue.popleft()


            if self.revise(x,y):

                if len(self.domains[x]) == 0:

                    return False


                for z in self.crossword.neighbors(x):

                    if z != y:

                        queue.append((z,x))


        return True



    def assignment_complete(self, assignment):

        return len(assignment) == len(self.crossword.variables)



    def consistent(self, assignment):

        for var, word in assignment.items():

            if len(word) != var.length:

                return False


        if len(set(assignment.values())) != len(assignment):

            return False



        for var in assignment:

            for neighbor in self.crossword.neighbors(var):

                if neighbor in assignment:

                    overlap = self.crossword.overlaps[var, neighbor]


                    if overlap is not None:

                        i,j = overlap


                        if assignment[var][i] != assignment[neighbor][j]:

                            return False


        return True



    def order_domain_values(self, var, assignment):

        values = []


        for value in self.domains[var]:

            ruled_out = 0


            for neighbor in self.crossword.neighbors(var):

                if neighbor in assignment:

                    continue


                overlap = self.crossword.overlaps[var, neighbor]


                if overlap is None:

                    continue


                i,j = overlap


                for word in self.domains[neighbor]:

                    if value[i] != word[j]:

                        ruled_out += 1


            values.append((value, ruled_out))


        values.sort(key=lambda x:x[1])


        return [v for v,_ in values]



    def select_unassigned_variable(self, assignment):

        variables = [
            v for v in self.crossword.variables
            if v not in assignment
        ]


        return min(
            variables,
            key=lambda v:(
                len(self.domains[v]),
                -len(self.crossword.neighbors(v))
            )
        )



    def backtrack(self, assignment):

        if self.assignment_complete(assignment):

            return assignment


        var = self.select_unassigned_variable(assignment)


        for value in self.order_domain_values(var, assignment):

            new_assignment = assignment.copy()

            new_assignment[var] = value


            if self.consistent(new_assignment):

                result = self.backtrack(new_assignment)


                if result is not None:

                    return result


        return None




def main():

    if len(sys.argv) not in [3,4]:

        sys.exit(
            "Usage: python generate.py structure words [output]"
        )


    structure = sys.argv[1]

    words = sys.argv[2]

    output = sys.argv[3] if len(sys.argv)==4 else None


    crossword = Crossword(structure, words)

    creator = CrosswordCreator(crossword)


    assignment = creator.solve()


    if assignment is None:

        print("No solution.")

    else:

        creator.print(assignment)

        if output:

            creator.save(assignment, output)



if __name__ == "__main__":

    main()