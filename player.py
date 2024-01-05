import board
import random
import math

# The aim of this coursework is to implement the minimax algorithm to determine the next move for a game of Connect.
# The goal in Connect is for a player to create a line of the specified number of pieces, either horizontally, vertically or diagonally.
# It is a 2-player game with each player having their own type of piece, "X" and "O" in this instantiation.
# You will implement the strategy for the first player, who plays "X". The opponent, who always goes second, plays "O".
# The number of rows and columns in the board varies, as does the number of pieces required in a line to win.
# Each turn, a player must select a column in which to place a piece. The piece then falls to the lowest unfilled location.
# Rows and columns are indexed from 0. Thus, if at the start of the game you choose column 2, your piece will fall to row 0 of column 2. 
# If the opponent also selects column 2 their piece will end up in row 1 of column 2, and so on until column 2 is full (as determined
# by the number of rows). 
# Note that board locations are indexed in the data structure as [row][column]. However, you should primarily be using checkFull(), 
# checkSpace() etc. in board.py rather than interacting directly with the board.gameBoard structure.
# It is recommended that look at the comments in board.py to get a feel for how it is implemented. 
#
# Your task is to complete the two methods, 'getMove()' and 'getMoveAlphaBeta()'.
#
# getMove() should implement the minimax algorithm, with no pruning. It should return a number, between 0 and (maxColumns - 1), to
# select which column your next piece should be placed in. Remember that columns are zero indexed, and so if there are 4 columns in
# you must return 0, 1, 2 or 3. 
#
# getMoveAlphaBeta() should implement minimax with alpha-beta pruning. As before, it should return the column that your next
# piece should be placed in.
#
# The only imports permitted are those already imported. You may not use any additional resources. Doing so is likely to result in a 
# mark of zero. Also note that this coursework is NOT an exercise in Python proficiency, which is to say you are not expected to use the
# most "Pythonic" way of doing things. Your implementation should be readable and commented appropriately. Similarly, the code you are 
# given is intended to be readable rather than particularly efficient or "Pythonic".
#
# IMPORTANT: You MUST TRACK how many nodes you expand in your minimax and minimax with alpha-beta implementations.
# IMPORTANT: In your minimax with alpha-beta implementation, when pruning you MUST TRACK the number of times you prune.
class Player:

	def __init__(self, name):
		self.name = name
		self.numExpanded = 0 # Use this to track the number of nodes you expand
		self.numPruned = 0 # Use this to track the number of times you prune
		self.iterative = False # Is set to True when running iterative deepening
		self.numExpandedPerMove = 0 # Tracks the number of nodes expanded per move
		self.transposition = True # Set to True/False to enable/disable transposition table caching
		self.table = {} # Transposition table
		self.cacheHits = 0 # Tracks the number of times the transposition table finds a match

	def getMove(self, gameBoard):
		self.numExpandedPerMove = 0
		if self.name == 'X':
			return self.minimax(gameBoard, -1, True)[0] # Set depth to -1 to run a full search (no depth cutoff)
			# return self.minimaxIterative(gameBoard, True) # Uncomment this to run iterative deepening
		else:
			return self.minimax(gameBoard, -1, False)[0] # For player 2 minimax AI
			# return self.minimaxIterative(gameBoard, False) # Uncomment this to run iterative deepening for player 2

	def getMoveAlphaBeta(self, gameBoard):
		self.numExpandedPerMove = 0
		if self.name == 'X':
			return self.minimaxAB(gameBoard, -1, True, -math.inf, math.inf)[0] # Set depth to -1 to run a full search (no depth cutoff)
			# return self.minimaxABIterative(gameBoard, True) # Uncomment this to run iterative deepening
		else:
			return self.minimaxAB(gameBoard, -1, False, -math.inf, math.inf)[0] # For player 2 minimaxAB AI
			# return self.minimaxABIterative(gameBoard, False) # Uncomment this to run iterative deepening for player 2

	def minimaxIterative(self, gameBoard, maxingPlayer):
		self.iterative = True
		self.transposition = False # Disabled due to issues with iterative deepening
		limit = 10000 # Limit on the number of nodes expanded per move
		depth = 2 # Starting depth
		column = random.randint(0, gameBoard.numColumns - 1)
		while self.numExpandedPerMove < limit and depth <= gameBoard.numColumns * gameBoard.numRows: # Run until the limit is reached/exceeded or the max depth is reached (width * height of board)
			column = self.minimax(gameBoard, depth, maxingPlayer)[0]
			print(f"Depth {depth}, {self.numExpandedPerMove} nodes expanded, column {column}")
			depth += 1
		return column

	def minimaxABIterative(self, gameBoard, maxingPlayer):
		self.iterative = True
		self.transposition = False
		limit = 10000
		depth = 2
		column = random.randint(0, gameBoard.numColumns - 1)
		while self.numExpandedPerMove < limit and depth <= gameBoard.numColumns * gameBoard.numRows:
			column = self.minimaxAB(gameBoard, depth, maxingPlayer, -math.inf, math.inf)[0]
			print(f"Depth {depth}, {self.numExpandedPerMove} nodes expanded, column {column}")
			depth += 1
		return column

	def minimax(self, gameBoard, depth, maxingPlayer):
		if self.transposition: # Check if transposition table is enabled
			index = str(gameBoard.gameBoard)
			if index in self.table: # Check if board state is in transposition table
				self.cacheHits += 1
				return self.table[index][0], self.table[index][1] # Return best move and score from table

		if depth == 0 or gameBoard.checkWin(): # Check if win or reached depth limit
			if gameBoard.lastPlay[2] == 'X': # Check if maximising player won
				if depth < 0:
					return None, 1 # Return 1 for maximising player (no depth limit)
				else:
					return None, depth # Higher score for shallower depths to encourage faster wins for maximising player
			else:
				if depth < 0:
					return None, -1 # Return -1 for minimising player (no depth limit)
				else:
					return None, -depth # Lower score for shallower depths to encourage faster wins for minimising player
		if gameBoard.checkFull():
			return None, 0

		self.numExpanded += 1
		self.numExpandedPerMove += 1
		maxCol = gameBoard.numColumns
		maxRow = gameBoard.numRows
		colOrder = []
		for i in range(maxCol):
			colOrder.append(math.ceil(maxCol // 2 + (1 - 2 * (i % 2)) * (i + 1) // 2)) # Order columns by middle first, then alternate
		if depth > 0:
			depth = depth - 1

		if maxingPlayer:
			maxEval = -math.inf
			column = random.randint(0, maxCol - 1)
			for col in colOrder:
				if gameBoard.colFills[col] < maxRow:
					temp = gameBoard.copy()
					temp.addPiece(col, 'X')
					eval = self.minimax(temp, depth, False)[1]
					if eval > maxEval:
						column = col
						maxEval = eval
			if self.transposition:
				self.table[index] = [column, maxEval] # Add board state with best move and score to transposition table
			return column, maxEval
		else:
			minEval = math.inf
			column = random.randint(0, maxCol - 1)
			for col in colOrder:
				if gameBoard.colFills[col] < maxRow:
					temp = gameBoard.copy()
					temp.addPiece(col, 'O')
					eval = self.minimax(temp, depth, True)[1]
					if eval < minEval:
						column = col
						minEval = eval
			if self.transposition:
				self.table[index] = [column, minEval]
			return column, minEval

	def minimaxAB(self, gameBoard, depth, maxingPlayer, alpha, beta):
		if self.transposition:
			index = str(gameBoard.gameBoard)
			if index in self.table:
				self.cacheHits += 1
				return self.table[index][0], self.table[index][1]

		if depth == 0 or gameBoard.checkWin(): # Check if win or reached depth limit
			if gameBoard.lastPlay[2] == 'X': # Check if maximising player won
				if depth < 0:
					return None, 1 # Return 1 for maximising player (no depth limit)
				else:
					return None, depth # Higher score for shallower depths to encourage faster wins for maximising player
			else:
				if depth < 0:
					return None, -1
				else:
					return None, -depth

		if gameBoard.checkFull():
			return None, 0

		self.numExpanded += 1
		self.numExpandedPerMove += 1
		maxCol = gameBoard.numColumns
		maxRow = gameBoard.numRows
		colOrder = []
		for i in range(maxCol):
				colOrder.append(math.ceil(maxCol // 2 + (1 - 2 * (i % 2)) * (i + 1) // 2))
		if depth > 0:
				depth = depth - 1

		if maxingPlayer:
			maxEval = -math.inf
			column = random.randint(0, maxCol - 1)
			for col in colOrder:
				if gameBoard.colFills[col] < maxRow:
					temp = gameBoard.copy()
					temp.addPiece(col, 'X')
					eval = self.minimaxAB(temp, depth, False, alpha, beta)[1]
					if eval > maxEval:
						column = col
						maxEval = eval
					alpha = max(alpha, maxEval)
					if beta <= alpha:
						self.numPruned += 1
						break
			if self.transposition:
				self.table[index] = [column, maxEval]
			return column, maxEval
		else:
			minEval = math.inf
			column = random.randint(0, maxCol - 1)
			for col in colOrder:
				if gameBoard.colFills[col] < maxRow:
					temp = gameBoard.copy()
					temp.addPiece(col, 'O')
					eval = self.minimaxAB(temp, depth, True, alpha, beta)[1]
					if eval < minEval:
						column = col
						minEval = eval
					beta = min(beta, minEval)
					if beta <= alpha:
						self.numPruned += 1
						break
			if self.transposition:
				self.table[index] = [column, minEval]
			return column, minEval
