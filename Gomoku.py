# Shahd Elnassag

import math
# Get Size From User
while True:
    getSize = input("Enter Gomoku Size 15 OR 19: " ).strip()
    if getSize in ['15','19']:
        gomokuSize = int(getSize)
        break
    else:
        print("Invalid Size. Please Enter Size 15 or 19 Only ^_^ ")

# Initialize Gomoku (Game State Representation)
def InitializeGomoku():
    gomokuBoard = []
    
    for i in range(gomokuSize):
        row = []
        for j in range(gomokuSize):
            row.append('*')
        gomokuBoard.append(row)
    return gomokuBoard
        
# Draw Gomoku Board (Formatted Output)
def drawGomoku(gomokuBoard):
    for i in range(len(gomokuBoard)):
        for j in range(len(gomokuBoard[i])):
            print(gomokuBoard[i][j], end= ' ')
        print()
    print()

# Accept Input from user and Move Generation
def getMove(goBoard,player):
    while True:
        move = input(f"{player}'s move (row,col): ")
        move = move.strip() # remove white spaces
        try:
            row,col = [int(x) for x in move.split(',')]
            if 0 <= row < gomokuSize and 0 <= col < gomokuSize:
                if goBoard[row][col] == '*':
                    goBoard[row][col] = player
                    return
                else:
                    print("Invalid Move , Please Try again")
            else:
                print("Move out of bounds, Please try again")
        except ValueError:
            print("Invalid Format, Enter row and col as (2,2)")

# if use choose B make AI W and via vers
def playerChoice(p):
    return 'B' if p == 'W' else 'W'

# Game Engine (Gomoku Rules)
def checkWinner(goBoard,player):
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

# Check if draw
def checkDraw(goBoard):
    for row in goBoard:
        for cell in row:
            if cell == '*':
                return False
    return True
# Gomoku Game with Human vs Human or Human vs AI (Minimax) (Josiane Usama Version)
# Minimax Evaluation Function
def evaluate(board, player):
    opponent = playerChoice(player)
    score = 0

    def count_sequence(r, c, dr, dc, symbol):
        count = 0
        for _ in range(5):
            if 0 <= r < gomokuSize and 0 <= c < gomokuSize and board[r][c] == symbol:
                count += 1
            r += dr
            c += dc
        return count

    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for row in range(gomokuSize):
        for col in range(gomokuSize):
            for dr, dc in directions:
                if count_sequence(row, col, dr, dc, player) == 5:
                    return 1000
                if count_sequence(row, col, dr, dc, opponent) == 5:
                    return -1000
    return score


# Minimax Algorithm
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
                if maximizing:
                    best = max(best, value)
                else:
                    best = min(best, value)
    return best

# Best Move for AI
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

# Main Game Loop
def startGame():
    board = InitializeGomoku()
        # Ask first player to choose Human vs Human or Human vs AI
    while True:
        mode = input("Choose game mode: 'Human' or 'AI': ").strip().lower()
        if mode in ['human', 'ai']:
            break
        else:
            print("Invalid input. Please type 'Human' or 'AI'.")

    while True:
        player1 = input("Player 1, choose your symbol (B or W): ").strip().upper()
        if player1 in ['B', 'W']:
            break
        else:
            print("Invalid choice. Please enter B or W.")
    
    player2 = playerChoice(player1)
    print(f"Player 1 is '{player1}' and Player 2 is '{player2}'")

    current_player = player1

    while True:
        drawGomoku(board)
        if current_player == player1:
            print("Player 1's Turn:")
            getMove(board, current_player)
        else:
            if mode == 'human':
                print("Player 2's Turn:")
                getMove(board, current_player)
            else:
                print("AI is thinking...")
                row, col = bestMove(board, current_player)
                board[row][col] = current_player
                print(f"AI played at ({row},{col})")

        if checkWinner(board, current_player):
            drawGomoku(board)
            if current_player == player1:
                print(f"Player 1 ({player1}) wins!")
            elif mode == 'human':
                print(f"Player 2 ({player2}) wins!")
            else:
                print(f"AI ({player2}) wins!")
            break

        if checkDraw(board):
            drawGomoku(board)
            print("It's a draw!")
            break

        current_player = playerChoice(current_player)

# Start the game
if __name__ == "__main__":
    startGame()
