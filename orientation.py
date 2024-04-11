import cv2 
import math
import numpy as np 
from collections import Counter
from imutils.paths import list_images

import time


class OrientationDetection:

    def __init__(self, alt=False):
       self.alt = alt
       self.process_time = 0
       self.base_scale = 5
       self.scale_increment = 5
       self.blurStrength = 1
       self.cannyTreshold1 = 45
       self.cannyTreshold2 = 105
       self.houghTreshold = 40
       self.minHoughLineLength = 15
       self.maxHoughLineGap = 5

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
        #edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, (3,3))
        
        return edges

    def _getLines(self, image):
        edges = self._detectEdges(image)
        lines = cv2.HoughLinesP(edges,1,np.pi/180,self.houghTreshold,self.minHoughLineLength,self.maxHoughLineGap)

        if lines is not None:
            return lines
        else:
            return None
        
    def getAngle(self, raw_image): 
        scale_factor = self.base_scale
        scale_counter = 0
        #list_of_lines=[]
        list_of_angles=[]
        list_of_common_angles=[]
        #start = time.time()
        # we need to detect atleast five scales of the image tha has a valid line
        # then we will append every lines to the list
        while scale_factor < 100 and scale_counter != 3:
            rescaled_img = self._rescaleImage(raw_image, scale_factor)
            lines = self._getLines(rescaled_img)
        
            if (lines is not None):
                
                for x1, y1, x2, y2 in lines[0]:
                    angle =  np.arctan2(y2 - y1, x2 - x1)
                    list_of_angles.append(angle)

                scale_counter+=1
             
            scale_factor+=self.scale_increment

        c = Counter(list_of_angles)
        k = c.most_common()
        return k[0][0]
    
    def _getOptimalLines(self, raw_image): 
        scale_factor = self.base_scale
        scale_counter = 0
        #list_of_lines=[]
        list_of_angles=[]
        list_of_common_angles=[]
        #start = time.time()
        # we need to detect atleast five scales of the image tha has a valid line
        # then we will append every lines to the list
        while scale_factor < 100 and scale_counter != 3:
            rescaled_img = self._rescaleImage(raw_image, scale_factor)
            lines = self._getLines(rescaled_img)
    
            if (lines is not None):
                
                for x1, y1, x2, y2 in lines[0]:
                    angle=  np.arctan2(y2 - y1, x2 - x1)
                    print(angle)
                    list_of_angles.append(angle)

                scale_counter+=1
             
            scale_factor+=self.scale_increment

        c = Counter(list_of_angles)
        k = c.most_common()
        return k[0][0]
        # return 0

            
    def testOrientation(self, raw_image):
        angle = self.getAngle(raw_image)

        length = 100
        raw_image = cv2.resize(raw_image,(240,240),interpolation=cv2.INTER_AREA) 
        center = (raw_image.shape[1] // 2, raw_image.shape[0] // 2)

        text = str(round(angle,2))

        # Choose font scale and thickness
        font_scale = 1
        font_thickness = 4

        # Choose font type and color
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        font_color = (0, 0, 255)  # white color

        # Get the size of the text to determine the position
        text_size = cv2.getTextSize(text, font_face, font_scale, font_thickness)[0]
        text_width, text_height = text_size
        text_x = 10  # left margin
        text_y = text_height + 10  # top margin

        cv2.putText(raw_image, text, (text_x, text_y), font_face, font_scale, font_color, font_thickness)
        cv2.circle(raw_image, (int(center[0]), int(center[1])), radius=10, color=(0, 0, 255), thickness=-3)
        cv2.line(raw_image, (int(center[0]),int(center[1])), (int(center[0]+length*np.cos(angle)),int(center[1]+length*np.sin(angle))), (0, 0, 255), 4)
        
        return raw_image
    
    def drawOrientation(self, raw_image, frame, x1, y1, x2, y2):
        angle = self.getAngle(raw_image)

        length = 250
        #raw_image = cv2.resize(image,(240,240),interpolation=cv2.INTER_AREA) 
        bbox_center = (int(x1+x2)/2,int(y1+y2)/2)

        text = str(round(angle,2))

        # Choose font scale and thickness
        font_scale = 1
        font_thickness = 2

        # Choose font type and color
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        font_color = (0, 0, 255)  # white color

        # Get the size of the text to determine the position
        text_size = cv2.getTextSize(text, font_face, font_scale, font_thickness)[0]
        text_width, text_height = text_size
        text_x = 10  # left margin
        text_y = text_height + 10  # top margin

        #cv2.putText(frame, text, (text_x, text_y), font_face, font_scale, font_color, font_thickness, cv2.LINE_AA)
        cv2.circle(frame, (int(bbox_center[0]), int(bbox_center[1])), radius=20, color=(0, 0, 255), thickness=-3)
        cv2.line(frame, (int(bbox_center[0]),int(bbox_center[1])), (int(bbox_center[0]+length*np.cos(angle)),int(bbox_center[1]+length*np.sin(angle))), (0, 0, 255), 5)
        
        return angle, frame


