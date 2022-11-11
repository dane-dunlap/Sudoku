from cgitb import text
import pygame
import requests
import sudoku_algo
import time
import sys
import os


WIDTH = 550
background_color = (251,247,245)
buffer = 5
mistakes = 0
#response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
#grid = response.json()["board"]
grid = [[0,0,1,0,0,0,0,0,0],
          [2,0,0,0,0,0,0,7,0],
          [0,7,0,0,0,0,0,0,0],
          [1,0,0,4,0,6,0,0,7],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,1,2,5,4,6],
          [3,0,2,7,6,0,9,8,0],
          [0,6,4,9,0,3,0,0,1],
          [9,8,0,5,2,1,0,6,0]]
grid_original = [[grid[x][y] for y in range (len(grid[0]))] for x in range (len(grid))]
solved_grid = [[grid[x][y] for y in range (len(grid[0]))] for x in range (len(grid))]
square_size = 50


def resource_path(relative_path):
    try:
        #PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def highlight(win,position,old_position):
    outline_size = 42
    i = position[0]
    j = position[1]
    pygame.draw.rect(win, (255,0,0), (i*square_size+buffer,j*square_size+buffer, outline_size ,outline_size), 2)
    if old_position != (0,0) and position != old_position:
        pygame.draw.rect(win, (255,255,255), (old_position[0]*square_size+buffer,old_position[1]*square_size+buffer, outline_size ,outline_size), 2)
    pygame.display.update()



def insert(win,position,solved_grid):
    i = position[1]
    j = position[0] 
    global mistakes
    mistake_margin = 30
    myfont = pygame.font.SysFont("Comic Sans MS",35)

    
    while True:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if grid_original[i-1][j-1] != 0:
                    return
                
                if event.key == 48:
                    grid[i-1][j-1] = event.key -48
                    pygame.draw.rect(win,background_color,(j*square_size+buffer,i*square_size+buffer,square_size-buffer*2,square_size-buffer*2))
                    pygame.display.update()


                if event.key-48 >0 and event.key-48 <10 and event.key - 48 == solved_grid[i-1][j-1]:
                    pygame.draw.rect(win,background_color,(position[0]*50+15,position[1]*50+15,30,30))
                    value = myfont.render(str(event.key-48),True,(0,0,0))
                    win.blit(value,(position[0]*50+15,position[1]*50))
                    grid[i-1][j-1] = event.key -48
                    pygame.draw.rect(win, (255,255,255), (position[0]*square_size+buffer,position[1]*square_size+buffer, 42 ,42), 2)
                    pygame.display.update()

                elif event.key-48>0 and event.key-48 <10 and event.key -48 != solved_grid[i-1][j-1]:
                    mistakes +=1
                    pygame.draw.rect(win, (255,255,255), (position[0]*square_size+buffer,position[1]*square_size+buffer, 42 ,42), 2)
                    
                    if mistakes ==3:
                        loser_message = myfont.render("You Lost!",1,(255,0,0))
                        win.blit(loser_message,(200,3))
                        pygame.display.update()
                        time.sleep(3)
                        pygame.quit()
                        return


                        
                    text = myfont.render("X", 0.7, (255, 0, 0))
                    win.blit(text, (420+mistake_margin*mistakes, 500))
                    pygame.display.update()
                     
                
                return
            return
                
                
def printboard(board):
    for i in range(len(board)):
        if i%3 ==0 and i != 0:
            print("---------")
        for j in range(len(board[0])):
            if j%3 ==0 and j !=0:
                print("|",end=" ")
            if j == 8:
                print(str(board[i][j])+" ")
            else:
                print(str(board[i][j]),end="")

def findempty(board):

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i,j)
    return None



def valid(board,num,pos):
    
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    
    for j in range(len(board)):
        if board[j][pos[1]] == num and pos[0] != j:
            return False

    box_x = pos[0]//3
    box_y = pos[1] //3

    for i in range(box_x*3,box_x*3+3):
        for j in range(box_y*3,box_y*3+3):
            if board[i][j] == num and (i,j) != pos:
                return False

    return True


def solve(board):
    find = findempty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(board,i,(row,col)) == True:
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False


def finish_game(win,board):
    myfont = pygame.font.SysFont("Comic Sans MS",35)
    find = findempty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(board,i,(row,col)) == True:
            board[row][col] = i
            value = myfont.render(str(i),True,(0,0,0))
            win.blit(value,((col+1)*50 +15,(row+1)*50))
            pygame.display.update()
            #time.sleep(0.5)
            if finish_game(win,board):
                return True
            board[row][col] = 0
            pygame.draw.rect(win,background_color,((col+1)*square_size+buffer,(row+1)*square_size+buffer,square_size-buffer*2,square_size-buffer*2))
            
            #time.sleep(0.5)
            pygame.display.update()

    return False

def checkwin(grid):
    for i in range(len(grid[0])):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return False
    return True
        

def introscreen():
    myfont = pygame.font.SysFont("Comic Sans MS",35)
    win = pygame.display.set_mode((WIDTH, WIDTH))
    subtitle_font = pygame.font.SysFont("Comic Sans MS", 22)
    win.fill(background_color)
    while True:
            
            text = myfont.render("Welcome to Dane's Sudoku!",True,(0,0,0))
            text_rect = text.get_rect(center=(WIDTH/2,200))
            win.blit(text,text_rect)
            text = subtitle_font.render("Press the f key to solve puzzle",True,(0,0,0))
            text_rect = text.get_rect(center=(WIDTH/2,300))
            win.blit(text,(text_rect))
            text = subtitle_font.render("[Press the spacebar to begin]",True,(0,255,0))
            text_rect = text.get_rect(center=(WIDTH/2,350))
            win.blit(text,(text_rect))
            pygame.display.update()
            
            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                if event.type == pygame.KEYDOWN and event.key == 32:
                    pygame.draw.rect(win,background_color,(0,0,WIDTH,WIDTH))
                    pygame.display.update()
                    return


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    myfont = pygame.font.SysFont("Comic Sans MS",35)
    mistakes =0
    solve(solved_grid)
    introscreen()
    old_pos= (0,0)
    
    while True:
        for event in pygame.event.get():
            pygame.init()
            if event.type == pygame.QUIT:
                        pygame.quit()
                        return

            for i in range(0,10):
                if i %3 ==0:
                    pygame.draw.line(win,(0,0,0),(50+50*i,50),(50 +50*i,500),4)
                    pygame.draw.line(win,(0,0,0),(50,50+50*i),(500,50+50*i),4)
                
                pygame.draw.line(win,(0,0,0),(50+50*i,50),(50 +50*i,500),2)
                pygame.draw.line(win,(0,0,0),(50,50+50*i),(500,50+50*i),2)
            pygame.display.update()

            for i in range(len(grid[0])):
                for j in range(len(grid[0])):
                    if (0<grid[i][j]<10):
                        value = myfont.render(str(grid[i][j]),True,(0,0,0))
                        win.blit(value,((j+1)*50 +15,(i+1)*50))

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP and event.button ==1:
                pos = pygame.mouse.get_pos()
                highlight(win,(pos[0]//50,pos[1]//50),(old_pos[0]//50,old_pos[1]//50))
                insert(win,(pos[0]//50,pos[1]//50),solved_grid)
                old_pos = pos

            if event.type == pygame.KEYDOWN:
                if event.key == 102:
                    finish_game(win,grid)
                    pygame.display.update()

        if checkwin(grid) == True:
            win_message = myfont.render("You Win!",1,(0,255,0))
            win.blit(win_message,(200,3)) 
            pygame.display.update()
            time.sleep(3)
            pygame.quit()
            return
               
            
            
main()




