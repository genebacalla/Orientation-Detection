import cv2 
import math
import numpy as np 
from imutils.paths import list_images
import time


class OrientationDetection:

    def __init__(self):
       self.process_time = 0
       self.base_scale = 5
       self.scale_increment = 5
       self.blurStrength = 0.5
       self.cannyTreshold1 = 50
       self.cannyTreshold2 = 100
       self.houghTreshold = 10
       self.minHoughLineLength = 1
       self.maxHoughLineGap = 1

    def _rescaleImage(self, image, scale):
        height, width,_ = image.shape
        new_width = int(width * scale/100)
        new_height = int(height * scale/100)

        resized_image = cv2.resize(image,(new_width, new_height),interpolation=cv2.INTER_AREA) 
        return resized_image

    def _detectEdges(self, image):
        blur = cv2.GaussianBlur(image, (5,5), self.blurStrength)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,self.cannyTreshold1,self.cannyTreshold2)
        
        return edges

    def _getLines(self, image):
        edges = self._detectEdges(image)
        lines = cv2.HoughLinesP(edges,1,np.pi/180,self.houghTreshold,self.minHoughLineLength,self.maxHoughLineGap)

        if lines is not None:
            return lines
        else:
            return None
        
    def _getOptimalLines(self, raw_image): 
        scale_factor = self.base_scale
        
        start = time.time()
        while scale_factor != 110:
            rescaled_img = self._rescaleImage(raw_image, scale_factor)
            lines = self._getLines(rescaled_img)
    
            if (lines is not None):
                self.process_time = time.time() - start
                return lines
                
            scale_factor+=self.scale_increment

        print("WARNING: NO OPTIMAL LINES DETECTED.")

    def getAngle(self, raw_image):

        angle=0
        lines = self._getOptimalLines(raw_image)
    
        for x1, y1, x2, y2 in lines[0]:
            angle =  np.arctan2(y2 - y1, x2 - x1)
            angle+=angle

        return angle/len(lines)

    def drawOrientation(self, raw_image):
        angle = self.getAngle(raw_image)

        length = 10000
        raw_image = cv2.resize(image,(240,240),interpolation=cv2.INTER_AREA) 
        center = (raw_image.shape[1] // 2, raw_image.shape[0] // 2)

        text = str(round(angle,2))

        # Choose font scale and thickness
        font_scale = 1
        font_thickness = 2

        # Choose font type and color
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        font_color = (255, 0, 255)  # white color

        # Get the size of the text to determine the position
        text_size = cv2.getTextSize(text, font_face, font_scale, font_thickness)[0]
        text_width, text_height = text_size
        text_x = 10  # left margin
        text_y = text_height + 10  # top margin

        cv2.putText(raw_image, text, (text_x, text_y), font_face, font_scale, font_color, font_thickness)
        cv2.line(raw_image, (int(center[0]),int(center[1])), (int(center[0]+length*np.cos(angle)),int(center[1]+length*np.sin(angle))), (255, 0, 255), 5)
        
        return raw_image


directory = 'G:/Sample/bottles'
bbox = OrientationDetection()

for images in list_images(directory):
    image = cv2.imread(images)
    cv2.imshow('hehe', bbox.drawOrientation(image))
    print(bbox.process_time)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  

