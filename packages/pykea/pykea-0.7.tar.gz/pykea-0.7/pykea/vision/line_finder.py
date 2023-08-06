import cv2
import numpy as np 
from time import sleep, time
from threading import Thread

class LineFinder:
    def __init__(self,
                hsv_v_max=20, 
                display_contour=True, 
                h_start=380,
                h_end=480,
                w_start=0,
                w_end=640,
                min_area=500,
                max_area=90000):
        self.hsv_v_max = hsv_v_max
        self.display_contour = display_contour
        self.line_center_xy = (0,0)
        self.line_area = 0
        self.line_angle = 0
        self.h_start=h_start
        self.h_end=h_end
        self.w_start=w_start
        self.w_end=w_end
        self.min_area = min_area
        self.max_area = max_area
        self.fps = 0
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.draw_screen = np.zeros((480,640,3), dtype=np.uint8)

        self.start_thread()

    def start_thread(self):
        if self.display_contour:
            self.t_show = Thread(target=self.show_frame)
            self.t_show.daemon = True
            self.t_show.start()
            # self.t_show.join()

    def show_frame(self):
        while True:
            image = cv2.circle(self.draw_screen, (int(self.line_center_xy[0]),int(self.line_center_xy[1])), 5, color = (255, 0, 0), thickness = cv2.FILLED)
            
            self.putTextRect(self.draw_screen, f'Angle: {str(int(self.line_angle))}', pos=(10,20))
            self.putTextRect(self.draw_screen, f'Center: {str(int(self.line_center_xy[0]))} {str(int(self.line_center_xy[1]))}', pos=(10,50))
            self.putTextRect(self.draw_screen, f'Area: {str(int(self.line_area))}', pos=(10,80))
            self.putTextRect(self.draw_screen, f'FPS: {str(int(self.fps))}', pos=(10,110))

            
            cv2.imshow('drawing', self.draw_screen)
            if cv2.waitKey(10) == 27:
                cv2.destroyAllWindows()
                self.cap.release() 
                break
        
    def process(self):
        start = time()
        _, frame = self.cap.read()
            
        image = frame[self.h_start:self.h_end, self.w_start:self.w_end] # frame[380:, :]
        image = cv2.GaussianBlur(image, (3,3), 0) 

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray,5)
        
        lower_black = np.array([0,0,0])
        upper_black = np.array([180, 255, self.hsv_v_max])

        mask = cv2.inRange(hsv, lower_black, upper_black)

        kernel=np.ones((3,3), np.uint8)
        opening=cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        closing=cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        contours = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]

        if contours:
            cnt_max = sorted(contours, key=cv2.contourArea, reverse=True)[0]
            self.line_area = cv2.contourArea(cnt_max)

            if self.line_area > self.min_area and self.line_area < self.max_area:
                rect = cv2.minAreaRect(cnt_max)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                # cv2.drawContours(image, [box], 0, 255, 1)
                self.draw_screen[:,:] = 0
                cv2.drawContours(self.draw_screen, cnt_max, -1, (0, 255, 0), 3, offset=(0,self.h_start))
                center = rect[0]
                rotation = rect[2]

                # Calculate angle
                h = self.h_end - self.h_start  # height of cropped image
                if box[0][1] > h//2: # if y of the first point is in the lower part of the image (orientation of the line rectangle)
                    self.line_angle = rotation
                else:
                    self.line_angle = rotation + 90

                self.line_center_xy = (int(center[0]),int(center[1])+self.h_start)

            else: # line ara too small
                self.line_center_xy = (-1,-1)
                self.line_area = -1
                self.line_angle = 999

        else:  # no contour found
            self.line_center_xy = (-1,-1)
            self.line_area = -1
            self.line_angle = 999

        self.fps = int(1/(time()-start))

        return frame


    def get_line_center(self):
        return self.line_center_xy
    
    
    def get_line_angle(self):
        return self.line_angle

    
    def get_line_area(self):
        return self.line_area

    
    def putTextRect(self, img, text, pos, scale=1, thickness=2, colorT=(255, 255, 255),
                colorR=(255, 0, 255), font=cv2.FONT_HERSHEY_PLAIN,
                offset=10, border=None, colorB=(0, 255, 0)):
    
        ox, oy = pos
        (w, h), _ = cv2.getTextSize(text, font, scale, thickness)

        x1, y1, x2, y2 = ox - offset, oy + offset, ox + w + offset, oy - h - offset

        cv2.rectangle(img, (x1, y1), (x2, y2), colorR, cv2.FILLED)
        if border is not None:
            cv2.rectangle(img, (x1, y1), (x2, y2), colorB, border)
        cv2.putText(img, text, (ox, oy), font, scale, colorT, thickness)
                    

if __name__ == '__main__':
    cam = LineFinder(hsv_v_max=60, display_contour=True, h_start=380,h_end=480)

    try:
        while True:
            # IMAGE PROCESSING
            img = cam.process()
            # START TRACKING
            print(cam.get_line_center())

            cv2.imshow('camera', img)
            if cv2.waitKey(10) == 27:
                cv2.destroyAllWindows()
                break
            
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        pass

