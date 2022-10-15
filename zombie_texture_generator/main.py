
from FaceExtractor import FaceExtractor
from image_generation import ImageGen

if __name__ == '__main__':

    ImageGen.run()
    f = FaceExtractor('images/')
    f.run()
    #f.save_faces()
    f.save_face_on_minecraft_zombie()




