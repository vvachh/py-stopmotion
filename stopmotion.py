import cv2, imageio
import sys,os


def wait_for_frame(prev_frame, wname, cap, size):
    '''
    onionskin prev_frame while displaying 
    '''
    key=1
    while key not in [13,27]:
        key = cv2.waitKey(7)
        ret,im = cap.read()
        # display the current frame with the prev_frame onionskinned
        im2 = cv2.addWeighted(prev_frame,0.5, im, 0.5,0)
        cv2.imshow(wname, cv2.resize(im2,size))
    exp=5
    imret = longExp(cap, exp)
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
    size= (im0.shape[1]//4, im0.shape[0]//4)
    key=1
    counter=0
    while key != 27:
        im0,key = wait_for_frame(im0,wname,cap,size)
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
    cap = cv2.VideoCapture(captureDevice)
    saveFrames('stupid Python stop motion', cap, direc)
    if savegif:
        saveMovie(direc)
