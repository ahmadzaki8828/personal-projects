# for the file to work as intended the file needs to be in the root directory of where you want to search
import os
import json
import shutil
from subprocess import PIPE, run
import sys

TARGET_DIR_WORD = "_game" #the word being search in each file name
FILE_TYPE = ".go" #used to find the type of files we want later used in the compile function
COMPILE_COMMAND = ["go", "build"]

def main(source, target):
    current_working_directory = os.getcwd()
    source_path = os.path.join(current_working_directory, source)
    target_path = os.path.join(current_working_directory, target)
    
    game_paths = find_all_game_paths(source_path)
    new_game_dirs = remove_word_from_paths(game_paths, TARGET_DIR_WORD)
    print(new_game_dirs)
    
    create_dir(target_path)
    for src, dest in zip(game_paths, new_game_dirs):
        destination_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, destination_path)
        compile_file(destination_path)
    
    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata(json_path, new_game_dirs)

if __name__ == "__main__":
    args = sys.argv
    # print(args)
    if len(args) != 3:
        if len(args) < 3:
            raise Exception("Target directory not specified")
        if len(args) > 3:
            raise Exception("Pass only source and target directory")

    source, target = sys.argv[1 :]
    # print(source, target)
    main(source,target)

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def find_all_game_paths(source): 
    game_paths = []
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if TARGET_DIR_WORD in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break #remove if you want the search to be recursively done and not only in the root directory
    return game_paths

def remove_word_from_paths(paths, word):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(word, "")
        new_names.append(new_dir_name)
    return new_names
        
def copy_and_overwrite(source, target):
    if os.path.exists(target):
         shutil.rmtree(target)
    shutil.copytree(source, target)

# more elements can be used to add more details
def make_json_metadata(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }
    with open(path, "w") as f:
        json.dump(data, f)
    
def compile_file(path):
    file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(FILE_TYPE):
                file_name = file
                break
        break
    if file_name is None:
        return
    
    command = COMPILE_COMMAND + [file_name]
    run_command(command, path)

def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)
    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True, shell=True) 
    print("compile result", result)
    os.chdir(cwd)

