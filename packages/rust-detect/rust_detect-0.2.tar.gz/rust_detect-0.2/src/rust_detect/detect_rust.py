import cv2
from sys import argv
import numpy as np
import os
import glob
import argparse


class Rust_Detection:
    def __init__(self, count=0):
        self.count = count

    def rust_detect(self,file):
        img = cv2.imread(file)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Range for lower red
        lower_red = np.array([0, 70, 70])
        upper_red = np.array([20, 200, 150])
        mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

        # range for upper red
        lower_red = np.array([170, 70, 70])
        upper_red = np.array([180, 200, 150])
        mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

        # add both masks
        mask = mask0+mask1

        output_img = cv2.bitwise_and(img, img, mask=mask)
        print(""" Welcome to the rust detection software!! 
            The software detects the rusted portion of metal
            and calculates nuber of rust piels for 
            comparitive analysis.\n\n""")
        print("**********************************************")
        print("\n\n\n Number of pixels depicting rust \n >> %d" %
              (np.sum(mask)/255))
        cv2.imshow('image1', output_img)
        cv2.imshow('image2', img)
        cv2.waitKey(0)
        cv2.imwrite('output_image%d.jpg' % self.count, output_img)
        cv2.imwrite('image%d.jpg' % self.count, img)
        cv2.destroyAllWindows()
        os.system("cls")
        os.system("color 0a")
        os.system("cls")

if __name__=="__main__":
    Rust_Detection().rust_detect("../../Images/photo-1583147247730-0ffa2ee86d72.jpg")