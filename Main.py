import requests
import shutil
import replicate
import sys
from PIL import Image
import os

def main():
    pass

def reduce_dir(folder_name, size=256):
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
    new_folder_dir = os.getcwd() + f'\\resized_{folder_name}'
    if f'resized_{folder_name}' not in os.listdir(os.getcwd()):
        os.mkdir(new_folder_dir)
    for i in range(len(reduced_imgs)):
        reduced_imgs[i].save(new_folder_dir + '\\resized_' + img_names[i])


def generate(prompt, output_size):
    for i in range(output_size):
        generate_img(prompt, i)

def generate_img(prompt,num):
    client = replicate.Client(api_token="fb98523b00914a49e3915e571bebe762f1d18827")
    model = client.models.get("stability-ai/stable-diffusion")
    output = model.predict(prompt=prompt)
    res  = requests.get(output[0], stream = True)
    if res.status_code == 200:
        with open(f'{prompt}{num}.png', 'wb') as f:
            #change where image gets saved to.
            shutil.copyfileobj(res.raw, f)
            print(f'Image {num} downloaded')
    else:
        print(f'Image {num} could not be downloaded')

def set_block_imges(block_names, imgs):
    #create a dictionary with block_names macthed to imgs:
    blocks_imgs_dict = {}
    for name in block_names:
        blocks_imgs_dict[name] = imgs
    

if __name__ == "__main__":
    main()