# coding=utf-8
import os  # nopep8
import sys  # nopep8
sys.path.append(os.path.join(os.path.dirname(__file__), "ztools", "lib"))  # nopep8
import nsc_builder
import shutil
import glob
import json

config = json.loads(open(f"{os.path.dirname(__file__)}/.config.json",encoding='utf-8').read())
input_dir = config.get("input_dir")
output_dir = config.get("game_dir")
assert(input_dir != None)
assert(output_dir != None)
other_category_dir = os.path.join(output_dir, "other")
os.makedirs(other_category_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

editor_mapper = None
editor_category_db_path = os.path.join(os.path.dirname(
    __file__), "ztools", "editor_category_db.json")
with open(editor_category_db_path, encoding='utf-8') as fd:
    editor_mapper = json.loads(fd.read())

cn_name_db = None
editor_category_db_path = os.path.join(os.path.dirname(
    __file__), "ztools", "cn_name_db.json")
with open(editor_category_db_path, encoding='utf-8') as fd:
    cn_name_db = json.loads(fd.read())

ignore_editor = ["Game Source Entertainment"]


def getFiles(dir):
    os.chdir(dir)
    files = [os.path.join(dir, x)
             for x in glob.glob("**/*.nsp", recursive=True)]
    files += [os.path.join(dir, x)
              for x in glob.glob("**/*.xci", recursive=True)]
    files += [os.path.join(dir, x)
              for x in glob.glob("**/*.nsz", recursive=True)]
    return files


def category():
    editor_dirs = os.listdir(output_dir)
    for editor_dir in editor_dirs:
        editor_dir = os.path.join(output_dir, editor_dir)
        os.chdir(editor_dir)
        game_dirs = os.listdir(editor_dir)
        if len(game_dirs) < 3:
            for game_dir in game_dirs:
                game_dir = os.path.join(editor_dir, game_dir)
                if os.path.exists(other_category_dir):
                    for file in os.listdir(game_dir):
                        src_file = os.path.join(game_dir, file)
                        dest_dir = os.path.join(other_category_dir, os.path.basename(game_dir))
                        shutil.move(src_file, dest_dir)
                else:
                    shutil.move(game_dir, other_category_dir)


def auto_manager():
    files = getFiles(input_dir)
    for file in files:
        if os.path.isfile(file):
            print(file)
            info = nsc_builder.get_info(file)
            editor = info.get("editor")
            if editor in ignore_editor:
                print(f"ignore_editor:{info}")
                continue
            if editor is None or editor not in editor_mapper:
                print(f"editor:{editor}")
                continue
            editor = editor_mapper.get(editor)
            dest_dir = os.path.join(output_dir, editor)
            name = cn_name_db.get(info.get('base_id'))
            if name is None:
                print(f"no_cn_name:{info}")
                continue
            fmt_str = f"{name} [{info.get('base_id') or info.get('content_id')}]"
            dest_dir = os.path.join(dest_dir, fmt_str)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(file, dest_dir)


if __name__ == '__main__':
    auto_manager()
    category()
