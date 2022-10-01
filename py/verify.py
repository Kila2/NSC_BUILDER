# coding=utf-8
import os  # nopep8
import sys  # nopep8
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "ztools", "lib"))  # nopep8
import nsc_builder

config = json.loads(open(f"{os.path.dirname(__file__)}/.config.json",encoding='utf-8').read())
input_dir = config.get("game_dir")
assert(input_dir != None)

def verify():
    editor_dirs = os.listdir(input_dir)
    for editor_dir in editor_dirs:
        editor_dir = os.path.join(input_dir, editor_dir)
        os.chdir(editor_dir)
        game_dirs = os.listdir(editor_dir)
        for game_dir in game_dirs:
            game_dir = os.path.join(editor_dir, game_dir)
            for file in os.listdir(game_dir):
                file_path = os.path.join(game_dir, file)
                print(f"verify {file_path}")
                nsc_builder.verify(file_path)

if __name__ == '__main__':
    verify()
