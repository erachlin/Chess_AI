class game():
    def __init__(self, in_possible_moves, in_state):
        self.state = in_state
        self.possible_moves = in_possible_moves
        self.check = False
        self.wK_pos = 'e1'
        self.bK_pos = 'e8'
        self.wK_moved = False
        self.wKR_moved = False
        self.wQR_moved = False
        self.wcastled = False
        self.bK_moved = False
        self.bKR_moved = False
        self.bQR_moved = False
        self.bcastled = False
        self.num_wQ = 1
        self.num_bQ = 1
        self.actual_moves_made = []
        self.last_move = ""
        self.turn = 'w'

    
    def play(self):
        state = self.state
        possible_moves = self.possible_moves
        legal_moves = make_legal_moves(possible_moves, state, "")
        candidate_moves = legal_moves['w']
        while len(candidate_moves) > 0:
            print(candidate_moves)
            move = input(self.turn + ' to move: ')
            move_found = False
            for tup in candidate_moves:
                if move in tup:
                    move_found = True
                    new_square = move[-2:]
                    old_square = tup[1]
                    piece = state[old_square].piece
                    state[old_square].piece = ""
                    state[new_square].piece = piece
                    if piece == 'wK':
                        self.wK_pos = new_square
                        self.wK_moved = True
                    elif piece == 'bK':
                        self.bK_pos = new_square
                        self.bK_moved = True
                        
                    self.actual_moves_made.append(move)
                    
                    if self.turn == 'w':
                        self.turn = 'b'
                        candidate_moves = self.prevent_check(self.make_legal_moves(possible_moves, state, move), state)
                        break
                    else:
                        self.turn = 'w'
                        candidate_moves = self.prevent_check(self.make_legal_moves(possible_moves, state, move), state)
                        break
                
            if not move_found:
                print('Invalid move, please try again')
            
    
        
                
    def num_queens(self, color):
        if color == 'w':
            return self.num_wQ
        else:
            return self.num_bQ    

    def prevent_check(self, legal_moves, state):
    
        color = self.turn

        temp_legal_moves = legal_moves[color]
        
        for new_move in legal_moves[color]:
            if color == 'w':
                temp_K_pos = self.wK_pos
            else:
                temp_K_pos = self.bK_pos
            temp_state = state
            piece = temp_state[new_move[1]].piece
            temp_state[new_move[1]].piece = ""
            temp_state[new_move[0][-2:]].piece = piece
            
            if move[0] == 'K':
                temp_K_pos = new_move[0][-2:]

            for item in temp_state.values():
                item.clear_control()

            self.make_legal_moves(possible_moves, temp_state, new_move)

            if color == 'w' and temp_state[temp_K_pos].bc > 0:
                temp_legal_moves.remove(new_move)
            elif color == 'b' and temp_state[temp_K_pos].wc > 0:
                temp_legal_moves.remove(new_move)
        
        return temp_legal_moves
        


    def make_legal_moves(self, possible_moves, state, last_move):
        

        legal_moves = {'w' : [], 'b' : []}
        for square in state:
            if not state[square].piece:
                continue
            
            file = square[0]
            rank = int(square[1])
            color = state[square].piece[0]
            piece = state[square].piece

            if piece == 'wP':

                wpm = possible_moves[square].P.wpm
                
                for move in wpm:
                    if move.find('='):
                        print(move)
                        continue
                    if move[0] == file and move[1] == str(rank + 1):
                        if not state[move].piece:
                            legal_moves[color].append((move, square))
                    elif move[0] == file and move[1] == str(rank + 2):
                        if not state[str(file + str(int(rank + 1)))].piece and not state[move].piece:
                            legal_moves[color].append((move, square))
                    else:
                        state[move].add_control(color)
                        if state[move].piece and state[move].piece[0] != color:
                            legal_moves[color].append((file + 'x' + move, square))
                        #absurd logic for en passant
                        elif last_move and rank == 5 and last_move[0] == str(move[0] + '5') and last_move[1][1] == '7' and not last_move[0][0].isupper():
                            legal_moves[color].append((file + 'x' + move, square))
                    
            if piece == 'bP':

                bpm = possible_moves[square].P.bpm
                
                for move in bpm:
                    if move.find('='):
                        continue
                    if move[0] == file and move[1] == str(rank - 1):
                        if not state[move].piece:
                            legal_moves[color].append((move, square))
                    elif move[0] == file and move[1] == str(rank - 2):
                        if not state[str(file + str(int(rank - 1)))].piece and not state[move].piece:
                            legal_moves[color].append((move, square))
                    else:
                        state[move].add_control(color)
                        if state[move].piece and state[move].piece[0] != color:
                            legal_moves[color].append((file + 'x' + move, square))
                        #absurd logic for en passant
                        elif rank == 4 and last_move[0] == str(move[0] + '4') and last_move[1][1] == '2' and not last_move[0][0].isupper():
                            legal_moves[color].append((file + 'x' + move, square))
                    
            
            if piece[1] == 'N':

                N = possible_moves[square].N
                
                for move in N:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    found_duplicate = False
                    if not state[move].piece:
                        #check for move to same square with same piece type from this color
                        for tup in legal_moves[color]:
                            if piece[1] + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    legal_moves[color].append(piece[1] + file + move, square)
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    legal_moves[color].append((piece[1] + str(rank) + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                    
                        if not found_duplicate:
                            legal_moves[color].append((piece[1] + move, square))
                    
                    #piece capture
                    elif state[move].piece[0] != color:
                        #check for move to same square with same piece type from this color
                        for tup in legal_moves[color]:
                            if piece[1] + 'x' + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    legal_moves[color].append(piece[1] + file + 'x' + move, square)
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    break
                                                    
                        legal_moves[color].append((piece[1] + 'x' + move, square)) 
                            
            
            if piece[1] == 'B':
                
                hrhf = possible_moves[square].B.hrhf
                hrlf = possible_moves[square].B.hrlf
                lrhf = possible_moves[square].B.lrhf
                lrlf = possible_moves[square].B.lrlf
                
                for move in hrhf:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    if not state[move].piece:
                        legal_moves[color].append((piece[1] + move, square))
                    elif state[move].piece[0] != color:
                        legal_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    else:
                        break
                for move in hrlf:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    if not state[move].piece:
                        legal_moves[color].append((piece[1] + move, square))
                    elif state[move].piece[0] != color:
                        legal_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    else:
                        break
                for move in lrhf:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    if not state[move].piece:
                        legal_moves[color].append((piece[1] + move, square))
                    elif state[move].piece[0] != color:
                        legal_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    else:
                        break
                for move in lrlf:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    if not state[move].piece:
                        legal_moves[color].append((piece[1] + move, square))
                    elif state[move].piece[0] != color:
                        legal_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    else:
                        break
                                                    
            if piece[1] == 'R':
                
                hr = possible_moves[square].R.hr
                lr = possible_moves[square].R.lr
                hf = possible_moves[square].R.hf
                lf = possible_moves[square].R.lf
                
                for move in hr:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    found_duplicate = False
                    if not state[move].piece:
                        #check for move to same square with same piece type from this color
                        for tup in legal_moves[color]:
                            if piece[1] + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    legal_moves[color].append((piece[1] + file + move, square))
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    legal_moves[color].append((piece[1] + str(rank) + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                    
                        if not found_duplicate:
                            legal_moves[color].append((piece[1] + move, square))
                    
                    #piece capture                               
                    elif state[move].piece[0] != color:
                        #check for move to same square with same piece type from this color
                        for tup in legal_moves[color]:
                            if piece[1] + 'x' + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    legal_moves[color].append(piece[1] + file + 'x' + move, square)
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    break
                        
                        if not found_duplicate:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    #your own piece blocking                                
                    else:
                        break
                                                    
                for move in lr:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    found_duplicate = False
                    if not state[move].piece:
                        #check for move to same square with same piece type from this color
                        for tup in legal_moves[color]:
                            if piece[1] + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    legal_moves[color].append(piece[1] + file + move, square)
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    legal_moves[color].append((piece[1] + str(rank) + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                    
                        
                        if not found_duplicate:
                            legal_moves[color].append((piece[1] + move, square))
                    
                    #piece capture                               
                    elif state[move].piece[0] != color:
                        #check for move to same square with same piece type from this color
                        for tup in legal_moves[color]:
                            if piece[1] + 'x' + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    legal_moves[color].append(piece[1] + file + 'x' + move, square)
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                                    
                        if not found_duplicate:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    #your own piece blocking
                    else:
                        break
                for move in hf:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    found_duplicate = False
                    if not state[move].piece:
                        #check for move to same square with same piece type from this color
                        for tup in legal_moves[color]:
                            if piece[1] + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    legal_moves[color].append(piece[1] + file + move, square)
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    legal_moves[color].append((piece[1] + str(rank) + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_dupliate = True
                                    break
                                    
                        
                        if not found_duplicate:
                            legal_moves[color].append((piece[1] + move, square))
                    
                    #piece capture                               
                    elif state[move].piece[0] != color:
                        #check for move to same square with same piece type from this color
                        for tup in legal_moves[color]:
                            if piece[1] + 'x' + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    legal_moves[color].append(piece[1] + file + 'x' + move, square)
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                                    
                        if not found_duplicate:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    #your own piece blocking
                    else:
                        break
                for move in lf:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    found_duplicate = False
                    if not state[move].piece:
                        #check for move to same square with same piece type from this color
                        for tup in legal_moves[color]:
                            if piece[1] + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    legal_moves[color].append(piece[1] + file + move, square)
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    legal_moves[color].append((piece[1] + str(rank) + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                    
                        if not found_duplicate:
                            legal_moves[color].append((piece[1] + move, square))
                    
                    #piece capture                               
                    elif state[move].piece[0] != color:
                        #check for move to same square with same piece type from this color
                        for tup in legal_moves[color]:
                            if piece[1] + 'x' + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    legal_moves[color].append(piece[1] + file + 'x' + move, square)
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                    legal_moves[color].remove(tup)
                                    legal_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                                    
                        if not found_duplicate:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    #your own piece blocking
                    else:
                        break
                        
            if piece[1] == 'Q':
                
                hrhf = possible_moves[square].Q.hrhf
                hrlf = possible_moves[square].Q.hrlf
                lrhf = possible_moves[square].Q.lrhf
                lrlf = possible_moves[square].Q.lrlf
                hr = possible_moves[square].Q.hr
                lr = possible_moves[square].Q.lr
                hf = possible_moves[square].Q.hf
                lf = possible_moves[square].Q.lf
                
                #bishop-type moves
                for move in hrhf:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    if self.num_queens(color) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break  

                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + 'x' + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break  

                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            legal_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                            
                for move in hrlf:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    if self.num_queens(color) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + move in tup:
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                        
                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + 'x' + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            legal_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                            
                for move in lrhf:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    if self.num_queens(color) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + 'x' + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            legal_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                            
                for move in lrlf:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    if self.num_queens(color) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break


                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + 'x' + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            legal_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                
                #rook-type moves
                for move in hr:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    if self.num_queens(color) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + 'x' + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            legal_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                                                    
                for move in lr:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    if self.num_queens(color) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break


                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + 'x' + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            legal_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                            
                for move in hf:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    if self.num_queens(color) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break


                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + 'x' + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            legal_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                            
                for move in lf:
                    if color == 'w':
                        state[move].add_control(color)
                    else:
                        state[move].control -= 1
                    if self.num_queens(color) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break


                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in legal_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        legal_moves[color].append(piece[1] + file + 'x' + move, square)

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        legal_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        legal_moves[color].append((piece[1] + square + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + 'x' + move, tup[1])
                                        legal_moves[color].remove(tup)
                                        legal_moves[color].append(update)
                                        found_duplicate = True
                                        break

                            if not found_duplicate:
                                legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            legal_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
            
            if piece[1] == 'K':
                
                K = possible_moves[square].K
                
                for move in K:
                    if not state[move].piece:
                        legal_moves[color].append((piece[1] + move, square))
                    elif state[move].piece[0] != color:
                            legal_moves[color].append((piece[1] + 'x' + move, square))
                        
        
        
        #legal_moves = prevent_check(legal_moves, state)
        
        return legal_moves