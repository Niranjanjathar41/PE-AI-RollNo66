# tictactoe_minimax.py
import math
def empty_cells(board):
    return [i for i, v in enumerate(board) if v==' ']

def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a]==board[b]==board[c] and board[a] != ' ':
            return board[a]
    if ' ' not in board: return 'Draw'
    return None

def minimax(board, player):
    winner = check_winner(board)
    if winner=='X': return (1, None)
    if winner=='O': return (-1, None)
    if winner=='Draw': return (0, None)
    if player == 'X':
        best = (-math.inf, None)
        for move in empty_cells(board):
            board[move] = 'X'
            val, _ = minimax(board, 'O')
            board[move] = ' '
            if val > best[0]:
                best = (val, move)
        return best
    else:
        best = (math.inf, None)
        for move in empty_cells(board):
            board[move] = 'O'
            val, _ = minimax(board, 'X')
            board[move] = ' '
            if val < best[0]:
                best = (val, move)
        return best

# Heuristic variant: pick immediate winning/blocking moves or center
def heuristic_move(board, player):
    # win if possible
    for m in empty_cells(board):
        board[m] = player
        if check_winner(board)==player:
            board[m] = ' '
            return m
        board[m] = ' '
    # block opponent
    opp = 'O' if player=='X' else 'X'
    for m in empty_cells(board):
        board[m] = opp
        if check_winner(board)==opp:
            board[m] = ' '
            return m
        board[m] = ' '
    # center
    if board[4]==' ': return 4
    # corner
    for c in [0,2,6,8]:
        if board[c]==' ': return c
    return empty_cells(board)[0]

if __name__ == "__main__":
    # Example: X is AI (minimax), O is human
    board = [' ']*9
    # make some moves
    board[0] = 'X'
    board[4] = 'O'
    print("Board:", board)
    score, move = minimax(board, 'X')
    print("Minimax chooses:", move, "score:", score)
    print("Heuristic chooses:", heuristic_move(board, 'X'))
