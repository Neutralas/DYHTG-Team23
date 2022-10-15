import os
import sys

import args
import cv2
import imutils
import numpy as np
from imutils.face_utils import rect_to_bb
import dlib
from FaceAligner import FaceAligner

np.set_printoptions(threshold=sys.maxsize)

class FaceExtractor():

    def __init__(self, directory,desiredFaceWidth=256):
        self.directory = directory
        self.output =  "zombie_skins/"
        self.images = []
        self.faces = []
        self.desiredFaceWidth = desiredFaceWidth


    def get_faces(self, image):
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        fa = FaceAligner(predictor, desiredFaceWidth=self.desiredFaceWidth)
        image = cv2.imread(image,cv2.IMREAD_UNCHANGED)
        image = imutils.resize(image, width=800)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 2)

        for rect in rects:
            # extract the ROI of the *original* face, then align the face
            # using facial landmarks
            (x, y, w, h) = rect_to_bb(rect)
            faceAligned = fa.align(image, gray, rect)
            self.faces.append(faceAligned)

    def load_images(self):
        # get images in directory in forms jpg, jpeg, png
        for file in os.listdir(self.directory):
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                self.images.append(file)
        return self.images


    def run(self):
        self.load_images()
        for image in self.images:
            self.get_faces(self.directory + image)
        return self.faces

    def save_faces(self):
        # save faces to directory
        for i, face in enumerate(self.faces):
            dim = (64, 64)
            resized = cv2.resize(face, dim, interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.directory+"/" + str(i) + '.jpg', resized)

    def save_face_on_minecraft_zombie(self):
        # import minecraft zombie
        # save faces to minecraft zombie
        face_start_pos = (64, 64)
        face_end_pos = (128, 128)
        dim = (64, 64)
        for i, face in enumerate(self.faces):
            base_img = cv2.imread("images/zombie.png", cv2.IMREAD_UNCHANGED)
            resized = cv2.resize(face, dim, interpolation=cv2.INTER_AREA)
            #make a true false mask of resized
            mask = np.average(resized,axis=2) > 10

            print('mask',mask.shape)
            #make a blood like mask
            blood_mask = FaceExtractor._generate_perlin_noise_2d((64, 64), (4, 4))
            blood_mask[~mask] = 0


            #replace only non black pixels
            base_img[face_start_pos[0]:face_end_pos[0],face_start_pos[1]:face_end_pos[1],:-1][mask] = resized[mask]
            """red_limit = np.full((64,64),255,dtype=np.uint8) - base_img[face_start_pos[0]:face_end_pos[0], face_start_pos[1]:face_end_pos[1], 2]
            red_limit = red_limit // 3
            base_img[face_start_pos[0]:face_end_pos[0],face_start_pos[1]:face_end_pos[1],2][mask] += np.minimum(((blood_mask*15).astype(np.uint8)),red_limit)[mask]
            """
            #if i is 1 just write the name of the file
            if i  == 1:
                cv2.imwrite(self.output + "zombie.png", base_img)
            else:
                cv2.imwrite(self.output + "zombie" + str(i+1 + ".png", base_img))

    def _generate_perlin_noise_2d(shape, res):
        def f(t):
            return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3

        delta = (res[0] / shape[0], res[1] / shape[1])
        d = (shape[0] // res[0], shape[1] // res[1])
        grid = np.mgrid[0:res[0]:delta[0], 0:res[1]:delta[1]].transpose(1, 2, 0) % 1
        # Gradients
        angles = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1)
        gradients = np.dstack((np.cos(angles), np.sin(angles)))
        g00 = gradients[0:-1, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
        g10 = gradients[1:, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
        g01 = gradients[0:-1, 1:].repeat(d[0], 0).repeat(d[1], 1)
        g11 = gradients[1:, 1:].repeat(d[0], 0).repeat(d[1], 1)
        # Ramps
        n00 = np.sum(grid * g00, 2)
        n10 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1])) * g10, 2)
        n01 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1] - 1)) * g01, 2)
        n11 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1] - 1)) * g11, 2)
        # Interpolation
        t = f(grid)
        n0 = n00 * (1 - t[:, :, 0]) + t[:, :, 0] * n10
        n1 = n01 * (1 - t[:, :, 0]) + t[:, :, 0] * n11
        return np.sqrt(2) * ((1 - t[:, :, 1]) * n0 + t[:, :, 1] * n1)