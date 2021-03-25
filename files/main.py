__winc_id__ = "ae539110d03e49ea8738fd413ac44ba8"
__human_name__ = "files"

import os, shutil, zipfile, os.path
from zipfile import ZipFile


# opdracht 1 clean_cache
# ?mss tempfile mod gebruiken om cache te maken???


def clean_cache():
    """
    Creates new cache dir in current dir.
    If already exists, removes all files and folders in cache dir
    """

    cache_folder = "cache"
    folder = "D:\\WincBackend\\files"  # folder variable verwijderen voor inleveren
    working_dir = os.getcwd()
    list_dir = os.listdir()
    if working_dir == folder:

        if cache_folder in list_dir:
            if len(os.listdir(cache_folder)) == 0:
                print(f"{cache_folder} directory is empty")
            else:
                print("Cache directory found.")
                print(f"removing all files and folders from {cache_folder} directory")

            for filename in os.listdir(cache_folder):
                file_path = os.path.join(cache_folder, filename)
                if os.path.isdir(file_path):
                    print(f"removing folder {file_path} and its content")
                    shutil.rmtree(file_path)
                else:
                    os.unlink(file_path)

        else:
            print("No cache directory found, creating new cache directory...")
            os.mkdir(cache_folder)
            print(f"{cache_folder} directory created!")

    else:
        print("You are not allowed to clean cache bro :P")


# opdracht 2 cache_zip


def cache_zip(zipfile_path, cache_dir_path):
    """
    takes a zip file path (str) and a cache dir path (str)
     as arguments,in that order.
     The function then unpacks the indicated
     zip file into a clean cache folder.
    """
    clean_cache()
    with ZipFile(zipfile_path) as zipObject:
        print(f"extracting files into {cache_dir_path}. Please wait... ")
        zipObject.extractall(path=cache_dir_path)
        print("extraction done!!!")


test_zipfile = os.path.join(os.getcwd(), "data.zip")
cache_folder = os.path.join(os.getcwd(), "cache")

# cache_zip(test_zipfile, cache_folder)


# opdracht 3 cached_files


def cached_files():
    """
    returns a list of all the files in absolute terms located in cache.
    folders are skipped

    """
    cache_folder = os.path.join(os.getcwd(), "cache")
    cache_list = []
    for filename in os.listdir(cache_folder):
        file_path = os.path.join(
            cache_folder, filename
        )  # zelfde als abs_path ???  waarom?
        abs_path = os.path.abspath(file_path)
        if os.path.isdir(file_path):
            print(f"Folder detected! Skipping folder: {filename}")
            # continue
        else:
            print(f"caching.. {filename}")
            cache_list.append(abs_path)
    print("All files cached!")
    return cache_list


cached_files()