# DYHTG-Team23
A repository for the greatest Team 23 for Do You Have The Guts Hackathon

If you want to try out our project, follow these steps:
## Keep in mind, this process can be improved greatly, so we accept any kind of tips and ideas :)

Start Minecraft, and create a new single player Creative, Super Flat world with Cheats On, we'll need it later.
Make sure you have Python installed
Clone the repository, and open a terminal and navigate to the repo folder
run: python main.py
next, you will get errors similar to this: (ModuleNotFoundError: No module named 'args')
for each error like this, type: pip install <missing module name> (e.g. pip install args)
then try running python main.py again, until you don't get missing module errors.

take extra care on these errors:
for cv2, use this command: pip install opencv-python
for dlib: https://www.geeksforgeeks.org/how-to-install-dlib-library-for-python-in-windows-10/
for skimage: use this command: pip install scikit-image
*for ERROR: CMake must be installed to build dlib: download it from https://cmake.org/download/ then, make sure when installing it, that option "Add CMake to the system path for all users" is selected.
*If it still doesn't work, you need download Visual Studio with C++: https://visualstudio.microsoft.com/visual-cpp-build-tools/

After that, you might get an error: FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:/Users/jonai/Code/DYHTG-Team23'
Change the path to be the path of the cloned repository.

Then, you will be asked to input the name of your minecraft world, do that.
You'll get a similar error to change the path again, you know the drill at this point.

Finally, you'll be asked to input 5 prompts for AI generation of images.

There might be more paths which need changing, but you should be able to figure it out on your own.

And that's it! Congratulations, and enjoy our spooky dungeon!
To generate it, go to your minecraft world and type in "/function spooky and autofill it

Enjoy!