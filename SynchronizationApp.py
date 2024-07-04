# Program that synchronizes two folders: source and replica.
# The program should maintain a full, identical copy of source folder at replica folder. 

import os
import shutil
import time
from datetime import datetime
import hashlib
import logging

import click


# Actual time
def actual_time():
    time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return time_now


# Function for findng item in list
def find_item_in_list(item_name, dir_path):
    
    for item in os.listdir(dir_path):
        if item == item_name:
            return os.path.join(dir_path, item)
    return 


# Function for comparing two files by modification time and cize
def compare_files(dir_path1, dir_path2):

    # Compare file modification times
    src_mtime = os.path.getmtime(dir_path1)
    rep_mtime = os.path.getmtime(dir_path2)
    if src_mtime != rep_mtime:
        return False
    
    # Compare file size
    src_size = os.path.getsize(dir_path1)
    rep_size = os.path.getsize(dir_path2)
    if src_size != rep_size:
        return False
    return True


# Function for 
def compute_md5(file_path):
    # Compute the md5 hash of item
    hash_md5 = hashlib.md5()
    # Opening file in binary mode
    with open(file_path, "rb") as f:
        # Read the file in chunks of 6144 bytes until the end of the file is reached
        for chunk in iter(lambda: f.read(6144), b""):
            # Update the hash object with the bytes of the current chunk
            hash_md5.update(chunk)
    # Return the hexadecimal representation of the digest (the computed hash)
    return hash_md5.hexdigest()


# Synchronization function
def synchronization(src_dir, rep_dir, logger):  

    # Ensuring that both paths are available
    if not os.path.isdir(src_dir):
        print("Error: source path is not a valid directory.")
        return
    if not os.path.isdir(rep_dir):
        print("Error: replica path is not a valid directory.")
        return

    # Working with each item/folder
    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        rep_item = os.path.join(rep_dir, item)
        item_name = os.path.basename(src_item)
        found_item = find_item_in_list(item_name, rep_dir)

        # Item copy/rewrite part
        if not os.path.isdir(src_item):
            if not found_item:
                shutil.copy2(src_item, rep_item)
                print(f" > Copied file: '{item_name}' to directory: '{rep_dir}' [{actual_time()}]")
                logger.info(f" > Copied file: '{item_name}' to directory: '{rep_dir}'")
            else:
                if compute_md5(src_item) == compute_md5(found_item):
                    continue
                else:
                    shutil.copy2(src_item, rep_item)
                    print(f"Overwritten file: '{item_name}' (didn't match source), directory: '{rep_dir}' [{actual_time()}]")
                    logger.info(f"Overwritten file: '{item_name}' (didn't match source), directory: '{rep_dir}'")

        # Folder part
        else:
            if not found_item:
                os.mkdir(rep_item)
                print(f" > Created directory: '{rep_item}' [{actual_time()}]")
                logger.info(f" > Created directory: '{rep_item}'")
            synchronization(src_item, rep_item, logger)


# Function for removing files in replica directory that is missing in source directory
def remove_redundant_files(src_dir, rep_dir, logger):
    
    for item in os.listdir(rep_dir):
        src_item = os.path.join(src_dir, item)
        rep_item = os.path.join(rep_dir, item)
        item_name = os.path.basename(rep_item)
        found_item = find_item_in_list(item_name, src_dir)

        if not os.path.isdir(rep_item):
            if not found_item:
                compared_file = False   
            else:
                if compute_md5(src_item) == compute_md5(found_item):
                    compared_file = True
                else:
                    compared_file = False             

            if compared_file == False:
                os.remove(rep_item)
                print(f" > Removed item: '{item_name}' in directory: '{rep_dir}' [{actual_time()}]")
                logger.info(f" > Removed item: '{item_name}' in directory: '{rep_dir}'")
        else:
            if not found_item:
                shutil.rmtree(rep_item)
                print(f" > Removed directory: '{rep_item}' [{actual_time()}]")
                logger.info(f" > Removed directory: '{rep_item}'")
            else:
                remove_redundant_files(src_item, rep_item, logger)


# Log file settings
def setup_logging(log_file_path):

    # Ensure the directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(message)s'
    )


@click.command()  # Decorator to define a Click command
@click.option(
    "-s",  # Short option flag
    "--source",  # Long option flag
    prompt="Source folder",  # Prompt text to display if the option is not provided
    type=click.Path(exists=True, file_okay=False, dir_okay=True)  # Option type with validation
)
@click.option(
    "-r",
    "--replica",
    prompt="Replica folder",
    type=click.Path(exists=False, file_okay=False, dir_okay=True, readable=True, writable=True),
)
@click.option(
    "-i",
    "--interval",
    prompt="Synchornization interval",
    type=click.DateTime(formats=["%H:%M:%S"]),
)
@click.option(
    "-lf",
    "--log-file-path",
    prompt="Log file path",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, readable=True, writable=True),
)


def main(source, replica, interval, log_file_path: str):

    setup_logging(log_file_path)
    logger = logging.getLogger("SyncApp")
    logger.info("Sychronization application started.")

    interval_seconds = (interval - datetime(1900, 1, 1)).total_seconds()
    logger.info(f"Sychronization interval was set to {interval_seconds} seconds.")

    print()

    try:
        while True:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"Starting synchronization... [{actual_time()}]")
            remove_redundant_files(source, replica, logger)
            synchronization(source, replica, logger)
            print(f"Synchronization complete. [{actual_time()}]\nRepeat in {interval_seconds} seconds. (press CTRL+C to end)\n")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("Goodbye!\n")
        logger.info("Sychronization application ended.")
        pass


if __name__ == "__main__":
    main()