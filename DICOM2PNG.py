import pydicom
import matplotlib.pyplot as plt
from pydicom.data import get_testdata_file
import numpy as np
from PIL import Image
import json
import os

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"
def convert_dicom(path,image_name='image',save_metadata=False,show_image=False,show_metadata=False):
    
    dc = pydicom.dcmread(path)

    image_data = dc.pixel_array
    img = Image.fromarray(image_data)

    my_dicom_file={}

    if save_metadata:
        for data in dc:
            if data.name!="Pixel Data":
                my_dicom_file[data.name]=str(data.value)
            else:
                my_dicom_file[data.name]=str(dc.pixel_array.shape)

        if show_metadata:
            for i in my_dicom_file:
                print("================================================================================")
                if i!="Pixel Data":
                    print(i+":","\n\t\t\t\t",my_dicom_file[i])
                else:
                    print(i+":","\n\t\t\t\t","Bit Depth of the Picture:",dc['BitsStored'].value,"Bit","("+str(np.power(2,dc['BitsStored'].value))+" Colors)")
                    print("\t\t\t\t Size of the picture:",my_dicom_file[i])
            print("================================================================================")

        with open(image_name+'.json', 'w') as f:
            json.dump(my_dicom_file, f)
        print("================================================================================")
        print("json",image_name+".json","has been saved Successfully!")
        

    # save image
    ar = dc.pixel_array

    min_val = np.min(ar)
    max_val = np.max(ar)

    normalized_numbers = (ar - min_val) / (max_val - min_val) * 255

    ar8 = normalized_numbers.astype(np.uint8)
    im = Image.fromarray(ar8) 
    im.save(image_name+".png")
    if show_image:
        plt.imshow(im ,cmap=plt.cm.grey)
        plt.show()
    print("image",image_name+".png","has been saved Successfully!")

print()
file_path=None
save_metadata = False
while(True):
    print(GREEN+"Please Enter the location of the folder that contains DICOM files or enter the location of DICOM file.")
    print(GREEN+"NOTE: if the Folder is the same as the tool's Folder, then just press enter.")
    file_path = input(GREEN+"Folder location: ")
    if file_path == "":
        file_path = "./"
    if os.path.exists(file_path):
        user_input = input(GREEN+"do you want to save the metadata as json file?(y/N):")
        save_metadata = user_input.lower()=='y'
        print(RESET)
        break
    else:
        print(RED+"============================================================================")
        print(RED+"the Folder location you entered doesn't exist, please enter a correct one!")
        print(RED+"============================================================================"+RESET)


if os.path.splitext(file_path)[1] == ".dcm":
    directory_path = os.path.dirname(file_path)
    file_name=os.path.splitext(file_path)[0]
    convert_dicom(path=file_path, save_metadata=save_metadata,image_name=file_name)
    print(GREEN+"============================================================================")
    print(GREEN+"conversion has been done Successfully!")
    print(GREEN+"Image is stored in same folder you choosed.")
    print(GREEN+"============================================================================"+RESET)

else:
    if file_path[-1] !="/":
        file_path = file_path+"/"
    files = os.listdir(file_path)
    os.makedirs(file_path+"images",exist_ok=True)
    for file in files:
        if os.path.splitext(file)[1] == ".dcm":
            file_full_name=file_path+"images/"+os.path.splitext(file)[0]
            convert_dicom(path=file_path+file, save_metadata=save_metadata,image_name=file_full_name)
    print(GREEN+"============================================================================")
    print(GREEN+"conversion has been done Successfully!")
    print(GREEN+"Images are stored in folder \"images\" in the folder you choosed")
    print(GREEN+"============================================================================")
print(RESET)

