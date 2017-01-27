assignments = []


def cross(A, B):
    return [a+b for a in A for b in B]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unitlist = row_units + col_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)
diagonal1 = [r+c for r, c in zip(rows, cols)]
diagonal2 = [r+c for r, c in zip(rows, sorted(cols, reverse=True))]



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    filtered_boxes = [box for box in values.keys() if len(values[box]) == 2]
    for box in filtered_boxes:
        d1 = values[box][0]
        d2 = values[box][1]
        for peer in peers[box]:
            if values[peer] == values[box]:
                for unit in units[box]:
                    if peer in unit:
                        for square in unit:
                            if square != peer and square != box:
                                values[square] = values[square].replace(d1, '')
                                values[square] = values[square].replace(d2, '')
                                if square in filtered_boxes:
                                    filtered_boxes.remove(square)
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    rows = 'ABCDEFGHI'
    cols = '123456789'
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)


def eliminate_diagonal(values, box, diagonal, digits):
    """
    Eliminate
    :param values:
    :param box:
    :param diagonal:
    :param digits:
    :return:
    """
    for square in diagonal:
        if len(values[square]) > 1 and square != box:
            values[square] = values[square].replace(digits, '')
    return values


def eliminate(values):
    """
    :param values:
    :return:
    """
    center_square = 'E5'
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_boxes:
        digits = values[box]
        diagonal = []
        if box in diagonal1 and box != center_square:
            diagonal = diagonal1
            values = eliminate_diagonal(values, box, diagonal, digits)
        elif box in diagonal2 and box != center_square:
            diagonal = diagonal2
            values = eliminate_diagonal(values, box, diagonal, digits)
        elif box == center_square:
            diagonal = set(diagonal1 + diagonal2)
            values = eliminate_diagonal(values, box, diagonal, digits)

        for peer in peers[box]:
            if len(values[peer]) > 1 and peer not in diagonal:
                values[peer] = values[peer].replace(digits, '')

    return values


def only_choice(values):
    """
    :param values:
    :return:
    """
    digits = '123456789'
    unitlist.append(diagonal1)
    unitlist.append(diagonal2)
    for unit in unitlist:
        for digit in digits:
            digit_exist = [box for box in unit if digit in values[box]]
            if len(digit_exist) == 1:
                values = assign_value(values, digit_exist[0], digit)

    return values


def reduce_puzzle(values):
    """
    :param values:
    :return:
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def solve(grid):
    """
        Find the solution to a Sudoku grid.
        Args:
            grid(string): a string representing a sudoku grid.
                Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        Returns:
            The dictionary representation of the final sudoku grid. False if no solution exists.
        """
    return search(grid_values(grid))


def search(values):
    values = reduce_puzzle(values)

    if not values:
        return False

    if all(len(values[box]) == 1 for box in boxes):
        return values

    min_pos, square = min((len(values[square]), square) for square in boxes if len(values[square]) > 1)

    for value in values[square]:
        new_grid = values.copy()
        new_grid = assign_value(new_grid, square, value)
        tried = search(new_grid)
        if tried:
            return tried


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
