
import pygame
import os
import time
import sys

pygame.init()

WHITE = (255,255,255)
GRAY = (192,192,192)
BLACK = (0,0,0)
YELLOW = (255,255,0)
FPS = 60
pygame.display.set_caption("Suduko Solver")


class Board:
    
    def __init__(self):

        self.width = 720
        self.height = 720
        self.rows = 9
        self.cols = 9
        self.gap = int(720/9)
        self.square = int(720/9)
        self.window = pygame.display.set_mode((self.width, self.height))
        

        self.b = [[5,3,0,0,7,0,0,0,0],
                  [6,0,0,1,9,5,0,0,0],
                  [0,9,8,0,0,0,0,6,0],
                  [8,0,0,0,6,0,0,0,3],
                  [4,0,0,8,0,3,0,0,1],
                  [7,0,0,0,2,0,0,0,6],
                  [0,6,0,0,0,0,2,8,0],
                  [0,0,0,4,1,9,0,0,5],
                  [0,0,0,0,8,0,0,7,9]]

        self.correct = [[5,3,4,6,7,8,9,1,2],
                        [6,7,2,1,9,5,3,4,8],
                        [1,9,8,3,4,2,5,6,7],
                        [8,5,9,7,6,1,4,2,3],
                        [4,2,6,8,5,3,7,9,1],
                        [7,1,3,9,2,4,8,5,6],
                        [9,6,1,5,3,7,2,8,4],
                        [2,8,7,4,1,9,6,3,5],
                        [3,4,5,2,8,6,1,7,9]]
        
        self.blocks = [[Block(self.b[i][j], i, j) for j in range(self.cols)] for i in range(self.rows)]


    def board(self): # draws lines to the window
        self.window.fill(GRAY)
   
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.window, (0,0,0), (0, i*self.gap), (self.width, i*self.gap), thick)
            pygame.draw.line(self.window, (0, 0, 0), (i * self.gap, 0), (i * self.gap, self.height), thick)
    
    def get_pos(self,pos):
        col, row = pos
        row = row//self.square
        col = col//self.square
        
        return row, col

    def find_empty(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.blocks[r][c].number == 0:
                    return r, c
    
    def is_valid(self, n, r, c):
            # Check row
        for i in range(self.cols):
            if self.blocks[r][i].number == n and c != i:
                return False

        # Check column
        for i in range(self.rows):
            if self.blocks[i][c].number == n and r != i:
                return False

        # Check box
        box_x = r // 3
        box_y = c // 3

        for i in range(box_x*3, box_x*3 + 3):
            for j in range(box_y * 3, box_y*3 + 3):
                if self.blocks[i][j].number == n and (i,j) != (r,c):
                    return False

        return True



 

    def write_to(self, n, r, c): # writes to the BLOCK
        self.blocks[r][c].number = n        
        pygame.display.flip()


    def is_correct(self):
        #if correct then draw a grean square around that one
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.blocks[r][c].number != self.correct[r][c]:
                    break
                elif self.blocks[r][c].number == self.correct[r][c]:
                    count +=1
        if count == 81:
            print("Solved")

    def display_squares(self): #displays the BLOCKS
        
        for i in self.blocks:
            for j in i:
                if j.number == 0:
                    pass
                else:
                    j.display(self.window)
    
    def back_track(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if self.is_valid(i, row, col):
                self.blocks[row][col].number = i

                if self.back_track():
                    return True

                self.blocks[row][col].number = 0

        return False

    def RUN_GAME(self):
        global board_arr
        clock = pygame.time.Clock()
        run = True
        self.board()
        self.display_squares()
        row, col = None, None  
        num = None
        

        while run:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    run = False


                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    mouse_pos = pygame.mouse.get_pos()
                    row, col= self.get_pos(mouse_pos)
                    
                    self.blocks[col][row].clear(self.window,row,col)
                    
                    pygame.display.flip()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.back_track()                        
                    if event.key == pygame.K_0:
                        num = 0
                    if event.key == pygame.K_1:
                        num = 1
                    if event.key == pygame.K_2:
                        num = 2
                    if event.key == pygame.K_3:
                        num = 3
                    if event.key == pygame.K_4:
                        num = 4
                    if event.key == pygame.K_5:
                        num = 5
                    if event.key == pygame.K_6:
                        num = 6
                    if event.key == pygame.K_7:
                        num = 7
                    if event.key == pygame.K_8:
                        num = 8
                    if event.key == pygame.K_9:
                        num = 9
                
            
            #something that re renders all the text
            if row != None and col != None and num != None:
                self.write_to(num, row, col)

            self.display_squares()
            #self.is_correct()  
            num = 0          
            clock.tick(FPS)
            pygame.display.flip()
        


class Block:  # youre going to have 81 total squares (9x9)

    def __init__(self, number, row, col): #number value, and (row, col) in the board_arr
        self.number = number
        self.gap = int(720/9)
        self.place = (self.gap/2, self.gap/2) # location where the text will be placed relative to the square
        self.row = row
        self.col = col
        self.font = pygame.font.SysFont('Arial', 40)
        


    def display(self, screen):
        text = self.font.render(str(self.number), 1, BLACK)
        screen.blit(text, pygame.Rect(self.col*self.gap + self.gap/3 , self.row*self.gap + self.gap/4, self.gap, self.gap))   

    def clear(self,screen,r,c):
        
        pygame.draw.rect(screen, GRAY, (c*self.gap + 4, r*self.gap + 4, self.gap - 10, self.gap - 10))
        pygame.display.flip()
        
#driver code

test = Board()
test.RUN_GAME()

