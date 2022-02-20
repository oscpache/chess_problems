# Source worth checking out: https://bradfieldcs.com/algos/graphs/knights-tour/
import random
import numpy as np


''' Describe Warnsdorff heuristic here '''
class WarnsdorffHeuristic(object):
	class knight:
		# A chess box is represented by a coordinate (x,y)
		'''
		The knight can make 4 possible movement choices (assuming it's in the center of the board)
		given an axis (e.g x) but since every movement can be made 1 or 2 boxes ahead, it 
		gives a total of 8 possible movement choices per axis. However, a knigth movement considering
		both axes needs to be a pair (p,q) such that if p == (+-)1 then q == (+-)2 or 
		if p == (+-)2 then q == (+-)1.
		According to mx and my definitions:
			~ (mx = -1,my = 2) means: move one box left and two boxes up  
			~ (mx = 2,mx = -1) means: move two boxes right and one box down  
		'''
		mx = [1,1,2,2,-1,-1,-2,-2] # movement in x-axis
		my = [2,-2,1,-1,2,-2,1,-1] # movement in y-axis

	def __init__(self, board_size=8):
		self.N = board_size
		self.trials = 0 # how many times the search process was restarted 
		self.T = np.empty((self.N, self.N), dtype=np.int8) # init chess board 
		self.T[:,:] = -1 # -1 means unvisited
		self.xo = random.randint(0, self.N-1) # initial position (randomly determine)
		self.yo = random.randint(0, self.N-1)

	def is_inside_board(self, x, y):
		'''
		This method determines if the box represented by coordinate (x,y) is valid 
		(it's inside the NxN chess board).
		'''
		if (x >= 0 and y >= 0) and (x < self.N and y < self.N):
			return True
		else:
			return False

	def is_box_free_and_valid(self, x, y):
		'''
		This method determines if the box represented by coordinate (x,y) is free and valid, 
		that is to say, it's not been visited and (x,y) exits. 
		''' 
		# T stands for Table (represents the chess board). All unvisited boxes are marked with -1
		if self.is_inside_board(x, y) and self.T[x, y] < 0:  
			return True
		else:
			return False

	def get_box_degree(self, x, y): 
		'''
		This method computes the degree of a chess box; think every box as a node and every 
		valid movement as an edge that joins two nodes. The resulting structure is known 
		as a graph and the degree of a node are all the outcoming edges from such node. 
		''' 
		degree = 0
		for i in range(0, len(self.knight.mx)):
			if self.is_box_free_and_valid(x + self.knight.mx[i], y + self.knight.my[i]):
				degree += 1
		return degree

	def next_move(self, x, y):
		'''
		This method defines the next movement to carry out. It returns a tuple of the form 
		(bool,int,int) indicating if the next movement is feasible or not along with the 
		coordinates.
		'''
		move_id = -1 # init it with a special mark 
		min_degree = len(self.knight.mx)+1 # max possible grade plus one (to mimic infinity)
		start = random.randint(0,len(self.knight.mx)-1) # choose the first movement to try out (randomly)

		# try out all possible movements  
		for k in range(0, len(self.knight.mx)):
			i = (start + k) % len(self.knight.mx) # i can take any values in [0,1,2,...,7]
			nx = x + self.knight.mx[i] # new x coordenate 
			ny = y + self.knight.my[i] # new y coordenate
			degree = self.get_box_degree(nx, ny)
			if self.is_box_free_and_valid(nx, ny) and degree < min_degree:
				min_degree = degree
				move_id = i

		#if the -1 mark is found (meaning, there was not any box left to visit)
		if move_id == -1: # print("Go back")
			return False, x, y
		#define next move (the one that take us to the node/box with minimum degree)
		nx = x + self.knight.mx[move_id]
		ny = y + self.knight.my[move_id]
		self.T[nx, ny] = self.T[x, y] + 1 #mark new box 
		return True,nx, ny

	def is_origin(self, x, y):
		#This method tests whether (x,y) is the origin coordinate or not.
		for i in range(0,len(self.knight.mx)): 
			if (x + self.knight.mx[i] == self.xo) and (y + self.knight.my[i] == self.yo):
				return True
		return False

	def generate_tour(self):
		'''
		This method generate a candidate solution and returns such candidate along with a flag 
		indicating if such solution is feasible.
		'''	  
		# set origin: (xo,yo)
		x = self.xo
		y = self.yo 
		self.T[x,y] = 0 # first movement: the tour has just started   
		# Warnsdorff heuristic
		for i in range(0, self.N*self.N - 1):
			is_possible_next_move, x, y = self.next_move(x, y) # next_move returns a tuple(Bool,int,int)
			if not is_possible_next_move:
				return False,self.T
		if not self.is_origin(x, y): # the tour must end where it started, if not, return false
			return False, self.T
		else:
			return True, self.T

	def restart(self):  
		# restart the chess board configuration and initial position to try again 
		self.T[:,:] = -1 #-1 means unvisited
		self.xo = random.randint(0, self.N-1) # initial position (randomly determine)
		self.yo = random.randint(0, self.N-1)
		self.trials += 1

	def build(self):
		is_feasible,tour = self.generate_tour()
		while not is_feasible:
			self.restart()
			is_feasible,tour = self.generate_tour()
		return tour
