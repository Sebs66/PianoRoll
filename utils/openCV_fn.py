import cv2
import os
import pathlib
import numpy as np
from PIL import Image, ImageTk, ImageEnhance
import shutil
import time
if __name__ == '__main__':
    from various import sorted_alphanumeric
else:
    from utils.various import sorted_alphanumeric

def eraseFilesinDataFolder(path):
    data_path = pathlib.Path(path).parent.joinpath('data')
    if not os.path.exists(data_path):
        return
    shutil.rmtree(data_path)

# Read the video from specified path
def takeFramesV2(videoPath:str,frameInterval:int,pictureLimit=float('inf')):
    '''
    Version2. Es más rápido ya que adelantamos en intervalos para sacar cada foto.\n
    videoPath: path of video file.\n
    frameInterval: N° frames between two screenshots\n
    pictureLimit: Qty of shots taken. If undefined, will take shots until the end of the video.
    '''
    t0 = time.time()
    eraseFilesinDataFolder(videoPath)
    parentFolder = pathlib.Path(videoPath).parent
    os.chdir(parentFolder)    
    try:
        # creating a folder named data
        if not os.path.exists('data'):
            os.makedirs('data')
        # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')

    cam = cv2.VideoCapture(str(videoPath))
    # frame
    currentframe = 0
    totalCaptures = 0
    nextFrame = 0
    lastImg = 0
    i = int(1)
    fileList = []
    while (totalCaptures < pictureLimit):
        ret, frame = cam.read() # Grabs, decodes and returns the next video frame. Returns false if no frames has been grabbed
        # Ret is the return value true or false, frame is a numpy.ndarray of the frame.
        if ret: # ret can be true or false.
            nextFrame += frameInterval #/ Vamos saltando frames según nuestro frameInterval.
            namePath = './data/'+str(i)+'__frame' + str(currentframe) + '.jpg'
            i+=1
            # writing the extracted images
            cv2.imwrite(namePath, frame)
            print(f'Capturing a new frame. N°:{i}')
            totalCaptures += 1 #/ Solo contamos si son diferentes!
            fileList.append(namePath)
            cam.set(1,nextFrame) #/ Adelantamos la captura al siguiente frame segun intervalo!
            # show how many frames are createdpython show image until user input
            currentframe += 1
        else:
            break    
    # Release all space and windows once done
    print('totalCaptures: ',totalCaptures)
    cam.release()
    cv2.destroyAllWindows()
    print('takeFramesV2()')
    print(f'Total Time: {int((time.time() - t0)/60):02}:{int((time.time() - t0)%60):02}')
    return fileList    

def takeFrames(videoPath:str,frameInterval:int,pictureLimit=float("inf")):
    t0 = time.time()
    print('takeFrames()')
    '''
    videoPath -> path del video; 
    frameInterval -> Cada cuantos frames sacamos 1 foto; 
    pictureLimit -> Cuantas fotos sacamos. Si no lo especificamos saca hasta que se acabe el video.
    '''
    #/ First remove all content of data folder.
    eraseFilesinDataFolder(videoPath)
    parentFolder = pathlib.Path(videoPath).parent
    os.chdir(parentFolder)
    print(os.getcwd())
    try:
        # creating a folder named data
        if not os.path.exists('data'):
            os.makedirs('data')
    
        # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')

    cam = cv2.VideoCapture(str(videoPath))
    # frame
    currentframe = 0
    totalCaptures = 0
    frameIndex = 0
    lastImg = 0
    i = int(0)
    fileList = []
    while (totalCaptures < pictureLimit):
        ret, frame = cam.read() # Grabs, decodes and returns the next video frame. Returns false if no frames has been grabbed
        # Ret is the return value true or false, frame is a numpy.ndarray of the frame.
        if ret: # ret can be true or false.
            frameIndex += 1 #/ Vamos saltando frames según nuestro frameInterval.
            # if video is still left continue creating images
            if frameIndex == frameInterval:
                #/ Comparamos frames.
                i = i + 1
                namePath = './data/'+str(i)+'__frame' + str(currentframe) + '.jpg'
                # writing the extracted images
                cv2.imwrite(namePath, frame)
                print(f'Capturing a new frame. N°:{totalCaptures}')
                #if lastImg != 0:
                    #
                    #error = comparingImgs(namePath,lastImg)
                    #if error <1:
                    #    #/ Las imagenes son muy parecidas (identicas), por lo que borramos la ultima de las 2.
                    #    os.remove(lastImg)
                    #else:
                    #    totalCaptures += 1 #/ Solo contamos si son diferentes!
                    #    fileList.append(namePath)
                totalCaptures += 1 #/ Solo contamos si son diferentes!
                fileList.append(namePath)
                frameIndex = 0 # Reiniciamos el contador de frames.
                lastImg = namePath
                #print('Total frames Captured',totalCapture,' frame N°',currentframe,'/',frame_count)
            # increasing counter so that it will
            # show how many frames are createdpython show image until user input
            currentframe += 1
        else:
            break    
    # Release all space and windows once done
    print('totalCaptures: ',totalCaptures)
    cam.release()
    cv2.destroyAllWindows()
    print('takeFrames()')
    print(f'Total Time: {int((time.time() - t0)/60):02}:{int((time.time() - t0)%60):02}')
    return fileList

def comparingImgs(imgPath2,imgPath1):
    #print(f'comparing {imgPath1},{imgPath2}')
    img1 = cv2.imread(imgPath1)
    img2 = cv2.imread(imgPath2)
    img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    error = mse(img1, img2)
    return error

def mse(img1, img2):
   h, w = img1.shape
   diff = cv2.subtract(img1, img2)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
   return mse

def cutImageByHeight(imgPath:pathlib.Path,height:int,finalPath:pathlib.Path):
    print(str(imgPath))
    image = cv2.imread(str(imgPath))
    cut_height = int(height) # Cut the image at a certain height
    image = image[:cut_height]
    print(str(finalPath))
    cv2.imwrite(str(finalPath), image) # Save.
    return finalPath

class VideoClass:
    def __init__(self,path:str):
        self.filename = path.split('/')[-1]
        self.path = path
        cap = cv2.VideoCapture(path)
        self.fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
        self.frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.frame_count/self.fps
    
    def get_first_img(self):
        cam = cv2.VideoCapture(self.path)
        ret, frame = cam.read()
        print(ret)
        destination = str(pathlib.Path(self.path).parent.joinpath('Cover.jpg'))
        if ret: # ret can be true or false.
            # writing the extracted images
            cv2.imwrite(destination, frame)
            cv2.destroyAllWindows()
        return destination

def resize_Image(image, maxsize):
    r1 = image.size[0]/maxsize[0] # width ratio
    r2 = image.size[1]/maxsize[1] # height ratio
    ratio = max(r1, r2)
    newsize = (int(image.size[0]/ratio), int(image.size[1]/ratio)) # keep image aspect ratio
    image = image.resize(newsize, Image.ANTIALIAS)
    return image

def crop(image:np.ndarray,height:int):
    """ Receives an np.ndarray representation of an Image and returns it upper part based on the height parameter."""
    image = image[0:height,0:]
    #imagen2 = imagen[height:imagen.shape[0],0:imagen.shape[1]]
    return image

def mergeImgs(video_path:str,image0:str,cropHeight:int,overlapHeight:int):
    '''
    This function will take the frames of a video and return a full image of the frames.
    each frame will be cropped by the cropHeight and stick toguether acording to the overlapHeight.
    '''
    print('mergeImgs')
    #/ Tenemos que volver atomar todos los frames esta vez!
    data_path = pathlib.Path(video_path).parent.joinpath('data')
    files = [str(file) for file in data_path.iterdir()]

    files = sorted_alphanumeric(files)
    print('image0',image0)
    final_img = cv2.imread(str(image0))
    image0 = str(image0).split('\\')[-1]
    print(image0)
    start = False
    for imagePath in files:
        if image0 in imagePath:
            start = True
            continue
        if start == False:
            continue
        #/ To here only if image is after or equal to image0.
        img = cv2.imread(imagePath)
        cropped_img = crop(img,cropHeight)
        cropped_img = cropped_img[0:overlapHeight,:]
        #print(cropped_img)
        final_img = np.concatenate((cropped_img,final_img), axis=0)
    
    file_path = f'{str(pathlib.Path(video_path).parent)}\\FullImage.png'
    cv2.imwrite(file_path,final_img)
    print(f'Full image saved at: {file_path}')
    return file_path


if __name__ == '__main__':
    path = 'E:\Media\HDPiano\Zoe Wees\Control - Full song.mkv'
    image0 = r'E:\\Media\\HDPiano\\Zoe Wees\\data\\12__frame11.jpg'
    Ycoord = int(484.65)
    overlap = 246
    mergeImgs(path,image0,Ycoord,overlap)
