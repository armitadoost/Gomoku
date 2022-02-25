"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 26, 2020
"""

def is_empty(board):
    '''Return True if board is empty, return False if board is not empty'''
    for x in range(len(board)):
      for y in range(len(board)):
        if board[x][y] != " ":
          return False

    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    '''Return OPEN, CLOSED, SEMIOPEN depending on the sequence pattern'''

    type_top = ""
    type_end = ""

    col = board[y_end][x_end]

    if (y_end - d_y*(length - 1)) >= 7 or (x_end - d_x*(length - 1)) >= 7 or (y_end - d_y*(length - 1)) <= 0 or (x_end - d_x*(length - 1)) <= 0:
        type_top = "CLOSED"

    elif board[y_end - d_y*(length)][x_end - d_x*(length)] == " ":
        type_top = "OPEN"

    elif board[y_end - d_y*(length)][x_end - d_x*(length)] != col:
        type_top = "CLOSED"

    if (y_end) >= 7 or (x_end) >= 7 or (y_end) <= 0 or (x_end) <= 0:
        type_end = "CLOSED"

    elif board[y_end + d_y][x_end + d_x] == " ":
        type_end = "OPEN"

    elif board[y_end + d_y][x_end + d_x] != col:
        type_end = "CLOSED"

    # Find final type
    if type_end != type_top:
        return "SEMIOPEN"
    elif type_end == type_top:
        return type_end


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    '''Return tuple of number of open and semi open sequences in a row'''
    open_seq_count = 0
    semi_open_seq_count = 0

    y_cur = y_start
    x_cur = x_start
    cur_seq_len = 0
    seq_type = " "

    while 0 <= y_cur < 8 and 0 <= x_cur < 8:
        if board[y_cur][x_cur] == col:
            cur_seq_len += 1

        elif board[y_cur][x_cur] != col:
            if cur_seq_len == length:
                seq_type = is_bounded(board, (y_cur-d_y), (x_cur-d_x), length, d_y, d_x)
                if seq_type == "OPEN":
                    open_seq_count += 1
                elif seq_type == "SEMIOPEN":
                    semi_open_seq_count += 1

            cur_seq_len = 0

        y_cur += d_y
        x_cur += d_x

    if cur_seq_len == length:
        seq_type = is_bounded(board, (y_cur - d_y), (x_cur - d_x), length, d_y, d_x)
        if seq_type == "OPEN":
            open_seq_count += 1
        elif seq_type == "SEMIOPEN":
            semi_open_seq_count += 1

    return open_seq_count, semi_open_seq_count


def detect_rows(board, col, length):
    '''Return total number of open and semiopen sequences on the entire board'''

    open_seq_count, semi_open_seq_count = 0, 0

    # Situation 1 - Horizontal
    d_y = 0
    d_x = 1

    for y in range(0,8):
        seq_total = detect_row(board, col, y, 0, length, d_y, d_x)
        open_seq_count += seq_total[0]
        semi_open_seq_count += seq_total[1]


    # Sitation 2 - Vertical
    d_y = 1
    d_x = 0

    for x in range(0,8):
        seq_total = detect_row(board, col, 0, x, length, d_y, d_x)
        open_seq_count += seq_total[0]
        semi_open_seq_count += seq_total[1]


    # Situation 3 - Diagonal
    d_y = 1
    d_x = 1

    for y in range(0,8):
        # diagonals that start from column 0
        seq_total = detect_row(board, col, y, 0, length, d_y, d_x)
        open_seq_count += seq_total[0]
        semi_open_seq_count += seq_total[1]

    for x in range(1,8):
        # diagonals that start from row 0
        seq_total = detect_row(board, col, 0, x, length, d_y, d_x)
        open_seq_count += seq_total[0]
        semi_open_seq_count += seq_total[1]

    # Situation 4 - Negative Diagonal
    d_y = 1
    d_x = -1

    for y in range(0,8):
        # diagonals that start from column 7
        seq_total = detect_row(board, col, y, 7, length, d_y, d_x)
        open_seq_count += seq_total[0]
        semi_open_seq_count += seq_total[1]

    for x in range(1,8):
        # diagonals that start from row 7
        seq_total = detect_row(board, col, 0, x, length, d_y, d_x)
        open_seq_count += seq_total[0]
        semi_open_seq_count += seq_total[1]


    return open_seq_count, semi_open_seq_count

def test_detect_rows():
    board = make_empty_board(8)
    x = 4; y = 0; d_x = -1; d_y = 1; length = 5; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (0,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def search_max(board):
    '''Return tuple of (y, x) coordinates for computer move that is optimal'''
    col = "b"
    move_y = 0
    move_x = 0

    for y in range(0,8):
        for x in range(0,8):
            if board[y][x] == " ":
                if move_y == 0 and move_x == 0:
                    top_score = score(board)
                    move_y = y
                    move_x = x

                board[y][x] = "b"


                if score(board) > top_score:
                    top_score = score(board)
                    move_y = y
                    move_x = x

                board[y][x] = " "

    return move_y, move_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def check_closed_rows(board, col, y_start, x_start, length, d_y, d_x):
    '''Return the number of closed sequences in a row'''
    closed_count = 0

    y_cur = y_start
    x_cur = x_start
    cur_seq_len = 0
    seq_type = " "

    while 0 <= y_cur < 8 and 0 <= x_cur < 8:
        if board[y_cur][x_cur] == col:
            cur_seq_len += 1

        elif board[y_cur][x_cur] != col:
            if cur_seq_len == length:
                seq_type = is_bounded(board, (y_cur-d_y), (x_cur-d_x), length, d_y, d_x)
                if seq_type == "CLOSED":
                    closed_count += 1

            cur_seq_len = 0

        y_cur += d_y
        x_cur += d_x

    if cur_seq_len == length:
        seq_type = is_bounded(board, (y_cur - d_y), (x_cur - d_x), length, d_y, d_x)
        if seq_type == "CLOSED":
            closed_count += 1

    return closed_count


def check_closed(board, col, length):
    '''Return the number of closed sequences on the entire board'''
    closed_count = 0

    # Situation 1 - Horizontal
    d_y = 0
    d_x = 1

    for y in range(0,8):
        seq_total = check_closed_rows(board, col, y, 0, length, d_y, d_x)
        closed_count += seq_total


    # Sitation 2 - Vertical
    d_y = 1
    d_x = 0

    for x in range(0,8):
        seq_total = check_closed_rows(board, col, 0, x, length, d_y, d_x)
        closed_count += seq_total


    # Situation 3 - Diagonal
    d_y = 1
    d_x = 1

    for y in range(0,8):
        # diagonals that start from column 0
        seq_total = check_closed_rows(board, col, y, 0, length, d_y, d_x)
        closed_count += seq_total

    for x in range(1,8):
        # diagonals that start from row 0
        seq_total = check_closed_rows(board, col, 0, x, length, d_y, d_x)
        closed_count += seq_total

    # Situation 4 - Negative Diagonal
    d_y = 1
    d_x = -1

    for y in range(0,8):
        # diagonals that start from column 7
        seq_total = check_closed_rows(board, col, y, 7, length, d_y, d_x)
        closed_count += seq_total

    for x in range(1,8):
        # diagonals that start from row 7
        seq_total = check_closed_rows(board, col, 0, x, length, d_y, d_x)
        closed_count += seq_total


    return  closed_count



def is_win(board):
    status = "Draw"  # If none of the cases below are met, it means the board is full

    # Continue playing

    for y in range(0,8):
        for x in range(0,8):
            if board[y][x] == " ":
                status = "Continue playing"

    # White won
    if detect_rows(board, "w", 5) != (0,0):
        status = "White won"

    # Black won
    if detect_rows(board, "b", 5) != (0,0):
            status = "Black won"

    #closed 5 sequences -- IS THIS CORRECT
    if check_closed(board, "w", 5) != 0:
        status = "White won"

    if check_closed(board, "b", 5) != 0:
        status = "Black won"

    return status

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")


def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)

    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)

    print_board(board)

    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    print(play_gomoku(8))
