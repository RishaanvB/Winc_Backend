__winc_id__ = "ae539110d03e49ea8738fd413ac44ba8"
__human_name__ = "files"

import os, shutil, os.path
from zipfile import ZipFile


# opdracht 1 clean_cache


def clean_cache():
    """
    Creates new cache dir in current dir.
    If already exists, removes all files and folders in cache dir
    """
    print("\nInitializing clean_cache")
    cache_folder = "cache"
    list_dir = os.listdir()

    if cache_folder in list_dir:
        if len(os.listdir(cache_folder)) == 0:
            print(f"Directory {cache_folder} is empty")
        else:
            print("Cache directory found.")
            print(f"Removing all files and folders from {cache_folder} directory")

        for filename in os.listdir(cache_folder):
            file_path = os.path.join(cache_folder, filename)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.unlink(file_path)

    else:
        print("No cache directory found, creating new cache directory...")
        os.mkdir(cache_folder)
        print(f"Created {cache_folder} directory!")


# opdracht 2 cache_zip


def cache_zip(zipfile_path, cache_dir_path):
    """
    takes a zip file path (str) and a cache dir path (str)
    then unpacks the 1st arg into 2nd arg.
    """
    print("\nInitializing extraction!!!")
    clean_cache()
    with ZipFile(zipfile_path) as zipObject:
        print(f"Extracting files into {cache_dir_path}. Please wait... ")
        zipObject.extractall(path=cache_dir_path)
        print("Extraction done!!!")


# cache_zip("D:\\WincBackend\\files\\data.zip", "D:\\WincBackend\\files\\cache")
# opdracht 3 cached_files


def cached_files():
    """
    returns a list of all the files in absolute terms located in cache.
    folders are skipped

    """
    print("\nInitializing cached_files")

    cache_folder = os.path.join(os.getcwd(), "cache")
    cache_list = []
    for filename in os.listdir(cache_folder):
        file_path = os.path.join(
            cache_folder, filename
        )  # zelfde als abs_path ???  waarom?
        abs_path = os.path.abspath(file_path)
        if os.path.isdir(file_path):
            print(f"Folder detected! Skipping folder: {filename}")
        else:
            cache_list.append(abs_path)
    print("All files cached!")
    return cache_list


# cached_files()


def find_password(file_paths):
    print("Checking for password...")
    print("...")
    print("...")
    print("...")
    for file in file_paths:
        with open(file) as file_data:
            file_datalist = file_data.readlines()
            for target in file_datalist:
                if "password" in target:
                    password = target.split(" ")[-1].strip()
                    print("Password found!!")
                    print(f"Password is---> {password}")
                    return password


# find_password(cached_files())
