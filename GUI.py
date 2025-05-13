import tkinter as tk
from tkinter import simpledialog, messagebox
import math

CELL_SIZE = 30
STONE_RADIUS = CELL_SIZE // 2 - 2

# Setup root for dialogs first
root = tk.Tk()
root.withdraw()

# Ask size
while True:
    getSize = simpledialog.askstring("Gomoku Size", "Enter Gomoku Size (15 or 19):")
    if getSize in ['15', '19']:
        gomokuSize = int(getSize)
        break
    else:
        messagebox.showerror("Invalid Input", "Please enter size 15 or 19 only.")

# Ask mode
while True:
    mode = simpledialog.askstring("Game Mode", "Choose game mode: Human or AI")
    if mode and mode.lower() in ['human', 'ai']:
        mode = mode.lower()
        break
    else:
        messagebox.showerror("Invalid Input", "Please enter 'Human' or 'AI'.")

# Ask player symbol
while True:
    player1 = simpledialog.askstring("Player 1", "Choose your symbol (B or W):")
    if player1 and player1.upper() in ['B', 'W']:
        player1 = player1.upper()
        break
    else:
        messagebox.showerror("Invalid Input", "Please enter B or W.")

player2 = 'B' if player1 == 'W' else 'W'
current_player = player1

# Game setup
def InitializeGomoku():
    return [['*' for _ in range(gomokuSize)] for _ in range(gomokuSize)]

def playerChoice(p):
    return 'B' if p == 'W' else 'W'

def checkWinner(goBoard, player):
    for row in range(gomokuSize):
        for col in range(gomokuSize):
            if goBoard[row][col] != player:
                continue
            if col <= gomokuSize - 5 and all(goBoard[row][col + k] == player for k in range(5)):
                return True
            if row <= gomokuSize - 5 and all(goBoard[row + k][col] == player for k in range(5)):
                return True
            if row <= gomokuSize - 5 and col <= gomokuSize - 5 and all(goBoard[row + k][col + k] == player for k in range(5)):
                return True
            if row <= gomokuSize - 5 and col >= 4 and all(goBoard[row + k][col - k] == player for k in range(5)):
                return True
    return False

def checkDraw(goBoard):
    return all(cell != '*' for row in goBoard for cell in row)

# Minimax logic
def evaluate(board, player):
    opponent = playerChoice(player)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    def count_sequence(r, c, dr, dc, symbol):
        count = 0
        for _ in range(5):
            if 0 <= r < gomokuSize and 0 <= c < gomokuSize and board[r][c] == symbol:
                count += 1
            r += dr
            c += dc
        return count

    for row in range(gomokuSize):
        for col in range(gomokuSize):
            for dr, dc in directions:
                if count_sequence(row, col, dr, dc, player) == 5:
                    return 1000
                if count_sequence(row, col, dr, dc, opponent) == 5:
                    return -1000
    return 0

def minimax(board, depth, maximizing, player):
    if checkWinner(board, 'B'):
        return 1000 if player == 'B' else -1000
    if checkWinner(board, 'W'):
        return 1000 if player == 'W' else -1000
    if checkDraw(board) or depth == 0:
        return evaluate(board, player)

    opponent = playerChoice(player)
    best = -math.inf if maximizing else math.inf

    for i in range(gomokuSize):
        for j in range(gomokuSize):
            if board[i][j] == '*':
                board[i][j] = player if maximizing else opponent
                value = minimax(board, depth - 1, not maximizing, player)
                board[i][j] = '*'
                best = max(best, value) if maximizing else min(best, value)
    return best

def bestMove(board, player, depth=2):
    best_score = -math.inf
    move = (-1, -1)
    for i in range(gomokuSize):
        for j in range(gomokuSize):
            if board[i][j] == '*':
                board[i][j] = player
                score = minimax(board, depth - 1, False, player)
                board[i][j] = '*'
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# GUI class
class GomokuGUI:
    def __init__(self, root, size, board, move_callback):
        self.root = root
        self.size = size
        self.board = board
        self.move_callback = move_callback
        self.canvas = tk.Canvas(root, width=size * CELL_SIZE, height=size * CELL_SIZE, bg="#DEB887")
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        for i in range(self.size):
            self.canvas.create_line(CELL_SIZE // 2, CELL_SIZE // 2 + i * CELL_SIZE,
                                    CELL_SIZE // 2 + (self.size - 1) * CELL_SIZE, CELL_SIZE // 2 + i * CELL_SIZE)
            self.canvas.create_line(CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2,
                                    CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2 + (self.size - 1) * CELL_SIZE)
        self.draw_stones()

    def draw_stones(self):
        self.canvas.delete("stone")
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] in ['B', 'W']:
                    self.draw_stone(i, j, self.board[i][j])

    def draw_stone(self, row, col, player):
        x = CELL_SIZE // 2 + col * CELL_SIZE
        y = CELL_SIZE // 2 + row * CELL_SIZE
        color = 'black' if player == 'B' else 'white'
        self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                x + STONE_RADIUS, y + STONE_RADIUS,
                                fill=color, tags="stone")

    def on_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 <= row < self.size and 0 <= col < self.size:
            self.move_callback(row, col)

# Main Game Logic
board = InitializeGomoku()

def move_handler(row, col):
    global current_player, gui
    if board[row][col] != '*':
        return

    if mode == 'ai' and current_player != player1:
        return

    board[row][col] = current_player
    gui.draw_stones()

    if checkWinner(board, current_player):
        messagebox.showinfo("Game Over", f"{'AI' if current_player == player2 and mode=='ai' else 'Player'} ({current_player}) wins!")
        gui.canvas.unbind("<Button-1>")
        return

    if checkDraw(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        gui.canvas.unbind("<Button-1>")
        return

    current_player = playerChoice(current_player)

    if mode == 'ai' and current_player == player2:
        gui.root.after(100, ai_move)

def ai_move():
    global current_player, gui
    row, col = bestMove(board, current_player)
    board[row][col] = current_player
    gui.draw_stones()

    if checkWinner(board, current_player):
        messagebox.showinfo("Game Over", f"AI ({current_player}) wins!")
        gui.canvas.unbind("<Button-1>")
        return

    if checkDraw(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        gui.canvas.unbind("<Button-1>")
        return

    current_player = playerChoice(current_player)

# Start GUI
root = tk.Tk()
root.title("Gomoku Game")
gui = GomokuGUI(root, gomokuSize, board, move_handler)
root.deiconify()
root.mainloop()
