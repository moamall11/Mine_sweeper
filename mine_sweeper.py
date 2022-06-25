import random
import re

class Board:
	"""represents the board of the game"""
	def __init__(self,dim_size,num_bombs):
		self.dim_size=dim_size
		self.num_bombs=num_bombs
		self.board=self._make_new_board()
		self._assign_values()
		self.dug=set()

	def _make_new_board(self):
		"""returns the board with the bombs planted randomly"""
		#make the empty board.
		board=[[None for _ in range(self.dim_size)] \
		for _ in range(self.dim_size)]
		#start planting the bombs in random locations.
		bombs_planted=0
		while bombs_planted < self.num_bombs:
			#get a random location on the board.
			loc = random.randint(0,(self.dim_size**2)-1)
			#get its row and column.
			row = loc // self.dim_size
			col = loc % self.dim_size
			#if it already has a bomb planted 
			#then end the iteration and continue to the next one.
			if board[row][col] == '*':
				continue
			#else, plant a bomb.
			board[row][col]='*'
			bombs_planted+=1
		return board

	def _assign_values(self):
		"""assign values to each location depending on 
		the number of the neighboring bombs"""
		for r in range(0,self.dim_size):
			for c in range(0,self.dim_size):
				#if it's already a bomb we don't need to calculate anything.
				if self.board[r][c] == '*':
					continue
				self.board[r][c] = self._get_num_neighboring_bombs(r,c)

	def _get_num_neighboring_bombs(self,row,col):
		"""returns the number of the neighboring bombs"""
		num_neighboring_bombs = 0
		#make sure not to go out of bounds 
		#(don't exceed the limits of the board).
		for r in range(max(0,row - 1),min(self.dim_size,row + 2)):
			for c in range(max(0,col - 1),min(self.dim_size,col + 2)):
				#check all the neighboring locations 
				#except the actual location.
				if r == row and c == col:
					continue
				if self.board[r][c] == '*':
					num_neighboring_bombs += 1
		return num_neighboring_bombs

	def dig(self,row,col):
		"""returns False when you dig a bomb else returns True"""
		#add the location to the set of locations that you dug.
		self.dug.add((row,col))

		if self.board[row][col] == '*':
			return False
		#if there is a bomb nearby don't do anything.
		elif self.board[row][col] > 0:
			return True
		#else, dig all the neighboring locations.
		for r in range(max(0,row - 1),min(self.dim_size,row + 2)):
			for c in range(max(0,col - 1),min(self.dim_size,col + 2)):
				#no need to dig a location if it's already dug.
				if (r,c) in self.dug:
					continue
				self.dig(r,c)
		return True

	def __str__(self):
		"""when an instance of the class is printed 
		it will return this function (it will print the board)"""
		#make a new list for the board.
		visible_board=[[' ' for _ in range(self.dim_size)] \
		for _ in range(self.dim_size)]
		#go through all the locations of the new board.
		for r in range(0,self.dim_size):
			for c in range(0,self.dim_size):
				if (r,c) in self.dug:
					visible_board[r][c] = str(self.board[r][c])
		for r in range(0,self.dim_size):
			print(''.join(str(visible_board[r])))
		return ''


def play(dim_size,num_bombs):
	"""play the game"""
	board=Board(dim_size,num_bombs)
	safe=True
	#break the loop when there are no more places to dig other than bombs. 
	while len(board.dug) < (board.dim_size **2) - board.num_bombs:
		print(board)
		loc = re.split(',(//s)*',
			input("where would you like to dig? row,column "))
		row,col=int(loc[0]),int(loc[-1])
		#when the location is out of bounds.
		if row < 0 or row > board.dim_size or col > board.dim_size or col < 0:
			print("invalid location, try again.")
			continue
		safe=board.dig(row,col)
		#break the loop when the user digs a bomb.
		if not safe:
			break
	if safe:
		print("CONGRATULATIONS!! YOU WON!")
	else:
		print("sorry, you dug a bomb :(")
		board.dug=[(r,c) for r in range(board.dim_size)
		 for c in range(board.dim_size)]
		print(board)

if __name__=='__main__':
	play(5,5)
