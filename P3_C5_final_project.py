import zipfile

from PIL import Image, ImageDraw
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
#openfile
def text_face_rec(t_input):
    print('''Processing...It may take a couple of minutes before you can see all the outcomes.''')
    file = 'readonly/images.zip'
    z_file = zipfile.ZipFile(file, 'r')
    file_names = [file.filename for file in z_file.infolist()]
    for i in range(len(file_names)):
        with z_file.open(file_names[i]) as myfile:
            img = Image.open(myfile)
            img = img.convert("RGB")
# word recogniton and output
        t_str = pytesseract.image_to_string(img)
        if '{}'.format(t_input.lower()) in t_str.lower():
            print('"{}" found in {}'.format(t_input, file_names[i]))
        else:
            print('No text "{}" can be found in {}'.format(t_input, file_names[i]))

# Face recognition
        c_faces = []
        faces = face_cascade.detectMultiScale(np.array(img), 1.3)
        drawing=ImageDraw.Draw(img)
        for x,y,w,h in faces:
            bound_box = (x,y,w,h)
            c_v = img.crop((x,y,x+w,y+h))
            c_v = c_v.resize((200,200))
            c_faces.append(c_v)
        contact_sheet = Image.new(img.mode, (200 * 5, 200 * 2))
        x = 0
        y = 0
        if len(c_faces) != 0:
            print('{} faces detected in {}'.format(len(c_faces), file_names[i]))
        try:
            first_image=c_faces[0]
            for f in c_faces:
                contact_sheet.paste(f, (x, y))
                if x+first_image.width == contact_sheet.width:
                    x=0
                    y=y+first_image.height
                else:
                    x=x+first_image.width
            display(contact_sheet)
        except:
            print('No faces found in {}'.format(file_names[i]))



word = input("Please enter a word (e.g. Mark)\n")
text_face_rec(word)
