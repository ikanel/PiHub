import os
import time
import threading
from guizero import App, Text,Picture
import simpleaudio.functionchecks as fc
from PIL import ImageFile,Image,ExifTags

banner=None
picture=None


def getPicture(imageUrl):
    global picture
    basewidth = 1024
    baseheight = 768
    app = App(title="Picture")
    app.width=basewidth
    app.height=baseheight
    app.tk.attributes("-fullscreen",True)
    drawPicture(imageUrl, app)
    app.display()
    picture=None
    app=None
    return picture

def drawPicture(imageUrl,master):
    basewidth = 1024
    baseheight = 768
    global picture
    if picture is not None:
        master=picture.master
        picture.destroy()
        master.focus()
        
    pilImage = rotateByExif(Image.open(imageUrl))
    if(pilImage.size[1]>pilImage.size[0]):
            basewidth=int(float(baseheight)/float(pilImage.size[1])*float(pilImage.size[0]))
        
    wpercent = (basewidth/float(pilImage.size[0]))
    hsize = int((float(pilImage.size[1])*float(wpercent)))
    rpil = pilImage.resize((basewidth,hsize), Image.ANTIALIAS)

    picture = Picture(master,image=rpil)
    return picture
    
    

def rotateByExif(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(image._getexif().items())

        if exif[orientation] == 3:
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image=image.rotate(90, expand=True)
        
    except (AttributeError, KeyError, IndexError):
    # cases: image don't have getexif
        pass
    return image

def getBanner(text):
    
    global banner
    if banner==None:
        app = App(title="Information")
        app.width=1200
        app.height=1090
        app.tk.attributes("-fullscreen",True)
        banner=Text(app,text=text)
        banner.size=50
        banner.text_color="red"
        app.display()
        banner=None
        app=None
    return banner


def updateBanner(text):
    
    global banner
    if banner is None:
        banner=getBanner(text)

    if banner is not None:
        banner.value=text
        banner.master.focus()

def updatePicture(filename):
    global picture
    if picture is None:
        getPicture(filename)
    else:
        master=picture.master
        drawPicture(filename, master)
        

def showPicture(filename):
    focus_thread = threading.Thread(target=takeFocus,args=(False,))
    focus_thread.start()
    
    picture_thread = threading.Thread(target=updatePicture,args=(filename,))
    picture_thread.start()
    
    
def showBanner(message):
    focus_thread = threading.Thread(target=takeFocus,args=(True,))
    focus_thread.start()

    banner_thread = threading.Thread(target=updateBanner,args=(message,))
    banner_thread.start()
         

def takeFocus(withMusic):
     os.system('echo "on 0" | cec-client RPI -s -d 1')
     os.system('echo "as" | cec-client RPI -s -d 1')
     if withMusic==True:
         fc.LeftRightCheck.run()


def switchOffTv():
     os.system('echo "standby 0" | cec-client RPI -s -d 1')


def switchOnTv():
     os.system('echo "on 0" | cec-client RPI -s -d 1')
     os.system('echo "as" | cec-client RPI -s -d 1')


#showBanner("Быстро всем за уроки!!!")
#time.sleep(5)
#showBanner("Быстро всем за уроки2!!!")
#time.sleep(5)
#showBanner("Быстро всем за уроки3!!!")
#showPicture("picture.jpg")
#showImageWithViewer("picture.JPG")

#time.sleep(1)
#showPicture("picture.JPG")
#time.sleep(5)

#updatePicture("picture.jpg")
#time.sleep(5)
#showPicture("PiHubShot.jpg")
