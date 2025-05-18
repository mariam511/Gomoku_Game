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


# Get Smart Move return nearest empty positions 5 * 5 gride
def smartMove(goBoard, last_move=None):
    positions = set()
    if last_move:
        last_row, last_col = last_move
        for i in range(last_row - 2, last_row + 3):
            for j in range(last_col - 2, last_col + 3):
                if 0 <= i < gomokuSize and 0 <= j < gomokuSize and goBoard[i][j] == '*':
                    positions.add((i,j))
    else:
        # Fallback to general scan
        for i in range(gomokuSize):
            for j in range(gomokuSize):
                if goBoard[i][j] != '*':
                    for x in range(-2,3):
                        for y in range(-2,3):
                            Posi = i + x 
                            Posj = j + y
                            if 0 <= Posi < gomokuSize and 0 <= Posj < gomokuSize and goBoard[Posi][Posj] == '*':
                                positions.add((Posi,Posj))
    if not positions:
        center = gomokuSize // 2
        return {(center, center)}
    return positions


# Gomoku Game with Human vs Human or Human vs AI (Minimax) (Josiane Usama Version)
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
    # Loop inside Positions from SmartMove to reduce time to get decition
    for i,j in smartMove(board):
        board[i][j] = player if maximizing else opponent
        value = minimax(board, depth - 1, not maximizing, player)
        board[i][j] = '*'
        if maximizing:
            best = max(best, value)
        else:
            best = min(best, value)
    return best

# Best Move for AI minimax
def bestMove(board, player, depth=2):
    best_score = -math.inf
    move = (-1, -1)
    for i,j in smartMove(board):
        board[i][j] = player
        score = minimax(board, depth - 1, False, player)
        board[i][j] = '*'
        if score > best_score:
            best_score = score
            move = (i, j)
    return move


# # #Alpha-beta Algorithm

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


# Main Game Loop
def startGame():
    board = InitializeGomoku()
    while True:
        mode = input("Choose game mode: 'HumanVsAi' or 'AIvsAI' or 'HumanVSHuman': ").strip().lower()
        if mode in ['humanvsai', 'aivsai','humanvshuman']:
            break
        else:
            print("Invalid input. Please type 'HumanVsAi' or 'AIvsAI'or 'HumanVSHuman'.")
    # Ask To Choose AI
    chooseAI = None
    if mode == 'humanvsai':
        while True:
            chooseAI = input("Choose which AI to play against (Minimax OR alpha-beta): ").strip().lower()
            if chooseAI in ['minimax', 'alpha-beta']:
                break
            else:
                print("Invalid choice. Please enter 'Minmax' or 'alpha-beta'.")

    while True:
        player1 = input("Choose your symbol for player 1(B or W): ").strip().upper()
        if player1 in ['B', 'W']:
            break
        else:
            print("Invalid choice. Please enter B or W.")
    
    player2 = playerChoice(player1)
    print(f"Player 1 is '{player1}' and Player 2 is '{player2}'")

    current_player = player1

    while True:
        drawGomoku(board)
        if mode == 'humanvshuman':
            if current_player == player1:
                print("Player 1's Turn:")
                getMove(board, current_player)
            else:
                print("Player 2's Turn:")
                getMove(board, current_player)
        if mode == 'humanvsai':
            if current_player == player1:
                print("Player 1's Turn:")
                getMove(board, current_player)
            else:
                if chooseAI == 'minimax':
                    print("MinMax is thinking...")
                    row, col = bestMove(board, current_player)
                    board[row][col] = current_player
                    print(f"Minmax played at ({row},{col})")
                else:
                    print("Alpha-beta is thinking...")
                    row, col = bestMove_alpha_beta(board, current_player)
                    board[row][col] = current_player
                    print(f"Alpha-beta played at ({row},{col})")
        else:  # AI vs AI
            if current_player == player1:
                print("Minimax AI's Turn:")
                row, col = bestMove(board, current_player)
            else:
                print("Alpha-Beta AI's Turn:")
                row, col = bestMove_alpha_beta(board, current_player)
            board[row][col] = current_player
            print(f"{current_player} AI played at ({row},{col})")

        if checkWinner(board, current_player):
            drawGomoku(board)
            print(f"{current_player} wins!")
            break

        if checkDraw(board):
            drawGomoku(board)
            print("It's a draw!")
            break

        current_player = playerChoice(current_player)

# Start the game
if __name__ == "__main__":
    startGame()
