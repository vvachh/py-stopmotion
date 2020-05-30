import cv2, imageio
import sys,os,io
import gphoto2 as gp
from PIL import Image
import numpy as np

def wait_for_frame(prev_frame, wname, cap, size):
    '''
    onionskin prev_frame while displaying 
    '''
    key=1
    while key not in [13,27]:
        key = cv2.waitKey(7)
        ret,im = cap.read()
        im = im
        # display the current frame with the prev_frame onionskinned
        im2 = cv2.addWeighted(prev_frame,0.5, im, 0.5,0)
        cv2.imshow(wname, cv2.resize(im2,size))
    exp=5
    imret = longExp(cap, exp)
    return imret, key

def wait_for_frame_gphoto2(prev_frame, wname,cam,size):
    '''
    onionskin prev_frame while displaying 
    gphoto2 version
    '''
    key=1
    while key not in [13,27]:
        key = cv2.waitKey(7)
        camera_file = gp.check_result(gp.gp_camera_capture_preview(cam))
        file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
        im = np.array(Image.open(io.BytesIO(file_data)))[:,:,::-1]
        # display the current frame with the prev_frame onionskinned
        im2 = cv2.addWeighted(prev_frame,0.5, im, 0.5,0)
        cv2.imshow(wname, cv2.resize(im2,size))
    exp=5
    imret = im
    return imret, key

def longExp(cap,exp):
    '''
    Average exp number of frames from cap 
    because webcam feeds are very shot-noisy.
    '''
    rAvg = None
    bAvg = None
    gAvg = None
    for i in range(exp):
        ret,frame = cap.read()
        (B, G, R) = cv2.split(frame.astype("float"))
        # if the frame averages are None, initialize them
        if rAvg is None:
            rAvg = R/exp
            bAvg = B/exp
            gAvg = G/exp
        # otherwise, compute the weighted average between the history of
        # frames and the current frames
        else:
            rAvg = (rAvg) + (R)/ (exp)
            gAvg = (gAvg) + ( G) / (exp)
            bAvg = (bAvg) + (B) / (exp)
    avg = cv2.merge([bAvg, gAvg, rAvg]).astype("uint8")
    return avg
def saveFrames(wname, cap,direc):
    '''
    stupid thing trying to mimic FrameByFrame
    Save individual frames with Return, stop frame capture with Esc
    '''
    ret, im0 = cap.read()
    size= (im0.shape[1]//2, im0.shape[0]//2)
    key=1
    counter=0
    while key != 27:
        im0,key = wait_for_frame(im0,wname,cap,size)
        cv2.imwrite(os.path.join(direc,str(counter).zfill(4)+'.jpg'), im0)
        counter+=1

def saveFrames_gphoto2(wname, cam,direc):
    '''
    stupid thing trying to mimic FrameByFrame
    Save individual frames with Return, stop frame capture with Esc
    gphoto2 version--supports capture from a DSLR
    '''
    camera_file = gp.check_result(gp.gp_camera_capture_preview(cam))
    file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
    im0 = np.array(Image.open(io.BytesIO(file_data)))

    size= (im0.shape[1], im0.shape[0])
    key=1
    counter=0
    while key != 27:
        im0,key = wait_for_frame_gphoto2(im0,wname,cam,size)
        cv2.imwrite(os.path.join(direc,str(counter).zfill(4)+'.jpg'), im0)
        counter+=1


def saveMovie(direc):
    '''
    Save movie to a gif
    '''
    filenames = [i for i in os.listdir(direc) if i!='final.gif']
    with imageio.get_writer(os.path.join(direc,'final.gif'), mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(os.path.join(direc,filename))
            writer.append_data(image)

if __name__=='__main__':
    '''
    commandline usage:
    python stopmotion.py [capture device id] [directory to save files] [save gif (True/False)]
    '''
    try:
        captureDevice = int(sys.argv[1])
        direc = sys.argv[2]
        savegif = bool(sys.argv[3])
    except IndexError:
        print('Usage: python stopmotion.py [device id] [directory] [save gif (T/F)]')
    if not os.path.isdir(direc):
        os.mkdir(direc)
    if captureDevice>=0:
        cap = cv2.VideoCapture(captureDevice)
        saveFrames('stupid Python stop motion', cap, direc)
        cap.release()
    else:
        cam = gp.Camera()
        saveFrames_gphoto2('stupid Python stop motion', cam, direc)
        cam.exit()

    if savegif:
        saveMovie(direc)
