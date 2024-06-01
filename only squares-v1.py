import multiprocessing
import pygame,os
import win32gui

pygame.init()

win1_color = (0,0,0)
win2_color = (0,0,255)
win1_size = (500,500)
win2_size = (500,500)

win1_rects = [pygame.Rect(0,175,200,200)]
win2_rects = [pygame.Rect(100,100,50,50),pygame.Rect(300,300,100,100)]

class win1:
    def __init__(self): 
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)
        self.window = pygame.display.set_mode(win1_size)
        pygame.display.set_caption("WIN1")

        self.rects = win1_rects

    def get_window_position(self):
        hwnd = pygame.display.get_wm_info()["window"]
        rect = win32gui.GetWindowRect(hwnd)
        return rect[:2]
    
    def draw(self, windows_dict):
        self.window.fill((255,255,255))

        try: # the code is in try except because we get error 100% of times on the first iteration because win2 position in the dict is ()
            win1_pos = windows_dict["win1"]
            win1_size = windows_dict["win1_size"]
            win1_rect = pygame.Rect(win1_pos[0],win1_pos[1],win1_size[0],win1_size[1])
            win2_pos = windows_dict["win2"]
            win2_size = windows_dict["win2_size"]
            win2_rect = pygame.Rect(win2_pos[0],win2_pos[1],win2_size[0],win2_size[1])
            if win1_rect.colliderect(win2_rect): # if the windows collide
                for rect in windows_dict["win2_rects"]:
                    rect_display_x = win2_pos[0] + rect.x # x on the screen
                    rect_display_y = win2_pos[1] + rect.y # y on the screen

                    x2 = rect_display_x - win1_pos[0]
                    y2 = rect_display_y - win1_pos[1]

                    rect.x = x2
                    rect.y = y2
                    pygame.draw.rect(self.window,win2_color, rect)
        except:
            pass
        for rect in self.rects:
            pygame.draw.rect(self.window, win1_color, rect)

def win1_func(windows_dict):
    window1 = win1()
    windows_dict["win1_size"] = window1.window.get_size()
    windows_dict["win1_rects"] = window1.rects

    running = True
    while running:
        windows_dict["win1"] = window1.get_window_position()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #print("win1:", windows_dict)

        window1.draw(windows_dict)

        pygame.display.update()

    pygame.quit()

class win2:
    def __init__(self): 
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (500,500)
        self.window = pygame.display.set_mode(win2_size)
        pygame.display.set_caption("WIN2")

        self.rects = win2_rects

    def get_window_position(self):
        hwnd = pygame.display.get_wm_info()["window"]
        rect = win32gui.GetWindowRect(hwnd)
        return rect[:2]
    
    def draw(self, windows_dict):
        self.window.fill((255,255,255))

        try: # the code is in try except because we get error 100% of times on the first iteration because win2 position in the dict is ()
            win1_pos = windows_dict["win1"]
            win1_size = windows_dict["win1_size"]
            win1_rect = pygame.Rect(win1_pos[0],win1_pos[1],win1_size[0],win1_size[1])
            win2_pos = windows_dict["win2"]
            win2_size = windows_dict["win2_size"]
            win2_rect = pygame.Rect(win2_pos[0],win2_pos[1],win2_size[0],win2_size[1])
            if win1_rect.colliderect(win2_rect): # if the windows collide
                for rect in windows_dict["win1_rects"]:
                    rect_display_x = win1_pos[0] + rect.x # x on the screen
                    rect_display_y = win1_pos[1] + rect.y # y on the screen

                    x2 = rect_display_x - win2_pos[0]
                    y2 = rect_display_y - win2_pos[1]

                    rect.x = x2
                    rect.y = y2
                    pygame.draw.rect(self.window,win1_color, rect)
        except:
            pass

        for rect in self.rects:
            pygame.draw.rect(self.window, win2_color, rect)

def win2_func(windows_dict):
    window2 = win2()
    windows_dict["win2_size"] = window2.window.get_size()
    windows_dict["win2_rects"] = window2.rects

    running = True
    while running:
        windows_dict["win2"] = window2.get_window_position()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #print("win2:", windows_dict)

        window2.draw(windows_dict)

        pygame.display.update()

    pygame.quit()

# Controller function to manage both functions using multiprocessing
def controller():
    manager = multiprocessing.Manager()
    shared_dict = manager.dict({"win1":(), "win1_size":(), "win1_rects":[], "win2":(), "win2_size":(), "win2_rects":[]})

    # Create separate processes for func1 and func2
    process1 = multiprocessing.Process(target=win1_func, args=(shared_dict,),)
    process2 = multiprocessing.Process(target=win2_func, args=(shared_dict,),)

    # Start both processes
    process1.start()
    process2.start()
    
    # actions that will happen while the processors run
    # change the param_dict which is the shared dict between the processors in order to have the values changed
    
    # Wait for both processes to finish
    process1.join()
    process2.join()

if __name__ == "__main__":
    controller()
