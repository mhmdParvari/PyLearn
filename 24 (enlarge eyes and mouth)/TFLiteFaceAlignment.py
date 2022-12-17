#!/usr/bin/python3
# -*- coding:utf-8 -*-

from cv2 import resize
import numpy as np
import cv2
import tensorflow as tf
from functools import partial
import time

class CoordinateAlignmentModel():
    def __init__(self, filepath, marker_nums=106, input_size=(192, 192)):
        self._marker_nums = marker_nums
        self._input_shape = input_size
        self._trans_distance = self._input_shape[-1] / 2.0

        self.eye_bound = ([35, 41, 40, 42, 39, 37, 33, 36],
                          [89, 95, 94, 96, 93, 91, 87, 90])

        # tflite model init
        self._interpreter = tf.lite.Interpreter(model_path=filepath)
        self._interpreter.allocate_tensors()

        # model details
        input_details = self._interpreter.get_input_details()
        output_details = self._interpreter.get_output_details()

        # inference helper
        self._set_input_tensor = partial(self._interpreter.set_tensor,
                                         input_details[0]["index"])
        self._get_output_tensor = partial(self._interpreter.get_tensor,
                                          output_details[0]["index"])

        self.pre_landmarks = None

    def _calibrate(self, pred, thd, skip=6):
        if self.pre_landmarks is not None:
            for i in range(pred.shape[0]):
                if abs(self.pre_landmarks[i, 0] - pred[i, 0]) > skip:
                    self.pre_landmarks[i, 0] = pred[i, 0]
                elif abs(self.pre_landmarks[i, 0] - pred[i, 0]) > thd:
                    self.pre_landmarks[i, 0] += pred[i, 0]
                    self.pre_landmarks[i, 0] /= 2

                if abs(self.pre_landmarks[i, 1] - pred[i, 1]) > skip:
                    self.pre_landmarks[i, 1] = pred[i, 1]
                elif abs(self.pre_landmarks[i, 1] - pred[i, 1]) > thd:
                    self.pre_landmarks[i, 1] += pred[i, 1]  
                    self.pre_landmarks[i, 1] /= 2
        else:
            self.pre_landmarks = pred

    def _preprocessing(self, img, bbox, factor=3.0):
        """Pre-processing of the BGR image. Adopting warp affine for face corp.

        Arguments
        ----------
        img {numpy.array} : the raw BGR image.
        bbox {numpy.array} : bounding box with format: {x1, y1, x2, y2, score}.

        Keyword Arguments
        ----------
        factor : max edge scale factor for bounding box cropping.

        Returns
        ----------
        inp : input tensor with NHWC format.
        M : warp affine matrix.
        """

        maximum_edge = max(bbox[2:4] - bbox[:2]) * factor
        scale = self._trans_distance * 4.0 / maximum_edge
        center = (bbox[2:4] + bbox[:2]) / 2.0
        cx, cy = self._trans_distance - scale * center

        M = np.array([[scale, 0, cx], [0, scale, cy]])

        cropped = cv2.warpAffine(img, M, self._input_shape, borderValue=0.0)
        inp = cropped[..., ::-1].astype(np.float32)

        return inp[None, ...], M

    def _inference(self, input_tensor):
        self._set_input_tensor(input_tensor)
        self._interpreter.invoke()

        return self._get_output_tensor()[0]

    def _postprocessing(self, out, M):
        iM = cv2.invertAffineTransform(M)
        col = np.ones((self._marker_nums, 1))

        out = out.reshape((self._marker_nums, 2))

        out += 1
        out *= self._trans_distance

        out = np.concatenate((out, col), axis=1)

        return out @ iM.T  # dot product

    def get_landmarks(self, image, detected_faces=None):
        """Predict the landmarks for each face present in the image.

        This function predicts a set of 68 2D or 3D images, one for each image present.
        If detect_faces is None the method will also run a face detector.

        Arguments
        ----------
        image {numpy.array} : The input image.

        Keyword Arguments
        ----------
        detected_faces {list of numpy.array} : list of bounding boxes, one for each
        face found in the image (default: {None}, format: {x1, y1, x2, y2, score})
        """

        for box in detected_faces:
            inp, M = self._preprocessing(image, box)
            out = self._inference(inp)
            pred = self._postprocessing(out, M)

            # self._calibrate(pred, 1, skip=6)
            # yield self.pre_landmarks

            yield pred


if __name__ == '__main__':

    from TFLiteFaceDetector import UltraLightFaceDetecion
    import sys
    
    fd = UltraLightFaceDetecion(
        "weights/RFB-320.tflite",
        conf_threshold=0.88)
    fa = CoordinateAlignmentModel(
        "weights/coor_2d106.tflite")

    # cap = cv2.VideoCapture(sys.argv[1])
    # color = (125, 255, 125)

    # while True:
    #     ret, frame = cap.read()

    #     if not ret:
    #         break

    #     start_time = time.perf_counter()

    #     boxes, scores = fd.inference(frame)

    #     for pred in fa.get_landmarks(frame, boxes):
    #         for p in np.round(pred).astype(np.int):
    #             cv2.circle(frame, tuple(p), 1, color, 1, cv2.LINE_AA)

    #     print(time.perf_counter() - start_time)

    #     cv2.imshow("result", frame)
    #     if cv2.waitKey(0) == ord('q'):
    #         break

    video_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, image = video_cap.read()
        if not ret: break
        
        height, width, _ = image.shape
        # print(height, width)
        mask = np.zeros((image.shape[0],image.shape[1],3), np.uint8)

        color = (125, 255, 125)

        boxes, scores = fd.inference(image)
        
        for pred in fa.get_landmarks(image, boxes):
            pred = np.round(pred).astype(np.int)
            # print(pred[40])

            left_eye_landmarks = []
            right_eye_landmarks = []
            lips_landmarks = []

            for i in [35, 36, 33, 37, 39, 42, 40, 41]:
                left_eye_landmarks.append(pred[i])
            for i in [89, 90, 87, 91, 93, 96, 94, 95]:
                right_eye_landmarks.append(pred[i])
            for i in [52, 55, 56, 53, 59,  58, 61, 68, 67, 71, 63, 64]:
                lips_landmarks.append(pred[i])

            cv2.drawContours(mask, np.array([left_eye_landmarks]), -1, (255,255,255), -1)
            cv2.drawContours(mask, np.array([right_eye_landmarks]), -1, (255,255,255), -1)
            cv2.drawContours(mask, np.array([lips_landmarks]), -1, (255,255,255), -1)

            # for index, p in enumerate(np.round(pred).astype(np.int)):
            #     # print(type(p))
            #     cv2.circle(image, tuple(p), 1, color, 1, cv2.LINE_AA)
            #     cv2.putText(image, str(index), p, cv2.FONT_HERSHEY_SIMPLEX, .4, color, 1)

            mask = mask / 255
            filter = mask * image
            filter = resize(filter, (0,0), fx=2, fy=2, interpolation= cv2.INTER_NEAREST)
            try:
                start_y = pred[40][1] - ((pred[33][1]-pred[40][1])//2)
                start_x = pred[40][0]
                for i in range(pred[40][1]*2, pred[33][1]*2):
                    for j in range(pred[35][0]*2, pred[39][0]*2): 
                        if filter[i][j].any():
                            # print(i,j)
                            
                            # sys.exit()
                            image[start_y+(i-(pred[40][1]*2))][start_x+(j-(pred[40][0]*2))] = filter[i][j]
                            
                            # sys.exit()
                            # image[i - height//2][j - width//2] = sheesh[i][j]
                            # image[i//2][j//2] = sheesh[i][j]
                
                start_y = pred[94][1] - ((pred[87][1]-pred[94][1])//2)
                start_x = pred[94][0]
                for i in range(pred[94][1]*2, pred[87][1]*2):
                    for j in range(pred[89][0]*2, pred[93][0]*2): 
                        if filter[i][j].any():
                            # print(i,j)
                            # sys.exit()
                            image[start_y+(i-(pred[94][1]*2))][start_x+(j-(pred[94][0]*2))] = filter[i][j]
                
                start_y = pred[53][1] + ((pred[53][1]-pred[63][1])//2)
                start_x = pred[53][0] 
                for i in range(pred[53][1]*2, pred[63][1]*2, -1):
                    for j in range(pred[52][0]*2, pred[61][0]*2):
                        if filter[i][j].any():
                            # print(i-(pred[53][1]*2))
                            image[start_y+(i-(pred[53][1]*2))][start_x+(j-(pred[53][0]*2))] = filter[i][j]
            except IndexError:
                break


        cv2.imshow("pauseC.jpg", image)
        
        # cv2.imwrite("wot1.jpg", filter)
        cv2.waitKey(1)