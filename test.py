from game import *

class ai():

	def __init__(self):

		self.max_depth = 3
		self.my_color = 'w'

	def Get_Current_State(self, game):

		self.state = game.state
        self.possible_moves = game.possible_moves
		self.wK_pos = game.wK_pos
        self.bK_pos = game.bK_pos
        self.wK_moved = game.wK_moved
        self.wKR_moved = game.wKR_moved
        self.wQR_moved = game.wQR_moved
        self.wcastled = game.wcastled
        self.bK_moved = game.bk_moved
        self.bKR_moved = game.bKR_moved
        self.bQR_moved = game.bQR_moved
        self.bcastled = game.bcastled
        self.num_wQ = game.num_wQ
        self.num_bQ = game.num_bQ
        self.actual_moves_made = game.actual_moves_made
        self.last_move = game.last_move
        self.turn = game.turn
        self.current_legal_moves = game.legal_moves



	def AB_Select_Move(self):

		alpha = float('-inf')
		beta = float('inf')

		max_value = self.Max_Value(self.state, alpha, beta)
		
		return move

	def Max_Value(self, state, alpha, beta):

		if Cutoff_Test(state):
			return self.Eval


	def Min_Value(self, state, alpha, beta):
		pass

	def Eval(state):

		control = 0

		for item in state.values():

			control += item.control

		if my_color == 'b':

			return -1*control

		else:
			return control




	def cutoff_test(self, depth):


		pass



		