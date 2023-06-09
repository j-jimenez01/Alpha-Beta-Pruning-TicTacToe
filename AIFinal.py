#creating the size of the board and setting it to empty
board = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
#following OOP and abp is abreviated for alpha beta pruining
class abp:
    #creating/displaying the gameBoard and filling in the spaces the player/bot choose to go
    def gameBoard(board):
      #player(X), bot(O) and if empty its (' ')
      chars = {1: 'X', -1: 'O', 0: ' '}
      row_sep = '\n---------------\n' #board lines
      row_strs = []
      print('---------------')#top row
      #creating the board and putting the players in the positions
      for row in board:
          cell_strs = [f' {chars[cell]} ' for cell in row]
          row_strs.append('|' + '||'.join(cell_strs) + '|')
      board_str = row_sep.join(row_strs)
      print(board_str)
       
    #checking if all possible scenarios where either the bot or player can win
    def checkingForWinner(board, player):
        #all possibilities for three in a row vertically, horizontally, and diagonally
        posibilities = [[board[0][0], board[0][1], board[0][2]],[board[1][0], board[1][1], board[1][2]],[board[2][0], board[2][1], board[2][2]],
                    [board[0][0], board[1][0], board[2][0]],[board[0][1], board[1][1], board[2][1]],[board[0][2], board[1][2], board[2][2]],
                    [board[0][0], board[1][1], board[2][2]],[board[0][2], board[1][1], board[2][0]]]
        #checking for 3 in a row to see if someone won
        if [player, player, player] in posibilities:
            return True
        return False

    #counting the amount of blank spots on the board
    def emptySpaces(board):
        es = []
        for x in range(len(board)):#looping through the rows
            for y in range(len(board[x])):#checking the open spots in each the row
                if board[x][y] == 0:#if the spot is open add it to the list
                    es.append([x, y])
        return es
    
    #having the player choose a spot on the board and handling edge cases incase the player doenst choose a good spot
    def player(board):
        #each position on the board for the user to choose and where it will be placed
        moves = {1: [0, 0], 2: [0, 1], 3: [0, 2], 
                 4: [1, 0], 5: [1, 1], 6: [1, 2],
                7: [2, 0], 8: [2, 1], 9: [2, 2]}
        while True:
            #using a try and catch block to handle error inputs so the code doesn't break
            try:
                #getting the users input as an integer to follow the board positions
                move = int(input('Enter a number between 1-9: '))
                if move < 1 or move > 9:#if user doesnt chose a number between 1-9
                    print('Choose a number between 1-9')
                elif not (moves[move] in abp.emptySpaces(board)):#if the spot they chose is taken
                    print('That spot is taken')
                else:#if they choose an open spot, it will be placed
                    board[moves[move][0]][moves[move][1]] = 1
                    break
            #if the user doesn't enter a number, the code wont break and tell the user to enter a number
            except(KeyError, ValueError):
                print('Must enter a number')

    #having the bot choose a move and placing it on the board
    def bot(board):
        result = abp.abpmm(board, len(abp.emptySpaces(board)), float('-inf'), float('inf'), -1)
        board[result[0]][ result[1]] = -1
    
    #alpha beta pruning algorithm for the bot to find the best spot on the board depending on the users placement
    def abpmm(board, depth, alpha, beta, player):
      # checking which player won and returning the score accordingly 
      if abp.checkingForWinner(board, 1) is True:
          return [None, None, 10]
      elif abp.checkingForWinner(board, -1) is True:
          return [None, None, -10]
      #returns a score of zero if the game has reached maximum depth
      elif depth == 0:
          return [None, None, 0]

      #if current player is maximing, best_score is set to -infinity
      #if current player is minizing, best_score is set to infinity 
      best_score = alpha if player == 1 else beta
      best_row = None
      best_col = None

      # Checks to see where the player can make a move and evaluates the resulting board
      for cell in abp.emptySpaces(board):
          # putting the player on the board
          board[cell[0]][cell[1]] = player
          # recursively calling the abpmm function to check the board state
          score = abp.abpmm(board, depth - 1, alpha, beta, -player)
          # removing the player from the position on the board
          board[cell[0]][cell[1]] = 0
        
          # If the current player is maximizing, updating decisions to perfrom alpha beta pruining 
          # to find the best position the bot thinks the player is going to make
          if player == 1:
              if score[2] > best_score:
                  best_score = score[2]
                  best_row = cell[0]
                  best_col = cell[1]
                  alpha = max(alpha, best_score)
              if beta <= alpha:
                  break
          # else the current player is minimizing, updating decisions to perfrom alpha beta pruining 
          # to find the best position the bot thinks it is going to make
          else:
              if score[2] < best_score:
                  best_score = score[2]
                  best_row = cell[0]
                  best_col = cell[1]
                  beta = min(beta, best_score)
              if beta <= alpha:
                  break
      #returning the row and column for the bot to be placed on
      return [best_row, best_col, best_score]

            
    #main
    def run():
        #printing the board with the numbers the player can choose to put the positions on
        print("---------------\n| 1 || 2 || 3 |\n---------------\n| 4 || 5 || 6 |\n---------------\n| 7 || 8 || 9 |\n---------------")
        currentPlayer = 1 #positive 1 means player and -1 means the bot
        #while the game ran out of spaces
        while not (len(abp.emptySpaces(board))==0):
            if currentPlayer == 1:#player's move
                abp.player(board)
                print("\nPlayer's move")
            else:#bot's move
                abp.bot(board)
                print("\nBot's Move")
            currentPlayer *= -1 #alternating between player
            abp.gameBoard(board)
            #chekcing if anyone won
            if (abp.checkingForWinner(board,-1) or abp.checkingForWinner(board,1)) is True:
                break
        #printing the winner or draw
        print('You Win' if abp.checkingForWinner(board, 1) else 'Bot Wins' if abp.checkingForWinner(board, -1) else 'Draw')
#end of the class

#calling the function in the class to run the code
abp.run()