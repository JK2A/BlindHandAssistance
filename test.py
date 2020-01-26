import cv2 as cv
import numpy as np

import os
from Beep2 import Beep2
from hand_recog import getHandPosition
from hackathon_object_detection import getObjectPositions, get_category_index
import Stream
import math
from Beep import WavePlayerLoop
"""AmitehMain():
// ret, frame = opencv.video()

{dict ->object: [x,y], .....} = kushmain(frame)
(x,y) = AkarshMain(frame)
string = JackMain()

"""

prevHandPos = None
prevObjectPos = None


def main():
	#os.system("python hackathon_object_detection.py ;2D") #runs kush's script
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/akarshkumar0101/Developer/Hackathons/BlindHandAssistance/Google_Key/Blind_Assistance.json"

	desired_object = Stream.main(get_category_index())

	video_capture = cv.VideoCapture(0)

	while(True):
		# prev_dist = math.inf
		ret, frame = video_capture.read()
		if not ret:
			continue
		# print(frame.shape)
		############ HAND POSITION ############
		hand_position = hand_detect_model(frame)
		if hand_position is not None:
			prevHandPos = hand_position
			cv.circle(frame, hand_position, 5, (255, 0, 0), -1)

		############ OBJECT POSITION ############
		object_dictionary = object_detect_model(frame)
		if desired_object not in object_dictionary:
			desired_object_locations_list = []
		else:
			desired_object_locations_list = object_dictionary[desired_object]

		if hand_position is not None:
			#calculate distance to correct object
			#beep = WavePlayerLoop("/Users/akarshkumar0101/Developer/Hackathons/BlindHandAssistance/Sounds/shortbeep.wav")
			#beep.run()
			beep = Beep2("/Users/akarshkumar0101/Developer/Hackathons/BlindHandAssistance/Sounds/shortbeep.wav")
			beep.play()
			dist = getMinimumDistance(desired_object_locations_list, hand_position, frame)
			print(dist)
			print(100000/dist)
			beep.change_volume(min(1, max(.1, 100000/dist)))

		cv.imshow('frame', frame)
		cv.waitKey(1)

	video_capture.release()
	cv.destroyAllWindows()


#kush stuff
#this should return a dictionary. {object_name: [(x, y)]}
def object_detect_model(frame):
	return getObjectPositions(frame)

#akarsh stuff
#this should return coordinates as tuple (x,y) for the center of ONE hand or None
def hand_detect_model(frame):
	return getHandPosition(frame)



#jack stuff
#this function should return a string for the desired object. ie: "apple"



#amitesh stuff
#this function will find the minimum distance between the hand and anyObject available.
def getMinimumDistance(obj_locations_list, hand_position, frame):
	m = frame.shape[0]**2 + frame.shape[1]**2
	for obj_loc in obj_locations_list:
		print("obj lock")
		print(obj_loc)

		print("hand pos")
		print(hand_position)

		global prevObjectPos

		dist = (obj_loc[0] - hand_position[0])**2 + (obj_loc[1] - hand_position[1]) ** 2
		if dist < m:
			m = dist
			prevObjectPos = obj_loc

		# m = min((obj_loc[0] - hand_position[0])**2 + (obj_loc[1] - hand_position[1])**2, m)

	return m


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
				
				
