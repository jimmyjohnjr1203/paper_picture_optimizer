import numpy as np
import cv2 as cv
from os import listdir, remove
from os.path import join, isfile, normpath
from tkinter import *
from tkinter import filedialog
from tkinter import ttk


# define optimize function
def optimize(*args):
    
    start_button.state(['disabled'])
    test = False
    try:
        file_path = normpath(input_path)
        if file_check.instate(['selected']):
            file_list = file_path
        elif folder_check.instate(['selected']):
            file_list = [join(file_path, f) for f in listdir(file_path) if isfile(join(file_path, f))]
            file_name_start = file_path
            print(file_path)
            folder_name = file_path.rpartition('\\')[2]
            print(folder_name)
        else:
            test = True
            test_folder = "C://Users//jackl//OneDrive//Pictures//picture_editor_test"
            file_list = [join(test_folder, f) for f in listdir(test_folder) if isfile(join(test_folder, f))]
    except:
        choosetype.set('Choose File')
        file_list = []

    index = 1
    new_list = []
    for path in file_list:
        if test == False:
            if '_page' in path:
                print('There was an image alredy modified')
                index += 1
            else:
                new_list.append(path)
        else:
            if '_final' in path:
                index += 1
            else:
                new_list.append(path)
    for path in new_list:
        if path.endswith(".jpg") or path.endswith(".png") or path.endswith(".jpeg"):
            # load image
            img = cv.imread(path)
            #original_width = np.size(img, 1)
            #original_height = np.size(img, 0)
            # convert to gray for better cropping
            gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            # apply ClAHE to gray for better cropping of non-black backgrounds
            gray = cv.equalizeHist(gray)
            gray_brighter = gray>127
            # crop from top and bottom
            row_check = np.any(gray_brighter,1)
            img = img[row_check]
            # crop from left and right
            column_check = np.any(gray_brighter,0)
            img = img[:,column_check]
            #cv.imshow('cropped image', img)
            # credit for next part: Jeru Luke on stack overflow
            #-----Converting image to LAB Color model----------------------------------- 
            lab= cv.cvtColor(img, cv.COLOR_BGR2LAB)

            #-----Splitting the LAB image to different channels-------------------------
            l, a, b = cv.split(lab)

            #-----Applying CLAHE to L-channel-------------------------------------------
            clahe = cv.createCLAHE(clipLimit=1.0, tileGridSize=(16,16))
            cl = clahe.apply(l)

            #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
            limg = cv.merge((cl,a,b))

            #-----Converting image from LAB Color model to RGB model--------------------
            img = cv.cvtColor(limg, cv.COLOR_LAB2BGR)
            # end credit
            # credit Soroush on Stack Overflow
            '''
            def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=3.0, threshold=5):
                """Return a sharpened version of the image, using an unsharp mask."""
                blurred = cv.GaussianBlur(image, kernel_size, sigma)
                sharpened = float(amount + 1) * image - float(amount) * blurred
                sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
                sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
                sharpened = sharpened.round().astype(np.uint8)
                if threshold > 0:
                    low_contrast_mask = np.absolute(image - blurred) < threshold
                    np.copyto(sharpened, image, where=low_contrast_mask)
                return sharpened
            # end credit
            img = unsharp_mask(img)
            '''
            contrast = 1.7
            brightness = -80
            img = cv.convertScaleAbs(img, alpha=contrast, beta=brightness)
            # save image in renamed file
            if test == False:
                new_name = file_name_start + '\\' + folder_name + "_page" + str(index) + ".jpg"
                print(new_name)
                cv.imwrite(new_name, img)
                #remove(path)
                index += 1
            else:
                #print(str(np.shape(img)))
                cv.imshow('final', img)
                cv.imwrite(path.strip(".jpg")+'_final.jpg', img)
                #cv.imshow('grayscale final', gray)
                if cv.waitKey(0) & 0xff == 27:
                    cv.destroyAllWindows()
        else: 
            print ("There was a folder or an invalid file in your directory")
    if len(file_list) != 0:
        finished.set('Done!')
    start_button.state(['!disabled'])

def choose_folder(*args):
    global input_path
    if file_check.instate(['selected']):
        input_path = filedialog.askopenfilename(title = 'Choose an item')
        choosetype.set('Press Start')
    elif folder_check.instate(['selected']):
        input_path = filedialog.askdirectory(title = 'Choose a folder')
        choosetype.set('Press Start')
    elif test_check.instate(['selected']):
        input_path = None
        choosetype.set('Press Start')
    else:
        choosetype.set('Choose type first!')

def set_empty_path(*args):
    global input_path
    input_path = None
    choosetype.set('Press Start')
# begin gui window
root = Tk()
root.title('Paper Picture Optimizer')
mainframe = ttk.Frame(root, padding = '3 3 12 12')
mainframe.grid(column = 0, row = 0, sticky = 'N W E S')
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)


fileorfolder = StringVar()
#input_path = StringVar()
finished = StringVar()
choosetype = StringVar()
#fileorfolder_entry = ttk.Entry(mainframe, width = 10, textvariable = fileorfolder)
#fileorfolder_entry = ttk.Checkbutton(mainframe, text='Folder?', variable = fileorfolder, onvalue = 'Folder', offvalue = 'File')
file_check = ttk.Radiobutton(mainframe, text = 'File', variable = fileorfolder, value = 'File')
folder_check = ttk.Radiobutton(mainframe, text = 'Folder', variable = fileorfolder, value = 'Folder')
test_check = ttk.Radiobutton(mainframe, text = 'Test', variable = fileorfolder, value = 'Test', command = set_empty_path)
folder_check.state(['selected'])
file_check.grid(column = 1, row = 1)
folder_check.grid(column = 2, row = 1)
test_check.grid(column = 3, row = 1)

#path_entry = ttk.Entry(mainframe, width = 20, textvariable = input_path)
path_entry_button = ttk.Button(mainframe, text = ' Choose item to Optimize ', command = choose_folder)
path_entry_button.grid(column = 2, row = 2, sticky = (W, E))
start_button = ttk.Button(mainframe, text = 'Start', command = optimize)
start_button.grid(column = 3, row = 3, sticky = (W, E))
ttk.Label(mainframe, textvariable = finished).grid(column = 1, row = 3, sticky = (W, E))
ttk.Label(mainframe, textvariable = choosetype).grid(column = 3, row = 2, sticky = (W, E))

#ttk.Label(mainframe, text = 'File(0) or Folder(1) or Test(2)').grid(column = 1, row = 1, sticky = W)
#ttk.Label(mainframe, text = 'File/Folder path:').grid(column = 1, row = 2, sticky = W)
for child in mainframe.winfo_children(): child.grid_configure(padx = 5, pady = 5)
#fileorfolder_entry.focus()
root.bind('<Return>', optimize)

root.mainloop()
