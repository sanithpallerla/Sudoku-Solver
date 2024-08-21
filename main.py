import pygame
from grid import Grid
from checkbox import Checkbox

def main():
    win = pygame.display.set_mode((1000,720))
    pygame.display.set_caption("SUDOKU")
    win.fill((255,255,255))
    board = Grid(9, 9, 720, 720, win)
    key = None
    
    # showDomain=True
    domainText="Show Domain"
    success=False
    boxes = []
    # button = Checkbox(win, 750, 150, 0, caption='BackTracking')
    # button.checked=True
    button2 = Checkbox(win, 750, 200, 1, caption='Forward Checking')
    button2.checked=True
    # boxes.append(button)
    boxes.append(button2)

    #quit the window when pressing esc key while running the code.
    run = True
    while run:
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                run=False
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cells[i][j].temp != 0:
                        if board.place(board.cells[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")   
                        key = None

                        if board.is_finished():
                            print("Game Over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                #if clicked on play button, solve the sudoku
                if 810 <= pos[0] <= 885 and 400 <= pos[1] <= 430:
                    # if button.checked:
                    #     success=board.backtracking()
                    # elif button2.checked:
                    #     success=board.forwardChecking()
                    if button2.checked:
                        success=board.forwardChecking()
                    

                if 780<=pos[0]<=910 and 300 <=pos[1]<=330:
                    board.showDomain=not board.showDomain
                    domainText="Show Domain" if board.showDomain else "Hide Domain"
                    if not board.showDomain and button2.checked:
                        board.updateDomain(board.model)
                    
                for box in boxes:
                    box.update_checkbox(event)
                    if box.checked is True:
                        for b in boxes:
                            if b != box:
                                b.checked = False
                #pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)
            
        board.draw()
        # redraw_window(win, board)
        if success:
            smallfont = pygame.font.SysFont('Bahnschrift',30) 
            text = smallfont.render('Game Over.' , True , 'green')
            win.blit(text , (790 , 600))
        
        for box in boxes:
            box.render_checkbox()

        # Show Domain Button
        pygame.draw.rect(win, (255,0,0), [780, 300, 130 , 30])
        smallfont = pygame.font.SysFont('Bahnschrift',16) 
        text = smallfont.render(domainText , True , 'black')
        win.blit(text , (795 , 310))

        #Play Button
        pygame.draw.rect(win, (0,255,0), [810, 400, 75 , 30])
        smallfont = pygame.font.SysFont('Bahnschrift',16) 
        text = smallfont.render('Play' , True , 'black')
        win.blit(text , (830 , 408))
        # board.draw()
        pygame.display.update()   
main()
pygame.quit()