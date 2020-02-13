import freenect
import cv2
import numpy as np
import time 
from stl_tools import numpy2stl
import os
import subprocess
import getpass
import sys
import glob
import shutil

import struct
import fileinput
import scipy.linalg
import scipy.optimize

import time

username = getpass.getuser()

# Paths for location for storing stl file and blockmesh dict to update stl file coordinates. 

stl_loc = os.getcwd() + "/SimpleFoam/constant/triSurface/depth_img.stl"
ctrl_loc = os.getcwd() + "/SimpleFoam/system/blockMeshDict"
iter_loc = os.getcwd() + "/SimpleFoam/system/controlDict"
bx_txt = os.getcwd() + "/BoxLayout.txt"
abl_loc = os.getcwd() + "/SimpleFoam/0/include/ABLConditions"
# Paramaters for plane for bounding box of the sandbox. 
PLANE_PARAMS = [-0.045925, 0.076807, 724.000000] #to be modified slightly for a specific system. Check Logs when running this code. 


################################################ KINECT FUNCTIONS #########################################

def get_depth():  #Function for getting the depth image from Kinect. 
    array,_ = freenect.sync_get_depth()
    #array = array.astype(np.uint8)
    return array
def ms_error(imageA, imageB): # Function for calculating the Mean Square Error of 
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err
def get_video(): # Function for getting a frame of RGB image from Kinect. 
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array



####################################CALIBRATION FUNCTIONS########################################################## 
def plane(x, y, params):
    #plane equation for slope subtraction
    a = params[0]
    b = params[1]
    c = params[2]
    z = a*x + b*y + c
    return z

"""Error function for fitting the planar parameters"""
def error(params, points):
    result = 0
    for (x,y,z) in points:
        plane_z = plane(x, y, params)
        diff = abs(plane_z - z)
        result += diff**2
    return result


def ar_calibration(fname=bx_txt):     # Read in the boxlayout.txt Calibration File
    f = open(fname,'r')
    lines = f.readlines()
    plane = lines[0].split('(')[1].split(')')[0].split(',')
    plane = np.array(plane,dtype=float)
    factor = 724./float(lines[0].split(')')[1].split(',')[1])
    vertices = []
    for k in range(1,len(lines)-1):
        l = lines[k]
        if len(l)>1:
            d = l.strip('(')
            d = d.strip(')')[:-2]
            data = d.strip().split(',')
            x = float(data[0])
            y = float(data[1])
            z = float(data[2])*factor
            vertices.append((x,y,z))
    f.close()

    #return the vertices of the 'good' boundary

    a = plane[0]#factor
    b = plane[1]#*factor
    c = 724.
    #Z = a*X + b*Y + c
    shp = np.zeros( (480,640) )
    bounds = [vertices[1][0],vertices[0][0],vertices[2][1],vertices[1][1]]
    bounds = [40,-30,30,-30]
    
    return generate_baseplane((a,b,c),shp[bounds[0]:bounds[1], bounds[2]:bounds[3]].shape), bounds


def calibrate(surface,baseplane,bounds): #scaling, setting zero point, removing dead pixels, and trimming edges
    
    surface = surface.astype('float32')   
    surface = surface[bounds[0]:bounds[1], bounds[2]:bounds[3]] - baseplane
    BAD_PIX = np.where(surface>=200)
    surface[BAD_PIX] = 0.#np.nan
    return np.nan_to_num(surface), BAD_PIX

def generate_baseplane(params,shape=(640,480)): # Get baseplane for calibration from boxlayout.txt
    X,Y = np.meshgrid(np.arange(0,shape[1]), np.arange(0,shape[0]))
    XX = X.flatten()
    YY = Y.flatten()
    Z = params[0]*X + params[1]*Y + params[2]
    return Z


def update_surface(baseplane,bounds,prev=None,FLOOR=-500):
    """Read updated topography and calibrate for use"""
   
    d = []
    for i in range(10):
        depth= get_depth()
        d.append(depth)
        
    #time average the readings to reduce noise
    #currently taking mean, maybe switch to median
    depth = np.median(d[::],axis=0)#/10.
    topo,pix = calibrate(depth,baseplane,bounds)

    return topo- np.nanmedian(topo)

############################################### MISC FUNCTIONS ##########################################

#Finding dimensions for the stl file to be pasted in controldict in openfoam. 
def iter_calc_bounding(filename):
    with open(filename,'rb') as f:
        Header = f.read(80)
        nn = f.read(4)
        Numtri = struct.unpack('i', nn)[0]
        record_dtype = np.dtype([
            ('Normals', np.float32, (3,)),
            ('Vertex1', np.float32, (3,)),
            ('Vertex2', np.float32, (3,)),
            ('Vertex3', np.float32, (3,)),
            ('atttr', '<i2', (1,)),
        ])
        xmax = -9999
        xmin = 9999
        ymax = -9999
        ymin = 9999
        zmax = -9999
        zmin = 9999
        for i in range(0, Numtri, 1):
            d = np.fromfile(f, dtype=record_dtype, count=1)
            v1 = d['Vertex1']
            v2 = d['Vertex2']
            v3 = d['Vertex3']
            v = np.hstack(((v1[:, np.newaxis, :]), (v2[:, np.newaxis, :]), (v3[:, np.newaxis, :])))
            x = v[..., 0].flatten()
            y = v[..., 1].flatten()
            z = v[..., 2].flatten()
            tmp_xmin = x.min()
            tmp_xmax = x.max()
            tmp_ymin = y.min()
            tmp_ymax = y.max()
            tmp_zmin = z.min()
            tmp_zmax = z.max()
            xmax = max((tmp_xmax, xmax))
            xmin = min((tmp_xmin, xmin))
            ymax = max((tmp_ymax, ymax))
            ymin = min((tmp_ymin, ymin))
            zmax = max((tmp_zmax, zmax))
            zmin = min((tmp_zmin, zmin))
    
    return (xmin, xmax, ymin , ymax, zmin , zmax)




def file_mod (ctrl_dict,pattern,value=""): # Function to update the BlockMeshDict with STL dimensions. 

    fh=fileinput.input(ctrl_dict,inplace=True)  
    for line in fh: 
        if pattern in line and line.startswith(pattern) :
                replacement= pattern + value + " ;"              
                sys.stdout.write(replacement+'\n')  
        else: 
            sys.stdout.write (line)
    fh.close()  

########################################### MAIN TO RUN APP ##########################################

if __name__ == "__main__":  


    try:       
        depth_pre = np.empty([360,640])
         
              
        while(True):                  
            
            baseplane, bounds = ar_calibration()
            depth = update_surface(baseplane,bounds,None)
            cols = list(np.shape(depth))
            depth = np.delete(depth,np.s_[cols[1] -30:cols[1]],axis=1)  
            depth = cv2.resize(depth,(640,360))  # 480  
                      
            mse = ms_error(depth,depth_pre)
            print(mse)
            if (mse  >400):
                cap = cv2.VideoCapture(os.getcwd()+'/timer.mp4')         
                frame_counter =0
                while(cap.isOpened()):
                    ret, frame = cap.read()
                    frame_counter += 1
                    cv2.imshow('timer',frame)
                    if cv2.waitKey(27) & 0xFF == ord('q'):
                        break
                    if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                          break 

                cap.release()
                cv2.destroyAllWindows() 
                
                

            if (mse>5 and mse< 400):          
                stl = numpy2stl(depth,os.getcwd()+"/SimpleFoam/constant/triSurface/depth_img.stl",   scale=1.5,solid=False)          


                folder_names = []
                orij_dir = ['constant','system','0']
                for entry_name in os.listdir(os.getcwd()+'/SimpleFoam/'):
                    entry_path = os.path.join(os.getcwd()+'/SimpleFoam/',entry_name)
                    if os.path.isdir(entry_path):
                        folder_names.append(entry_name) 

                for i in folder_names: 
                    if i not in orij_dir:
                       f = os.path.join(os.getcwd()+'/SimpleFoam/'+i)
                       shutil.rmtree(f)

                config={}
                with open("config") as f:
                    for line in f:
                        (key, val) = line.split(':')
        
                        config[key] = val.rstrip('\n')

                stl_cor = iter_calc_bounding(stl_loc)
                file_mod(ctrl_loc,"xMin ",str(stl_cor[0]))
                file_mod(ctrl_loc,"xMax ",str(stl_cor[1]))
                file_mod(ctrl_loc,"yMin ",str(stl_cor[2]))
                file_mod(ctrl_loc,"yMax ",str(stl_cor[3]))
                file_mod(ctrl_loc,"zMin ",str(stl_cor[4]-100))
                file_mod(ctrl_loc,"zMax ",str(stl_cor[5]+100))
                file_mod(abl_loc, "zGround uniform ",str(stl_cor[0]))
                file_mod(abl_loc, "Uref", config['Uref'])
                file_mod(abl_loc, "Zref", config['Zref'])
                file_mod(abl_loc, "z0", config['z0'])
       
                file_mod(ctrl_loc, "xCells", config['xCells'])
                file_mod(ctrl_loc, "yCells", config['yCells'])
                file_mod(ctrl_loc, "zCells", config['zCells'])
               
                subprocess.call(['bash '+ os.getcwd() + "/SimpleFoam/simplefoam"],shell=True) #Running openfoam through a bash script. 
                sim_update =  cv2.imread(os.getcwd()+"/sim_updated.jpeg")
                sim_update =  cv2.resize(sim_update,(500,500))
                cv2.namedWindow('standby',cv2.WINDOW_NORMAL)
                cv2.resizeWindow('standby', 500,500)
                cv2.imshow('standby', sim_update)               
                cv2.waitKey(5000)
                cv2.destroyAllWindows()
                
        
                depth_pre = depth # Reassign this depth as previous depth for mse comparision
            time.sleep(2) # Rerun the loop every second or whenever SimpleFoam is finished.  

    except KeyboardInterrupt:
        pass   
