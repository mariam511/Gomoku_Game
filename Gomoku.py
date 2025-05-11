# Shahd Elnassag

# Get Size From User Accept Input
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
                
# check if draw
def checkDraw(goBoard):
    for row in goBoard:
        for cell in row:
            if cell == '*':
                return False
    return True
# Test code above Human VS Human
def testGame():
    board = InitializeGomoku()
        # Ask first player to choose B or W
    while True:
        player1 = input("Player 1, choose your symbol (B or W): ").strip().upper()
        if player1 in ['B', 'W']:
            break
        else:
            print("Invalid choice. Please enter B or W.")

    player2 = playerChoice(player1)

    print(f" Player 1 is '{player1}' and Player 2 is '{player2}'")
    
    
    current_player = 'B'  

    while True:
        drawGomoku(board)

        if current_player == player1:
            print("Player 1's Plays:")
        else:
            print("Player 2's Plays:")

        getMove(board, current_player)

        if checkWinner(board, current_player):
            drawGomoku(board)
            winner = "Player 1" if current_player == player1 else "Player 2"
            print(f"{winner} ({current_player}) wins the game!")
            break

        if checkDraw(board):
            drawGomoku(board)
            print("It's a draw!")
            break

        current_player = playerChoice(current_player)
    
    
    

# Start the game
if __name__ == "__main__":
    testGame()
