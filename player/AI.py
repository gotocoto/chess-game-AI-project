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
    '''
    # Constants
    PHALANGIAN_PENALTY = 20
    DEVELOPMENT_BONUS = 20
    CENTER_SQUARES = [(3, 3), (3, 4), (4, 3), (4, 4)]
    WIDER_CENTER_SQUARES = [(2, 2), (2, 3), (2, 4), (2, 5), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (5, 2), (4, 2), (3, 2)]
    BLACK_PIECES = "PNBRQK"
    WHITE_PIECES = "pnbrqk"

    def calculateb(self,gametiles):
        
        # Initialize variables
        materialValue = 0
        onBoard = {piece: 0 for piece in "PNBRQKPpnbrqk-"}
        pieceValues = {'P': -100, 'N': -350, 'B': -350, 'R': -525, 'Q': -1000, 'K': -10000, 'p': 100, 'n': 350, 'b': 350, 'r': 525, 'q': 1000, 'k': 10000, '-': 0}
        # Precompute piece values and count
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile.tostring()
                onBoard[piece] += 1
                materialValue += pieceValues[piece]

        # Material evaluation
        totalMaterialAdvantage = self.evaluate_material(onBoard)

        # Center control evaluation
        centerControl = self.evaluate_center_control(gametiles)

        # Development and phalangian evaluation
        developmentRating = self.evaluate_development(gametiles)

        # Mobility evaluation
        mobility = self.evaluate_mobility(gametiles)

        # Final evaluation
        value = totalMaterialAdvantage + centerControl + developmentRating + mobility
        return value

    def evaluate_material(self,onBoard):
        standardPieceValues = {'P': -100, 'N': -325, 'B': -350, 'R': -500, 'Q': -900, 'K': 0, 'p': 100, 'n': 325, 'b': 350, 'r': 500, 'q': 900, 'k': 0, '-':0}
        standardMaterialValue = sum(standardPieceValues[piece] * count for piece, count in onBoard.items())
        winningSide = 'p' if standardMaterialValue > 0 else 'P'
        md = abs(standardMaterialValue)
        pa = onBoard[winningSide]
        materialTotal = sum(abs(standardPieceValues[piece] * count) for piece, count in onBoard.items())
        ms = min(2400, md) + (md * pa * (8000 - materialTotal)) / (6400 * (pa + 1))
        totalMaterialAdvantage = min(3100, ms)
        return totalMaterialAdvantage

    def evaluate_center_control(self,gametiles):
        centerControl = 0
        for m, k in self.CENTER_SQUARES:
            tile = gametiles[m][k].pieceonTile.tostring()
            if tile in self.BLACK_PIECES:
                centerControl -= 10
            else:
                centerControl += 10
        return centerControl

    def evaluate_development(self,gametiles):
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
        if white_occupied_squares < 16:
            development_rating -= 60  # Penalty for White if not all back-rank squares are occupied

        if black_occupied_squares < 16:
            development_rating += 60  # Penalty for Black if not all back-rank squares are occupied

        return development_rating
    def evaluate_piece_development(self,piece_type, side, file):
        # Customize piece development evaluation based on piece type, side, and file (column)
        score = 0
        if piece_type == 'P' and side == 'W' and file not in [0, 7]:
            score += 10  # Bonus for White pawns in the center files (not on the edge)
        elif piece_type == 'p' and side == 'B' and file not in [0, 7]:
            score -= 10  # Penalty for Black pawns in the center files (not on the edge)
        
        # Add more evaluation logic for other pieces, sides, and files as needed
        
        return score
    def evaluate_mobility(self,gametiles):
        # Add your mobility evaluation here
        # Calculate the mobility
        mobility = 0
        return mobility
    

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




















                        
