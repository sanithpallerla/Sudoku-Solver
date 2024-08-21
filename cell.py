import pygame
pygame.font.init()
class Cell:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height, domain = {i for i in range(1,10)}):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.domain=domain

    def setToString(self,num):
        numbers=list(num)
        matrix = [[num for num in numbers[i:i+3]] for i in range(0, 9, 3)]
        return matrix


    def draw(self, win,showDomain):
        fnt = pygame.font.SysFont("Bahnschrift", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        if showDomain:
            if self.temp != 0 and self.value == 0:
                text = fnt.render(str(self.temp), 1, (128,128,128))
                win.blit(text, (x+5, y+5))
            elif not(self.value == 0):
                text = fnt.render(str(self.value), 1, (0, 0, 0))
                win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        else:
            if self.value == 0:
                fnt = pygame.font.SysFont("Bahnschrift", 20)
                strMatrix=self.setToString(self.domain)
                for idx,string in enumerate(strMatrix):
                    text = fnt.render(str(string).strip("[").strip(']'), 1, (0,0,255))
                    win.blit(text, ((x+15), (y+10)+idx*20))
            if not(self.value == 0):
                text = fnt.render(str(self.value), 1, (0, 0, 0))
                win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(self, win, showDomain,g=True):
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        
        if showDomain:
            fnt = pygame.font.SysFont("Bahnschrift", 40)
            pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
            if g:
                pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
            else:
                pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)
        else:
            if self.value==0:
                fnt = pygame.font.SysFont("Bahnschrift", 20)
                pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)
                strMatrix=self.setToString(self.domain)
                for idx,string in enumerate(strMatrix):
                    pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 1)
                    pygame.display.update()
                    pygame.time.delay(100)
                    text = fnt.render(str(string).strip("[").strip(']'), 1, (0,0,255))
                    win.blit(text, ((x+15), (y+10)+idx*20))
            else:
                fnt = pygame.font.SysFont("Bahnschrift", 40)

                pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

                text = fnt.render(str(self.value), 1, (0, 0, 0))
                win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
                if g:
                    pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
                else:
                    pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val