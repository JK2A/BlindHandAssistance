import cv2 as cv
import numpy as np

import os

from hand_recog import getHandPosition



"""AmitehMain():
// ret, frame = opencv.video()

{dict ->object: [x,y], .....} = kushmain(frame)
(x,y) = AkarshMain(frame)
string = JackMain()

"""


def main():
	#os.system("python hackathon_object_detection.py ;2D") #runs kush's script
	#desired_object = get_desired_object()
	video_capture = cv.VideoCapture(0)
	while(True):
		ret, frame = video_capture.read()
		if not ret:
			continue
		#object_dictionary = object_detect_model(frame)
		#desired_object_locations_list = object_dictionary[desired_object]
		hand_position = hand_detect_model(frame)

		if hand_position is not None:
			cv.circle(frame, hand_position, 5, (255,0,0), -1)

		#if hand_position != None:
			#calculate distance to correct object
		cv.imshow('frame',frame)
		cv.waitKey(1)

	cap.release()
	cv.destroyAllWindows()


#kush stuff
#this should return a dictionary. {object_name: [(x, y)]}
def object_detect_model(frame):
	pass

#akarsh stuff
#this should return coordinates as tuple (x,y) for the center of ONE hand or None
def hand_detect_model(frame):
	return getHandPosition(frame)


#jack stuff
#this function should return a string for the desired object. ie: "apple"
def get_desired_object(desired_object):

	pass

#amitesh stuff
#this function will find the minimum distance between the hand and anyObject available.
def getMinimumDistance(obj_locations_list, hand_position, frame):
	min = frame.shape(0)**2 + frame.shape(1)**2
	for obj_loc in obj_locations_list:
		min = min((obj_loc[0] - hand_pos[0])**2 + (obj_loc[1] - hand_pos[1])**2, min)
	return min


main()



"""
KushMain(frame):
	

AkarshMain(frame):
	
JackMain():


"""

#getting input from akarsh and kush with coordinates of hand and coordinates of objects and object you want from jack
#first function: use the word from jack to filter objects from kush objects list. Return new short list
#second function: with remaining objects, check hand coordinates in relation to object coordinates for each object to hand. return the minimum distance
#third function: make sounds at a certain speed based on distance
#main function: Call function 1. get the word and store it.
				#Call kush function and get list of objects. pass it into function 1, and store filtered_list.
				#Call ak function and get hand position.
				#call 2nd function and store the minimum distance. 
				#Pass minimum distance to 3rd function. to play new rate of beeps.
				
				
