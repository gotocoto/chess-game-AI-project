from board.move import move
from board.tile import Tile
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

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
    def calculateb(self,gametilesOLD):
        #LOWER NUMBER IS better for black and higher number better for white
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
                                attacks[move[0]][move[1]].append(gametiles[m][k])
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
        WinningSide = 'p' if (materialValue>0) else 'P'
        MD = abs(materialValue)
        PA = onBoard[WinningSide]
        materialTotal = sum(list(map(lambda x: abs(pieceWeight[x[0]]*x[1]),onBoard.items())))
        MS = min(2400,MD)+(MD*PA*(8000-materialTotal))/(6400*(PA+1))
        TotalMaterialAdvantage = min(3100,MS)
        print(TotalMaterialAdvantage)
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
        '''
        Attacking enemy pieces pinning own pieces
            Pieces attacking enemy pieces that pin own ones are due some bigger bonus than the standard
            one for attacking pieces (by 1/4 bigger), even if the pinning piece is well defended and the
            attacking piece is of bigger power in relation to the pinner, as this might have some important
            tactical implications.
        Bishop the colour of a weak spot in the enemy king position with the enemy side having no bishop of the same colour
            In that case the bishop without an enemy counterpart would score +20cps for any weak spot
            of the same colour, as attacking chances would greatly increase with queens on the board.
        Flexible pawn structures
            A flexible pawn structure would be any group of 3 ps with the following characteristics:
            - being important in some way
            - most of the moves of the ps of that group would result in another group of ps sharing the
            same characteristics
            Most notable flexible pawn structures would be the following:
            - group consisting of 3 horizontally adjacent ps (eg. wpsd4,e4,f4); those ps control a range of
            continuous squares, and besides they could easily transpose into a group with an apex p
            - group with an apex p (eg. wpsd3,e4,f3); this structure is important because of the apex p,
            and besides it could easily transpose into a group of ps with a lead p horizontally adjacent to
            another own p
            - group of ps with a lead p horizontally adjacent to another own p; this group could easily
            transpose into three horizontally adjacent ps or a larger diagonal connection
            Flexible pawn structures might score the following bonus points:
            +2cps for a group consisting of 3 horizontally adjacent ps
            +5cps for a group with a lead p horizontally adjacent to another own p
            +10cps for a group with an apex p
            Other groups of 3 ps would not share the same characteristics of flexibility. A diagonal
            connection of 3 ps, for example, would crumble with any move of a pawn of the group and no
            other flexible structure would replace it; a group of 3 ps with one root pawn connecting to 2
            more advanced ps (eg. wpsd3,e4,c4) with the best of moves could only transpose to a group of
            3 horizontally adjacent ps, the least valuable of the flexible structures.
            Flexibility bonus points would receive also larger groups of ps with 3 of them exhibiting the
            above characteristics. Structures with a least advanced p on the 2nd rank would not be
            considered.
        Mobility takes precedence over attacks
            In the case a certain piece has very good attacking potential, but very low mobility (no free or
            just one free squares), it would be wise not to consider such moves at all, as usually deeper
            into the game attacking potential could whittle away, but mobility will remain low. That could
            be a losing variation, even if the piece attacks important squares of the enemy king shelter.
            Sometimes engines commit such mistakes.

        Temporary backward pawn
            A temporary backward pawn would be one that can not advance at the moment, but whose
            advance could be supported in the future by another p. Eg. wpb3, bpsc5,b7 - c5 is such a
            pawn, but bpb5 is possible at a later stage
            -5cps for such a p
        Control of squares into the enemy camp on the 5th rank on the side where the enemy king has castled
            Controlling squares into the enemy camp on the 5th rank on the side where the enemy king
            has castled (or taken refuge) will be due double the bonus points for the usual case of
            controlling squares into the enemy camp, because this could have some vital importance in
            terms of reinforcements for king attack.
        The hub pawn
            The hub pawn would be a pawn that is a lead pawn of one diagonal connection and a root
            pawn of another one. Eg. wpsb3,c4,b5 - c4 would be such a p That is, hub pawns concern
            doubling. Such double ps are preferable to other types of double ps, of course, because they
            are better defended. The hub pawn is the center point of the entire group and it is very sturdy.
            Therefore, it deserves some bonus.
            +4cps for such a pawn
        An apex hub pawn
            An apex hub pawn would be a pawn that is a lead pawn of one diagonal connection and a
            medium p of another diagonal connection. Eg. wps c3,d4,e5,e3 - d4 would be such a p. Such a
            hub pawn would be extremely sturdy, because it is defended by 2 own ps, and is practically an
            apex p, if we consider the smaller c3,d4,e3 structure. As it is very important for the integrity
            of the larger structure, and considering its strength, 1/3 higher bonus than that for a standard
            hub pawn might be indicated.
            +6cps for such a p
        A medium hub pawn
            A medium hub pawn would be a p that is a medium p of one diagonal connection and a root p
            of another diagonal connection. Eg. wps c3,d4,c5,e5 - d4 would be such a p. Of course, such a
            hub pawn would be very important for the integrity of the entire structure, but the peculiarity
            here is that this pawn supports 2 lead ps, so its role is only additionally highlighted.
            +8cps for such a p
            Again, the doubling with such structures of diagonally connected ps is less harshly felt.
        Considerable space disadvantage
            Well, some call such positions cramped. When one of the sides has more than 2 pieces with
            mobility lower than 2 available squares, each piece should get an additional penalty of -20cps,
            as sometimes just the low mobility scores will not be able to paint the real picture on the
            board. In such cases even larger fixed structures will have difficulties with seeking out
            drawish variations.

        Bishop on the same diagonal with an enemy bishop with own ps in between along thatdiagonal
            When a bishop is on the same diagonal with an enemy bishop with own pawns but no enemy
            pawns in between that diagonal, it will be due some penalty points because of tactical
            considerations.
            -11cps in the case of a single own p along that diagonal
            -5cps in the case of 2 own ps
        Vertical span of a group of pawns
            The vertical span of a single group of pawns, especially if it is bigger, will matter in terms of
            creating attacking possibilities on the enemy king.
            +5cps for each rank the group spans
        Unopposed pawn when defended by another own pawn fixed by an enemy pawn
            Eg. wpsb2,d4, bpsd5,c4,b4 - c4 would be such a p for black, supported by d5. In some cases
            c4 could also qualify for a potential passer.
            1/3 higher value for an unopposed p (potential passer), as this pawn will last a longer time on
            its position
        King attacking enemy objects
            King attacking enemy objects (obviously in the endgame) will be due some lower bonus than
            the standard one for attacking objects, as even in the endgame such an attacking king is
            exposed to some risks.
            1/5 lower value for attacking
        More than one pawns and pieces on the same diagonal with enemy bishop the colour of the diagonal the own pawns and pieces are on
            Such an arrangement would be due some tiny penalty because of possible tactical implications
            -2mps in case of 2 own ps or pieces on the same diagonal
            -5mps in case of more than 2 own ps or pieces on the same diagonal
        Closeness of an apex pawn to the enemy king
            This could be considered alternatively to considering closeness for lead pawns.
            Double values for an apex p close to the enemy king (just 1,2 or 3 squares in between), in case
            such a pawn is leading more than 2 pawns on both diagonals. Such a pawn is undoubtedly a
            tremendous force.
            +30cps with just one square in between
            +20cps with 2 squares in between
            +10cps with 3 squares in between
        Attacking pieces with restricted mobility
            Pieces attacking enemy pieces with restricted mobility (no free or just one free available
            square) will be due 1/2 higher bonus than the standard one, because this might have some
            very important tactical implications. Own pieces with restricted mobility, attacked at that, are
            to be avoided at any cost.
            When considering this, only attacks on pieces with different power will be taken into account,
            i.e., knights attacking enemy bishops or rooks attacking enemy knights, etc.
        Semi-backward p with the pawn making it semi-backward being unopposed
            Eg. wpb5, bpsd7,c7 - c7 is such a pawn. 1/3 higher penalty for such a pawn would be
            indicated, as in the case the semi-backward p advances, the enemy pawn making it backward
            will have also the option of moving further forward, in distinction to the usual case (eg. wpb5,
            bpsd7,c7,b6 - here c7 gets the standard penalty, as b6 fixes wpb5).
            This type of pawn will be considered only for the 7th and 6th ranks, for when the p advances
            further, usually pieces for the side with the semi-backward p will have predominant control of
            the square in front of the p, making it not a weakness.
            7th rank might get the standard value, and the 6th rank a bit lower penalty.
        Semi-backward pawn diagonally connecting to a less advanced own pawn
            Eg. wpb4, bpsd6,c6,b7 This type of semi-backward p (c6) will deserve 2/3 lower penalty than
            the standard one, as at some point of time its advance could be supported by the less advanced
            own p (by playing c7-c6 in this case).
            Such a pawn could be considered only for the 6th rank, as when the pawn moves forward,
            usually own pieces will have sufficient control of the square in front of it, making it not a
            weakness.
        Bishops in terms of enemy pawns on squares the colour of the bishop
            Bishops will get a bonus of 2cps for each enemy pawn on a square the colour of the bishop. In
            case such ps are fixed, the bonus will be double, and will rise to treble when the fixed enemy
            ps are placed on central e or d files. This will be meaningful for bishop versus bishop or
            bishop versus knight configurations.
            Of course, the other way round, considering penalties for bishops in terms of own ps on
            squares the colour of the bishop, will be even more important, as, in distinction to the
            previous case, this will concern not only the attacking potential of the piece, but also its
            mobility.
            Penalties might be dispensed just as above, but with a minus sign and multiplied by 2 or 3.
            I think the blend of both ways to assess a bishop's relevance on the board might be the optimal
            fashion of proceeding, as this will minimize the risk of omitting important information.
            I think this is very important to do for bishops, otherwise the evaluation will not be quite
            correct. I have seen unbelievable instances of top engines being blind and losing games on
            such counts even in fairly simple endings.
        Hub pawns in terms of ranks
            Obviously, hub pawns could be considered from the 3rd through the 5th rank (a hub pawn on
            the 6th rank would have a protected passer as its lead pawn, which is pretty much
            meaningless).
            1/5 higher value for a hub pawn on the 4th rank in relation to a hub pawn on the 3rd rank, and
            in turn 1/5 higher value for a hub pawn on the 5th rank in relation to a hub pawn on the 4th
            rank.
        Complications - Tactical prowess in terms of capturing ability
            This might be very important tactically.
            For each piece and pawn on the board possible captures will be considered under the
            supposition that the piece or pawn starts capturing enemy objects and continues capturing all
            the way as if it has a continuous right of move until it has captured all enemy objects. If there
            are capturing ramifications along the way, they will be considered separately until all are
            exhausted. Then we will proceed to counting the length of capturing variations and assigning
            bonus points. Capturing the enemy king will not be considered, of course.
            The 3 lengthiest capturing variations will get bonus points.
            The lengthiest one will get +7mps for each capturing move
            The second lengthiest will get +5mps for each capturing move
            and the third lengthiest will get +3mps (but, of course, larger values could also be tested)
            The procedure will be repeated for each piece and pawn on the board with possible capturing
            moves. In the end we will have a decent picture of the capturing prowess of each piece and
            pawn. This, in turn, might be useful in complicated positions. When there are a lot of possible
            captures and lengthy ways, the values for this technique might be increased accordingly.
        Mobility in terms of own and enemy pawns and pieces influencing the availability of free squares
        This might be interesting to check. As it is actually very difficult to forestall in detail mobile
        squares availability with a timeframe, an attempt at introducing further mobility criteria could
        not be damaging overall.
        Each square occupied by an own piece on which a piece could be mobile if it were not for the
        own piece will get +10mps
        Each square occupied by an own pawn on which a piece could be mobile if it were not for the
        own pawn will get +5mps (as pawns are slower in moving)
        Each square controlled by an enemy piece on which a piece could be mobile if it were not for
        the enemy piece controlling it will get +20mps
        Each square controlled by an enemy pawn on which a piece could be mobile if it were not for
        the enemy pawn controlling it, will get +15mps
        The sum total will represent the mobility of the piece in terms of this indicator.
        This will be repeated for all pieces.
        Checking mobility in this way might be a second option complementing the standard way of
        calculating mobility. It will be interesting to compare results with both options. Maybe this
        will provide some indication of an optimal way of calculating mobility.
        Semi-backward pawn when part of the king shelter
        When a semi-backward p is part of the king shelter, it will be due some higher penalty, by 1/3,
        because of its tricky position. Moving the p will be subject to conditions.
        One pawn making 2 enemy ps semi-backward
        When one and the same pawn makes 2 enemy ps semi-backward, the semi-backwards will
        score half their usual penalties each, as in this case they are much less of a weakness.
        Root pawns when fixed
        When root pawns are fixed by enemy pawns, they will score bigger penalties, by 1/3, as the
        weakness becomes enduring. Bigger penalties will score also root pawns that are backward or
        backward-fated, because of partially restricted mobility. 1/4 bigger penalty in this case might
        be a decent assessment.
        6
        Attacking more than one enemy pieces of different capacity on an x-ray
        Pieces attacking more than one enemy pieces of different capacity on an x-ray will deserve
        some bonus because of tactical considerations.
        +4cps for any enemy piece after the first
        Different capacity will mean rooks attacking knights and bishops, or bishops attacking knights
        and rooks, queen attacking bishops and knights on a line and queen attacking rooks and
        knights on a diagonal.
        Additional bonus points for apex pawns in terms of the number of ps they are leading
        Apex ps will get some bonus relative to the number of pawns they are leading along both
        diagonals.
        +2cps for each p that is led along one of the diagonals
        2 bishops next to each other
        2 bishops next to each other horizontally or vertically will get some bonus points because of
        continuous control of squares. In this way the bishops will control 4 continuous squares on an
        adjacent rank, when they are horizontally adjacent to each other, and 4 continuous squares on
        an adjacent file, when they are vertically adjacent to each other.
        +12cps for such an arrangement
        This might be especially useful with king attacks.
        Congestion of pieces in terms of forming compact groups
        When pieces are adjacent to each other horizontally, vertically or diagonally, as if forming a
        single group of pawns, they would be due some penalty points, as this is a bad indication
        overall for the health of the position.
        -2mps for each piece member of a group defined as a group of pawns
        But, of course, higher penalties could also be tested.
        Kings will not be considered for this.
        Potential for winning tempo
        Winning tempo is an important tactical indicator.
        The number of moves with attacks on pieces of bigger power will be considered. Meaning,
        bishops and knights attacking rooks and queen, rooks attacking an enemy queen. The moves
        will be counted even when an attack would produce a loss in material. We check all such
        moves for the sides.
        Each move of this quality gets +3mps.
        Pawns will also be included.
        Possible pawn attacking moves on any of the enemy pieces, regardless of whether the pawn is
        lost or not, will get +2mps, a bit lower value than that for pieces, because usually pawns are
        less relevant tactically.
        Space advantage for pawns in terms of the file they are on
        This will be considered only for pawns gaining space advantage that are fixed. It might make
        sense to assign different bonus points for such pawns in terms of files apart from the usual
        bonus points assigned to pawns in the general case, when they are not gaining space, not
        7
        fixed, etc., because such pawns will constitute a lasting positional feature and calibration
        could only help have a better positional assessment with a timeframe.
        Under the supposition we do not know where the kings have castled, the following bonus
        points might be dispensed:
        a and h pawns could get the standard value
        b and g ps will get +3cps over that when on the 5th rank, and +7cps over that when on the 6th
        rank
        c and f ps will get +5cps over the standard value when on the 5th rank and +10cps over the
        standard value when on the 6th rank
        d and e ps will get +8cps over the standard when on the 5th rank, and +15cps over the
        standard when on the 6th rank.
        Pawns storming the enemy side where the enemy king has not castled
        Pawns storming the other side than the side where the enemy king has castled (usually this
        would be the queen side) would be due some bonus points. I really think it does not matter if
        the storming pawns on that side are in a minority or in a majority, the important thing would
        be to attack, try to gain space advantage and open files. Minority pawns are usually just
        quicker in moving.
        +10cps for a pawn on the 4th rank
        +15cps for a pawn on the 5th rank
        and +20cps for a pawn on the 6th rank, clashing with an enemy pawn on the 7th, if, of course,
        such a move is tactically relevant.
        Tandems and triplets with x-ray attacks
        Tandems and triplets (queen and bishop on the same diagonal, queen and rook on a file or
        rank, and queen and 2 rooks on a file or rank) might have some added value when considering
        x-ray attacks upon enemy pieces on the same line. Tandems and triplets, of course, provide
        strength.
        +6cps for a queen and bishop attacking an enemy piece along an x-ray
        +10cps for queen and rook attacking an enemy piece along an x-ray
        and +15cps for queen and 2 rooks attacking an enemy piece along an x-ray
        King finding shelter behind a hub pawn
        A king finding shelter behind a hub pawn, even in the center of the board, will be due some
        additional bonus points to the usual points assigned to shelters, as hub pawns are very sturdy.
        But this will be considered only when the king is immediately behind the hub pawn or just
        one square away, and with hub pawns members of a group of ps of at least 4 ps in all.
        +5cps for such a king
        Rook outposts
        Rook outposts will be squares on the 5th or 6th ranks, with no enemy pawns being able to
        attack them, and no enemy minor pieces within the next 3 moves.
        +3cps additionally to other bonus points for a rook on such a square on the 5th rank
        +5cps, if the rook occupies a square on the 6th rank
        Although rooks are usually mobile pieces, having a quiet place for rest in the enemy camp is
        certainly an advantage
        8
        Bishop on a diagonal adjacent to a diagonal occupied by an own group of ps led by a
        lead p
        This will be considered only if the group of ps is larger than 2 ps.
        Eg. bbc8, bpsc7,d6,e5 Such a bishop would be due some bonus because of control of
        complementary squares in a specific area of the board (in this case the c8-h3 and b8-h2
        diagonals).
        +5mps for the bishop for any member of the diagonal connection
        Mutual piece defence
        Mutual piece defence will be the case when 2 pieces defend each other simultaneously. Queen
        and bishop defending each other on a diagonal, 2 rooks defending each other on files or ranks,
        and queen and rook defending each other on files or ranks would qualify.
        Mutual piece defence is an optimal way of defending, as even if one of the pieces is forced to
        move, it can still do so on another square of the current diagonal, maintaining the mutual
        piece defence. This would not be true of other types of defence. So some bonus points would
        be due for flexibility.
        The following bonus points could be dispensed (additionally to other bonus points for
        defending pieces):
        mutual piece defence of queen and bishop +2cps
        mutual piece defence of 2 rooks +3cps
        mutual piece defence of queen and rook +5cps
        Maybe here is the place to say why 2 knights defending each other would get not bonus
        points, but penalty points instead. In the first place, 2 knights defending each other are a very
        rigid configuration, when one of the knights is forced to move, the mutual defence will
        crumble instantly. Secondly, and most importantly, 2 knights defending each other limit each
        other's mobility in a painful way, as knights are usually not very mobile and each free square
        is valuable. Therefore, penalties assigned to such knights are justified, and might even be big
        enough.
        Mutual piece-pawn defence
        Mutual piece-pawn defence will be the case when a piece defends a pawn and vice-versa.
        Only bishop and pawn mutually defending each other will be considered. (eg. wpb2, wbc3)
        The specificity here is that, apart from the piece and bishop defending each other, for which
        they will get some bonus for general defence, in the case of the bishop being captured, the
        own pawn will advance one square, which is a good sign.
        +1cp additionally for this arrangement
        Mutual defence of queen and pawn is also valid on the same counts, but +1mp would hardly
        be essential in deciding the game.
        Penalties for rooks on open and semi-open files in terms of existence of other own pieces
        in front of the rooks on those files
        When there are other own pieces (bishops and knights) in front of a rook on an open or semi-
        open file, some penalties will be assigned to the rook, as, obviously, those pieces stand in the
        way of the rook.
        -5cps for each own piece in front of the rook on an open file
        -3cps for each own piece in front of the rook on a semi-open file
        9
        When the rooks are double on open and semi-open files, the penalties for each own piece in
        front of the rooks might be increased accordingly, as such pieces will stand in the way of a
        bigger potential. With double rooks, the existence of own pieces in between the rooks will be
        considered in the same way.
        The same penalties will be applied to queen and rook on an open and semi-open file, and 3
        heavy pieces on open and semi-open files, but increased a bit in conformance to the potential
        of the heavy pieces.
        Double fianchetto
        Developing both bishops on the long diagonals would hardly compensate for the loss of
        control of center. Therefore, this is not a good opening strategy.
        -20cps for such an arrangement
        Bishop on the second rank and b or g files defending an own end file pawn on the 3rd
        rank
        A bishop on the 2nd rank and b or g files defending an own end file pawn on the 3rd rank (a
        or h pawn; eg. wbb2,wpa3, or wbg2,wph3) would be due a tiny bonus, as it is more difficult
        to attack the bishop there, and this will also make the pawn safer.
        +1cp
        Bishops on both sides of the board
        Placing the bishops on both sides of the board (the queen and king side), instead of just on one
        of the sides, would give a tiny bonus, as usually in this way the bishops control better one and
        the other side.
        +2cps
        Mobility of squares from where the enemy king could be checked
        Mobility for such squares should be scored double, as usually this would force a variation or
        an array of variations on the enemy side, providing additional opportunities for development
        of own pieces or improving the mobility of the piece that checks the king.
        Bonus for rooks for more than one enemy minors on the same line
        Rooks are due some bonus in the case more than one enemy minor pieces are placed on one
        and the same line (file or rank). Obviously, this creates beneficial tactical opportunities.
        +2cps for any minor after the first on the same file or rank
        The queen could also get bonus for such an arrangement.
        +15mps
        Own pieces standing in the way of a tandem of queen and bishop
        When own pieces (that would be rooks and knights) stand in the way of a tandem of queen
        and bishop on the same diagonal (meaning being placed in front of both pieces, or in
        between), that would naturally lower the potential of the tandem for some time. The
        subtraction of some points from the bonus for the tandem would be indicated.
        -4cps in this case
        10
        Mobility for the queen in terms of accessible squares on lines and diagonals
        Generally, it would be good that the queen keeps to the standard ratio of available mobile
        squares on lines and diagonals, which is close to 3 to 2 in favour of mobile squares on lines
        (files and ranks).
        Points might be dispensed in the following way:
        Perfect ratio of 3 to 2 in favour of mobility on lines - queen gets a bonus of +10cps
        Ratio in the interval from 3.5 to 2 to 3 to 1.7 in favour of mobility on lines - queen gets a
        bonus of +5cps
        Ratio above those values in favour of mobility on lines, or prevailing mobility for the queen
        on diagonals - queen gets a penalty of -7cps
        Again, this rule should not be generalized too much, because the queen is a very mobile piece
        and easily transfers to different locations on the board using for the purpose alternately mobile
        squares on lines and diagonals, but the specific ratio numbers might still be an indication of
        the good health of the queen or the own pieces around it. When the ratio is lopsided, there are
        chances that something is wrong either with the queen itself, or with the own pieces in its
        immediate surrounding.
        Bonus points for bishops in terms of more than one enemy pieces on the same diagonal
        Bishops would be due some bonus in the case more than one enemy pieces are placed on the
        same diagonal the colour of the bishops.
        +7mps for each enemy piece after the first on one and the same diagonal the colour of the
        specific bishop (but enemy bishops would not be considered for this)
        This might have its tactical justification.
        A queen might get some bonus points, too, when more than one enemy pieces (rooks and
        knights, but not bishops and queens) are placed on one and the same diagonal, regardless of
        the colour of the diagonals the queen currently controls.
        +3mps for any enemy rook or knight after the first piece on one and the same diagonal
        Why penalties for weak pawns should be higher in the endgame
        In the endgame, factors like opposition of kings and zugzwang play an important role, and the
        side with the more weak pawns will usually have to make concessions on both factors because
        of its weaknesses. This will, in turn, lead to a very probable loss of the game. Therefore, in the
        endgame penalties for weak pawns should be increased accordingly by a sufficient margin. In
        very simple pawn endings the penalties for weak ps should be even bigger, as zugzwang and
        opposition of kings play an even bigger role. Penalties for weak pawns should include, at
        least, double, isolated and backward pawns.
        Penalties for undefended pieces
        Pieces that are not defended by any own pieces or pawns (kings will be included into the
        defence) will be due some well deserved penalty points because of obvious tactical
        implications.
        Penalty points might be dispensed in the following way:
        -5cps for any piece that is not defended by either another own piece, or an own pawn
        -7cps for any such piece in the case that the number of undefended pieces exceeds two
        But, of course, penalties for undefended pieces might be differentiated.
        An undefended queen might get -10cps, and undefended rook -5cps, and an undefended minor
        piece -3cps.'''
        value = TotalMaterialAdvantage
        return value


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
























                        
