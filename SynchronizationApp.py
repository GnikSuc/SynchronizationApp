# Program that synchronizes two folders: source and replica.
# The program should maintain a full, identical copy of source folder at replica folder. 

import os
import time
import shutil
from datetime import datetime
import logging


 # (Aditional feature)
"""
def list_check(dir_path, nr, space):

    sub_dir = os.path.basename(dir_path)
    for i in range(1, nr):
        space += " "

    if not os.path.isdir(dir_path):
        print(f"Error: {dir_path} is not a valid directory.")

    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
    
        if os.path.isfile(item_path):
            item_size = os.path.getsize(item_path)
            item_name = os.path.basename(item_path)
            item_date = time.strftime("%Y-%m-%d %H:%M:%S",(time.localtime(os.path.getmtime(item_path))))
            print(f"{space}> {sub_dir} - {item_name} (size: {item_size}, date: {item_date})")
        elif os.path.isdir(item_path):
            item_name = os.path.basename(item_path)
            print(f"{space}> {item_name} (folder)")
            nr += 1
            list_check(item_path, nr, space)
        else:
            break
    print()
"""

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

        # Item part
        if not os.path.isdir(src_item):
            if not found_item:
                compared_file = False
            else:
                compared_file = compare_files(src_item, found_item)

            if compared_file == False:
                shutil.copy2(src_item, rep_item)
                print(f" > Coppied item: '{item_name}' to directory: '{rep_dir}'")
                logger.info(f" > Coppied item: '{item_name}' to directory: '{rep_dir}'")

        # Folder part
        else:
            if not found_item:
                os.mkdir(rep_item)
                print(f" > Created directory: '{rep_item}'")
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
                compared_file = compare_files(rep_item, found_item)

            if compared_file == False:
                os.remove(rep_item)
                print(f" > Removed item: '{item_name}' in directory: '{rep_dir}'")
                logger.info(f" > Removed item: '{item_name}' in directory: '{rep_dir}'")
        else:
            if not found_item:
                shutil.rmtree(rep_item)
                print(f" > Removed directory: '{rep_item}'")
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
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(message)s'
    )


def main_loop():

    # Prompt the user for both paths
    source = str(input("\nEnter full source directory: "))
    replica = str(input("Enter full replica directory: "))

    # Prompt the user for the log file path
    log_file_path = input("Enter the name for the log file (e.g. C:/app/logfile.log): ")
    setup_logging(log_file_path)
    logger = logging.getLogger("SyncApp")
    logger.info("Sychronization application started.")

    # Prompt the user for sync interval in seconds
    time_sync = int(input("Enter synchronization interval (seconds): "))
    logger.info(f"Sychronization interval was set to {time_sync} seconds.")

    # (Aditional feature)
    """
    print("\n___Source & replica list:___\n")
    nr = 1
    space = ""
    list_check(source, nr, space)
    list_check(replica, nr, space)
    """
    print()

    try:
        while True:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"Starting synchronization... [{now}]")
            remove_redundant_files(source, replica, logger)
            synchronization(source, replica, logger)
            print(f"Synchronization complete.\nRepeat in {time_sync} seconds. (press CTRL+C to end)\n")
            time.sleep(time_sync)
    except KeyboardInterrupt:
        print("Goodbye!\n")
        logger.info("Sychronization application ended.")
        pass

if __name__ == "__main__":
    main_loop()