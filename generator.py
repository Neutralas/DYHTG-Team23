import random
import os
from distutils.dir_util import copy_tree

class MazeGeneration:

    os.chdir("C:/Users/jonai/Code/DYHTG-Team23")
    world_name = input("Please enter the name of the world: ")
    path_to_base = os.getcwd() + "/maze_datapack"
    path_to_save = f"C:/Users/jonai/AppData/Roaming/.minecraft/saves/{world_name}/datapacks/maze_datapack"

    def run(self):

        action_list=["fill ~ ~2 ~ ~ ~2 ~ cobweb", "fill ~ ~2 ~ ~ ~2 ~ cobweb", "summon minecraft:zombie",
                    "setblock ~ ~ ~ glowstone", "setblock ~ ~ ~ glowstone", "fill ~2 ~ ~ ~-2 ~10 ~-15 stone replace black_concrete",
                    "fill ~2 ~ ~ ~-2 ~10 ~-15 granite replace black_concrete", "fill ~2 ~ ~ ~-2 ~10 ~-15 diorite replace black_concrete",
                    "fill ~2 ~ ~ ~-2 ~10 ~-15 andesite replace black_concrete", "fill ~2 ~ ~ ~-2 ~10 ~-15 deepslate replace black_concrete",
                    "effect give @a nausea 8", "summon minecraft:lightning_bolt ~-1 ~ ~"]

        with open(self.path_to_base + "/data/scary/functions/maze_black.mcfunction", "r") as f1:
            lines = f1.readlines()

            with open(self.path_to_base + "/data/scary/functions/maze.mcfunction", "w") as f2:
                f2.writelines("spawnpoint\n")
                f2.writelines("give @a diamond_sword\n")
                f2.writelines("give @a diamond_chestplate\n")
                f2.writelines("give @a diamond_helmet\n")
                f2.writelines("give @a diamond_leggings\n")
                f2.writelines("give @a diamond_boots\n")
                f2.writelines("give @a cooked_porkchop 64\n")
                f2.writelines("effect give @a fire_resistance 5000\n")
                f2.writelines("gamerule sendCommandFeedback false\n")
                for i, line in enumerate(lines):
                    if i < 493:
                        f2.writelines(line)
                    elif i >= 493 and i < 1461:
                        line_new = line.split(" ")
                        line_new[2] = "~-1"
                        line_new[5] = "~-1"
                        line_new[7] = f"command_block{{Command:'{random.choice(action_list)}'}}"
                        line_new[8] = "replace grass_block\n"
                        line_new = " ".join(line_new)
                        f2.writelines(line_new)
                    elif i > 1462:
                        line_new = line.split(" ")
                        line_new[7] = "polished_blackstone_pressure_plate"
                        line_new = " ".join(line_new)
                        f2.writelines(line_new)

                f2.writelines("\nfill ~0 ~-1 ~0 ~40 ~-1 ~40 blackstone replace grass_block")
                f2.writelines("\nfill ~0 ~ ~0 ~40 ~ ~40 rail keep")

        self.copy_folder()

    def copy_folder(self):
        copy_tree(self.path_to_base, self.path_to_save)