from game import *
import copy
import operator
import pickle
import re

def recursive_items(dictionary):

	for key, value in dictionary.items():
		if type(value) is dict:
			yield (key, value)
			yield from recursive_items(value)
		else:
			yield (key, value)

class current_state():

    def __init__(self, game):

        self.board = game.state
        self.wK_pos = game.wK_pos
        self.bK_pos = game.bK_pos
        self.wK_moved = game.wK_moved
        self.wKR_moved = game.wKR_moved
        self.wQR_moved = game.wQR_moved
        self.wcastled = game.wcastled
        self.bK_moved = game.bK_moved
        self.bKR_moved = game.bKR_moved
        self.bQR_moved = game.bQR_moved
        self.bcastled = game.bcastled
        self.num_wQ = game.num_wQ
        self.num_bQ = game.num_bQ
        self.last_move = game.last_move
        self.turn = game.turn
        self.attributes = [self.wcastled, self.wK_moved, self.wKR_moved, self.wQR_moved,
                 self.bcastled, self.bK_moved, self.bKR_moved, self.bQR_moved]
        self.current_legal_moves = game.legal_moves
        self.actual_moves_made = game.actual_moves_made
        self.algebraic_state = ""
        self.value = 0


class ai(game):


	def __init__(self, game, in_depth, in_color):
		
		self.max_depth = in_depth
		self.my_color = in_color
		self.positions_seen = [game.state]
		self.possible_moves = game.possible_moves
		self.actual_moves_made = []
		self.memory = {}
		self.current_best = ""
		self.consciousness = {}



	def print_cache(self):

		#print(self.consciousness)
		print(self.memory)
		for position in self.positions_seen:
			self.Print_Board(position)

	def Algebraic_State(self, line):

		if not line:
			return ""

		name = ""
		for move in line:

			name += move[0]

		return name




	def AB_Select_Move(self, game):



		master_state = current_state(game)
		self.actual_moves_made = master_state.actual_moves_made
		
		temp_moves_made = self.actual_moves_made
		#print(temp_moves_made)
		#print(temp_moves_made)
		algebraic_state = self.Algebraic_State(self.actual_moves_made)
		mem_copy = copy.deepcopy(self.memory)
		for key, value in recursive_items(mem_copy):
			if isinstance(key, str) and key not in algebraic_state and len(key) < len(algebraic_state):
				try:
					del self.memory[key]
				except:
					continue
			elif isinstance(value, str) and value not in algebraic_state and len(value) < len(algebraic_state):
				try:
					del self.memory[value]
				except:
					del self.memory[key]
		
		if len(temp_moves_made) > 1:
			for key, value in recursive_items(self.memory):
				print (key, value)
		# if temp_moves_made:
		# 	if master_state.turn == 'w':
		# 		#position = str(int((len(temp_moves_made)) / 2)) + '.' + temp_moves_made[-2][0] + temp_moves_made[-1][0]

		# 	else:

		# 		position = str(int((((len(temp_moves_made) + 1)) / 2))) + '.' + temp_moves_made[-1][0]
		# else:
		# 	position = 'starting'
		self.consciousness[algebraic_state] = master_state
		alpha = float('-inf')
		beta = float('inf')
		best_move_value = self.Max_Value(master_state, self.max_depth , alpha, beta, temp_moves_made)
		#print(consciousness)
		print(self.memory)
		#self.print_cache()
		
		#self.print_cache()

		kscastle = 'O-O'
		qscastle = 'O-O-O'
		#move_order = list(dict(sorted(self.memory[position].items(), key=operator.itemgetter(1),reverse=True)).keys())
		#print(position)
		#print(self.memory[algebraic_state])
		
		move_order = dict(sorted(self.memory[algebraic_state].items(), key=operator.itemgetter(1),reverse=True))
		#print(move_order)
		best_move = list(move_order.keys())[0]
		for move in master_state.current_legal_moves:
			if move[0] == kscastle or move[0] == qscastle:
				print(best_move)
				if move_order[best_move] < 10:
					castle = move[0]
					return castle

		ordered_moves = list(move_order.keys())
		print('ordered moves: ', ordered_moves)
		if temp_moves_made:
		# 	#print(temp_moves_made[-1][0])
			pattern = '(?<=' + temp_moves_made[-1][0] + ').*'
			#print(pattern)
			best_move = re.search(pattern, ordered_moves[0])[0]
		# else:
		# 	pattern = '(?<=\.).*'
		# 	move = re.search(pattern, ordered_moves[0])[0]
		
		# move_sequence = move_order[0]
		# diff = len(move_sequence) - len()
		
		return best_move

	def Max_Value(self, working_memory, depth, alpha, beta, temp_moves_made):

		color = working_memory.turn
		#print(color)
		#print(working_memory.board)

		if self.Cutoff_Test(working_memory, depth, color):
			return self.Eval(working_memory.board, temp_moves_made[1][0])

		
		moves = working_memory.current_legal_moves
		cache = {}
		# if temp_moves_made:
		# 	if color == 'w':
		# 		position = str(int((len(temp_moves_made)) / 2)) + '.' + temp_moves_made[-2][0] + temp_moves_made[-1][0]
		# 	else:
		# 		position = str(int((((len(temp_moves_made) + 1)) / 2))) + '.' + temp_moves_made[-1][0]
		# else:
		# 	position = 'starting'
		
		#print('max: ', position, current_depth)
		position = self.Algebraic_State(temp_moves_made)

		value = float('-inf')
		#print('white:',moves)
		#prev_alpha = alpha
		for move in moves:

			#print(move)
			current_line = copy.deepcopy(temp_moves_made)
			current_line.append(move)
			algebraic_state = self.Algebraic_State(current_line)
			# if self.Seen_Position(algebraic_state) and temp_moves_made:
			# 	best_seen = list(dict(sorted(self.memory[algebraic_state].items(), key=operator.itemgetter(1),reverse=True)).values())[0]

			# 	print(best_seen, algebraic_state, self.Algebraic_State(self.actual_moves_made))
			# 	value = max(value, best_seen)
			# 	if best_seen >= alpha:
			# 		return best_seen


			# 	alpha = max(alpha, best_seen)
			# 	continue

			if self.Hanging_Piece(working_memory.board, move[0], color):
				continue

			
			position_state = copy.deepcopy(working_memory)

			#print(algebraic_state)
			self.Calculate_Move(position_state, move)
			move = move[0]
			predicted_value = self.Min_Value(position_state, depth-.5, alpha, beta, current_line)
			
			position_state.value = predicted_value
			#print(value, predicted_value)
			value = max(value, predicted_value)
			# if temp_moves_made:
			# 	if color == 'w':
			# 		move_num  = str(int((len(temp_moves_made)) / 2)) + '.' + temp_moves_made[-2][0] + temp_moves_made[-1][0]
			# 		#print('max1: ', move_num)
			# 	else:
			# 		move_num = str(int((((len(temp_moves_made) + 1)) / 2))) + '.' + temp_moves_made[-1][0] + move
			# 		#print('max2: ', move_num)
				
			self.consciousness[algebraic_state] = position_state
			cache[algebraic_state] = predicted_value
			
			# else:
			# 	move_num = '1.' + move
			# 	cache[move_num] = predicted_value

			self.positions_seen.append(position_state.board)
			#print(algebraic_state)
			#print(algebraic_state)
			
			if value >= beta:

				return value
			

			alpha = max(alpha, value)
			#print(algebraic_state, ' alpha = ', alpha)

		# if alpha > prev_alpha:
		# 	current_best = move[0]
		# 	prev_alpha = alpha

		
		print(position)
		if position == 'Nc3Nc6e3e6':
			print(cache)
		
		self.memory[position] = cache


		#print('white', moves, current_depth)
		return value

	def Min_Value(self, working_memory, depth, alpha, beta, temp_moves_made):

		# if temp_moves_made[0][0] == 'a3':
		# 	print(depth)
		# color = 'w'
		# if self.my_color == 'w':
		# 	color = 'b'
		color = working_memory.turn
		#print(color)
		if self.Cutoff_Test(working_memory, depth, color):

			return self.Eval(working_memory.board, temp_moves_made[1][0])
		
		
		moves = working_memory.current_legal_moves
		#print('black: ', moves)
		cache = {}
		# if color == 'w':
		# 	position = str(int((len(temp_moves_made)) / 2)) + '.' + temp_moves_made[-2][0] + temp_moves_made[-1][0]
		# else:
		# 	position = str(int((((len(temp_moves_made) + 1)) / 2))) + '.' + temp_moves_made[-1][0]
		
		position = self.Algebraic_State(temp_moves_made)

		#print('min:', position, current_depth)
		value = float('inf')
		#print('black', moves)
		for move in moves:

			current_line = copy.deepcopy(temp_moves_made)
			current_line.append(move)
			algebraic_state = self.Algebraic_State(current_line)
			# if self.Seen_Position(algebraic_state):

			# 	best_seen = list(dict(sorted(self.memory[algebraic_state].items(), key=operator.itemgetter(1),reverse=True)).values())[0]
			# 	print(best_seen, algebraic_state, self.Algebraic_State(self.actual_moves_made))
			# 	if best_seen <= alpha:
			# 		return best_seen

			# 	beta = min(beta, best_seen)
			# 	continue

			if self.Hanging_Piece(working_memory.board, move[0], color):
				continue

			
			

			position_state = copy.deepcopy(working_memory)
			self.Calculate_Move(position_state, move)
			
			move = move[0]
			predicted_value = self.Max_Value(position_state, depth-.5, alpha, beta, current_line)
			position_state.value = predicted_value

			# elif (self.Capture_Hanging_Piece(position_state.board, move, color)):
			# 	if position_state.board[move[-2:]].piece[1] != 'P':
			# 		predicted_value -= 5
			#print(value, predicted_value)
			value = min(value, predicted_value)
			# if color == 'w':
			# 	move_num  = str(int((len(temp_moves_made)) / 2)) + '.' + temp_moves_made[-2][0] + temp_moves_made[-1][0]
			# 	#print('min1: ', move_num)
			# else:
			# 	move_num = str(int((((len(temp_moves_made) + 1)) / 2))) + '.' + temp_moves_made[-1][0] + move
			# 	#print('min2: ', move_num)

			self.consciousness[algebraic_state] = position_state
			cache[algebraic_state] = predicted_value

			if value <= alpha:
				#print(algebraic_state + ' is less than alpha')
				#self.depth -= 0.5
				return value
			
			beta = min(beta, value)
			
			#print(algebraic_state, ' beta = ', beta)

		print(position)
		if position == 'Nc3Nc6e3e6':
			print(cache)
		self.memory[position] = cache
		
		return value


	def Eval(self, position, last_move):

		control = 0
			
		white_material = 0
		black_material = 0

		# self.Print_Board(position)
		# self.Show_Control(position)

		for item in position.values():

			control += item.control
			if item.piece == 'wP':
				white_material += 1
			elif item.piece == 'bP':
				black_material += 1
			if item.piece == 'wB':
				white_material += 3
			elif item.piece == 'bB':
				black_material += 3
			if item.piece == 'wN':
				white_material += 3
			elif item.piece == 'bN':
				black_material += 3
			if item.piece == 'wR':
				white_material += 5
			elif item.piece == 'bR':
				black_material += 5
			if item.piece == 'wQ':
				white_material += 9
			elif item.piece == 'bQ':
				black_material += 9



		if self.my_color == 'b':

			control -= black_material - white_material
			
			return -1*control

		else:
			#print(control)
			control += white_material - black_material
			return control




	def Cutoff_Test(self, state, depth, color):

		if color == 'w' and state.board[state.wK_pos].bc > 0 and state.current_legal_moves:

			if len(state.current_legal_moves) <= 3:
				return False

		elif color == 'b' and state.board[state.bK_pos].wc > 0 and state.current_legal_moves:

			if len(state.current_legal_moves) <= 3:
				return False

		elif depth >= 0:

			return False

		

		return True


	def Seen_Position(self, algebraic_state):
		
		for key, value in recursive_items(self.memory):
			#print(key)
			if algebraic_state == key:
				print('already seen ' + algebraic_state + ': ', value)
				return True

		return False

	def Hanging_Piece(self, state, move, color):

		if move == 'O-O' or move == 'O-O-O':
			return False

		if color == 'w':



			if state[move[-2:]].control <= -1:
				return True

			elif state[move[-2:]].control == 0 and state[move[-2:]].bc >= 1:
				return True

		else:
			if state[move[-2:]].control >= 1:
				return True

			elif state[move[-2:]].control == 0 and state[move[-2:]].wc >= 1:
				return True

		return False

	def Capture_Hanging_Piece(self, state, move, color):


		if move == 'O-O' or move == 'O-O-O':
			return False

		if color == 'w':

			if state[move[-2:]].control > 0 and state[move[-2:]].piece:

				return True

		else:

			if state[move[-2:]].control < 0 and state[move[-2:]].piece:

				return True

		return False




	def Show_Control(self, state):

        #did this function in descending order because that's how I'll be printing it, didn't really need to though

		eigth = []
		seventh= []
		sixth = []
		fifth = []
		fourth = []
		third = []
		second = []
		first = []


		for square in state:

			control = state[square].control

			if square[1] == '8':

				if control < 0:
					eigth.append('[' + str(control) + ']')
				else:
					eigth.append('[ ' + str(control) + ']')
			
			elif square[1] == '7':
			
				if control < 0:
					seventh.append('[' + str(control) + ']')
				else:
					seventh.append('[ ' + str(control) + ']')

			elif square[1] == '6':

				if control < 0:
					sixth.append('[' + str(control) + ']')
				else:
					sixth.append('[ ' + str(control) + ']')            

			elif square[1] == '5':

				if control < 0:
					fifth.append('[' + str(control) + ']')
				else:
					fifth.append('[ ' + str(control) + ']')

			elif square[1] == '4':

				if control < 0:
					fourth.append('[' + str(control) + ']')
				else:
					fourth.append('[ ' + str(control) + ']')

			elif square[1] == '3':

				if control < 0:
					third.append('[' + str(control) + ']')
				else:
					third.append('[ ' + str(control) + ']')

			elif square[1] == '2':
			
				if control < 0:
					second.append('[' + str(control) + ']')
				else:
					second.append('[ ' + str(control) + ']')

			elif square[1] == '1':
			
				if control < 0:
					first.append('[' + str(control) + ']')
				else:
				 first.append('[ ' + str(control) + ']')

		print('8', ''.join(eigth), '\n7', ''.join(seventh), '\n6', ''.join(sixth), '\n5', ''.join(fifth), '\n4', ''.join(fourth), '\n3', ''.join(third), '\n2', ''.join(second), '\n1', ''.join(first))
		print('   a ', ' b ', ' c ', ' d ', ' e ', ' f ', ' g ', ' h ')

	


	def Calculate_Move(self, state, move):

		#print(move)
		color = state.turn
		# if color == 'w':
		# 	color = 'b'
		# else:
		# 	color = 'w'
		#print(color)
		if move[0] != 'O-O' and move[0] != 'O-O-O' and move[0].find('=') == -1: 

			new_square = move[0][-2:]
			old_square = move[1]
			piece = state.board[old_square].piece

			#en passant capture
			if move[0].find('x') != -1 and not state.board[new_square].piece:
				if color == 'w':
					state.board[new_square[0] + '5'].piece = ""
				else:
					state.board[new_square[0] + '4'].piece = ""


			state.board[old_square].piece = ""
			state.board[new_square].piece = piece


			if piece == 'wK':
				state.wK_pos = new_square
				state.wK_moved = True
			elif piece == 'bK':
				state.bK_pos = new_square
				state.bK_moved = True
			elif piece == 'wR':
				if old_square == 'a1':
					state.wQR_moved = True
				elif old_square == 'h1':
					state.wKR_moved = True
			elif piece == 'bR':
				if old_square == 'a8':
					state.bQR_moved = True
				elif old_square == 'h8':
					state.bKR_moved = True




		else:
			if move == 'O-O':

				if color == 'w':
					state.board['e1'].piece = ""
					state.board['f1'].piece = 'wR'
					state.board['g1'].piece = 'wK'
					state.board['h1'].piece = ""

					state.wcastled = True
					state.wK_pos = 'g1'


				else:
					state.board['e8'].piece = ""
					state.board['f8'].piece = 'bR'
					state.board['g8'].piece = 'bK'
					state.board['h8'].piece = ""

					state.bcastled = True
					state.bK_pos = 'g8'


			elif move == 'O-O-O':

				if color == 'w':
					state.board['e1'].piece = ""
					state.board['d1'].piece = 'wR'
					state.board['c1'].piece = 'wK'
					state.board['a1'].piece = ""

					state.wcastled = True
					state.wK_pos = 'c1'

				else:
					state.board['e8'].piece = ""
					state.board['d8'].piece = 'bR'
					state.board['c8'].piece = 'bK'
					state.board['a8'].piece = ""

					state.bcastled = True
					state.bK_pos = 'c8'

			else:
				old_square = move[1]

				prom_square = move[0][-4:-2]
				state.board[old_square].piece = ""
				if move[0][-1] == 'Q':
					state.board[prom_square].piece = str(color + 'Q')

					if color == 'w':
						state.num_wQ += 1
					else:
						state.num_bQ += 1


				elif move[-1] == 'R':
					state.board[prom_square].piece = str(color + 'R')

				elif move[-1] == 'N':
					state.board[prom_square].piece = str(color + 'N')

				elif move[-1] == 'B':
					state.board[prom_square].piece = str(color + 'B')

		attributes = [state.wcastled, state.wK_moved, state.wKR_moved, state.wQR_moved,
                 state.bcastled, state.bK_moved, state.bKR_moved, state.bQR_moved]


		if color == 'w':
			color = 'b'
		else:
			color = 'w'

		candidate_moves = self.Make_Candidate_Moves(state.board, move, state.num_wQ, state.num_bQ, attributes)
		#print(candidate_moves)
		#prevent check
		added_queen = False
		temp_candidate_moves = copy.deepcopy(candidate_moves[color])

		for new_move in candidate_moves[color]:
			if color == 'w':
				temp_K_pos = state.wK_pos
			else:
				temp_K_pos = state.bK_pos

			temp_state = copy.deepcopy(state.board)

			if new_move[0] != 'O-O' and new_move[0] != 'O-O-O' and new_move[0].find('=') == -1:

				piece = temp_state[new_move[1]].piece

				#en passant capture
				if new_move[0].find('x') != -1 and not temp_state[new_move[0][-2:]].piece:
					if color == 'w':
						temp_state[new_move[0][-2] + '5'].piece = ""
					else:
						temp_state[new_move[0][-2] + '4'].piece = ""

				temp_state[new_move[1]].piece = ""
				temp_state[new_move[0][-2:]].piece = piece

				if new_move[0][0] == 'K':
					temp_K_pos = new_move[0][-2:]

			elif new_move[0] == 'O-O':
				if color == 'w':
					temp_state['e1'].piece = ""
					temp_state['f1'].piece = 'wR'
					temp_state['g1'].piece = 'wK'
					temp_state['h1'].piece = ""
					temp_K_pos = 'g1'

				else:
					temp_state['e8'].piece = ""
					temp_state['f8'].piece = 'bR'
					temp_state['g8'].piece = 'bK'
					temp_state['h8'].piece = ""
					temp_K_pos = 'g8'

			elif new_move[0] == 'O-O-O':
				if color == 'w':
					temp_state['e1'].piece = ""
					temp_state['d1'].piece = 'wR'
					temp_state['c1'].piece = 'wK'
					temp_state['a1'].piece = ""
					temp_K_pos = 'c1'

				else:
					temp_state['e8'].piece = ""
					temp_state['d8'].piece = 'bR'
					temp_state['c8'].piece = 'bK'
					temp_state['a8'].piece = ""
					temp_K_pos = 'c8'

			#promotion
			else:
				prom_square = new_move[0][-4:-2]
				temp_state[new_move[1]].piece = ""
				if new_move[0][-1] == 'Q':
					temp_state[prom_square].piece = str(color + 'Q')
					if color == 'w':
						state.num_wQ += 1
					else:
						state.num_bQ += 1
						added_queen = True

				elif new_move[0][-1] == 'R':
					temp_state[prom_square].piece = str(color + 'R')

				elif new_move[0][-1] == 'N':
					temp_state[prom_square].piece = str(color + 'N')

				elif new_move[0][-1] == 'B':
					temp_state[prom_square].piece = str(color + 'B')
		    
			self.Make_Candidate_Moves(temp_state, new_move, state.num_wQ, state.num_bQ, attributes)

			if added_queen and color == 'w':
				state.num_wQ -= 1
			elif added_queen and color == 'b':
				state.num_bQ -= 1

			if color == 'w' and temp_state[temp_K_pos].bc > 0:
				temp_candidate_moves.remove(new_move)
				#print('removed ' + new_move[0])
			elif color == 'b' and temp_state[temp_K_pos].wc > 0:
				temp_candidate_moves.remove(new_move)

		state.current_legal_moves = temp_candidate_moves
		#print(color, state.current_legal_moves)

		if color == 'b':
			state.turn = 'b'
		else:
			state.turn = 'w'

		return state