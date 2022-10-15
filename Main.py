import requests
import shutil
import replicate
import sys
from PIL import Image
import os

class ImageGen():

    def run(self):
        self.clean_folders()
        print("The AI needs 5 prompts to generate images that will plague your nightmares....")
        for i in range(5):
            valid = False
            while not valid:
                user_input = input(f"Prompt nº {i}: ")
                try:
                    self.generate(user_input ,1)
                    valid = True
                except Exception as e:
                    print("trying again")
        self.reduce_dir()
        self.set_block_imgs(['stone.png','granite.png','diorite.png','andesite.png','deepslate.png'])

    def reduce_dir(self, folder_name='new_images', size=256):
        folder_as_dir = os.getcwd() + '\\' + folder_name
        dir_names = os.listdir(folder_as_dir)
        img_names = []
        reduced_imgs = []
        for i in range(len(dir_names)):
            if dir_names[i][-4:] == '.png':
                img_names.append(dir_names[i])
                img_name = img_names[i]
                img = Image.open(f'{folder_as_dir}\\{img_name}')
                resized_img = img.resize((size,size))
                reduced_imgs.append(resized_img)
            else:
                print(f'{folder_as_dir}\\{dir_names[i]} does not end in .png')

        #change where images go to.
        new_folder_dir = os.getcwd() + f'\\scaled_images'
        for i in range(len(reduced_imgs)):
            reduced_imgs[i].save(new_folder_dir + '\\resized_' + img_names[i])


    def generate(self, prompt, output_size):
        for i in range(output_size):
            self.generate_img(prompt, i)

    def generate_img(prompt,num):
        img_file = os.getcwd() + '\\new_images'
        client = replicate.Client(api_token="3a7ca8c73be5a611ab2c01d84cbe4b7db3ae84e3")
        model = client.models.get("stability-ai/stable-diffusion")
        try:
            output = model.predict(prompt=prompt)
        except Exception as e:
            print(e)
            print("AI api crashed")
            raise Exception("AI crash")
        res  = requests.get(output[0], stream = True)
        if res.status_code == 200:
            with open(f'{img_file}\\{prompt}{num}.png', 'wb') as f:
                #change where image gets saved to.
                shutil.copyfileobj(res.raw, f)
                print(f'{prompt} image generated')
        else:
            print(f'Image {num} could not be downloaded')

    def set_block_imgs(self, block_names, img_folder='scaled_images'):
        new_img_location = os.getcwd() + f'\\{img_folder}'
        block_img_location = os.getcwd() + '\\scary_pack\\assets\minecraft\\textures\\block'

        # for blocks in the name list
        for i,name in enumerate(block_names):
            # get the next image in our new_images file
            new_block = Image.open(new_img_location + '\\' +os.listdir(img_folder)[i])
            # delete old file
            os.remove(f'{block_img_location}\\{name}')
            # save new block with the name of the old block
            new_block.save(f'{block_img_location}\\{name}')

    def clean_folders(self):
        new_images = os.getcwd() + '\\new_images'
        scaled_images = os.getcwd() + f'\\scaled_images'
        for elt in os.listdir(new_images):
            os.remove(new_images + f'\\{elt}')
        for elt in os.listdir(scaled_images):
            os.remove(scaled_images + f'\\{elt}')
