from board.move import move
from board.tile import Tile
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random
import copy

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr

    '''
    Major factors that go into a chess eval. function
    - Material
    - Pawn Structure
    - Evaluation of Pieces
    - Mobility
    - Center Control
    - King Safety
    - Space
    https://chess.stackexchange.com/questions/41180/how-do-you-program-a-chess-bot-with-specific-style
    Examples of Eval out there-  https://www.chessprogramming.org/Evaluation

    A majority of the code was made with the help of chatGBT but the parts of the evaluation functions were determine from research into the
    historically best methods for evaluating the states. The parameters were farther tuned to optimize the win rate of the machine.
    '''
    # Constants
    PHALANGIAN_PENALTY = 20
    DEVELOPMENT_BONUS = 20
    CENTER_SQUARES = [(3, 3), (3, 4), (4, 3), (4, 4)]
    WIDER_CENTER_SQUARES = [(2, 2), (2, 3), (2, 4), (2, 5), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (5, 2), (4, 2), (3, 2)]
    BLACK_PIECES = "PNBRQK"
    WHITE_PIECES = "pnbrqk"

    def calculateb(self, gametiles):
        # Initialize variables
        materialValue = 0
        onBoard = {piece: 0 for piece in "PNBRQKPpnbrqk-"}
        pieceValues = {
            'P': -100, 'N': -350, 'B': -350, 'R': -525, 'Q': -1000, 'K': -10000,
            'p': 100, 'n': 350, 'b': 350, 'r': 525, 'q': 1000, 'k': 10000, '-': 0
        }

        # Precompute piece values and count
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile.tostring()
                onBoard[piece] += 1
                materialValue += pieceValues[piece]

        # Material evaluation
        totalMaterialAdvantage = self.evaluate_material(gametiles)

        # Center control evaluation
        centerControl = self.evaluate_center_control(gametiles)

        # Development and phalangian evaluation
        developmentRating = self.evaluate_development(gametiles)

        # Mobility evaluation
        mobility = self.evaluate_mobility(gametiles,'Black')

        # Pawn Structure evaluation
        pawnStructure = self.evaluate_pawn_structure(gametiles)

        # Safety evaluation
        safety = self.evaluate_piece_safety(gametiles)
        #safety = 0
         # Print component values
        print("Total Material Advantage:", totalMaterialAdvantage)
        print("Center Control:", centerControl)
        print("Development Rating:", developmentRating)
        print("Mobility:", mobility)
        print("Pawn Structure:", pawnStructure)
        print("Safety:", safety)
        # Evaluate the opening stage (prioritize development)
        if onBoard['P'] + onBoard['p'] >= 28:
            value = totalMaterialAdvantage + 2*developmentRating + mobility + centerControl + pawnStructure + safety*2
        else:
            # In the middle and endgame, prioritize material advantage
            value = totalMaterialAdvantage + centerControl + mobility + pawnStructure + safety*2
        #value = totalMaterialAdvantage
        return value

    def evaluate_piece_safety(self, gametiles):
        # Initialize piece safety score
        piece_safety_score = 0

        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile.tostring()
                if piece != '-':
                    # Evaluate the safety of each piece
                    safety = len(self.evaluate_piece_protection(gametiles, x, y, piece))
                    true_safety = 0
                    if(safety==0):
                        true_safety =-20
                    else:
                        true_safety = safety*5
                    # Add or subtract safety scores based on the piece color
                    if piece.islower():
                        piece_safety_score += safety
                    else:
                        piece_safety_score -= safety

        return piece_safety_score
    def evaluate_piece_protection(self, gametiles, x, y, piece):
        # Can be improved by getting all the attacking squares then checking 
        # Evaluate how well a piece is protected
        defending_pieces = []

        # Iterate through all pieces on the board
        for px in range(8):
            for py in range(8):
                if px == x and py == y:
                    continue  # Skip the current square
                attacker = gametiles[py][px].pieceonTile.tostring()
                if attacker.lower() == piece.lower():
                    # Found a piece defending the current piece
                    defending_pieces.append((px, py))
                elif attacker.lower() == 'p' and self.can_move_to(x, y, px, py, gametiles):
                    # Check if a black pawn can move to defend
                    defending_pieces.append((px, py))

        return defending_pieces
    def can_move_to(self, x, y, target_x, target_y, gametiles):
        piece = gametiles[y][x].pieceonTile.tostring()

        def is_clear_path(start_x, start_y, end_x, end_y):
            # Helper function to check if the path is clear of other pieces
            dx = abs(end_x - start_x)
            dy = abs(end_y - start_y)
            
            if dx == 0:
                step_y = 1 if end_y > start_y else -1
                for i in range(start_y + step_y, end_y, step_y):
                    if gametiles[i][start_x].pieceonTile.tostring()!='-':
                        return False
            elif dy == 0:
                step_x = 1 if end_x > start_x else -1
                for i in range(start_x + step_x, end_x, step_x):
                    if gametiles[start_y][i].pieceonTile.tostring()!='-':
                        return False
            elif dx == dy:
                step_x = 1 if end_x > start_x else -1
                step_y = 1 if end_y > start_y else -1
                i, j = start_x + step_x, start_y + step_y
                while i != end_x and j != end_y:
                    if gametiles[j][i].pieceonTile.tostring()!='-':
                        return False
                    i += step_x
                    j += step_y
            return True

        if piece.lower() == 'p':
            # Pawn movement
            if x + 1 == target_x or x - 1 == target_x:
                return y - 1 == target_y
            if x == target_x:
                if piece.islower():
                    if y - target_y == 1 and not gametiles[target_y][target_x].pieceonTile.tostring()!='-':
                        return True
                else:
                    if target_y - y == 1 and not gametiles[target_y][target_x].pieceonTile.tostring()!='-':
                        return True

        if piece.lower() == 'n':
            # Knight movement
            # Calculate all squares a knight can reach and check if the target square is one of them
            possible_moves = [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
                            (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]
            return (target_x, target_y) in possible_moves

        if piece.lower() == 'b':
            # Bishop movement
            # Check if it can move diagonally to the target square
            if abs(target_x - x) == abs(target_y - y):
                return is_clear_path(x, y, target_x, target_y)

        if piece.lower() == 'r':
            # Rook movement
            # Check if it can move vertically or horizontally to the target square
            if target_x == x or target_y == y:
                return is_clear_path(x, y, target_x, target_y)

        if piece.lower() == 'q':
            # Queen movement
            # Check if it can move to the target square diagonally, vertically, or horizontally
            if (abs(target_x - x) == abs(target_y - y)) or target_x == x or target_y == y:
                return is_clear_path(x, y, target_x, target_y)

        if piece.lower() == 'k':
            # King movement
            # Check if it can move to the target square in any direction
            return abs(target_x - x) <= 1 and abs(target_y - y) <= 1

        return False


    def evaluate_open_files(self, gametiles):
        # Initialize open file score
        open_file_score = 0

        # Evaluate open files (files without pawns)
        # You can iterate through the board and assess each file's openness

        return open_file_score

    def find_piece_position(self, gametiles, piece):
        # Helper function to find the position (x, y) of a specific piece on the board
        for x in range(8):
            for y in range(8):
                if gametiles[y][x].pieceonTile.tostring() == piece:
                    return x, y

        return -1, -1  # Return (-1, -1) if the piece is not found

    def count_attacking_pieces(self, gametiles, x, y):
        # Helper function to count how many enemy pieces are attacking a specific square
        # You can iterate through the board and check for enemy piece attacks

        return 0  # Return the count of attacking pieces

    # Constants for safety evaluation
    KING_EXPOSURE_PENALTY = 10
    def evaluate_material(self, gametiles):
        material_advantage = 0

        # Define piece values with positive and negative values
        piece_values = {
            'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 10000,
            'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -10000, '-': 0
        }

        # Adjust positional values with the same structure but with reversed values
        positional_values = {
            'P': [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [-10, -10, -10, -10, -10, -10, -10, -10],
                [-5, -5, -10, -10, -10, -10, -5, -5],
                [-5, -5, -10, -20, -20, -10, -5, -5],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [-5, 5, 10, 0, 0, 10, 5, -5],
                [-5, -10, -10, 20, 20, -10, -10, -5],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            'N': [
                [50, 40, 30, 30, 30, 30, 40, 50],
                [40, 20, 0, 0, 0, 0, 20, 40],
                [30, 0, -10, -15, -15, -10, 0, 30],
                [30, -5, -15, -20, -20, -15, -5, 30],
                [30, 0, -15, -20, -20, -15, 0, 30],
                [30, -5, -10, -15, -15, -10, -5, 30],
                [40, 20, 0, -5, -5, 0, 20, 40],
                [50, 40, 30, 30, 30, 30, 40, 50]
            ],
            'B': [
                [20, 10, 10, 10, 10, 10, 10, 20],
                [10, 0, 0, 0, 0, 0, 0, 10],
                [10, 0, -5, -10, -10, -5, 0, 10],
                [10, -5, -5, -10, -10, -5, -5, 10],
                [10, 0, -10, -10, -10, -10, 0, 10],
                [10, -10, -10, -10, -10, -10, -10, 10],
                [10, -5, 0, 0, 0, 0, -5, 10],
                [20, 10, 10, 10, 10, 10, 10, 20]
            ],
            'R': [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, -5, -10, -10, -10, -10, -5, 0],
                [5, 0, 0, 0, 0, 0, 0, 5],
                [5, 0, 0, 0, 0, 0, 0, 5],
                [5, 0, 0, 0, 0, 0, 0, 5],
                [5, 0, 0, 0, 0, 0, 0, 5],
                [5, 0, 0, 0, 0, 0, 0, 5],
                [0, 0, 0, -5, -5, 0, 0, 0]
            ],
            'Q': [
                [20, 10, 10, 5, 5, 10, 10, 20],
                [10, 0, 0, 0, 0, 0, 0, 10],
                [10, 0, -5, -5, -5, -5, 0, 10],
                [5, 0, -5, -5, -5, -5, 0, 5],
                [0, 0, -5, -5, -5, -5, 0, 5],
                [10, -5, -5, -5, -5, -5, 0, 10],
                [10, 0, -5, 0, 0, 0, 0, 10],
                [20, 10, 10, 5, 5, 10, 10, 20]
            ],
            'K': [
                [-20, -30, -10, 0, 0, -10, -30, -20],
                [-20, -20, 0, 0, 0, 0, -20, -20],
                [10, 20, 20, 20, 20, 20, 20, 10],
                [20, 30, 30, 40, 40, 30, 30, 20],
                [30, 40, 40, 50, 50, 40, 40, 30],
                [40, 50, 50, 60, 60, 50, 50, 40],
                [50, 60, 60, 70, 70, 60, 60, 50],
                [60, 70, 70, 80, 80, 70, 70, 60]
            ],
            'p': [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5, 5, 10, 25, 25, 10, 5, 5],
                [0, 0, 0, 20, 20, 0, 0, 0],
                [5, -5, -10, 0, 0, -10, -5, 5],
                [5, 10, 10, -20, -20, 10, 10, 5],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            'n': [
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20, 0, 0, 0, 0, -20, -40],
                [-30, 0, 10, 15, 15, 10, 0, -30],
                [-30, 5, 15, 20, 20, 15, 5, -30],
                [-30, 0, 15, 20, 20, 15, 0, -30],
                [-30, 5, 10, 15, 15, 10, 5, -30],
                [-40, -20, 0, 5, 5, 0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50]
            ],
            'b': [
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 10, 10, 5, 0, -10],
                [-10, 5, 5, 10, 10, 5, 5, -10],
                [-10, 0, 10, 10, 10, 10, 0, -10],
                [-10, 10, 10, 10, 10, 10, 10, -10],
                [-10, 5, 0, 0, 0, 0, 5, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20]
            ],
            'r': [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [5, 10, 10, 10, 10, 10, 10, 5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [0, 0, 0, 5, 5, 0, 0, 0]
            ],
            'q': [
                [-20, -10, -10, -5, -5, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 5, 5, 5, 0, -10],
                [-5, 0, 5, 5, 5, 5, 0, -5],
                [0, 0, 5, 5, 5, 5, 0, -5],
                [-10, 5, 5, 5, 5, 5, 0, -10],
                [-10, 0, 5, 0, 0, 0, 0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20]
            ],
            'k': [
                [20, 30, 10, 0, 0, 10, 30, 20],
                [20, 20, 0, 0, 0, 0, 20, 20],
                [-10, -20, -20, -20, -20, -20, -20, -10],
                [-20, -30, -30, -40, -40, -30, -30, -20],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-40, -50, -50, -60, -60, -50, -50, -40],
                [-50, -60, -60, -70, -70, -60, -60, -50],
                [-60, -70, -70, -80, -80, -70, -70, -60]
            ]
        }

        # Evaluate material advantage based on piece values and positions
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile.tostring()
                if(piece!='-'):
                    material_advantage += -piece_values[piece]*2
                    material_advantage += positional_values[piece][y][x]*.2

        return material_advantage
    def evaluate_center_control(self,gametiles):
        centerControl = 0
        for m, k in self.CENTER_SQUARES:
            tile = gametiles[m][k].pieceonTile.tostring()
            if tile in self.BLACK_PIECES:
                centerControl -= 20
            else:
                centerControl += 20
        for m,k in self.WIDER_CENTER_SQUARES:
            tile = gametiles[m][k].pieceonTile.tostring()
            if tile in self.BLACK_PIECES:
                centerControl -= 10
            else:
                centerControl += 10
        return centerControl


    def evaluate_development(self, gametiles):
        # Initialize a dictionary to keep track of piece development by type and side
        piece_development = {'P': 0, 'N': 0, 'B': 0, 'R': 0, 'Q': 0, 'K': 0, 'p': 0, 'n': 0, 'b': 0, 'r': 0, 'q': 0, 'k': 0}

        # Count how many squares are occupied in the first two ranks (for White) and last two ranks (for Black)
        white_occupied_squares = sum(1 for x in range(8) for y in range(2) if gametiles[y][x].pieceonTile.tostring() != '-')
        black_occupied_squares = sum(1 for x in range(8) for y in range(6, 8) if gametiles[y][x].pieceonTile.tostring() != '-')

        # Evaluate piece development
        for x in range(8):
            for piece_type in piece_development:
                piece_count = sum(1 for y in range(8) if gametiles[y][x].pieceonTile.tostring() == piece_type)
                if piece_count > 0:
                    # Check the side (White or Black)
                    side = 'W' if piece_type.isupper() else 'B'
                    # Evaluate the piece development based on its type and side
                    piece_development[piece_type] += self.evaluate_piece_development(piece_type, side, x)

        # Calculate a development rating based on the accumulated piece development scores
        development_rating = 0
        for piece_type, score in piece_development.items():
            if piece_type.islower():
                development_rating += score
            else:
                development_rating -= score

        # Adjust the development rating based on the number of occupied squares in the back ranks
        development_rating -= white_occupied_squares*12  # Penalty for White if not all back-rank squares are occupied

        development_rating += black_occupied_squares*12  # Penalty for Black if not all back-rank squares are occupied
        '''
        # Check additional factors and adjust the development rating accordingly
        if gametiles[0][1].pieceonTile.tostring() == 'N' and gametiles[0][2].pieceonTile.tostring() == 'B':
            development_rating += 20  # +20 for developing N before B

        if gametiles[0][1].pieceonTile.tostring() == 'N' and gametiles[0][4].pieceonTile.tostring() == 'Q':
            development_rating -= 30  # -30 for developing Q before 2 minor pieces are developed

        if gametiles[0][1].pieceonTile.tostring() == 'N' and gametiles[0][3].pieceonTile.tostring() == 'R':
            development_rating -= 50  # -50 for developing R before 2 minors are developed
        '''
        # Add more conditions for other factors

        # Determine if Black is more developed and adjust the development rating accordingly
        

        return development_rating

    def evaluate_piece_development(self, piece_type, side, file):
        # Customize piece development evaluation based on piece type, side, and file (column)
        score = 0

        # Adjust the score based on piece type and file (column)
        if piece_type == 'P' and side == 'W' and file not in [0, 7]:
            score += 10  # Bonus for White pawns in the center files (not on the edge)
        elif piece_type == 'p' and side == 'B' and file not in [0, 7]:
            score -= 10  # Penalty for Black pawns in the center files (not on the edge)
        
        # Add more evaluation logic for other pieces, sides, and files as needed

        return score
    def evaluate_mobility(self, gametiles, alliance):
        # Initialize mobility score
        mobility = 0

        # Get all pieces of the current side
        pieces = []
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile
                if piece.tostring() != '-' and piece.alliance == alliance:
                    pieces.append(piece)

        # Calculate mobility for each piece
        for piece in pieces:
            legal_moves = piece.legalmoveb(gametiles)
            if(legal_moves is not None):
                mobility += len(legal_moves)

        return mobility
    def evaluate_pawn_structure(self, gametiles):
        # Initialize variables to track pawn structure evaluation
        pawn_structure_score = 0
        doubled_pawns_penalty = 0
        isolated_pawns_penalty = 0
        backward_pawns_penalty = 0
        central_pawns_bonus = 0

        for x in range(8):
            white_pawns_in_column = sum(1 for y in range(8) if gametiles[y][x].pieceonTile.tostring() == 'P')
            black_pawns_in_column = sum(1 for y in range(8) if gametiles[y][x].pieceonTile.tostring() == 'p')

            # Doubled Pawns
            if white_pawns_in_column > 1:
                doubled_pawns_penalty += (white_pawns_in_column - 1) * 10

            if black_pawns_in_column > 1:
                doubled_pawns_penalty -= (black_pawns_in_column - 1) * 10

            # Isolated Pawns
            if white_pawns_in_column > 0 and black_pawns_in_column == 0:
                isolated_pawns_penalty += white_pawns_in_column * 15

            if black_pawns_in_column > 0 and white_pawns_in_column == 0:
                isolated_pawns_penalty -= black_pawns_in_column * 15

            # Backward Pawns
            if white_pawns_in_column > 0:
                for y in range(8):
                    if gametiles[y][x].pieceonTile.tostring() == 'P':
                        if not self.has_supporting_pawn(gametiles, 'W', x, y):
                            backward_pawns_penalty += 20

            if black_pawns_in_column > 0:
                for y in range(8):
                    if gametiles[y][x].pieceonTile.tostring() == 'p':
                        if not self.has_supporting_pawn(gametiles, 'B', x, y):
                            backward_pawns_penalty -= 20

            # Central Pawns Bonus
            if x in [3, 4]:
                central_pawns_bonus += (black_pawns_in_column - white_pawns_in_column) * 10

        # Calculate the overall pawn structure score
        pawn_structure_score = doubled_pawns_penalty + isolated_pawns_penalty + backward_pawns_penalty + central_pawns_bonus

        return -1*pawn_structure_score

    def has_supporting_pawn(self, gametiles, side, x, y):
        # Check if there is a supporting pawn on an adjacent file
        if side == 'W':
            opposite_side = 'B'
        else:
            opposite_side = 'W'

        # Check left diagonal
        if x > 0 and y < 7 and gametiles[y + 1][x - 1].pieceonTile.tostring() == opposite_side:
            return True

        # Check right diagonal
        if x < 7 and y < 7 and gametiles[y + 1][x + 1].pieceonTile.tostring() == opposite_side:
            return True

        return False






    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles
    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles
    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles



"""

        def getDeffenders(attacks,m,k,alliance):
            deffenders= []
            for i in attacks[m][k]:
                if(i.pieceonTile.alliance==alliance):
                    deffenders.append(i.pieceonTile.tostring())
            return deffenders
        #LOWER NUMBER IS better for black and higher number better for white
        CENTER_TILES=[(3,3),(3,4),(4,3),(4,4)]
        WIDER_CENTER_TILES=[(2,2),(2,3),(2,4),(2,5),(3,5),(4,5),(5,5),(5,4),(5,3),(5,2),(4,2),(3,2)]
        BLACK_TILES= "PNBRQK"
        WHITE_TILES= "pnbrqk"
        gametiles = gametilesOLD.copy()
        materialValue=0
        onBoard = {}
        for i in "PNBRQKPpnbrqk-":
            onBoard[i]=0
        pieceWeight = {'P':-100,'N':-350,'B':-350,'R':-525,'Q':-1000,'K':-10000,'p':100,'n':350,'b':350,'r':525,'q':1000,'k':10000,'-':0}
        
        for x in range(8):
            for y in range(8):
                onBoard[gametiles[y][x].pieceonTile.tostring()]+=1
        #mapToValue = lambda x: pieceWeight[x[0]]*x[1]
        materialValue = sum(list(map(lambda x: pieceWeight[x[0]]*x[1],onBoard.items())))
        #print(materialValue)
        allWhitePieces = [[0 for x in range(8)] for y in range(8)]
        allBlackPieces = [[0 for x in range(8)] for y in range(8)]
        for m in range(8):
            for k in range(8):
                if(gametiles[m][k].pieceonTile.tostring()!='-'):
                    tile = copy.deepcopy(gametiles[m][k])
                    tile.pieceonTile.alliance='White'
                    allWhitePieces[m][k] = tile
                    tile = copy.deepcopy(gametiles[m][k])
                    tile.pieceonTile.alliance='Black'
                    allBlackPieces[m][k] = tile
                else:
                    allWhitePieces[m][k] = gametiles[m][k]
                    allBlackPieces[m][k] = gametiles[m][k]
        movableOptions = [[[] for x in range(8)] for y in range(8)]
        attacks = [[[] for x in range(8)] for y in range(8)]
        #Gets all the moves to every square
        for m in range(8):
            for k in range(8):
                
                #print(gametiles[m][k].pieceonTile.tostring(),m,k)
                
                if(gametiles[m][k].pieceonTile.tostring()!="-"):
                    
                    #print(gametiles[m][k].pieceonTile.tostring(),gametiles[m][k].pieceonTile.alliance,m,k)
                    gametiles[m][k].tileCorrdinate= m*8+k
                    
                    #print(emptyBoard[m][k].tileCorrdinate)
                    moves=gametiles[m][k].pieceonTile.legalmoveb(gametiles)
                    #print(gametiles[m][k].pieceonTile.calculatecoordinates())
                    if moves is not None:
                        for move in moves:
                                movableOptions[move[0]][move[1]].append(gametiles[m][k])
                    if(gametiles[m][k].pieceonTile.alliance=="Black"):
                        allWhitePieces[m][k].pieceonTile.alliance="Black"
                        moves=gametiles[m][k].pieceonTile.legalmoveb(allWhitePieces)
                        if moves is not None:
                            for move in moves:
                                    attacks[move[0]][move[1]].append(gametiles[m][k])
                        allWhitePieces[m][k].pieceonTile.alliance="White"
                    else:
                        allBlackPieces[m][k].pieceonTile.alliance="White"
                        moves=gametiles[m][k].pieceonTile.legalmoveb(allBlackPieces)
                        if moves is not None:
                            for move in moves:
                                    attacks[move[0]][move[1]].append(gametiles[m][k])
                        allBlackPieces[m][k].pieceonTile.alliance="Black"
                    #emptyBoard[m][k] = Tile(emptyBoard[m][k].tileCorrdinate,nullpiece())
        

        #print(attacks)
        
        #Gets if white is checked
        #movex.checkw(gametiles)[0]=='checked'
        #Gets if black is checked
        #movex.checkb(gametiles)[0]=='checked'
        #Function that gets the pieces attacking a square
        #Function that gets the places from a space a piece can move
        #moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
        #From the following source https://www.chessprogramming.org/images/5/58/Addendum5LCEC_2012.pdf

        #Material
        #https://www.chessprogramming.org/Material_Hash_Table Chess 4.5
        standardPieceWeight = {'P':-100,'N':-325,'B':-350,'R':-500,'Q':-900,'K':0,'p':100,'n':325,'b':350,'r':500,'q':900,'k':0,'-':0}
        standardMaterialValue = sum(list(map(lambda x: standardPieceWeight[x[0]]*x[1],onBoard.items())))
        WinningSide = 'p' if (standardMaterialValue>0) else 'P'
       
        MD = abs(standardMaterialValue)
        PA = onBoard[WinningSide]
        materialTotal = sum(list(map(lambda x: abs(standardPieceWeight[x[0]]*x[1]),onBoard.items())))
        MS = min(2400,MD)+(MD*PA*(8000-materialTotal))/(6400*(PA+1))
        TotalMaterialAdvantage = min(3100,MS)
        print(WinningSide,standardMaterialValue,onBoard[WinningSide],MS)
        assert(TotalMaterialAdvantage>=0)
        if(materialValue<0):
            TotalMaterialAdvantage = -1*TotalMaterialAdvantage 
        #print(TotalMaterialAdvantage)
       
        #Piece-square Tables
        #Pawn Structure
        #Evaluation of pieces
        #Mobility
        #Center Control
        #Connectivity
        #Trapped Pieces
        #King Safety
        #Space
        #Tempo

        #Opening
        
        Control of center http://www.winboardengines.de/doc/LittleChessEvaluationCompendium-2010-04-07.pdf
        Control of focal center (i.e. the squares e4,d4,e5,d5)
        Pawns occupying the focal center
        +40 for each p on such a square
        Pieces occupying the focal center
        +20 for a minor piece and +30 for q on such a square
        Pawns keeping control of focal center
        +10 for such a function (eg. the c3,d3,e3,f3 ps are controlling one square each as well as the
        c4,d4,e4,f4 ps do)
        Pieces keeping control of focal center
        +10 for such a function for each square a piece controls (eg. the wnf3 has under control the d4
        and e5 squares, so it would get a bonus of +20). This concerns all pieces.'''
        centerControl = 0
        for m in [3,4]:
            for k in [3,4]:
                tile =gametiles[m][k].pieceonTile.tostring()
                if(tile=='P'):
                    centerControl-=40
                if(tile=='p'):
                    centerControl+=40
                if(tile in 'BN'):
                    centerControl-=20
                if(tile in 'bn'):
                    centerControl+=20 
                if(tile=='Q'):
                    centerControl-=30
                if(tile=='q'):
                    centerControl+=30
                for attacker in attacks[m][k]:
                    if(attacker.pieceonTile.alliance=="Black"):
                        centerControl-=10
                    else:
                        centerControl+=10
        '''
        Control of wider center (i.e. the squares bound by c3-f3-f6-c6 excluding the focal centersquares)
        Pieces occupying the wider center
        +10 is given for every piece on a square of the wider center
        '''

        for x,y in WIDER_CENTER_TILES:
            tile =gametiles[m][k].pieceonTile.tostring()
            if(tile=='-'):
                continue
            elif(tile in BLACK_TILES):
                centerControl-=10
            else:
                centerControl+=10
        developmentRating = 0
        if(onBoard['-']<34):
            developed={'P':0}
            for i in 'RNBQKBNR':
                developed[i]=0
            for index, item in enumerate('RNBQKBNR'):
                if(gametiles[0][index].pieceonTile.tostring()!=item):
                    developed[item]+=1
            for i in range(8):
                if(gametiles[1][index].pieceonTile.tostring()!='P'):
                    developed['P']+=1
            

            # knights 0,1 0,6
            # bishops 0,2 0,5
            #+20 for developing n before b
            
            if(developed['N']>developed['B']):
                developmentRating -= 20
            #-30 for developing q before 2 minor pieces are developed
            if(developed['Q']==1 and developed['N']+developed['B']<2):
                developmentRating += 20
            #-50 for developing r before 2 minors are developed
            if(developed['R']==1 and developed['N']+developed['B']<2):
                developmentRating += 20
            #+60 for castling to developing pieces on the other side
            if(gametiles[0][6].pieceonTile.tostring()=='K'):
                developmentRating -= 60
            
            #+50 for castling short to castling long if both possible
            if(gametiles[0][2].pieceonTile.tostring()=='K'):
                developmentRating -= 50
        
        '''
        Phalangian development (also middlegame)
        Probably borrowed by Phalanx, I do not know. This assumes development of pawns and
        pieces in compact order. -20 for own p into the enemy camp unsupported by other ps (eg.
        wpb5, wpa2, no c pawn). -30 for own piece into the enemy camp unsupported by other pawns
        or pieces.
        '''
        phalangianDevelopment = 0
        for m in range(4,7):
            for k in range(4,7):
                tile =gametiles[m][k].pieceonTile.tostring()
                if(tile=='P'):
                    deffenders = getDeffenders(attacks,m,k,"Black")
                    if(len(deffenders)==0):
                        phalangianDevelopment +=20
                    if('P' not in deffenders):
                        phalangianDevelopment +=30
        #print("PHILALSDSNAD A"+str(phalangianDevelopment))

        
        '''
        Mobility
        +    10 for each free square a piece has access to'''
        mobility = 0
        for m in range(8):
            for k in range(8):
                for x,y,piece in movableOptions[m][k]:
                    if(piece in BLACK_TILES):
                        mobility-=10
                    else:
                        mobility+=10
        
        coordination = 0
        attackingPotential= 0
        for m in range(8):
            for k in range(8):
                for x,y,piece in movableOptions[m][k]:
                    if(piece in BLACK_TILES):
                        mobility-=10
                    else:
                        mobility+=10
        
        value = TotalMaterialAdvantage + centerControl + phalangianDevelopment +developmentRating +mobility
        return value
"""




















                        
