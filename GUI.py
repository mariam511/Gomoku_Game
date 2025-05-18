import tkinter as tk
from tkinter import simpledialog, messagebox
import math

CELL_SIZE = 30
STONE_RADIUS = CELL_SIZE // 2 - 2

# Setup root for dialogs first
root = tk.Tk()
root.withdraw()

def playerChoice(p):
    return 'B' if p == 'W' else 'W'

# Get Size From User
while True:
    getSize = simpledialog.askstring("Gomoku Size", "Enter Gomoku Size (15 or 19):")
    if getSize in ['15', '19']:
        gomokuSize = int(getSize)
        break
    else:
        messagebox.showerror("Invalid Input", "Please enter size 15 or 19 only ^_^ ")

while True:
    mode = simpledialog.askstring("Choose Game Mode", "Choose game mode: 'HumanVsAi' or 'AIvsAI' or 'HumanVSHuman':")
    if mode and mode.lower() in ['humanvsai', 'aivsai','humanvshuman']:
        mode = mode.lower()
        break
    else:
        messagebox.showerror("Invalid input. Please type 'HumanVsAi' or 'AIvsAI'or 'HumanVSHuman'.")
        
# Ask To Choose AI
chooseAI = None
if mode == 'humanvsai':
    while True:
        chooseAI = simpledialog.askstring("Choose AI", "Choose which AI to play against (Minimax OR Alpha-beta): ")
        if chooseAI and chooseAI.lower() in ['minimax', 'alpha-beta']:
            chooseAI = chooseAI.lower()
            break


# Ask player symbol
while True:
    player1 = simpledialog.askstring("Player 1", "Choose your symbol (B or W):")
    if player1 and player1.upper() in ['B', 'W']:
        player1 = player1.upper()
        break
    else:
        messagebox.showerror("Invalid Input", "Please enter B or W.")

player2 = playerChoice(player1)
# player2 = 'B' if player1 == 'W' else 'W'
current_player = player1

# Game setup
def InitializeGomoku():
    gomokuBoard = []
    for i in range(gomokuSize):
        row = []
        for j in range(gomokuSize):
            row.append('*')
        gomokuBoard.append(row)
    return gomokuBoard

def checkWinner(goBoard, player):
    for row in range(gomokuSize):
        for col in range(gomokuSize):
            if goBoard[row][col] != player:
                continue
            # Check Horizontal
            if col <= gomokuSize - 5:
                win = True
                for k in range(5):
                    if goBoard[row][col + k] != player:
                        win = False
                        break
                if win: 
                    return True
                
            # Check Vertical
            if row <= gomokuSize - 5:
                win = True
                for k in range(5):
                    if goBoard[row + k][col] != player:
                        win = False
                        break
                if win: 
                    return True
                
            # Check Diagonal
            if row <= gomokuSize - 5 and col <= gomokuSize - 5:
                win = True
                for k in range(5):
                    if goBoard[row + k][col + k] != player:
                        win = False
                        break
                if win: 
                    return True
                
            # Check reverse Diagonal
            if row <= gomokuSize - 5  and col >= 4:
                win = True
                for k in range(5):
                    if goBoard[row + k][col - k] != player:
                        win = False
                        break
                if win: 
                    return True

def checkDraw(goBoard):
    for row in goBoard:
        for cell in row:
            if cell == '*':
                return False
    return True
def evaluate(board, player):
    opponent = playerChoice(player)
    score = 0
    size = len(board)
    directions = [(0,1), (1,0), (1,1), (1,-1)]

    def evaluate_line(r, c, dr, dc):
        nonlocal score
        player_count = 0
        opponent_count = 0
        empty_count = 0
        for i in range(5):
            nr, nc = r + i * dr, c + i * dc
            if not (0 <= nr < size and 0 <= nc < size):
                return
            if board[nr][nc] == player:
                player_count += 1
            elif board[nr][nc] == opponent:
                opponent_count += 1
            else:
                empty_count += 1
        if player_count > 0 and opponent_count > 0:
            return  
        if player_count == 5:
            score += 100000
        elif player_count == 4 and empty_count == 1:
            score += 10000
        elif player_count == 3 and empty_count == 2:
            score += 1000
        elif player_count == 2 and empty_count == 3:
            score += 100
        elif opponent_count == 5:
            score -= 100000
        elif opponent_count == 4 and empty_count == 1:
            score -= 9000
        elif opponent_count == 3 and empty_count == 2:
            score -= 800
        elif opponent_count == 2 and empty_count == 3:
            score -= 80

    for r in range(size):
        for c in range(size):
            for dr, dc in directions:
                evaluate_line(r, c, dr, dc)
    return score

# ordering moves according to their priorities
def orderedMoves(board):
    size = len(board)
    empty_cells = []
    for row in range(size):
        for col in range(size):
            if board[row][col] == '*':
                score = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        r, c = row + dr, col + dc
                        if 0 <= r < size and 0 <= c < size:
                            if board[r][c] != '*':  
                                score += 1
                empty_cells.append(((row, col), score))
    empty_cells.sort(key=lambda x: -x[1])
    return [pos for pos, _ in empty_cells]


def minimax(board, depth, maximizing, player):
    if checkWinner(board, 'B'):
        return 1000 if player == 'B' else -1000
    if checkWinner(board, 'W'):
        return 1000 if player == 'W' else -1000
    if checkDraw(board) or depth == 0:
        return evaluate(board, player)

    opponent = playerChoice(player)
    best = -math.inf if maximizing else math.inf

    
    for i,j in orderedMoves(board):
        board[i][j] = player if maximizing else opponent
        value = minimax(board, depth - 1, not maximizing, player)
        board[i][j] = '*'
        if maximizing:
            best = max(best, value)
        else:
            best = min(best, value)
    return best
# AI Move
def bestMove(board, player, depth=2, last_move=None):
    best_score = -math.inf
    move = (-1, -1)
    for i,j in orderedMoves(board):
        board[i][j] = player
        score = minimax(board, depth - 1, False, player)
        board[i][j] = '*'
        if score > best_score:
            best_score = score
            move = (i, j)
    return move
# # # Alpha-beta Algorithm
#minimax_alpha_beta algorithm
def minimax_alpha_beta(node, depth, isMaximizingPlayer, alpha, beta, player):
    if checkWinner(node, 'B'):
        return 1000 if player == 'B' else -1000
    if checkWinner(node, 'W'):
        return 1000 if player == 'W' else -1000
    if checkDraw(node) or depth == 0:
        return evaluate(node, player)
    
    opponent = playerChoice(player)

    if isMaximizingPlayer:
        bestVal = -math.inf
        for row, col in orderedMoves(node):  
            node[row][col] = player
            value =  minimax_alpha_beta(node, depth -1, False, alpha, beta, player)
            node[row][col] = '*'
            bestVal = max(bestVal, value)
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal

    else:
        bestVal = math.inf
        for row, col in orderedMoves(node): 
            node[row][col] = opponent
            value = minimax_alpha_beta(node, depth - 1, True, alpha, beta, player)
            node[row][col] = '*'
            bestVal = min(bestVal, value)
            beta = min(beta, bestVal)
            if beta <= alpha:
                break
        return bestVal
    
#best move minimax_alpha_beta 
def bestMove_alpha_beta(board, player, depth=2):
    best_score = -math.inf
    move = (-1, -1)
    alpha = -math.inf
    beta = math.inf
    for i, j in orderedMoves(board):
        board[i][j] = player
        score = minimax_alpha_beta(board, depth - 1, False, alpha, beta, player)
        board[i][j] = '*'
        if score > best_score:
            best_score = score
            move = (i, j)
        alpha = max(alpha, best_score)
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

    if mode == 'humanvsai' and current_player != player1:
        return
    
    if mode == 'aivsai':
        return

    board[row][col] = current_player
    gui.draw_stones()

    if checkWinner(board, current_player):
        messagebox.showinfo("Game Over", f" Player ({current_player}) wins!")
        gui.canvas.unbind("<Button-1>")
        return

    if checkDraw(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        gui.canvas.unbind("<Button-1>")
        return

    current_player = playerChoice(current_player)

    if mode == 'humanvsai' and current_player == player2:
        gui.root.after(100, ai_move)

def ai_move():
    global current_player, gui
    
    if chooseAI == 'minimax':
        if current_player == player1:
            row, col = bestMove(board, current_player)  # Minimax
        else:
            row, col = bestMove(board, current_player)  # Minimax for player2 as well
    elif chooseAI == 'alpha-beta':
        if current_player == player1:
            row, col = bestMove_alpha_beta(board, current_player)  # Alpha-Beta
        else:
            row, col = bestMove_alpha_beta(board, current_player)
            

    if current_player == player1:
        row, col = bestMove(board, current_player)  # Minimax
    else:
        row, col = bestMove_alpha_beta(board, current_player) # Alpha-Beta
    
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
    
    if mode == 'aivsai':
        gui.root.after(300, ai_move)

# Start GUI
root = tk.Tk()
root.title("Gomoku Game")
gui = GomokuGUI(root, gomokuSize, board, move_handler)
if mode == 'humanvsai' and current_player == player2:
    gui.root.after(1000, ai_move)
root.deiconify()

if mode == 'aivsai':
    gui.canvas.unbind("<Button-1>")
    gui.root.after(1000, ai_move)
root.mainloop()
