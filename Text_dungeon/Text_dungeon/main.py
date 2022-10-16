import pygame as py
import os
import sys
import PyObjects as po
import API
import threading
from queue import Queue

def start_menu():
    #necessary set up
    py.init()
    py.display.set_caption("AI dungeon")
    win = py.display.set_mode((400, 600))

    #this queue is used for passing info between threads
    queue = Queue()

    #this flag determines whether the program is in writing mode or in waiting for backend response
    #True = writing, False = waiting
    state_flag = True

    #texture imports
    #file paths
    dirname = os.getcwd()
    text_file = os.getcwd() + '\\text'
    image_file = os.getcwd() + '\\image'
    textures_file = os.getcwd() + '\\textures'

    #instatiate objects
    # since we don't have many objects I'll make a dictionary where all of them are stored for easy access
    elements = {
        'input': po.InputBox(0, 500, 600, 100, py.font.Font(None, 32), default_text="You wake up in a creepy dungeon"),
        'text': po.Text(0,400, "", py.font.Font(None, 32)),
        'image': po.Image(0, 0, image_file + '\\main.png'),
        'text_box': po.Image(0, 500, textures_file + '\\block.png')
    }
    elements['input'].select()

    #outer loop is the general game
    while True:
        py.event.pump()
        run_state = True

        if state_flag:
            print("writing")
            #if player writing, they can type
            elements['input'].select()
            # call API function giving input_bar.text.text
            #this code is how you get teh data
            display(win, elements, queue)
            state_flag = False

        else:
            print("waiting")
            # if player waiting, they can't type
            elements['input'].unselect()
            listener = threading.Thread(target=API.threading_api_calls, args=(queue, elements['text'].text), daemon=True)
            listener.start()
            #print(queue.empty())
            display(win, elements, queue)
            elements['text'].change_text(queue.get())
            elements['image'] = po.Image(0, 0, image_file + '\\main.png')
            queue.task_done()
            state_flag = True

        #inner loop is the running in wait or running in write



def display(win, elements, queue):
    deleting = False
    while True:
        #events
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if event.type == py.KEYUP and event.key == py.K_BACKSPACE:
                deleting = False

            #if event.type == py.KEYDOWN and

            if event.type == py.KEYDOWN and elements['input'].active:
                if event.key == py.K_BACKSPACE or deleting:
                    deleting = True
                    elements['input'].delete()
                elif event.key == py.K_RETURN:
                    queue.put(True)
                    queue.put(elements['input'].text.text)
                else:
                    elements['input'].write(event.unicode)

        # output to window
        win.fill((255, 255, 255))
        elements['image'].draw(win)
        elements['text'].draw(win)
        elements['text_box'].draw(win)
        elements['input'].draw(win)


        if not queue.empty():
            # if the first item is not a boolean, it means there was an error in the thread
            # so we look for it and catch it with the error handler
            end_flag = queue.get()
            queue.task_done()
            if type(end_flag) != type(True):
                raise Exception(end_flag)
            return  # exit loop to change state

        py.display.update()

if __name__ == "__main__":
    start_menu()

