import multiprocessing
import pygame,os
import win32gui

pygame.init()

win_size = (500,500)

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

win1_shapes = [rect(0,200,200,200), circle(100,100,50), text(10,10,"This is a test to see how the text works",0),text(300,300,"Text 2 to see multi window test",0)]
win2_shapes = [rect(100,100,50,50),rect(300,300,100,100), line((-100,-100), (400,400),3), ellipse(10,200,50,80),rect(-100,20,150,150)]
combined_shapes = win1_shapes + win2_shapes

class win:
    def __init__(self, win_num:int, total_win_num:int, win_x, win_y): 
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_x, win_y)
        self.window = pygame.display.set_mode(win_size)
        pygame.display.set_caption("WIN"+str(win_num))
        self.win_num = win_num
        self.total_win_num = total_win_num

        self.shapes = combined_shapes

    def get_window_position(self):
        hwnd = pygame.display.get_wm_info()["window"]
        rect = win32gui.GetWindowRect(hwnd)
        return rect[:2]
    
    def draw(self, windows_dict):
        self.window.fill((255,255,255))
        current_win_pos = windows_dict["win"+str(self.win_num)]
        for shape in self.shapes:
            try:
                shape.draw(shape.x,shape.y,self.window, windows_dict["windows colors"][self.win_num-1])
            except:
                shape.draw(shape.x,shape.y,self.window, windows_dict["windows colors"][0])
        
        for win_num in range(1,self.total_win_num+1):
            win_pos = windows_dict["win"+str(win_num)]
            for shape in windows_dict["win"+str(win_num)+"_shapes"]:
                x,y = shape.x,shape.y
                shape_screen_x = win_pos[0] + x
                shape_screen_y = win_pos[1] + y
                x = shape_screen_x - current_win_pos[0]
                y = shape_screen_y - current_win_pos[1]
                try:
                    shape.draw(x,y,self.window, windows_dict["windows colors"][win_num-1])
                except:
                    shape.draw(x,y,self.window, windows_dict["windows colors"][1])

def win_func(windows_dict:dict, win_num:int, total_win_num:int, win_x, win_y):
    window = win(win_num, total_win_num, win_x, win_y)
    windows_dict["win"+str(win_num)+"_size"] = window.window.get_size()
    windows_dict["win"+str(win_num)+"_shapes"] = window.shapes

    running = True
    while running:
        windows_dict["win"+str(win_num)] = window.get_window_position()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try: # will get error on the first iteration always because win2 variables are not defines
            window.draw(windows_dict)
        except:
            pass

        pygame.display.update()

    pygame.quit()


# Controller function to manage both functions using multiprocessing
def controller():
    desktop = win32gui.GetDesktopWindow()
    rect = win32gui.GetClientRect(desktop)
    display_width = rect[2] - rect[0] # getting it for the windows positioning
    display_height = rect[3] - rect[1]

    manager = multiprocessing.Manager()
    total_win_num = 5
    shared_dict_pre = {}
    for i in range(total_win_num):
        shared_dict_pre["win"+str(i+1)] = ()
        shared_dict_pre["win"+str(i+1)+"_size"] = ()
        shared_dict_pre["win"+str(i+1)+"_shapes"] = []
    shared_dict_pre["windows colors"] = [
        (0,0,0),
        (0,0,255),
        (0,255,0),
        (255,0,0)
    ]

    shared_dict = manager.dict(shared_dict_pre)
    processors = []

    x,y = 0,50
    for process_num in range(1,total_win_num+1):
        process = multiprocessing.Process(target=win_func, args=(shared_dict, process_num, total_win_num, x,y))
        processors.append(process)
        x += win_size[0]
        
        if x + win_size[0] >= display_width:
            x = 0
            y += win_size[1]
        if y + win_size[1] >= display_height: # if the y is out of screen we start over the positioning
            x = 0
            y = 50
        
    for process in processors:
        process.start()
    
    for process in processors:
        process.join()
"""
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
"""

if __name__ == "__main__":
    controller()
