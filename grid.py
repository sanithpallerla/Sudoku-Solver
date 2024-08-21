# guiapp.py
import pygame
pygame.font.init()
from cell import Cell
import numpy as np

def list_to_numpy(lst):
    '''This function is used to convert list into numpy array'''
    return np.asarray(lst)

class Grid:
    showDomain=True
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    # board = [
    #     [7, 8, 5, 4, 3, 9, 1, 2, 6],
    #     [6, 1, 2, 8, 7, 5, 3, 4, 9],
    #     [4, 9, 3, 6, 2, 1, 5, 7, 8],
    #     [8, 5, 7, 9, 4, 3, 2, 6, 1],
    #     [2, 6, 1, 7, 5, 8, 9, 3, 4],
    #     [9, 3, 4, 1, 6, 2, 7, 8, 5],
    #     [5, 7, 8, 3, 9, 4, 6, 1, 2],
    #     [1, 2, 6, 5, 8, 7, 4, 9, 3],
    #     [3, 4, 9, 2, 1, 6, 8, 0, 0]
    # ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    ###########################################################################################
    ### You need to work of these functions only ###
    
    def goalCheck(self,state):
        '''
        This function takes a parameter: state of type list[list[int]] which holds current board value 
        which you can use to check if the board is solved or not.

        Function returns a boolean value
        '''
        # solved = [
        #     [7, 8, 5, 4, 3, 9, 1, 2, 6],
        #     [6, 1, 2, 8, 7, 5, 3, 4, 9],
        #     [4, 9, 3, 6, 2, 1, 5, 7, 8],
        #     [8, 5, 7, 9, 4, 3, 2, 6, 1],
        #     [2, 6, 1, 7, 5, 8, 9, 3, 4],
        #     [9, 3, 4, 1, 6, 2, 7, 8, 5],
        #     [5, 7, 8, 3, 9, 4, 6, 1, 2],
        #     [1, 2, 6, 5, 8, 7, 4, 9, 3],
        #     [3, 4, 9, 2, 1, 6, 8, 5, 7]
        # ]
        for i in range(9):
            for j in range(9):
                if not(self.validate_number(state,i,j,state[i][j])):
                    return False
        return True

    def validate_number(self,grid, row, col, num):
        '''This function is used to validate number based on sudoku rules'''
        # Check if the given number is already present in the same row

        for i in range(9):
            if col != i:
                if grid[row][i] == num:
                    return False

        # Check if the given number is already present in the same column
        for i in range(9):
            if row != i:
                if grid[i][col] == num:
                    return False

        # Check if the given number is already present in the same 3x3 sub-grid
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if row != (row_start+i) and col!= (col_start+j):
                    if grid[row_start + i][col_start + j] == num:
                        return False

        return True

    def check_row(self,row,state,domain = 0):
        '''This function is used to update domain based on pre-filled numbers in row'''
        for i in range(9):
            if state[row][i] in domain:
                domain.remove(state[row][i])
        return domain

    def check_col(self,col,state,domain = 0):
        '''This function is used to update domain based on prefilled numbers in column'''
        for i in range(9):
            if state[i][col] in domain:
                domain.remove(state[i][col])
        return domain

    def updateDomain(self,state):
        '''
        This Function takes a parameter: state of type list[list[int]] which holds current board value
        which you can use to check if the board is solved or not.
        You need to update the domain for each unassigned cell.
        Access the cells value using self.cells property.

        Function returns void.
        '''

        for row in range(9):
            for col in range(9):
                if state[row][col] == 0:
                    default_domain = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                    domain = self.check_row(row,state,default_domain)
                    domain = self.check_col(col,state,domain)
                    self.cells[row][col].domain = domain

    def update_model(self):
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set(val)
            self.update_model()

            if self.valid(self.model, val, (row,col)) and self.solve():
                return True
            else:
                self.cells[row][col].set(0)
                self.cells[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cells[row][col].set_temp(val)

    def draw(self):
        self.win.fill((255,255,255))
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(self.win,self.showDomain)
        
    def valid(bo, num, pos):
    # Check row
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(bo)):
            if bo[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if bo[i][j] == num and (i,j) != pos:
                    return False

        return True

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    return False
        return True

    def solve(self):
        li,pos,flag = self.findEmpty()

        if flag == 0:
            return True

        if not pos:
            return False
        
        row,col = pos

        for i in li:
            if self.valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def findEmpty(self):
        state=self.model
        minValues = 10
        minDomain = set()
        position = ()
        emptyFlag = 0
        for i in range(9):
            for j in range(9):
                if state[i][j] == 0:
                    emptyFlag = 1
                    domain = self.cells[i][j].domain
                    if(minValues > len(domain) and len(domain) > 0):
                        minValues = len(domain)
                        minDomain = domain
                        position = (i,j)
        if(minValues == 10):
            return (None,None,emptyFlag)
        return (minDomain,position,emptyFlag)

    def isValid(self,r,c,k):
        state=self.model
        notInRow=k not in state[r]
        notInCol=k not in [state[i][c] for i in range(9)]
        notInBox=k not in [state[i][j] for i in range(r//3*3,r//3*3+3) for j in range(c//3*3,c//3*3+3)]
        return notInRow and notInCol and notInBox

    def backtracking(self,r=0,c=0):
        state=self.model
        for r in range(9):
            for c in range(9):
                if state[r][c]==0:
                    for digit in range(1,10):
                            state[r][c]=digit
                            self.cells[r][c].set(digit)
                            self.cells[r][c].draw_change(self.win,self.showDomain,self.isValid(r,c,digit))
                            pygame.display.update()
                            pygame.time.delay(100)
                            if self.goalCheck(self.model):
                                return True
                            else:
                                if self.backtracking(r,c+1):
                                    return True
                                state[r][c]=0
                    return False

    def forwardChecking(self):
        state=self.model
        self.updateDomain(state)
        # self.draw()
        domain,position,emptyFlag=self.findEmpty()
        if emptyFlag == 0:
            return self.goalCheck(state)
        if not position:
            return False
        row,col = position

        for digit in domain:
            if (self.isValid(row,col,digit)):
                state[row][col] = digit
                self.cells[row][col].set(digit)
                self.cells[row][col].draw_change(self.win,self.showDomain,True)
                # self.update_model()
                pygame.display.update()
                pygame.time.delay(100)
                if self.forwardChecking():
                    return self.goalCheck(state)         
        return False