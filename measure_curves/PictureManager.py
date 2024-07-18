from constants import *

# FD. take_Pic()
# purp. Take a picture of a specimens by saving the display in the images folder
def takePic(surface,savePath):
    def contains_numeric(s):
        num = ""
        if any(char.isdigit() for char in s):
            for char in s:
                if char.isdigit():
                    num += char
            return int(num)
        return 0
    
    # Navigate the dir images and determine the next item in the sequence
    def getFileName(path):
        # get a list of the items in the dir
        files = os.listdir(path)
        files = [x.split(".")[0] for x in files]
        files = [contains_numeric(x) for x in files]
        if len(files)>0:
            maxFileNum = max(files)
            nextDigit = maxFileNum+1
        else:
            nextDigit = 0
        totalDigits = len(str(nextDigit))
        finalName = ["0" for _ in range(6-totalDigits)]
        finalName = "".join(finalName)+ str(nextDigit) + ".png"
        finalName = jn(path,finalName)
        # print(finalName)
        # print(os.path.exists(finalName))
        return (finalName)
        
        
    new_path = os.path.split(savePath)[0]
    if not os.path.exists(jn(new_path,"images")):
        os.mkdir(jn(new_path,"images"))
    savePicPath = jn(new_path,"images")
    # os.startfile(savePicPath)
    pygame.image.save(surface, getFileName(savePicPath))