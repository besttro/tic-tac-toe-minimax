import tkinter as tk
from tkinter import messagebox

HUMAN = 'X'
AI = 'O'
EMPTY = ''

board = [[EMPTY for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
player_turn = True

def make_move(row, col, player):
    board[row][col] = player
    buttons[row][col]['text'] = player
    buttons[row][col]['state'] = 'disabled'

def on_click(row, col):
    global player_turn
    if board[row][col] == EMPTY and player_turn:
        make_move(row, col, HUMAN)
        if check_winner(board, HUMAN):
            end_game("You win!")
            return
        elif is_draw(board):
            end_game("It's a draw!")
            return
        player_turn = False
        root.after(300, ai_move)

def ai_move():
    global player_turn
    best_score = float('inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                score = minimax(board, 0, True)
                board[i][j] = EMPTY
                if score < best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        make_move(best_move[0], best_move[1], AI)
        if check_winner(board, AI):
            end_game("AI wins!")
        elif is_draw(board):
            end_game("It's a draw!")
    player_turn = True

def minimax(temp_board, depth, is_maximizing):
    if check_winner(temp_board, HUMAN):
        return 1
    if check_winner(temp_board, AI):
        return -1
    if is_draw(temp_board):
        return 0

    if is_maximizing:  # Human
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if temp_board[i][j] == EMPTY:
                    temp_board[i][j] = HUMAN
                    score = minimax(temp_board, depth + 1, False)
                    temp_board[i][j] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:  # AI
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if temp_board[i][j] == EMPTY:
                    temp_board[i][j] = AI
                    score = minimax(temp_board, depth + 1, True)
                    temp_board[i][j] = EMPTY
                    best_score = min(score, best_score)
        return best_score

def check_winner(b, player):
    for i in range(3):
        if all(b[i][j] == player for j in range(3)) or all(b[j][i] == player for j in range(3)):
            return True
    if all(b[i][i] == player for i in range(3)) or all(b[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(b):
    return all(b[i][j] != EMPTY for i in range(3) for j in range(3))

def end_game(message):
    messagebox.showinfo("Game Over", message)
    root.quit()

# Initialize the GUI
root = tk.Tk()
root.title("Tic-Tac-Toe (Human Maximizer, AI Minimizer)")

for i in range(3):
    for j in range(3):
        btn = tk.Button(root, text='', font=('Arial', 40), width=5, height=2,
                        command=lambda row=i, col=j: on_click(row, col))
        btn.grid(row=i, column=j)
        buttons[i][j] = btn

root.mainloop()
