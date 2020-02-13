import cv2
import numpy as np
import pygame 
import os 
import time 
import sys

class align_gui(object): # Creates a GUI using only OpenCV. Scroll from mouse zooms in and out and dragging the mouse drags the sandbox vizualization for alignment on surface. 
   

    def __init__(self, img, screen_name = 'Sandbox Alignment', onLeftClickFunction = None):
        self.screen_name = screen_name
        self.img = img
        self.onLeftClickFunction = onLeftClickFunction
        #self.TRACKBAR_TICKS = 1000
        self.align_calc = align_calc(img.shape, self)
        self.lButtonDownLoc = None
        self.mButtonDownLoc = None
        self.rButtonDownLoc = None
        cv2.namedWindow(self.screen_name, flags=cv2.WINDOW_GUI_NORMAL)
        cv2.setWindowProperty(self.screen_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        self.redo_image()
        cv2.setMouseCallback(self.screen_name, self.onMouse)
       
    def onMouse(self,event, x,y,_ignore1,_ignore2): # Responses of mouse interactions. X and Y are the coordinates of pixels in the image. 
        
        if event == cv2.EVENT_MOUSEMOVE:
            return

        elif event == cv2.EVENT_RBUTTONDOWN:
            #record where the user started to right-drag
            self.mButtonDownLoc = np.array([y,x])

        elif event == cv2.EVENT_RBUTTONUP and self.mButtonDownLoc is not None: #Detect if user has finished dragging right. 
            
            dy = y - self.mButtonDownLoc[0]
            pixelsPerDoubling = 0.2*self.align_calc.shape[0] #lower = zoom more (Actual 0.2)
            changeFactor = (1.0+abs(dy)/pixelsPerDoubling)
            changeFactor = min(max(1.0,changeFactor),5.0)

            if changeFactor < 1.05:
                dy = 0 #this was a click, not a draw. So don't zoom, just re-center.

            if dy > 0: #moved down, so zoom out.
                zfactor = 1.0/changeFactor

            else:
                zfactor = changeFactor

            self.align_calc.zoom(self.mButtonDownLoc[0], self.mButtonDownLoc[1], zfactor)

        elif event == cv2.EVENT_LBUTTONDOWN:
            #the user pressed the left button. 
            coordsInDisplayedImage = np.array([y,x])
            coordsInFullImage = self.align_calc.ul + coordsInDisplayedImage

            if self.onLeftClickFunction is not None:
                self.onLeftClickFunction(coordsInFullImage[0],coordsInFullImage[1])
        
    def redo_image(self):
        pzs = self.align_calc
        
        cv2.imshow(self.screen_name, self.img[pzs.ul[0]:pzs.ul[0]+pzs.shape[0], pzs.ul[1]:pzs.ul[1]+pzs.shape[1]])

class align_calc(object): # Mathematical calculations for panning and zooming of a sandbox vizualization. Also creates a widget to show the bounds of an image in the top left corner. 
    
    MIN_SHAPE = np.array([50,50])
    
    def __init__(self, imShape, parentWindow):
        self.ul = np.array([0,0]) #upper left of the zoomed rectangle (expressed as y,x)
        self.imShape = np.array(imShape[0:2])
        self.shape = self.imShape #current dimensions of rectangle        
        self.parentWindow = parentWindow

    def zoom(self,rel_cy,rel_cx,zfactor):
        self.shape = (self.shape.astype(np.float)/zfactor).astype(np.int)
        self.shape[:] = np.max(self.shape) 
        self.shape = np.maximum(align_calc.MIN_SHAPE,self.shape) #prevent zooming in too far
        c = self.ul+np.array([rel_cy,rel_cx])
        self.ul = c-self.shape/2
        self.bounds_redo_image()


    def bounds_redo_image(self): #Prevents user from zooming outside the image. Also draws the present rectangular bound of the vizualization in the widget. 
        
        self.ul = np.maximum(0,np.minimum(self.ul, self.imShape-self.shape))
        self.shape = np.minimum(np.maximum(align_calc.MIN_SHAPE,self.shape), self.imShape-self.ul)
        yFraction = float(self.ul[0])/max(1,self.imShape[0]-self.shape[0])
        xFraction = float(self.ul[1])/max(1,self.imShape[1]-self.shape[1])
        self.parentWindow.redo_image()


    def setYAbsoluteOffset(self,yPixel):
        self.ul[0] = min(max(0,yPixel), self.imShape[0]-self.shape[0])
        self.bounds_redo_image()


    def setXAbsoluteOffset(self,xPixel):
        self.ul[1] = min(max(0,xPixel), self.imShape[1]-self.shape[1])
        self.bounds_redo_image()


    def setYFractionOffset(self,fraction): # pans the rectangle in the widget based on the location in Y direction 
        
        self.ul[0] = int(round((self.imShape[0]-self.shape[0])*fraction))
        self.bounds_redo_image()


    def setXFractionOffset(self,fraction): # pans the rectangle in the widget based on the location in X direction 
        
        self.ul[1] = int(round((self.imShape[1]-self.shape[1])*fraction))
        self.bounds_redo_image()





if __name__ == "__main__":
    
    vid_loc = os.getcwd() + "/SimpleFoam/sim.avi"
    p1 = 0 # Initializing the two variables storing time for when the sim ogv file is changed. 
    p2 = 0 

    while (os.path.exists(vid_loc)==True): # Checks if the simulation file exists or not.

        p1 = float("%0.2f"%os.path.getctime(vid_loc)) # Getting initial time when the sim ogv file was last changed
        pygame.init() # initializing pygame object
        infos = pygame.display.Info() #Display info of current machine's screen
        screen_size = (infos.current_w, infos.current_h)
        cap = cv2.VideoCapture(vid_loc) # Reading in the sim ogv file.
        frame_counter =0 # Initializing a counter for displaying the sim ogv file frame by frame.
        
        while(True): #Infinite while loop
                               
                ret, frame = cap.read() #Dividing up the video in every frame and initializing the cap object.
                                
                frame_counter += 1 # Increments of counter for every frame. 
                print (frame_counter)

                if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT): # If condition to check if the frame has reached its end or not. 
                    frame_counter = 0  # Counter becomes zero if sim.ogv has reached its end.
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

                frame= cv2.resize(frame,screen_size)               
                key= cv2.waitKey(3000)   # Every frame is displayed for 2 seconds each. 
                p2 = float("%0.2f"%os.path.getctime(vid_loc)) # The time for last change in sim ogv file is checked while displaying every frame.
                if (p1 != p2) == True:#If condition for comparing time of edit of sim ogv file. If they are not the same means that file has updated   

                    #cv2.waitKey(2000) &       
                    
                    break 
          
                if key == ord('p'):            # Condition to pause currently running sim.ogv. Press P !
                    while True:
                        key2 = cv2.waitKey(1000000) or 0xff
                        
                        if key2 == ord('p'):
                            break

                if key == ord('q'):            # Condition for quitting the currently running the video. Press Q ! 
                    sys.exit()
                
                window = align_gui(frame, "Sandbox Alignment")
                



    
