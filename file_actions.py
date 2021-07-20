import win32api
import csv
import os
import shutil
import pathlib

def read_csv():
    """Reads the default csv file called 'defaults.csv'.
    Returns a dictionary of all the defaults"""
    with open('defaults.csv', newline='') as file:
        read_file = csv.DictReader(file)
        file_dictionary = list(read_file)
        if file_dictionary == []:
            return {}
        return file_dictionary[0]

def write_csv(new_dictionary):
    """Receives as a parameter a dictionary, and writes to csv file
    'defaults.csv' the new dictionary appended to the information written
    before"""
    if os.path.exists('defaults.csv'):
        actual_dictionary = read_csv()
    else:
        actual_dictionary = {}
    with open('defaults.csv','w',newline='') as file:
        if(list(new_dictionary.keys())[0] in actual_dictionary.keys()):
            del actual_dictionary[list(new_dictionary.keys())[0]]
            fieldnames = list(actual_dictionary.keys()) + list(new_dictionary.keys())
            writer = csv.DictWriter(file, fieldnames = fieldnames)
            writer.writeheader()
            row = actual_dictionary
            row.update(new_dictionary)
            writer.writerow(row)
        else:
            fieldnames = list(actual_dictionary.keys()) + list(new_dictionary.keys())
            writer = csv.DictWriter(file, fieldnames = fieldnames)
            writer.writeheader()
            row = actual_dictionary
            row.update(new_dictionary)
            writer.writerow(row)

def get_disks():
    """Returns a list with the current disks in the system"""
    discosStr = win32api.GetLogicalDriveStrings()
    discosList = [x for x in discosStr if x.isalpha()]
    return discosList

def get_disk_files(disk):
    """Receives the name of the disk chossen and returns a list of files
    inside of it"""
    path = '{}:'.format(disk)
    files = os.listdir(path)
    not_important = ['$RECYCLE.BIN','System Volume Information']
    for f in not_important:
        if f in files:
            files.remove(f)
    return files

def get_disk_name(disks):
    """Receives a list of the actual disks
    in the pc and asks you to input one of them, returns
    the input. If the input is not in the list the prosess will be repeated"""
    for disk in disks:
        print(disk)
    disk = input('Por favor inserte el nombre del disco a respaldar: ')
    if disk in disks:
        write_csv({'disk':disk})
        return disk
    else: 
        disk = get_disk_name(disks)
        return disk

def zip_file(name):
    """This function creates a new ziped file
    with the same name of file to be ziped"""
    disk = read_csv()['disk']
    path = os.path.join(disk + ':', name)
    current_dir = os.getcwd()
    os.chdir(disk + ':')
    try:    
        shutil.make_archive(path,'zip',path)
    except OSError as err:
        print(err)
    os.chdir(current_dir)
    return path + '.zip'

