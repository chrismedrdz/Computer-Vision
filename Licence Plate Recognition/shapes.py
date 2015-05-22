import numpy as np
import cv2

img = cv2.imread('input/image.png')
gray = cv2.imread('input/image.png',0)

#ret,thresh = cv2.threshold(gray,127,255,1)

#contours,h = cv2.findContours(thresh,1,2)
#contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


ret, thresh = cv2.threshold(gray, 127, 255,0)
contours,hierarchy = cv2.findContours(thresh,2,1)
cnt = contours[0]

hull = cv2.convexHull(cnt,returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)

for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    cv2.line(img,start,end,[0,255,0],2)
    cv2.circle(img,far,5,[0,0,255],-1)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''
print contours

for cnt in contours:
#for cnt in range(0, len(contours)):
    #if (cnt % 2 == 0):
        print cnt
        #epsilon 0.1*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
        #hull = cv2.convexHull(cnt)
        print len(approx)
        if len(approx)==5:
            print "pentagon"
            cv2.drawContours(img,[cnt],0,255,-1)
        elif len(approx)==3:
            print "triangle"
            cv2.drawContours(img,[cnt],0,(0,255,0),-1)
        elif len(approx)==4:
            print "square"
            cv2.drawContours(img,[cnt],0,(0,0,255),-1)
        elif len(approx) == 9:
            print "half-circle"
            cv2.drawContours(img,[cnt],0,(255,255,0),-1)
        elif len(approx) > 15:
            print "circle"
            cv2.drawContours(img,[cnt],0,(0,255,255),-1)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''