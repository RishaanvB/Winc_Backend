__winc_id__ = "ae539110d03e49ea8738fd413ac44ba8"
__human_name__ = "files"

import os, shutil, zipfile, os.path
from zipfile import ZipFile


# opdracht 1 clean_cache


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
                print(f"removing all files and folders from {cache_folder} directory")

            for filename in os.listdir(cache_folder):
                file_path = os.path.join(cache_folder, filename)
                if os.path.isdir(file_path):
                    print(f"removing folder {file_path} and its content")
                    shutil.rmtree(
                        file_path
                    )  # removes files/ (not linked files, didnt really understand what those are supposed to be)
                else:
                    print(f"removing {file_path}")
                    os.unlink(
                        file_path
                    )  # removes all dirs with content and subsequent dirs

        else:
            print(
                f"No cache directory found, creating directory with name {cache_folder}..."
            )
            os.mkdir(cache_folder)
            print(f"{cache_folder} directory created!")

    else:
        print("You are not allowed to clean cache bro :P")


# opdracht 2 cache_zip
cache_folder = os.path.join(os.getcwd(), "cache")
zipfile_path = os.path.join(os.getcwd(), "data.zip")


def cache_zip(zipfile_path, cache_dir_path):
    clean_cache()  # cleans cache first or creates new cache dir before extracting
    zipfile_path = os.path.join(cache_folder, zipfile_path)
    print(zipfile.is_zipfile(zipfile_path), "print if is zipfile")

    with ZipFile(zipfile_path) as zipObject:
        zipObject.extractall(path=cache_dir_path)


cache_zip(zipfile_path, cache_folder)
