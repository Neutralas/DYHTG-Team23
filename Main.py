from FaceExtractor import FaceExtractor
from image_generation import ImageGen
from generator import MazeGeneration
import os

if __name__ == '__main__':
    print("Starting Maze Setup...")
    image_generator = ImageGen()
    maze_generator = MazeGeneration()

    image_generator.run()
    maze_generator.run()

    os.chdir("C:/Users/jonai/Code/DYHTG-Team23")
    
    f = FaceExtractor('images/')
    f.run()
    f.save_faces()
    f.save_face_on_minecraft_zombie()

    print("Setup Done!")