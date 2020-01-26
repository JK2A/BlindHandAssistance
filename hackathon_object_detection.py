import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import pathlib
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

import cv2
import time

# methods

def load_model(model_name):
  base_url = 'http://download.tensorflow.org/models/object_detection/'
  model_file = model_name + '.tar.gz'
  model_dir = tf.keras.utils.get_file(
    fname=model_name, 
    origin=base_url + model_file,
    untar=True)

  model_dir = pathlib.Path(model_dir)/"saved_model"

  model = tf.saved_model.load(str(model_dir))
  model = model.signatures['serving_default']

  return model


def show_inference(model, image, category_index):
  # the array based representation of the image will be used later in order to prepare the
  # result image with boxes and labels on it.
  image_np = image

  # Actual detection.
  output_dict = run_inference_for_single_image(model, image_np)
  # Visualization of the results of a detection.
  vis_util.visualize_boxes_and_labels_on_image_array(
    image_np,
    output_dict['detection_boxes'],
    output_dict['detection_classes'],
    output_dict['detection_scores'],
    category_index,
    instance_masks=output_dict.get('detection_masks_reframed', None),
    use_normalized_coordinates=True,
    line_thickness=8)

  detected_objects = {}
  current = 0

  while current < len(output_dict['detection_scores']) and output_dict['detection_scores'][current] > 0.7:
    current_obj_index = output_dict['detection_classes'][current] # int
    obj_name = category_index[current_obj_index]['name'] # string
    location = output_dict['detection_boxes'][current] # pass in 1x4 np array
  
    x = int(np.average((location[1], location[3])) * image_np.shape[1])
    y = int(np.average((location[0], location[2])) * image_np.shape[0])
    location = (x,y)
        
    if obj_name not in detected_objects:
      detected_objects[obj_name] = []
    detected_objects[obj_name].append(location)

    current += 1


  # print(detected_objects)


  # imshow here
  cv2.imshow('video', image_np)
  cv2.waitKey(1)

  return detected_objects

# ymin, xmin, ymax, xmax = box




def run_inference_for_single_image(model, image):
  image = np.asarray(image)
  # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
  input_tensor = tf.convert_to_tensor(image)
  # The model expects a batch of images, so add an axis with `tf.newaxis`.
  input_tensor = input_tensor[tf.newaxis,...]

  # Run inference
  output_dict = model(input_tensor)

  # All outputs are batches tensors.
  # Convert to numpy arrays, and take index [0] to remove the batch dimension.
  # We're only interested in the first num_detections.
  num_detections = int(output_dict.pop('num_detections'))
  output_dict = {key:value[0, :num_detections].numpy() 
                 for key,value in output_dict.items()}
  output_dict['num_detections'] = num_detections

  # detection_classes should be ints.
  output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
   
  # Handle models with masks:
  if 'detection_masks' in output_dict:
    # Reframe the the bbox mask to the image size.
    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
              output_dict['detection_masks'], output_dict['detection_boxes'],
               image.shape[0], image.shape[1])      
    detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                       tf.uint8)
    output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()
    
  return output_dict

# end

def main():

  # patch tf1 into `utils.ops`
  utils_ops.tf = tf.compat.v1

  # Patch the location of gfile
  tf.gfile = tf.io.gfile

  # List of the strings that is used to add correct label for each box.
  PATH_TO_LABELS = 'data/mscoco_label_map.pbtxt'
  category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)



  model_name = 'ssd_mobilenet_v1_coco_2017_11_17'
  detection_model = load_model(model_name)

  video_capture = cv2.VideoCapture(0)

  while True:
    ret, frame = video_capture.read(0)
    final_dict = show_inference(detection_model, frame, category_index)

    

if __name__ == "__main__":
  main()
  