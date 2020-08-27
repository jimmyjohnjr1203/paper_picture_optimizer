import numpy as np
import cv2
from os import listdir, remove
from os.path import join, isfile

test_folder = "test_picture.jpg"
test = True
index = 1
# ask for file/folder path to image
if test != True:
    file_or_folder = input("File(0) or Folder(1): ")
    if file_or_folder == 0:
        file_path = input("File path: ")
        file_list = file_path
    else:
        file_path = input("Folder path: ")
        file_list = [join(file_path, f) for f in listdir(file_path) if isfile(join(file_path, f))]
        file_name_start = file_path
else:
    file_list = [test_folder]
    #file_list = [join(test_folder, f) for f in listdir(test_folder) if isfile(join(test_folder, f))]

for path in file_list:
    if path.endswith(".jpg") or path.endswith(".png") or path.endswith(".jpeg"):
        # load image
        img = cv2.imread(path)
        original_width = np.size(img, 1)
        original_height = np.size(img, 0)
        # show original image
        if test == True:
            pass
            #cv2.imshow('original', img)
        # convert to gray for better cropping
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray_brighter = gray>127
        # crop from top and bottom
        row_check = np.any(gray_brighter,1)
        img = img[row_check]
        # crop from left and right
        column_check = np.any(gray_brighter,0)
        img = img[:,column_check]
        cv2.imshow('cropped image', img)
        # credit for next part: Jeru Luke on stack overflow
        #-----Converting image to LAB Color model----------------------------------- 
        lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

        #-----Splitting the LAB image to different channels-------------------------
        l, a, b = cv2.split(lab)

        #-----Applying CLAHE to L-channel-------------------------------------------
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(16,16))
        cl = clahe.apply(l)

        #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
        limg = cv2.merge((cl,a,b))

        #-----Converting image from LAB Color model to RGB model--------------------
        img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        # end credit
        contrast = 2
        brightness = -100
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
        # save image in renamed file
        if test == False:
            cv2.imwrite(file_name_start + "_page" + str(index), img)
            remove(path)
            index += 1
        else:
            #print(str(np.shape(img)))
            cv2.imshow('final', img)
            cv2.imwrite(path+'.jpg', img)
            #cv2.imshow('grayscale final', gray)
            if cv2.waitKey(0) & 0xff == 27:
                cv2.destroyAllWindows()
    else: 
        print ("There was a folder or an invalid file in your directory")
