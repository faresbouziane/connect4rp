from copy import deepcopy
from math import inf
import time

MAX = 1
MIN = -1
depth = 5
humanpiece = 1
robotpiece = 2
class ConnectFourBoard :
    
    def __init__(self,w,h):
        self.board = [[0 for _ in range(w)] for _ in range(h)]
        self.w = w
        self.h = h
        self.pieces = [1,2]
        self.heur=None
        self.lastmove= None
        self.winner= None
    
    def repos(self,x):
        y=0
        if x >= 0 and x < self.w :
            while y != self.h and self.board[y][x] == 0 :
                y+=1
            if y == 0:
                return False
            y-=1
            return x,y
        
    
    def possmoves(self):
        moves = []
        for x in range(self.w):
            m = self.repos(x) 
            if m:
                moves.append(m)
        return moves

    def makeMove(self,x, y, piece):
        if (x,y) in self.possmoves():
            self.board[y][x] = piece
            self.lastmove = (x,y)
            return True
        else :
            print("Not a possible move.")
            return False

    def Win(self,x0,y0,piece):
        count1 = 1 #horizontaly
        x=x0-1
        while x>=0 and self.board[y0][x] == piece:
            count1 +=1
            x-=1
            if count1 == 4:
                self.winner = piece
                return True
        
        x=x0+1
        while x < self.w and self.board[y0][x] == piece:
            count1 +=1
            x+=1
            if count1 == 4:
                self.winner = piece
                return True

        count2 = 1 #verticaly 
        y=y0-1 
        while y>=0 and self.board[y][x0] == piece:
            count2 +=1
            y -=1
            if count2 == 4:
                self.winner = piece
                return True
        y=y0+1
        while y < self.h and self.board[y][x0] == piece:
            count2 +=1
            y += 1
            if count2 == 4:
                self.winner = piece
                return True

        count3 = 1 #diagonaly TL BR 
        x=x0-1
        y=y0-1 
        while y>=0 and x>=0 and self.board[y][x] == piece:
            count3 +=1
            y -=1
            x -=1
            if count3 == 4:
                self.winner = piece
                return True
        x=x0+1
        y=y0+1
        while y < self.h and x < self.w and self.board[y][x] == piece:
            count3 +=1
            x += 1
            y += 1
            if count3 == 4:
                self.winner = piece
                return True
        
        count4 = 1 #diagonaly BL TR 
        x=x0-1
        y=y0+1 
        while y < self.h and x>=0 and self.board[y][x] == piece:
            count4 +=1
            y +=1
            x -=1
            if count4 == 4:
                self.winner = piece
                return True
        x=x0+1
        y=y0-1
        while y >= 0 and x < self.w and self.board[y][x] == piece:
            count4 +=1
            x += 1
            y -= 1
            if count4 == 4:
                self.winner = piece
                return True
        return False

    def gameover(self):
        if self.winner :
            return True
        if not self.possmoves():
            self.winner = "draw"
            return True
        return False


    def heureval(self,piece):
        if self.gameover():
            if self.winner == piece :
                self.heur = inf
            elif self.winner == "draw" :
                self.heur = 0
            else:
                self.heur = -inf
        else:
            temp = self.board
            innercounter = 0
            outercounter = 0
            self.heur = 0
            if self.pieces[0] == piece :
                ind = 0
            else:
                ind = 1
            spots = 4

            current = None
            
            #########phase 1 , vertical + killing dead cells
            for x in range(self.w):
                spots=4
                for y in range(self.h-1,-1,-1):
                    if temp[y][x] == 0:
                        if y+1 < spots:
                            spots=4
                        for y in range(y-1,-1,-1):
                            temp[y][x]= -1      #make it dead cell
                        break
                    if current == None:
                        current == temp[y][x]
                        spots -= 1
                    elif temp[y][x] == current:
                        spots -=1
                    else:
                        current = temp[y][x]
                        spots = 3
                
                if current == piece:    
                    innercounter += 4-spots
                elif current == None:
                    pass
                else:
                    innercounter -= 4-spots

            self.heur += innercounter       #first phase complete

            ###### phase 2 horizontality, this is the easiest use of deadcells
            ###### if we find -1 , n3awdu lhsab and we abort that side before that x in the next steps, ill find a way to implement this
            y=self.h-1
            innercounter = 0

            while y>=0 and y<self.h :
                x=0
                spots = 4
                step= [0,None]         # [0] is for how empty step i took and [1] is for the x after last empty step, that to be able to track down back to it and start counting from there later
                current = None
                while x<self.w:
                    if self.w-x < spots-step[0]:    #not enough spots left for four
                            break
                    if temp[y][x] == -1:        #if dead cell we reset the counting and stuff, 
                        spots= 4
                        step = [0,None]
                        current = None
                        while x+1<self.w and temp[y][x+1] == -1:
                            x+=1            #this changes in next ones
                    else :                          # just to remember i was trying to assing last x before emoty to restart from there
                        if temp[y][x] == 0:
                            if step[0] <=3:
                                step[0] +=1
                            current = 0
                        elif current == None:
                            current = temp[y][x]
                            spots -= 1
                            step[1] = x
                        elif temp[y][x] == current:
                            spots -=1
                            step[1] = x
                                       # i just thought smth before closing, in step track the last before if its the same current, but if not same capable empty spaces ykunu available for the other player too, donc u hv to track them too, either add a new pair to the tuple or just find a solution gn
                        elif  current == 0: 
                            if step[1] == None or temp[y][step[1]] == temp[y][x]:
                                spots-=1
                                current = temp[y][x]
                                step[1] = x
                            else:               #i think can be optimised but idc this is more general bah mch kul situation ndirlha code for it
                                spots = 4
                                x = step[1]
                                step= [0,None]
                                current = None
                        else:
                            spots = 3
                            step = [0,x]
                            current = temp[y][x]
                            


                    if spots !=4 and spots==step[0] :
                        if temp[y][step[1]] == piece:
                            innercounter += 4-spots
                        else:
                            innercounter -= 4-spots   
                        if x+1<self.w :
                            if temp[y][x+1] != -1:
                                x-=3
                            spots=4
                            step= [0,None]
                            current = None  
                    x +=1
                y +=1

            self.heur += innercounter       #phase 2 (horizantal), complete
            # now phase 3 which is from top left to bottom right, there is in our situiation
            # kayn 6 possible lines for connecting 4 , 
            # to memomorise , hnrat starting points bhad tartib: (y,x)
            # [(2,0),(1,0),(0,0),(0,1),(0,2),(0,3)]
            # condition to while are y<self.h and x<self.w
            innercounter = 0
            lines = [(2,0),(1,0),(0,0),(0,1),(0,2),(0,3)]

            for (y,x) in lines:
                spots = 4
                step= [0,None]         # [0] is for how empty step i took and [1] is for the x after last empty step, that to be able to track down back to it and start counting from there later
                current= None
                while x<self.w and y<self.h:
                    if min(self.w-x,self.h-y) < spots-step[0]:    #not enough spots left for four
                            break
                    if temp[y][x] == -1:        #if dead cell we reset the counting and stuff, 
                        spots= 4
                        step = [0,None]
                        current = None
                        while x+1<self.w and y+1<self.h and temp[y+1][x+1] == -1:
                            y,x=(y+1,x+1)          #wewewewe
                    else :                          # 
                        if temp[y][x] == 0:
                            if step[0] <=3:
                                step[0] +=1
                            current = 0
                        elif current == None:
                            current = temp[y][x]
                            spots -= 1
                            step[1] = (y,x)
                        elif temp[y][x] == current:
                            spots -=1
                            step[1] = (y,x)
                                    # i just thought smth before closing, in step track the last before if its the same current, but if not same capable empty spaces ykunu available for the other player too, donc u hv to track them too, either add a new pair to the tuple or just find a solution gn
                        elif  current == 0: 
                            if step[1] == None or temp[step[1][0]][step[1][1]] == temp[y][x]:
                                spots-=1
                                current = temp[y][x]
                                step[1] = (y,x)
                            else:               #i think can be optimised but idc this is more general bah mch kul situation ndirlha code for it
                                spots = 4
                                (y,x) = step[1]
                                step= [0,None]
                                current = None
                        else:
                            spots = 3
                            step = [0,(y,x)]
                            current = temp[y][x]
                            

                    if spots !=4 and spots==step[0] :
                        if temp[step[1][0]][step[1][1]] == piece:
                            innercounter += 4-spots
                        else:
                            innercounter -= 4-spots   
                        if x+1<self.w and y+1<self.h :
                            if temp[y+1][x+1] != -1:
                                y,x=(y-3,x-3)
                            spots=4
                            step= [0,None]
                            current = None  
                    y,x=(y+1,x+1)
                


            self.heur += innercounter       #phase 3 (topleft botright), complete
            # omg now phase 4 which is from bottom left to top right
            # kayn 6 possible lines also for connecting 4 , 
            # heres starting points bhad tartib: (y,x)
            # [(3,0),(4,0),(5,0),(5,1),(5,2),(5,3)]
            # condition to while are y>=0 and x<self.w and this time nzidu lel x while naksu l y

            innercounter=0
            lines = [(3,0),(4,0),(5,0),(5,1),(5,2),(5,3)]

            for (y,x) in lines:
                spots = 4
                step= [0,None]         # [0] is for how empty step i took and [1] is for the x after last empty step, that to be able to track down back to it and start counting from there later
                current= None
                while x<self.w and y>=0:
                    if min(self.w-x,y+1) < spots-step[0]:    #not enough spots left for four
                            break
                    if temp[y][x] == -1:        #if dead cell we reset the counting and stuff, 
                        spots= 4
                        step = [0,None]
                        current = None
                        while x+1<self.w and y-1>=0 and temp[y-1][x+1] == -1:
                            y,x=(y-1,x+1)          #waahfsaeeae
                    else :                          # 
                        if temp[y][x] == 0:
                            if step[0] <=3:
                                step[0] +=1
                            current = 0
                        elif current == None:
                            current = temp[y][x]
                            spots -= 1
                            step[1] = (y,x)
                        elif temp[y][x] == current:
                            spots -=1
                            step[1] = (y,x)
                                    #
                        elif  current == 0: 
                            if step[1] == None or temp[step[1][0]][step[1][1]] == temp[y][x]:
                                spots-=1
                                current = temp[y][x]
                                step[1] = (y,x)
                            else:               #i think can be optimised but idc this is more general bah mch kul situation ndirlha code for it
                                spots = 4
                                (y,x) = step[1]
                                step= [0,None]
                                current = None
                        else:
                            spots = 3
                            step = [0,(y,x)]
                            current = temp[y][x]
                            

                    if spots !=4 and spots==step[0] :
                        if temp[step[1][0]][step[1][1]] == piece:
                            innercounter += 4-spots
                        else:
                            innercounter -= 4-spots   
                        if x+1<self.w and y-1>=0 :
                            if temp[y-1][x+1] != -1:
                                y,x=(y+3,x-3)
                            spots=4
                            step= [0,None]
                            current = None  
                    y,x=(y-1,x+1)
                


            self.heur += innercounter       #phase 4 (downleft topright), complete

            #heuristic finished (hopefully), the world will be destroyed after this heuristic

                    
    @staticmethod
    def printboard(board):
        str_line = '---------------------------'
        printedBoard = f"{str_line}\n"+"".join(map(lambda line: " | ".join(map(str, line))+f"\n{str_line}\n", board))
        print(printedBoard)


class Play:
    @staticmethod
    def HumanTurn (state,col):
        x = int(input("choose the collumn number you wanna put your piece in : "))
        while x not in [i[0] for i in state.possmoves()]:
            x = int(input("wrong move , retry with an available collumn number : "))
        x,y = state.repos(x)
        state.makeMove(x,y,humanpiece)
        state.Win(x,y,humanpiece)

    @staticmethod
    def RobotTurn (state):
        _,(x,y) = Play.minimaxAlphaBetaPruning(state,depth,alpha=-inf, beta=+inf, player=MAX)
        print("the Mini robot has played its turn.")
        state.makeMove(x,y,robotpiece)
        state.Win(x,y,robotpiece)

        

    @staticmethod
    def minimaxAlphaBetaPruning(state ,depth, alpha=-inf, beta=+inf, player=MAX):
        if depth == 0 or state.gameover():

            state.heureval(robotpiece)
            return state.heur
        else :
            bestmove= None
            
            succs = []
            for (x,y) in state.possmoves():
                succ = deepcopy(state)
                succ.makeMove(x,y,max(1,1+player))
                succ.Win(x,y,max(1,1+player))
                succs.append(succ)

            bestmove = succs[0].lastmove    #initialise the first move then it will change for the better moves
            
            if player == MAX:
                v= -inf
                for succ in succs:
                    t = Play.minimaxAlphaBetaPruning(succ,depth-1,alpha,beta,-player)
                    if t>v :
                        v=t
                        bestmove= succ.lastmove
                    if v >= beta :
                        if depth == 5 :
                            print(v,bestmove)
                            return v,bestmove
                        else:
                            return v
                    alpha = max(alpha, v)

            elif player == MIN:
                v= +inf
                for succ in succs:
                    t = Play.minimaxAlphaBetaPruning(succ,depth-1,alpha,beta,-player)
                    if t<v:
                        v=t
                        bestmove= succ.lastmove
                    if v <= alpha :
                        return v
                       
                    beta = min(beta, v)
            if depth == 5:
                print(v,bestmove)
                return v,bestmove
            else :
                return v
                
# probleem rahu that when u calculate heuristic when all the child nodes are -inf u wont get a move to do so it blocks, do a new heuristic
#          
def main():
    w,h=7,6
    connect = ConnectFourBoard(w,h)

    #this is only human versus robot, can be easily modified to be other modes
    while not connect.gameover():
        connect.printboard(connect.board)
        Play.HumanTurn(connect)
        if connect.gameover():
            break
        connect.printboard(connect.board)
        Play.RobotTurn(connect)
    connect.printboard(connect.board)
    if connect.winner == humanpiece:
        print("********     you won!     ********")
    elif connect.winner == robotpiece:
        print("********     you lost!     ********")
    elif connect.winner == "draw":
        print("********     its a draw!     ********")
    else:
        print("there is error")

        #notices:
        #   i can add timed input so the user have limited time to enter or else he will be randomly played
        #   etc...


if __name__ == "__main__":
    main()
        
        
