"""
This example code creates a 2d list (2d matrix) that can store seating.
The matrix is populated with a since all seats are available
"""

# our test matrix has 4 rows and 10 columns
n_row = 19
n_col = 26

# available seat
available_seat = 'a'

# create some available seating
seating = []
for r in range(n_row):
    row = []
    for c in range(n_col):
        row.append(available_seat)
    seating.append(row)

# print available seating row
for r in range(n_row):
    print(r+1, end="\t")
    for c in range(n_col):
        print(seating[r][c], end=" ")
    print()
