import copy

#square info for board state
class si:
    def __init__(self):
        self.piece = ""
        self.control = 0
        self.wc = 0
        self.bc = 0
    
    def add_control(self, color):
        if color == 'w':
            self.wc += 1
            self.control += 1
        else:
            self.bc += 1
            self.control -= 1
    
    def clear_control(self):
        self.control = 0
        self.wc = 0
        self.bc = 0

#pawn control by color      
class pc:
    def __init__(self, in_wpm, in_bpm):
        self.wpm = in_wpm
        self.bpm = in_bpm

#bishop control on separate diagonals
class bc:
    def __init__(self):
        self.hrhf = []
        self.hrlf = []
        self.lrhf = []
        self.lrlf = []

class rc:
    def __init__(self):
        self.hr = []
        self.lr = []
        self.hf = []
        self.lf = []

class qc:
    def __init__(self):
        self.hrhf = []
        self.hrlf = []
        self.lrhf = []
        self.lrlf = []
        self.hr = []
        self.lr = []
        self.hf = []
        self.lf = []
        

#moves by piece
class mbp:
    def __init__(self):
        self.P = pc
        self.N = []
        self.B = bc
        self.R = rc
        self.Q = qc
        self.K = []

def setup_game():

    state = {}
    possible_moves = {}
    for i in range(0,8):
        for j in range(1,9):
            state[str(chr(ord('a') + i) + str(j))] = si()
            possible_moves[str(chr(ord('a') + i) + str(j))] = mbp()

    for square in possible_moves:
        
        file = ord(square[0]) - 96
        rank = int(square[1])
        #pawn moves
        wpm = []
        bpm = []
        if rank > 1 and rank < 8:
            if rank == 2:
                wpm.append(square[0] + '4')
                wpm.append(square[0] + '3')
                bpm.append(square[0] + '1=Q')
                bpm.append(square[0] + '1=R')
                bpm.append(square[0] + '1=B')
                bpm.append(square[0] + '1=N')
                if file > 1:
                    wpm.append(chr(file + 95) + str(rank + 1))
                    bpm.append(chr(file + 95) + '1=Q')
                    bpm.append(chr(file + 95) + '1=R')
                    bpm.append(chr(file + 95) + '1=B')
                    bpm.append(chr(file + 95) + '1=N')
                if file < 8:
                    wpm.append(chr(file + 97) + str(rank + 1))
                    bpm.append(chr(file + 97) + '1=Q')
                    bpm.append(chr(file + 97) + '1=R')
                    bpm.append(chr(file + 97) + '1=B')
                    bpm.append(chr(file + 97) + '1=N')
            elif rank == 7:
                bpm.append(square[0] + '5')
                bpm.append(square[0] + '6')
                wpm.append(square[0] + '8=Q')
                wpm.append(square[0] + '8=R')
                wpm.append(square[0] + '8=B')
                wpm.append(square[0] + '8=N')
                if file > 1:
                    bpm.append(chr(file + 95) + str(rank - 1))
                    wpm.append(chr(file + 95) + '8=Q')
                    wpm.append(chr(file + 95) + '8=R')
                    wpm.append(chr(file + 95) + '8=B')
                    wpm.append(chr(file + 95) + '8=N')
                if file < 8:
                    bpm.append(chr(file + 97) + str(rank - 1))
                    wpm.append(chr(file + 97) + '8=Q')
                    wpm.append(chr(file + 97) + '8=R')
                    wpm.append(chr(file + 97) + '8=B')
                    wpm.append(chr(file + 97) + '8=N')
            else:
                wpm.append(square[0] + str((rank+1)))
                bpm.append(square[0] + str((rank-1)))
                if file > 1:
                    wpm.append(chr(file + 95) + str(rank + 1))
                    bpm.append(chr(file + 95) + str(rank - 1))
                if file < 8:
                    wpm.append(chr(file + 97) + str(rank + 1))
                    bpm.append(chr(file + 97) + str(rank - 1))
                
        possible_moves[square].P = pc(wpm, bpm)

        #knight moves
        N = []
        if(file + 1) <= 8 and (rank - 2) >= 1:
            N.append(str(chr(file + 97)) + str(rank - 2))
        if (file + 2) <= 8 and (rank - 1) >= 1:
            N.append(str(chr(file + 98)) + str(rank - 1))
        if (file + 2) <= 8 and (rank + 1) <= 8:
            N.append(str(chr(file + 98)) + str(rank + 1))
        if (file + 1) <= 8 and (rank + 2) <= 8:
            N.append(str(chr(file + 97)) + str(rank + 2))
        if (file - 1) >= 1 and (rank + 2) <= 8:
            N.append(str(chr(file + 95)) + str(rank + 2))
        if (file - 2) >= 1 and (rank + 1) <= 8:
            N.append(str(chr(file + 94)) + str(rank + 1))
        if (file - 2) >= 1 and (rank - 1) >= 1:
            N.append(str(chr(file + 94)) + str(rank - 1))
        if (file - 1) >= 1 and (rank - 2) >= 1:
            N.append(str(chr(file + 95)) + str(rank - 2))

        possible_moves[square].N = N

        #bishop/queen moves
        bm = bc()
        qm = qc()
        
        hrhf = []
        hrhf_rank = rank + 1
        hrhf_file = file + 1
        
        hrlf = []
        hrlf_rank = rank + 1
        hrlf_file = file - 1
        
        lrhf = []
        lrhf_rank = rank - 1
        lrhf_file = file + 1
        
        lrlf = []
        lrlf_rank = rank - 1
        lrlf_file = file - 1
        
        for i in range(1,9):
            
            if hrhf_rank <= 8 and hrhf_file <= 8:
                hrhf.append(str(chr(hrhf_file + 96)) + str(hrhf_rank))
            if hrlf_rank <= 8 and hrlf_file >= 1:
                hrlf.append(str(chr(hrlf_file + 96)) + str(hrlf_rank))
            if lrhf_rank >= 1 and lrhf_file <= 8:
                lrhf.append(str(chr(lrhf_file + 96)) + str(lrhf_rank))
            if lrlf_rank >= 1 and lrlf_file >= 1:
                lrlf.append(str(chr(lrlf_file + 96)) + str(lrlf_rank))
            
            hrhf_rank += 1
            hrhf_file += 1
            hrlf_rank += 1
            hrlf_file -= 1
            lrhf_rank -= 1
            lrhf_file += 1
            lrlf_rank -= 1
            lrlf_file -= 1
        
        
        for item in hrhf:
            bm.hrhf.append(item)
            qm.hrhf.append(item)
        for item in hrlf:
            bm.hrlf.append(item)
            qm.hrlf.append(item)
        for item in lrhf:
            bm.lrhf.append(item)
            qm.lrhf.append(item)
        for item in lrlf:
            bm.lrlf.append(item)
            qm.lrlf.append(item)
        
        possible_moves[square].B = bm

        #rook/queen moves
        rm = rc()
        
        hr = []
        hr_rank = rank + 1
        
        lr = []
        lr_rank = rank - 1
        
        hf = []
        hf_file = file + 1
        
        lf = []
        lf_file = file - 1
        
        for i in range(1,9):
        
            if hr_rank <= 8:
                hr.append(str(chr(file + 96)) + str(hr_rank))
            if lr_rank >= 1:
                lr.append(str(chr(file + 96)) + str(lr_rank))
            if hf_file <= 8:
                hf.append(str(chr(hf_file + 96)) + str(rank))
            if lf_file >= 1:
                lf.append(str(chr(lf_file + 96)) + str(rank))
                
            hf_file += 1
            hr_rank += 1
            lf_file -= 1
            lr_rank -= 1
            
        for item in hr:
            rm.hr.append(item)
            qm.hr.append(item)
        for item in lr:
            rm.lr.append(item)
            qm.lr.append(item)
        for item in hf:
            rm.hf.append(item)
            qm.hf.append(item)
        for item in lf:
            rm.lf.append(item)
            qm.lf.append(item)
        
        possible_moves[square].R = rm
        possible_moves[square].Q = qm
        
        #king moves
        K = []
        hrhf_rank = rank + 1
        hrhf_file = file + 1
        hrlf_rank = rank + 1
        hrlf_file = file - 1
        lrhf_rank = rank - 1
        lrhf_file = file + 1
        lrlf_rank = rank - 1
        lrlf_file = file - 1
        
        if hrhf_file <= 8 and hrhf_rank <= 8:
            K.append(str(chr(hrhf_file + 96)) + str(hrhf_rank))
        if hrhf_file <= 8:
            K.append(str(chr(hrhf_file + 96)) + str(rank))
        if lrhf_file <= 8 and lrhf_rank >= 1:
            K.append(str(chr(lrhf_file + 96)) + str(lrhf_rank))
        if lrhf_rank >= 1:
            K.append(str(chr(file + 96)) + str(lrhf_rank))
        if lrlf_file >= 1 and lrlf_rank >= 1:
            K.append(str(chr(lrlf_file + 96)) + str(lrlf_rank))
        if hrlf_file >= 1:
            K.append(str(chr(hrlf_file + 96)) + str(rank))
        if hrlf_file >= 1 and hrlf_rank <= 8:
            K.append(str(chr(hrlf_file + 96)) + str(hrlf_rank))
        if hrhf_rank <= 8:
            K.append(str(chr(file + 96)) + str(hrhf_rank))
        
        possible_moves[square].K = K
        
    for square in state:
        if square == 'a1' or square == 'h1':
            state[square].piece = 'wR'
        if square == 'b1' or square == 'g1':
            state[square].piece = 'wN'
        if square == 'c1' or square == 'f1':
            state[square].piece = 'wB'
        if square == 'd1':
            state[square].piece = 'wQ'
        if square == 'e1':
            state[square].piece = 'wK'
        if square == 'a8' or square == 'h8':
            state[square].piece = 'bR'
        if square == 'b8' or square == 'g8':
            state[square].piece = 'bN'
        if square == 'c8' or square == 'f8':
            state[square].piece = 'bB'
        if square == 'd8':
            state[square].piece = 'bQ'
        if square == 'e8':
            state[square].piece = 'bK'
        if square[1] == '2':
            state[square].piece = 'wP'
        if square[1] == '7':
            state[square].piece = 'bP'

    return state, possible_moves



            



class game():
    def __init__(self, in_possible_moves, in_state):
        self.state = in_state
        self.possible_moves = in_possible_moves
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
        self.attributes = [self.wcastled, self.wK_moved, self.wKR_moved, self.wQR_moved,
                 self.bcastled, self.bK_moved, self.bKR_moved, self.bQR_moved]
        self.legal_moves = self.Make_Candidate_Moves(self.state, ("", ""), 1, 1, self.attributes)
        


    def Make_Candidate_Moves(self, state, last_move, num_wQ, num_bQ, attributes):
        

        candidate_moves = {'w' : [], 'b' : []}

        for item in state.values():
            item.clear_control()

        for square in state:

            if not state[square].piece:
                continue
            
            file = square[0]
            rank = int(square[1])
            color = state[square].piece[0]
            piece = state[square].piece

            if piece == 'wP':

                wpm = self.possible_moves[square].P.wpm
                
                for move in wpm:

                    if move[0] == file and move[1] == str(rank + 1):
                        if not state[move[:2]].piece:
                            candidate_moves[color].append((move, square))

                    elif move[0] == file and move[1] == str(rank + 2):
                        if not state[str(file + str(int(rank + 1)))].piece and not state[move].piece:
                            candidate_moves[color].append((move, square))
                    else:
                        state[move[:2]].add_control(color)

                        if state[move[:2]].piece and state[move[:2]].piece[0] != color:
                            candidate_moves[color].append((file + 'x' + move, square))
                        #absurd logic for en passant
                        elif last_move and rank == 5 and last_move[0] == str(move[0] + '5') and last_move[1][1] == '7' and not last_move[0][0].isupper():

                            candidate_moves[color].append((file + 'x' + move, square))
            
                

            if piece == 'bP':

                bpm = self.possible_moves[square].P.bpm
                
                for move in bpm:
                    
                    if move[0] == file and move[1] == str(rank - 1):
                        if not state[move[:2]].piece:
                            candidate_moves[color].append((move, square))
                    elif move[0] == file and move[1] == str(rank - 2):
                        if not state[str(file + str(int(rank - 1)))].piece and not state[move].piece:
                            candidate_moves[color].append((move, square))
                    else:
                        state[move[:2]].add_control(color)

                        if state[move[:2]].piece and state[move[:2]].piece[0] != color:
                            candidate_moves[color].append((file + 'x' + move, square))
                        #absurd logic for en passant
                        elif rank == 4 and last_move[0] == str(move[0] + '4') and last_move[1][1] == '2' and not last_move[0][0].isupper():

                            candidate_moves[color].append((file + 'x' + move, square))
                    
            
            if piece[1] == 'N':

                N = self.possible_moves[square].N
                
                for move in N:
                    state[move].add_control(color)
                    found_duplicate = False
                    if not state[move].piece:
                        #check for move to same square with same piece type from this color
                        for tup in candidate_moves[color]:
                            if piece[1] + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    candidate_moves[color].append((piece[1] + file + move, square))
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    candidate_moves[color].append((piece[1] + str(rank) + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                    
                        if not found_duplicate:
                            candidate_moves[color].append((piece[1] + move, square))
                    
                    #piece capture
                    elif state[move].piece[0] != color:
                        #check for move to same square with same piece type from this color
                        for tup in candidate_moves[color]:
                            if piece[1] + 'x' + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    candidate_moves[color].append((piece[1] + file + 'x' + move, square))
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    break
                                                    
                        candidate_moves[color].append((piece[1] + 'x' + move, square)) 
                            
            
            if piece[1] == 'B':
                
                hrhf = self.possible_moves[square].B.hrhf
                hrlf = self.possible_moves[square].B.hrlf
                lrhf = self.possible_moves[square].B.lrhf
                lrlf = self.possible_moves[square].B.lrlf
                
                for move in hrhf:
                    state[move].add_control(color)
                    if not state[move].piece:
                        candidate_moves[color].append((piece[1] + move, square))
                    elif state[move].piece[0] != color:
                        candidate_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    else:
                        break
                for move in hrlf:
                    state[move].add_control(color)
                    if not state[move].piece:
                        candidate_moves[color].append((piece[1] + move, square))
                    elif state[move].piece[0] != color:
                        candidate_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    else:
                        break
                for move in lrhf:
                    state[move].add_control(color)
                    if not state[move].piece:
                        candidate_moves[color].append((piece[1] + move, square))
                    elif state[move].piece[0] != color:
                        candidate_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    else:
                        break
                for move in lrlf:
                    state[move].add_control(color)
                    if not state[move].piece:
                        candidate_moves[color].append((piece[1] + move, square))
                    elif state[move].piece[0] != color:
                        candidate_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    else:
                        break
                                                    
            if piece[1] == 'R':
                
                hr = self.possible_moves[square].R.hr
                lr = self.possible_moves[square].R.lr
                hf = self.possible_moves[square].R.hf
                lf = self.possible_moves[square].R.lf
                
                for move in hr:
                    state[move].add_control(color)
                    found_duplicate = False
                    if not state[move].piece:
                        #check for move to same square with same piece type from this color
                        for tup in candidate_moves[color]:
                            if piece[1] + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    candidate_moves[color].append((piece[1] + file + move, square))
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    candidate_moves[color].append((piece[1] + str(rank) + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                    
                        if not found_duplicate:
                            candidate_moves[color].append((piece[1] + move, square))
                    
                    #piece capture                               
                    elif state[move].piece[0] != color:
                        #check for move to same square with same piece type from this color
                        for tup in candidate_moves[color]:
                            if piece[1] + 'x' + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    candidate_moves[color].append((piece[1] + file + 'x' + move, square))
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    break
                        
                        if not found_duplicate:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    #your own piece blocking                                
                    else:
                        break
                                                    
                for move in lr:
                    state[move].add_control(color)
                    found_duplicate = False
                    if not state[move].piece:
                        #check for move to same square with same piece type from this color
                        for tup in candidate_moves[color]:
                            if piece[1] + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    candidate_moves[color].append((piece[1] + file + move, square))
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    candidate_moves[color].append((piece[1] + str(rank) + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                    
                        
                        if not found_duplicate:
                            candidate_moves[color].append((piece[1] + move, square))
                    
                    #piece capture                               
                    elif state[move].piece[0] != color:
                        #check for move to same square with same piece type from this color
                        for tup in candidate_moves[color]:
                            if piece[1] + 'x' + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    candidate_moves[color].append((piece[1] + file + 'x' + move, square))
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                                    
                        if not found_duplicate:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    #your own piece blocking
                    else:
                        break
                for move in hf:
                    state[move].add_control(color)
                    found_duplicate = False
                    if not state[move].piece:
                        #check for move to same square with same piece type from this color
                        for tup in candidate_moves[color]:
                            if piece[1] + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    candidate_moves[color].append((piece[1] + file + move, square))
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    candidate_moves[color].append((piece[1] + str(rank) + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_dupliate = True
                                    break
                                    
                        
                        if not found_duplicate:
                            candidate_moves[color].append((piece[1] + move, square))
                    
                    #piece capture                               
                    elif state[move].piece[0] != color:
                        #check for move to same square with same piece type from this color
                        for tup in candidate_moves[color]:
                            if piece[1] + 'x' + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    candidate_moves[color].append((piece[1] + file + 'x' + move, square))
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                                    
                        if not found_duplicate:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    #your own piece blocking
                    else:
                        break
                for move in lf:
                    state[move].add_control(color)
                    found_duplicate = False
                    if not state[move].piece:
                        #check for move to same square with same piece type from this color
                        for tup in candidate_moves[color]:
                            if piece[1] + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    candidate_moves[color].append((piece[1] + file + move, square))
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    candidate_moves[color].append((piece[1] + str(rank) + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                    
                        if not found_duplicate:
                            candidate_moves[color].append((piece[1] + move, square))
                    
                    #piece capture                               
                    elif state[move].piece[0] != color:
                        #check for move to same square with same piece type from this color
                        for tup in candidate_moves[color]:
                            if piece[1] + 'x' + move in tup:
                                #different files
                                if file != tup[1][0]:
                                    #add new
                                    candidate_moves[color].append((piece[1] + file + 'x' + move, square))
                                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                
                                #different ranks
                                else:
                                    #add new
                                    candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))
                                    
                                    #delete and update old
                                    update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break
                                                    
                        if not found_duplicate:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
                        break
                    #your own piece blocking
                    else:
                        break
                        
            if piece[1] == 'Q':
                
                hrhf = self.possible_moves[square].Q.hrhf
                hrlf = self.possible_moves[square].Q.hrlf
                lrhf = self.possible_moves[square].Q.lrhf
                lrlf = self.possible_moves[square].Q.lrlf
                hr = self.possible_moves[square].Q.hr
                lr = self.possible_moves[square].Q.lr
                hf = self.possible_moves[square].Q.hf
                lf = self.possible_moves[square].Q.lf
                
                #bishop-type moves
                for move in hrhf:
                    state[move].add_control(color)
                    if self.num_queens(color, num_wQ, num_bQ) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + move in tup or piece[1] + str(rank) + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + 'x' + move in tup or piece[1] + str(rank) + 'x' + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + 'x' + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            candidate_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                            
                for move in hrlf:
                    state[move].add_control(color)
                    if self.num_queens(color, num_wQ, num_bQ) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + move in tup or piece[1] + str(rank) + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + 'x' + move in tup or piece[1] + str(rank) + 'x' + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + 'x' + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            candidate_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                            
                for move in lrhf:
                    state[move].add_control(color)
                    if self.num_queens(color, num_wQ, num_bQ) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        candidate_moves[color].append((piece[1] + square + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif rank != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                    else:
                                        #add new
                                        candidate_moves[color].append((piece[1] + square + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            candidate_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                            
                for move in lrlf:
                    state[move].add_control(color)
                    if self.num_queens(color, num_wQ, num_bQ) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + move in tup or piece[1] + str(rank) + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + 'x' + move in tup or piece[1] + str(rank) + 'x' + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + 'x' + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            candidate_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                
                #rook-type moves
                for move in hr:
                    state[move].add_control(color)
                    if self.num_queens(color, num_wQ, num_bQ) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + move in tup or piece[1] + str(rank) + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + 'x' + move in tup or piece[1] + str(rank) + 'x' + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + 'x' + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            candidate_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                                                    
                for move in lr:
                    state[move].add_control(color)
                    if self.num_queens(color, num_wQ, num_bQ) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + move in tup or piece[1] + str(rank) + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + 'x' + move in tup or piece[1] + str(rank) + 'x' + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + 'x' + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            candidate_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                            
                for move in hf:
                    state[move].add_control(color)
                    if self.num_queens(color, num_wQ, num_bQ) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + move in tup or piece[1] + str(rank) + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + 'x' + move in tup or piece[1] + str(rank) + 'x' + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + 'x' + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            candidate_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
                            
                for move in lf:

                    state[move].add_control(color)
                    if self.num_queens(color, num_wQ, num_bQ) > 1:
                        if not state[move].piece:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + move in tup or piece[1] + str(rank) + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + move, square))

                        #piece capture                               
                        elif state[move].piece[0] != color:
                            #check for move to same square with same piece type from this color
                            for tup in candidate_moves[color]:
                                if piece[1] + 'x' + move in tup:
                                    #different files
                                    if file != tup[1][0]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + file + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][0] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break

                                    #different ranks
                                    elif str(rank) != tup[1][1]:
                                        #add new
                                        candidate_moves[color].append((piece[1] + str(rank) + 'x' + move, square))

                                        #delete and update old
                                        update = (piece[1] + tup[1][1] + 'x' + move, tup[1])
                                        candidate_moves[color].remove(tup)
                                        candidate_moves[color].append(update)
                                        found_duplicate = True
                                        break
                                    
                                elif piece[1] + file + 'x' + move in tup or piece[1] + str(rank) + 'x' + move in tup:
                                    #add new
                                    candidate_moves[color].append((piece[1] + square + 'x' + move, square))

                                    #delete and update old
                                    update = (piece[1] + tup[1] + move, tup[1])
                                    candidate_moves[color].remove(tup)
                                    candidate_moves[color].append(update)
                                    found_duplicate = True
                                    break  

                            if not found_duplicate:
                                candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        #your own piece blocking
                        else:
                            break
                    
                    #only one queen for this color
                    else:
                        if not state[move].piece:
                            candidate_moves[color].append((piece[1] + move, square))
                        elif state[move].piece[0] != color:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
                            break
                        else:
                            break
            
            if piece[1] == 'K':
                
                K = self.possible_moves[square].K
                
                for move in K:
                    state[move].add_control(color)
                    if not state[move].piece:
                        candidate_moves[color].append((piece[1] + move, square))
                    elif state[move].piece[0] != color:
                            candidate_moves[color].append((piece[1] + 'x' + move, square))
        

        self.Castling(state, candidate_moves, attributes)
        
        return candidate_moves

    def num_queens(self, color, num_wQ, num_bQ):
            if color == 'w':
                return num_wQ
            else:
                return num_bQ    

    def Prevent_Check(self, candidate_moves):

        color = self.turn
        added_queen = False
        temp_candidate_moves = copy.deepcopy(candidate_moves[color])

        for new_move in candidate_moves[color]:
            if color == 'w':
                temp_K_pos = self.wK_pos
            else:
                temp_K_pos = self.bK_pos
            
            temp_state = copy.deepcopy(self.state)

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
                        self.num_wQ += 1
                    else:
                        self.num_bQ += 1
                    added_queen = True

                elif new_move[0][-1] == 'R':
                    temp_state[prom_square].piece = str(color + 'R')

                elif new_move[0][-1] == 'N':
                    temp_state[prom_square].piece = str(color + 'N')

                elif new_move[0][-1] == 'B':
                    temp_state[prom_square].piece = str(color + 'B')
            
            self.Make_Candidate_Moves(temp_state, new_move, self.num_wQ, self.num_bQ, self.attributes)

            if added_queen and color == 'w':
                self.num_wQ -= 1
            elif added_queen and color == 'b':
                self.num_bQ -= 1

            if color == 'w' and temp_state[temp_K_pos].bc > 0:
                temp_candidate_moves.remove(new_move)
                #print('removed ' + new_move[0])
            elif color == 'b' and temp_state[temp_K_pos].wc > 0:
                temp_candidate_moves.remove(new_move)
        
        return temp_candidate_moves



    def Print_Board(self,state):

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
            
            if square[1] == '8':
                if not state[square].piece:
                    eigth.append('[  ]')
                else:
                    eigth.append('[' + state[square].piece + ']')
            elif square[1] == '7':
                if not state[square].piece:
                    seventh.append('[  ]')
                else:
                    seventh.append('[' + state[square].piece + ']')
            elif square[1] == '6':
                if not state[square].piece:
                    sixth.append('[  ]')
                else:
                    sixth.append('[' + state[square].piece + ']')            
            elif square[1] == '5':
                if not state[square].piece:
                    fifth.append('[  ]')
                else:
                    fifth.append('[' + state[square].piece + ']')
            elif square[1] == '4':
                if not state[square].piece:
                    fourth.append('[  ]')
                else:
                    fourth.append('[' + state[square].piece + ']')
            elif square[1] == '3':
                if not state[square].piece:
                    third.append('[  ]')
                else:
                    third.append('[' + state[square].piece + ']')
            elif square[1] == '2':
                if not state[square].piece:
                    second.append('[  ]')
                else:
                    second.append('[' + state[square].piece + ']')
            elif square[1] == '1':
                if not state[square].piece:
                    first.append('[  ]')
                else:
                    first.append('[' + state[square].piece + ']')

        print('8', ''.join(eigth), '\n7', ''.join(seventh), '\n6', ''.join(sixth), '\n5', ''.join(fifth), '\n4', ''.join(fourth), '\n3', ''.join(third), '\n2', ''.join(second), '\n1', ''.join(first))
        print('   a ', ' b ', ' c ', ' d ', ' e ', ' f ', ' g ', ' h ')


    def Square_Control(self):

        #did this function in descending order because that's how I'll be printing it, didn't really need to though

        eigth = []
        seventh= []
        sixth = []
        fifth = []
        fourth = []
        third = []
        second = []
        first = []


        for square in self.state:
            
            control = self.state[square].control

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

    def Castling(self, state, candidate_moves, attributes):    
        

        wcastled = attributes[0]
        bcastled = attributes[4]
        wK_moved = attributes[1]
        wKR_moved = attributes[2]
        wQR_moved = attributes[3]
        bK_moved = attributes[5]
        bKR_moved = attributes[6]
        bQR_moved = attributes[7]

        #white castle
        if not wcastled and not wK_moved and not wKR_moved:
            if not state['f1'].piece and not state['g1'].piece and state['f1'].bc == 0 and state['g1'].bc == 0 and state['e1'].bc == 0:
                candidate_moves['w'].append(('O-O', 'e1' ))
        if not wcastled and not wK_moved and not wQR_moved:
            if not state['d1'].piece and not state['c1'].piece and not state['b1'].piece:
                if state['e1'].bc == 0 and state['d1'].bc == 0 and state['c1'].bc == 0:
                    candidate_moves['w'].append(('O-O-O', 'e1'))
        
        #black castle
        if not bcastled and not bK_moved and not bKR_moved:
            if not state['f8'].piece and not state['g8'].piece and state['f8'].wc == 0 and state['g8'].wc == 0 and state['e8'].wc == 0:
                candidate_moves['b'].append(('O-O', 'e8' ))
        if not bcastled and not bK_moved and not bQR_moved:
            if not state['d8'].piece and not state['c8'].piece and not state['b8'].piece:
                if state['e8'].wc == 0 and state['d8'].wc == 0 and state['c8'].wc == 0:
                    candidate_moves['b'].append(('O-O-O', 'e8'))

    def Play(self, white):

            self.legal_moves = self.Prevent_Check(self.legal_moves)
            while len(self.legal_moves) > 0:
                self.Print_Board(self.state)
                self.Square_Control()
                #print(self.legal_moves)
                move_found = False
                if self.turn == 'w':
                    move = white.AB_Select_Move(self)
                    print('white\'s move: ', move)
                elif self.turn == 'b':
                    move = black.AB_Select_Move(self)
                    print('black\'s move: ', move)

                    #move = input(self.turn + ' to move ')

                attributes = self.attributes
                
                for tup in self.legal_moves:
                    if move in tup:
                        move_found = True
                        if move != 'O-O' and move != 'O-O-O' and move.find('=') == -1: 
                            
                            new_square = move[-2:]
                            old_square = tup[1]
                            piece = self.state[old_square].piece

                            #en passant capture
                            if move.find('x') != -1 and not self.state[new_square].piece:
                                if self.turn == 'w':
                                    self.state[new_square[0] + '5'].piece = ""
                                else:
                                    self.state[new_square[0] + '4'].piece = ""

                            
                            self.state[old_square].piece = ""
                            self.state[new_square].piece = piece
                            #print('state changed')
                            

                            if piece == 'wK':
                                self.wK_pos = new_square
                                self.wK_moved = True
                                self.attributes[1] =True
                            elif piece == 'bK':
                                self.bK_pos = new_square
                                self.bK_moved = True
                                self.attributes[5] = True

                            elif piece == 'wR':
                                if old_square == 'a1':
                                    self.wQR_moved = True
                                    self.attributes[3] = True
                                elif old_square == 'h1':
                                    self.wKR_moved = True
                                    self.attributes[2] = True
                            elif piece == 'bR':
                                if old_square == 'a8':
                                    self.bQR_moved = True
                                    self.attributes[7] = True
                                elif old_square == 'h8':
                                    self.bKR_moved = True
                                    self.attributes[6] = True

                            


                        else:
                            if move == 'O-O':

                                if self.turn == 'w':
                                    self.state['e1'].piece = ""
                                    self.state['f1'].piece = 'wR'
                                    self.state['g1'].piece = 'wK'
                                    self.state['h1'].piece = ""

                                    self.wcastled = True
                                    self.attributes[0] = True
                                    self.wK_pos = 'g1'


                                else:
                                    self.state['e8'].piece = ""
                                    self.state['f8'].piece = 'bR'
                                    self.state['g8'].piece = 'bK'
                                    self.state['h8'].piece = ""

                                    self.bcastled = True
                                    self.attributes[4] = True
                                    self.bK_pos = 'g8'


                            elif move == 'O-O-O':
                                print('castle')
                                if self.turn == 'w':
                                    self.state['e1'].piece = ""
                                    self.state['d1'].piece = 'wR'
                                    self.state['c1'].piece = 'wK'
                                    self.state['a1'].piece = ""

                                    self.wcastled = True
                                    self.attributes[0] = True
                                    self.wK_pos = 'c1'

                                else:
                                    self.state['e8'].piece = ""
                                    self.state['d8'].piece = 'bR'
                                    self.state['c8'].piece = 'bK'
                                    self.state['a8'].piece = ""

                                    self.bcastled = True
                                    self.attributes[4] = True
                                    self.bK_pos = 'c8'

                            else:

                                prom_square = move[-4:-2]
                                self.state[old_square].piece = ""
                                if move[-1] == 'Q':
                                    self.state[prom_square].piece = str(self.turn + 'Q')

                                    if self.turn == 'w':
                                        self.num_wQ += 1
                                    else:
                                        self.num_bQ += 1


                                elif new_move[-1] == 'R':
                                    self.state[prom_square].piece = str(self.turn + 'R')

                                elif new_move[-1] == 'N':
                                    self.state[prom_square].piece = str(self.turn + 'N')

                                elif new_move[-1] == 'B':
                                    self.state[prom_square].piece = str(self.turn + 'B')

                        self.actual_moves_made.append(tup)

                        if self.turn == 'w':
                            self.turn = 'b'
                            #print('from acutal white candidate_moves: ')
                            self.legal_moves = self.Prevent_Check(self.Make_Candidate_Moves(self.state, tup, self.num_wQ, self.num_bQ, attributes))
                            
                            break
                        else:
                            self.turn = 'w'
                            #print( 'from actual black candidate_moves ')
                            self.legal_moves = self.Prevent_Check(self.Make_Candidate_Moves(self.state, tup, self.num_wQ, self.num_bQ, attributes))
                            break


                    
                if not move_found:
                    print('Invalid move, please try again')
            
    
        
                
