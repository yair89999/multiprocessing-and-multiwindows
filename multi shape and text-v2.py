import multiprocessing
import pygame,os
import win32gui

pygame.init()

win1_color = (0,0,0)
win2_color = (0,0,255)
win1_size = (500,500)
win2_size = (500,500)

fonts = [pygame.font.SysFont("", 30),pygame.font.SysFont("", 40)]

class rect:
    def __init__(self,x,y, width, height):
        self.x,self.y,self.width,self.height = x,y,width,height
    def draw(self, x,y, window, color):
        pygame.draw.rect(window, color, [x,y,self.width,self.height])
class circle:
    def __init__(self,x,y, radius):
        self.x,self.y,self.radius = x,y,radius
    def draw(self, x,y, window, color):
        pygame.draw.circle(window, color, (x,y), self.radius)
class ellipse:
    def __init__(self, x,y ,width, height):
        self.x,self.y,self.width,self.height = x,y,width,height
    def draw(self, x,y, window, color):
        pygame.draw.ellipse(window,color, [x,y,self.width,self.height])
class line:
    def __init__(self, start_pos:tuple, end_pos:tuple, width):
        self.x,self.y = start_pos
        self.x_change, self.y_change = end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]
        self.width = width
    def draw(self, x, y, window, color):
        start_pos = (x,y)
        end_pos = (x + self.x_change, y + self.y_change)
        pygame.draw.line(window, color, start_pos, end_pos, self.width)
class text:
    def __init__(self,x,y,txt, font_index):
        self.x,self.y,self.txt, self.font_index = x,y,txt, font_index
    def draw(self,x,y,window,color):
        window.blit(fonts[self.font_index].render(self.txt, True, color), (x,y))

win1_shapes = [rect(0,175,200,200), circle(100,100,50), text(10,10,"This is a test to see how the text works",0)]
win2_shapes = [rect(100,100,50,50),rect(300,300,100,100), line((10,10), (370,370),3), ellipse(10,200,50,80)]

class win1:
    def __init__(self): 
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)
        self.window = pygame.display.set_mode(win1_size)
        pygame.display.set_caption("WIN1")

        self.shapes = win1_shapes

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
                for rect in windows_dict["win2_shapes"]:
                    rect_display_x = win2_pos[0] + rect.x # x on the screen
                    rect_display_y = win2_pos[1] + rect.y # y on the screen

                    x2 = rect_display_x - win1_pos[0] # changing the x to fit the new screen
                    y2 = rect_display_y - win1_pos[1] # changing the y to fit the new screen

                    rect.draw(x2,y2,self.window, win2_color)
        except Exception as e:
            print("ERROR",e)
            pass
        for shape in self.shapes:
            shape.draw(shape.x,shape.y,self.window, win1_color)

def win1_func(windows_dict):
    window1 = win1()
    windows_dict["win1_size"] = window1.window.get_size()
    windows_dict["win1_shapes"] = window1.shapes

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

        self.shapes = win2_shapes

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
                for shape in windows_dict["win1_shapes"]:
                    shape_display_x = win1_pos[0] + shape.x # x on the screen
                    shape_display_y = win1_pos[1] + shape.y # y on the screen

                    x2 = shape_display_x - win2_pos[0] # changing the x to fit the new screen
                    y2 = shape_display_y - win2_pos[1] # changing the y to fit the new screen

                    shape.draw(x2,y2,self.window, win1_color)
        except:
            pass

        for shape in self.shapes:
            shape.draw(shape.x,shape.y,self.window, win2_color)

def win2_func(windows_dict):
    window2 = win2()
    windows_dict["win2_size"] = window2.window.get_size()
    windows_dict["win2_shapes"] = window2.shapes

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
    shared_dict = manager.dict({"win1":(), "win1_size":(), "win1_shapes":[], "win2":(), "win2_size":(), "win2_shapes":[]})

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
