from locale import ABDAY_1
import random
import time


def convert(l):
    """coverts letter into index"""
    A = ord(l) - 65
    return A

def rconvert(n):
    """ it converts from column number to letter"""
    return chr(65+n)

def inarow_Neast(ch, r_start, c_start, A, N):
    num_rows = len(A)      # Number of rows is len(A)
    num_cols = len(A[0])   # Number of columns is len(A[0])
    if r_start < 0 or r_start >= num_rows:
        return False       # Out of bounds in rows
    # Other out-of-bounds checks...
    if c_start < 0 or c_start > num_cols - N:
        return False       # Out of bounds in columns
    # Are all of the data elements correct?
    for i in range(N):                  # Loop index i as needed
        if A[r_start][c_start+i] != ch: # Check for mismatches
            return False                # Mismatch found--return False
    return True                         # Loop found no mismatches--return True

def inarow_Nsouth(ch, r_start, c_start, A, N):
    num_rows = len(A)
    num_cols = len(A[0])
    if c_start<0 or c_start>= num_cols:
        return False
    if r_start<0 or r_start> num_rows-N:
        return False
    if r_start<0 or r_start>num_rows+N:
        return False
    for i in range(N):
        if A[r_start+i][c_start]!= ch:
            return False
    return True

class BoardUser:
    """A data type representing a battleship board
       with an arbitrary number of rows and columns.
    """

    def __init__(self):
        """Construct objects of type Board, with the given width and height."""
        width = 10 
        height = 10
        self.width = width
        self.height = height
        self.data = [[' ']*10 for row in range(10)]

        # We do not need to return anything from a constructor!

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # The string to return
        for row in range(0, self.height):
            s += (chr(65 + row)+ " " + '|')
            for col in range(0, self.width):
                s += (self.data[row][col] + '|')
            s += '\n'

        s += "  " + (2*self.width + 1) * '-'   # Bottom of the board
        s += '\n' + "  "
        for col in range(0, self.width): # Add code here to put the numbers underneath
            s+= ' '+ str(col)

        s += '\n'
        return s       # The board is complete; return it


               
    def clear(self):
        """ should clear the board that calls it""" 

        for x in range(self.height):
            for y in range(self.width):
                self.data[x][y] = ' '
    

    def Counthits(self):
        """ counts the number of ships that have been hit and returns that value"""
        n = 0
        for i in range(self.height):
            for x in range(self.width):
                if self.data[i][x] == '*':
                    n+= 1

        return n
        
    def checkifWin(self):
        """ checks if the number of hits = the total number of hits needed to win and returns TRUE or FALSE"""
        totalhitstowin = 17
        if self.Counthits() == totalhitstowin:
            return True
        else:
            return False
               


    def allowsShip(self, shiptype, Srow, Scol, orient):
        """It checks to see if the ship positioning is appropiate"""
        L = {"A":5, "B":4, "C": 3 , "S":3, "D": 2 }

        for x in range(10):
            if shiptype in self.data[x]:
                return False
            else:
                if orient == 'vert':
                    if Srow + L[shiptype] > 9:
                        return False
                    else: 
                        for x in range(Srow, Srow + L[shiptype]):
                            if self.data[x][Scol] != ' ':
                                return False
                        return True
                if orient == 'hor':
                    if Scol + L[shiptype] > 9:
                        return False
                    else: 
                        for x in range(Scol, Scol + L[shiptype]):
                            if self.data[Srow][x] != ' ':
                                return False
                        return True
                
    def PlaceShips(self,shiptype,Srow, Scol, orient ):
        """function that places ship of type A,B,C,S,D of sizes 5,4,3,3,2 respectively
        on a starting grid position given by Srow and Scol in an orientation vert or hor 
        shiptype, and orient should be introduced as strings"""
        Srow = convert(Srow)
        L = {"A":5, "B":4, "C": 3 , "S":3, "D": 2 }
        if self.allowsShip(shiptype, Srow, Scol, orient) == False:
            return False
        else:
            if shiptype in L:
                if orient == 'vert' :
                    for x in range(Srow, Srow + L[shiptype]):
                        self.data[x][Scol] = shiptype
                elif orient == 'hor' :
                    for x in range(Scol, Scol + L[shiptype]):
                        self.data[Srow][x] = shiptype
                else:
                    return False
            else:
                return False
                

        
    def addMove(self, let, col):
        """It allows each player to choose a position for the missile they launch"""
        
        row = ord(let) - 65
        
        if col not in range(10) or row not in range(10):
            return False
        elif self.data[row][col] in "ABCSD":
            self.data[row][col] = "*"
        elif self.data[row][col] == " ":
            self.data[row][col] = "~"
        else:
            return False
            
    def setAIboard(self):
        """sets the board for the AI randomly using the PlaceShips Function"""
        L = ['A','B','C','S','D']
        J = ['hor', 'vert']
        for x in L:
            A = random.choice(range(1,10))
            B = random.choice(range(1,10))
            C = random.choice(J)
            while self.allowsShip(x,A,B,C) is False:
                A = random.choice(range(1,10))
                B = random.choice(range(1,10))
                C = random.choice(J)
            self.PlaceShips(x,rconvert(A),B,C)
            
    def AIMove(self): # VVVV  IMPORTANT< change all () to [] while referencing self.data
        """function that decides which grid spot to shoot a missile based on the current grid"""      
        L = {"A":5, "B":4, "C": 3 , "S":3, "D": 2 }
        D= self.data
        if "*" not in D:
            X = random.choice(range(10))
            Y = random.choice(range(10))
            return [rconvert(X),Y]
        else:
            for row in range(1,9):
                for col in range(1,9):
                    if self.data[row][col]== "*":
                        if self.data[row+1][col] == "*" and self.data[row-1][col] == " ":
                            result = [(row-1)(col)]
                        elif self.data[row][col+1] == "*" and self.data[row][col-1] == " ":
                            result = [(row)(col-1)]
                        elif self.data[row-1][col] == " ":
                            result = [(row-1)(col)]
                        elif self.data[row+1][col] == " ":
                            result = [(row+1)(col)]
                        elif self.data[row][col-1] == " ":
                            result = [(row)(col-1)]                    
                        elif self.data[row][col+1] == " ":
                            result = [(row)(col+1)]
                        else:
                            continue
        # A = result[1]
        # B = chr(65+A)
        # result[1]=B
        return result

    """def hostGame(self):
            This method brings everything together into the familiar game.
            print('Welcome to Connect Four!')
            while True:
                print()
                print(self)
                
                self.setAIboard()
                
                print(self)
                if self.checkifWin():
                    print("Congratulations")
                    break 
                
                Let = str(input("Letter choice for missile attack:"))
                Col = int(input("Column choice for missile attack:"))
                
                while self.addMove(Let, Col) == False:
                     Col = int(input("Column choice for missile attack:"))
                self.addMove(Let, Col)
                print(self)"""


    def completesink(self,row,col):
            """Decides if a ship is sunk or not
            self references the board that is displayed with hits or misses """
            D= self.data
            if inarow_Neast("*", row , col, D, 5) == True:
                return "5H" 
            elif inarow_Nsouth("*", row , col, D, 5) == True:
                return "5V"
            else:
                if inarow_Neast("*", row , col, D, 4) == True:
                    if self.data[row][col-1] == '~' or col == 0:
                        if col == 6 or self.data[row][col+4] == '~':
                            return "4H"
                        else:
                            return False
                    else:
                        return False

                elif inarow_Nsouth("*", row , col, D, 4) == True:
                    if self.data[row+1][col] == '~' or row == 0:
                        if row == 6 or self.data[row+4][col] == '~':
                            return "4V"
                        else:
                            return False
                    else:
                        return False
                else:
                    if inarow_Neast("*", row , col, D, 3) == True:
                        if self.data[row][col-1] == '~' or col == 0:
                            if col == 7 or self.data[row][col+3] == '~':
                                return "3H"
                            else:
                                return False
                        else:
                            return False
                    elif inarow_Nsouth("*", row , col, D, 3) == True:
                        if self.data[row+1][col] == '~' or row == 0:
                            if row == 7 or self.data[row+3][col] == '~':
                                return "3V"
                            else:
                                return False
                        else:
                            return False
                    else:
                        if inarow_Neast("*", row , col, D, 2) == True:
                            if self.data[row][col-1] == '~' or col == 0:
                                if col == 8 or self.data[row][col+2] == '~':
                                    return "2H"
                                else:
                                    return False
                            else:
                                return False
                        elif inarow_Nsouth("*", row , col, D, 2) == True:
                            if self.data[row+1][col] == '~' or row == 0:
                                if row == 8 or self.data[row+2][col] == '~':
                                    return "2V"
                                else:
                                    return False
                            else:
                                return False

    def replace(self, row, col):
        """ if a ship has fully sunk, replace the ship with a letter of its type. 
        SELF here references the board that is displayed that has hits or misses"""
        for row in range(10):
            for col in range(10):
                if self.data[row][col]== "*":
                    A = self.completesink(row,col)
                    B = int(A[0])
                    C = A[1]
                    D = BoardComp.data[row][col] #this draws on what the data in the grid for AI is so that it can paste it 
                    if A != False:
                        if C == "H":
                            for x in range(B):
                                self.data[row][col+x] = D
                        elif C == "V":
                            for x in range(B):
                                self.data[row+x][col] = D


class BoardUser2:
    """A data type representing a battleship board
       with an arbitrary number of rows and columns.
    """

        
    def __init__(self):
        """Construct objects of type Board, with the given width and height."""
        width = 10 
        height = 10
        self.width = width
        self.height = height
        self.data = [[' ']*10 for row in range(10)]

        # We do not need to return anything from a constructor!

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # The string to return
        for row in range(0, self.height):
            s += (chr(65 + row)+ " " + '|')
            for col in range(0, self.width):
                s += (self.data[row][col] + '|')
            s += '\n'

        s += "  " + (2*self.width + 1) * '-'   # Bottom of the board
        s += '\n' + "  "
        for col in range(0, self.width): # Add code here to put the numbers underneath
            s+= ' '+ str(col)

        s += '\n'
        return s       # The board is complete; return it


               
    def clear(self):
        """ should clear the board that calls it""" 

        for x in range(self.height):
            for y in range(self.width):
                self.data[x][y] = ' '
    

    def Counthits(self):
        """ counts the number of ships that have been hit and returns that value"""
        n = 0
        for i in range(self.height):
            for x in range(self.width):
                if self.data[i][x] == '*':
                    n+= 1

        return n
        
    def checkifWin(self):
        """ checks if the number of hits = the total number of hits needed to win and returns TRUE or FALSE"""
        totalhitstowin = 17
        if self.Counthits() == totalhitstowin:
            return True
        else:
            return False
               


    def allowsShip(self, shiptype, Srow, Scol, orient):
        """It checks to see if the ship positioning is appropiate"""
        L = {"A":5, "B":4, "C": 3 , "S":3, "D": 2 }

        for x in range(10):
            if shiptype in self.data[x]:
                return False
            else:
                if orient == 'vert':
                    if Srow + L[shiptype] > 9:
                        return False
                    else: 
                        for x in range(Srow, Srow + L[shiptype]):
                            if self.data[x][Scol] != ' ':
                                return False
                        return True
                if orient == 'hor':
                    if Scol + L[shiptype] > 9:
                        return False
                    else: 
                        for x in range(Scol, Scol + L[shiptype]):
                            if self.data[Srow][x] != ' ':
                                return False
                        return True
                
    def PlaceShips(self,shiptype,Srow, Scol, orient ):
        """function that places ship of type A,B,C,S,D of sizes 5,4,3,3,2 respectively
        on a starting grid position given by Srow and Scol in an orientation vert or hor 
        shiptype, and orient should be introduced as strings"""
        Srow = convert(Srow)
        L = {"A":5, "B":4, "C": 3 , "S":3, "D": 2 }
        if self.allowsShip(shiptype, Srow, Scol, orient) == False:
            return False
        else:
            if shiptype in L:
                if orient == 'vert' :
                    for x in range(Srow, Srow + L[shiptype]):
                        self.data[x][Scol] = shiptype
                elif orient == 'hor' :
                    for x in range(Scol, Scol + L[shiptype]):
                        self.data[Srow][x] = shiptype
                else:
                    return False
            else:
                return False
                

        
    def addMove(self, let, col):
        """It allows each player to choose a position for the missile they launch"""
        
        row = ord(let) - 65
        
        if col not in range(10) or row not in range(10):
            return False
        elif self.data[row][col] in "ABCSD":
            self.data[row][col] = "*"
        elif self.data[row][col] == " ":
            self.data[row][col] = "~"
        else:
            return False
            
    def setAIboard(self):
        """sets the board for the AI randomly using the PlaceShips Function"""
        L = ['A','B','C','S','D']
        J = ['hor', 'vert']
        for x in L:
            A = random.choice(range(1,10))
            B = random.choice(range(1,10))
            C = random.choice(J)
            while self.allowsShip(x,A,B,C) is False:
                A = random.choice(range(1,10))
                B = random.choice(range(1,10))
                C = random.choice(J)
            self.PlaceShips(x,rconvert(A),B,C)
            
    def AIMove(self): # VVVV  IMPORTANT< change all () to [] while referencing self.data
        """function that decides which grid spot to shoot a missile based on the current grid"""      
        L = {"A":5, "B":4, "C": 3 , "S":3, "D": 2 }
        D= self.data
        if "*" not in D:
            X = random.choice(range(10))
            Y = random.choice(range(10))
            return [rconvert(X),Y]
        else:
            for row in range(1,9):
                for col in range(1,9):
                    if self.data[row][col]== "*":
                        if self.data[row+1][col] == "*" and self.data[row-1][col] == " ":
                            result = [(row-1)(col)]
                        elif self.data[row][col+1] == "*" and self.data[row][col-1] == " ":
                            result = [(row)(col-1)]
                        elif self.data[row-1][col] == " ":
                            result = [(row-1)(col)]
                        elif self.data[row+1][col] == " ":
                            result = [(row+1)(col)]
                        elif self.data[row][col-1] == " ":
                            result = [(row)(col-1)]                    
                        elif self.data[row][col+1] == " ":
                            result = [(row)(col+1)]
                        else:
                            continue
        # A = result[1]
        # B = chr(65+A)
        # result[1]=B
        return result

    """def hostGame(self):
            This method brings everything together into the familiar game.
            print('Welcome to Connect Four!')
            while True:
                print()
                print(self)
                
                self.setAIboard()
                
                print(self)
                if self.checkifWin():
                    print("Congratulations")
                    break 
                
                Let = str(input("Letter choice for missile attack:"))
                Col = int(input("Column choice for missile attack:"))
                
                while self.addMove(Let, Col) == False:
                     Col = int(input("Column choice for missile attack:"))
                self.addMove(Let, Col)
                print(self)"""


    def completesink(self,row,col):
            """Decides if a ship is sunk or not
            self references the board that is displayed with hits or misses """
            D= self.data
            if inarow_Neast("*", row , col, D, 5) == True:
                return "5H" 
            elif inarow_Nsouth("*", row , col, D, 5) == True:
                return "5V"
            else:
                if inarow_Neast("*", row , col, D, 4) == True:
                    if self.data[row][col-1] == '~' or col == 0:
                        if col == 6 or self.data[row][col+4] == '~':
                            return "4H"
                        else:
                            return False
                    else:
                        return False

                elif inarow_Nsouth("*", row , col, D, 4) == True:
                    if self.data[row+1][col] == '~' or row == 0:
                        if row == 6 or self.data[row+4][col] == '~':
                            return "4V"
                        else:
                            return False
                    else:
                        return False
                else:
                    if inarow_Neast("*", row , col, D, 3) == True:
                        if self.data[row][col-1] == '~' or col == 0:
                            if col == 7 or self.data[row][col+3] == '~':
                                return "3H"
                            else:
                                return False
                        else:
                            return False
                    elif inarow_Nsouth("*", row , col, D, 3) == True:
                        if self.data[row+1][col] == '~' or row == 0:
                            if row == 7 or self.data[row+3][col] == '~':
                                return "3V"
                            else:
                                return False
                        else:
                            return False
                    else:
                        if inarow_Neast("*", row , col, D, 2) == True:
                            if self.data[row][col-1] == '~' or col == 0:
                                if col == 8 or self.data[row][col+2] == '~':
                                    return "2H"
                                else:
                                    return False
                            else:
                                return False
                        elif inarow_Nsouth("*", row , col, D, 2) == True:
                            if self.data[row+1][col] == '~' or row == 0:
                                if row == 8 or self.data[row+2][col] == '~':
                                    return "2V"
                                else:
                                    return False
                            else:
                                return False

    def replace(self, row, col):
        """ if a ship has fully sunk, replace the ship with a letter of its type. 
        SELF here references the board that is displayed that has hits or misses"""
        for row in range(10):
            for col in range(10):
                if self.data[row][col]== "*":
                    A = self.completesink(row,col)
                    B = int(A[0])
                    C = A[1]
                    D = BoardComp.data[row][col] #this draws on what the data in the grid for AI is so that it can paste it 
                    if A != False:
                        if C == "H":
                            for x in range(B):
                                self.data[row][col+x] = D
                        elif C == "V":
                            for x in range(B):
                                self.data[row+x][col] = D


class BoardComp:
    """This class corresponds to opponenent played by the computer
    """
    
    def __init__(self):
        """Construct objects of type Board, with the given width and height."""
        width = 10 
        height = 10
        self.width = width
        self.height = height
        self.data = [[' ']*10 for row in range(10)]

        # We do not need to return anything from a constructor!

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # The string to return
        for row in range(0, self.height):
            s += (chr(65 + row)+ " " + '|')
            for col in range(0, self.width):
                s += (self.data[row][col] + '|')
            s += '\n'

        s += "  " + (2*self.width + 1) * '-'   # Bottom of the board
        s += '\n' + "  "
        for col in range(0, self.width): # Add code here to put the numbers underneath
            s+= ' '+ str(col)

        s += '\n'
        return s       # The board is complete; return it


               
    def clear(self):
        """ should clear the board that calls it""" 

        for x in range(self.height):
            for y in range(self.width):
                self.data[x][y] = ' '
    

    def Counthits(self):
        """ counts the number of ships that have been hit and returns that value"""
        n = 0
        for i in range(self.height):
            for x in range(self.width):
                if self.data[i][x] == '*':
                    n+= 1

        return n
        
    def checkifWin(self):
        """ checks if the number of hits = the total number of hits needed to win and returns TRUE or FALSE"""
        totalhitstowin = 17
        if self.Counthits() == totalhitstowin:
            return True
        else:
            return False
               


    def allowsShip(self, shiptype, Srow, Scol, orient):
        """It checks to see if the ship positioning is appropiate"""
        L = {"A":5, "B":4, "C": 3 , "S":3, "D": 2 }

        for x in range(10):
            if shiptype in self.data[x]:
                return False
            else:
                if orient == 'vert':
                    if Srow + L[shiptype] > 9:
                        return False
                    else: 
                        for x in range(Srow, Srow + L[shiptype]):
                            if self.data[x][Scol] != ' ':
                                return False
                        return True
                if orient == 'hor':
                    if Scol + L[shiptype] > 9:
                        return False
                    else: 
                        for x in range(Scol, Scol + L[shiptype]):
                            if self.data[Srow][x] != ' ':
                                return False
                        return True
                
    def PlaceShips(self,shiptype,Srow, Scol, orient ):
        """function that places ship of type A,B,C,S,D of sizes 5,4,3,3,2 respectively
        on a starting grid position given by Srow and Scol in an orientation vert or hor 
        shiptype, and orient should be introduced as strings"""
        Srow = convert(Srow)
        L = {"A":5, "B":4, "C": 3 , "S":3, "D": 2 }
        if self.allowsShip(shiptype, Srow, Scol, orient) == False:
            return False
        else:
            if shiptype in L:
                if orient == 'vert' :
                    for x in range(Srow, Srow + L[shiptype]):
                        self.data[x][Scol] = shiptype
                elif orient == 'hor' :
                    for x in range(Scol, Scol + L[shiptype]):
                        self.data[Srow][x] = shiptype
                else:
                    return False
            else:
                return False
                

        
    def addMove(self, let, col):
        """It allows each player to choose a position for the missile they launch"""
        
        row = ord(let) - 65
        
        if col not in range(10) or row not in range(10):
            return False
        elif self.data[row][col] in "ABCSD":
            self.data[row][col] = "*"
        elif self.data[row][col] == " ":
            self.data[row][col] = "~"
        else:
            return False
            
    def setAIboard(self):
        """sets the board for the AI randomly using the PlaceShips Function"""
        L = ['A','B','C','S','D']
        J = ['hor', 'vert']
        for x in L:
            A = random.choice(range(1,10))
            B = random.choice(range(1,10))
            C = random.choice(J)
            while self.allowsShip(x,A,B,C) is False:
                A = random.choice(range(1,10))
                B = random.choice(range(1,10))
                C = random.choice(J)
            self.PlaceShips(x,rconvert(A),B,C)
            
    def AIMove(self): # VVVV  IMPORTANT< change all () to [] while referencing self.data
        """function that decides which grid spot to shoot a missile based on the current grid"""      
        L = {"A":5, "B":4, "C": 3 , "S":3, "D": 2 }
        D= self.data
        if "*" not in D:
            X = random.choice(range(10))
            Y = random.choice(range(10))
            return [rconvert(X),Y]
        else:
            for row in range(1,9):
                for col in range(1,9):
                    if self.data[row][col]== "*":
                        if self.data[row+1][col] == "*" and self.data[row-1][col] == " ":
                            result = [(row-1)(col)]
                        elif self.data[row][col+1] == "*" and self.data[row][col-1] == " ":
                            result = [(row)(col-1)]
                        elif self.data[row-1][col] == " ":
                            result = [(row-1)(col)]
                        elif self.data[row+1][col] == " ":
                            result = [(row+1)(col)]
                        elif self.data[row][col-1] == " ":
                            result = [(row)(col-1)]                    
                        elif self.data[row][col+1] == " ":
                            result = [(row)(col+1)]
                        else:
                            continue
        # A = result[1]
        # B = chr(65+A)
        # result[1]=B
        return result

    """def hostGame(self):
            This method brings everything together into the familiar game.
            print('Welcome to Connect Four!')
            while True:
                print()
                print(self)
                
                self.setAIboard()
                
                print(self)
                if self.checkifWin():
                    print("Congratulations")
                    break 
                
                Let = str(input("Letter choice for missile attack:"))
                Col = int(input("Column choice for missile attack:"))
                
                while self.addMove(Let, Col) == False:
                     Col = int(input("Column choice for missile attack:"))
                self.addMove(Let, Col)
                print(self)"""


    def completesink(self,row,col):
            """Decides if a ship is sunk or not
            self references the board that is displayed with hits or misses """
            D= self.data
            if inarow_Neast("*", row , col, D, 5) == True:
                return "5H" 
            elif inarow_Nsouth("*", row , col, D, 5) == True:
                return "5V"
            else:
                if inarow_Neast("*", row , col, D, 4) == True:
                    if self.data[row][col-1] == '~' or col == 0:
                        if col == 6 or self.data[row][col+4] == '~':
                            return "4H"
                        else:
                            return False
                    else:
                        return False

                elif inarow_Nsouth("*", row , col, D, 4) == True:
                    if self.data[row+1][col] == '~' or row == 0:
                        if row == 6 or self.data[row+4][col] == '~':
                            return "4V"
                        else:
                            return False
                    else:
                        return False
                else:
                    if inarow_Neast("*", row , col, D, 3) == True:
                        if self.data[row][col-1] == '~' or col == 0:
                            if col == 7 or self.data[row][col+3] == '~':
                                return "3H"
                            else:
                                return False
                        else:
                            return False
                    elif inarow_Nsouth("*", row , col, D, 3) == True:
                        if self.data[row+1][col] == '~' or row == 0:
                            if row == 7 or self.data[row+3][col] == '~':
                                return "3V"
                            else:
                                return False
                        else:
                            return False
                    else:
                        if inarow_Neast("*", row , col, D, 2) == True:
                            if self.data[row][col-1] == '~' or col == 0:
                                if col == 8 or self.data[row][col+2] == '~':
                                    return "2H"
                                else:
                                    return False
                            else:
                                return False
                        elif inarow_Nsouth("*", row , col, D, 2) == True:
                            if self.data[row+1][col] == '~' or row == 0:
                                if row == 8 or self.data[row+2][col] == '~':
                                    return "2V"
                                else:
                                    return False
                            else:
                                return False

    def replace(self, row, col):
        """ if a ship has fully sunk, replace the ship with a letter of its type. 
        SELF here references the board that is displayed that has hits or misses"""
        for row in range(10):
            for col in range(10):
                if self.data[row][col]== "*":
                    A = self.completesink(row,col)
                    B = int(A[0])
                    C = A[1]
                    D = BoardComp.data[row][col] #this draws on what the data in the grid for AI is so that it can paste it 
                    if A != False:
                        if C == "H":
                            for x in range(B):
                                self.data[row][col+x] = D
                        elif C == "V":
                            for x in range(B):
                                self.data[row+x][col] = D



class BoardComp2:
    """This class corresponds to opponenent played by the computer
    """
        
    def __init__(self):
        """Construct objects of type Board, with the given width and height."""
        width = 10 
        height = 10
        self.width = width
        self.height = height
        self.data = [[' ']*10 for row in range(10)]

        # We do not need to return anything from a constructor!

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # The string to return
        for row in range(0, self.height):
            s += (chr(65 + row)+ " " + '|')
            for col in range(0, self.width):
                s += (self.data[row][col] + '|')
            s += '\n'

        s += "  " + (2*self.width + 1) * '-'   # Bottom of the board
        s += '\n' + "  "
        for col in range(0, self.width): # Add code here to put the numbers underneath
            s+= ' '+ str(col)

        s += '\n'
        return s       # The board is complete; return it



    def Counthits(self):
        """ counts the number of ships that have been hit and returns that value"""
        n = 0
        for i in range(self.height):
            for x in range(self.width):
                if self.data[i][x] == '*':
                    n+= 1

        return n
        
    def checkifWin(self):
        """ checks if the number of hits = the total number of hits needed to win and returns TRUE or FALSE"""
        totalhitstowin = 17
        if self.Counthits() == totalhitstowin:
            return True
        else:
            return False
               
        #Keep in mind that A has to be created already. 
    def addMove(self, let, col, A):
        """It allows each player to choose a position for the missile they launch"""
        
        row = ord(let) - 65
        
        if col not in range(10) or row not in range(10):
            return False
        elif A.data[row][col] in "ABCSD":
            self.data[row][col] = "*"
        elif A.data[row][col] == " ":
            self.data[row][col] = "~"
        else:
            return False
            

    def AIMove(self): # VVVV  IMPORTANT< change all () to [] while referencing self.data
        """function that decides which grid spot to shoot a missile based on the current grid"""      
        L = {"A":5, "B":4, "C": 3 , "S":3, "D": 2 }
        D= self.data
        if "*" not in D:
            X = random.choice(range(10))
            Y = random.choice(range(10))
            return [rconvert(X),Y]
        else:
            for row in range(1,9):
                for col in range(1,9):
                    if self.data[row][col]== "*":
                        if self.data[row+1][col] == "*" and self.data[row-1][col] == " ":
                            result = [(row-1)(col)]
                        elif self.data[row][col+1] == "*" and self.data[row][col-1] == " ":
                            result = [(row)(col-1)]
                        elif self.data[row-1][col] == " ":
                            result = [(row-1)(col)]
                        elif self.data[row+1][col] == " ":
                            result = [(row+1)(col)]
                        elif self.data[row][col-1] == " ":
                            result = [(row)(col-1)]                    
                        elif self.data[row][col+1] == " ":
                            result = [(row)(col+1)]
                        else:
                            continue
        # A = result[1]
        # B = chr(65+A)
        # result[1]=B
        return result

    """def hostGame(self):
            This method brings everything together into the familiar game.
            print('Welcome to Connect Four!')
            while True:
                print()
                print(self)
                
                self.setAIboard()
                
                print(self)
                if self.checkifWin():
                    print("Congratulations")
                    break 
                
                Let = str(input("Letter choice for missile attack:"))
                Col = int(input("Column choice for missile attack:"))
                
                while self.addMove(Let, Col) == False:
                     Col = int(input("Column choice for missile attack:"))
                self.addMove(Let, Col)
                print(self)"""


    def completesink(self,row,col):
            """Decides if a ship is sunk or not
            self references the board that is displayed with hits or misses """
            D= self.data
            if inarow_Neast("*", row , col, D, 5) == True:
                return "5H" 
            elif inarow_Nsouth("*", row , col, D, 5) == True:
                return "5V"
            else:
                if inarow_Neast("*", row , col, D, 4) == True:
                    if self.data[row][col-1] == '~' or col == 0:
                        if col == 6 or self.data[row][col+4] == '~':
                            return "4H"
                        else:
                            return False
                    else:
                        return False

                elif inarow_Nsouth("*", row , col, D, 4) == True:
                    if self.data[row+1][col] == '~' or row == 0:
                        if row == 6 or self.data[row+4][col] == '~':
                            return "4V"
                        else:
                            return False
                    else:
                        return False
                else:
                    if inarow_Neast("*", row , col, D, 3) == True:
                        if self.data[row][col-1] == '~' or col == 0:
                            if col == 7 or self.data[row][col+3] == '~':
                                return "3H"
                            else:
                                return False
                        else:
                            return False
                    elif inarow_Nsouth("*", row , col, D, 3) == True:
                        if self.data[row+1][col] == '~' or row == 0:
                            if row == 7 or self.data[row+3][col] == '~':
                                return "3V"
                            else:
                                return False
                        else:
                            return False
                    else:
                        if inarow_Neast("*", row , col, D, 2) == True:
                            if self.data[row][col-1] == '~' or col == 0:
                                if col == 8 or self.data[row][col+2] == '~':
                                    return "2H"
                                else:
                                    return False
                            else:
                                return False
                        elif inarow_Nsouth("*", row , col, D, 2) == True:
                            if self.data[row+1][col] == '~' or row == 0:
                                if row == 8 or self.data[row+2][col] == '~':
                                    return "2V"
                                else:
                                    return False
                            else:
                                return False

    def replace(self, row, col):
        """ if a ship has fully sunk, replace the ship with a letter of its type. 
        SELF here references the board that is displayed that has hits or misses"""
        for row in range(10):
            for col in range(10):
                if self.data[row][col]== "*":
                    A = self.completesink(row,col)
                    B = int(A[0])
                    C = A[1]
                    D = BoardComp.data[row][col] #this draws on what the data in the grid for AI is so that it can paste it 
                    if A != False:
                        if C == "H":
                            for x in range(B):
                                self.data[row][col+x] = D
                        elif C == "V":
                            for x in range(B):
                                self.data[row+x][col] = D


# In order to start the match AI vs AI without fog of war, type: PlayAI().Game()
# In order to start a match against an AI with fog of war, type: PlayHuman().Game()
class PlayHuman:

    def Game(self):
        """ this function puts everything together and creates a game that plays itself (AI vs AI)"""

        B2 = BoardComp2()
        B = BoardComp()
        A = BoardUser()

        B.setAIboard()
        
        print("Captain, Welcome to a friendly match of Battle Ship!")
        print("Your navy is being released to the water, one sec...")
        time.sleep(2)
        A.setAIboard()
        print(A)
        Commands = input("Are you happy with this strategic arrangement? ('yes' or 'no'")
        while Commands == "no":
            print("Roger that.","Your navy is being released to the water, one sec...")
            A.clear()
            A.setAIboard()
            time.sleep(2)
            print(A)
            print("Your navy is ready for battle")
            Commands = str(input("Are you happy with this strategic arrangement? ('yes' or 'no')     "))

        print(B2)
        print(A)
        print("At your command captain")
        time.sleep(2)
        print("An enemy navy has been spotted on our radar")
        time.sleep(2)
        print("Captain, they are throwing missiles at us!")
        time.sleep(1)
        print("Let's show them the mistake they've just made")
        while True:
            # X = str(input("Captain, which row should we hit next?"))
            # print(X)
            # Y = str(input("One more thing Captain, which column should we hit?"))

            B2.addMove(str(input("Captain, which row should we hit now?")), int(input("One more thing Captain, which column should we hit next?")), B)
            print(B2)
            
            time.sleep(1)
            print("Wise choice captain!", "You can see the status of the enemy fleet in the radar")


            time.sleep(2)

            A.addMove(str(A.AIMove()[0]), A.AIMove()[1])
            print(A)

            print("The enemy has retaliated!", "~Evaluate potential damanges in our radar")

            if A.checkifWin() == True:
                print("Your fleet has been destroyed, better start swimming")
                break
            if B.checkifWin() == True:
                print("You have won this battle, but let's stay vigilant...")
                break

        
# In order to start the match AI vs AI without fog of war, type: PlayAI().Game()
# In order to start a match against an AI with fog of war, type: PlayHuman().Game()

class PlayAI:

    def Game(self):
        """ this function puts everything together and creates a game that plays itself (AI vs AI)"""
    

        B = BoardComp()
        
        A = BoardUser()
        print(B)
        print(A)
        B.setAIboard()
        A.setAIboard()

        while True:
        
            B.addMove(str(B.AIMove()[0]), B.AIMove()[1])

            A.addMove(str(A.AIMove()[0]), A.AIMove()[1])

            print(B)
            print(A)

            if A.checkifWin() == True:
                print("AI 01 Wins the Match")
                break
            if B.checkifWin() == True:
                print("AI 10 Wins the Match")
                break