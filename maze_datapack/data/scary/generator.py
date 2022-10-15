import random

action_list=["fill ~ ~2 ~ ~ ~2 ~ cobweb", "summon minecraft:zombie",
             "setblock ~ ~ ~ glowstone", "setblock ~ ~ ~ glowstone", "fill ~2 ~ ~ ~-2 ~10 ~-10 stone replace black_concrete",
             "fill ~2 ~ ~ ~-2 ~10 ~-10 granite replace black_concrete", "fill ~2 ~ ~ ~-2 ~10 ~-10 diorite replace black_concrete",
             "fill ~2 ~ ~ ~-2 ~10 ~-10 andesite replace black_concrete", "fill ~2 ~ ~ ~-2 ~10 ~-10 deepslate replace black_concrete",
             "effect give @a nausea 5", "summon minecraft:lightning_bolt ~-1 ~ ~"]

with open("functions/maze_black.mcfunction", "r") as f1:
    lines = f1.readlines()

    with open("functions/maze_v2.mcfunction", "w") as f2:
        f2.writelines("give @a iron_sword\n")
        for i, line in enumerate(lines):
            if i < 491:
                f2.writelines(line)
            elif i >= 491 and i < 1459:
                line_new = line.split(" ")
                line_new[2] = "~-1"
                line_new[5] = "~-1"
                line_new[7] = f"command_block{{Command:'{random.choice(action_list)}'}}"
                line_new[8] = "replace grass_block\n"
                line_new = " ".join(line_new)
                f2.writelines(line_new)
            elif i > 1460:
                line_new = line.split(" ")
                line_new[7] = "polished_blackstone_pressure_plate"
                line_new = " ".join(line_new)
                f2.writelines(line_new)

        f2.writelines("\nfill ~0 ~-1 ~0 ~40 ~-1 ~40 blackstone replace grass_block")
        f2.writelines("\nfill ~0 ~ ~0 ~40 ~ ~40 rail keep")