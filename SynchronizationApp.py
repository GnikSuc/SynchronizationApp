# Program that synchronizes two folders: source and replica.
# The program should maintain a full, identical copy of source folder at replica folder. 

import os
import time
import shutil

# funkce na ukázku obsahu složky, kterou zavolám
def list_check(dir_path):

    dir_name = os.path.basename(dir_path)
    print(f"Files in {dir_path}:")

    if not os.path.isdir(dir_path):
        print(f"Error: {dir_path} is not a valid directory.")

    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
    
        if os.path.isfile(item_path):
            file_size = os.path.getsize(item_path)
            file_name = os.path.basename(item_path)
            file_date = time.strftime("%Y-%m-%d %H:%M:%S",(time.localtime(os.path.getmtime(item_path))))

            print(f"{dir_name} - {file_name} (size: {file_size}, date: {file_date});")

        else:
            return
    print()

# funkce pro vyhledání souboru v zadané složce a vrací její cestu, pokud je nalezena.
def find_file_in_list(file_name, dir_path):
    
    for item in os.listdir(dir_path):
        if item == file_name:
            return os.path.join(dir_path, item)
    return 


# Compare two files by modification time and content
def compare_files(src_path, rep_path):
    
    # Compare file modification times
    src_mtime = os.path.getmtime(src_path)
    rep_mtime = os.path.getmtime(rep_path)
    if src_mtime != rep_mtime:
        return False
    
    # Compare file size
    src_size = os.path.getsize(src_path)
    rep_size = os.path.getsize(rep_path)
    if src_size != rep_size:
        return False

    return True


# funkce pro odstranění souborů, které nejsou v source adresáři
def delete_files():
    ss


# funkce synchronizace 
def synchronization(src_dir, rep_dir):  

    if not os.path.isdir(src_dir):
        print("Error: source path is not a valid directory.")
        return

    if not os.path.isdir(rep_dir):
        print("Error: replica path is not a valid directory.")
        return
    
    counter = 0

    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        rep_item = os.path.join(rep_dir, item)
        file_name = os.path.basename(src_item)

        found_file = find_file_in_list(file_name, rep_dir)
        if not found_file == None:
            compared_file = compare_files(src_item, found_file)
        else:
            compared_file = False

        if compared_file == False:
            counter += 1
            src_file_name = os.path.basename(src_item)
            rep_dir_name = os.path.basename(rep_dir)
            shutil.copy2(src_item, rep_item)

    if counter == 1:
        print(f"{counter} file added.")
    elif counter != 0:
        print(f"{counter} files added.")
    else:
        print("No files added.")



source = "C:/Users/Herní mašina/Documents/Visual studio code/Python/Veeam task/source"
replica = "C:/Users/Herní mašina/Documents/Visual studio code/Python/Veeam task/replica"

print()
list_check(source)
list_check(replica)

def main_loop():
    
    try:
        while True:
            print("Starting synchronization...")
            synchronization(source, replica)
            print("Synchronization complete. Waiting for 20 seconds... []\n")
            time.sleep(20)
    except KeyboardInterrupt:
        print("Goodbye!\n")
        pass

if __name__ == "__main__":
    main_loop()

