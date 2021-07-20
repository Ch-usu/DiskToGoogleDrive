import file_actions
import google_actions
import os
import time
from dateutil.parser import parse
from pytz import timezone

def reset_disk():
    """Writes on the csv file disk No"""
    file_actions.write_csv({'disk':'No'})

def  reset_folder():
    """writes on the csv file folder_name No"""
    file_actions.write_csv({'folder_name':'No'})

def reset_id():
    """writes on the csv file id No"""
    file_actions.write_csv({'id':'No'})

def manage_disk_actions():
    """This function manages the disk selection it works with
    2 cases
    1) If there is a file defaults.csv it either asks the user to chosse a disk
    and returns a list of the files in the disk chossen or just returns the list of the
    files chossen before and registered in the disk.csv
    2) If there is not a file disk.csv it creates it and asks the user to chosse a disk
    (The No string in the csv file indicates that there is not a file chossen)"""
    disks = file_actions.get_disks()
    if os.path.exists('defaults.csv')  and 'disk' in file_actions.read_csv().keys():
        if 'No' in file_actions.read_csv()['disk']:
            disk_name = file_actions.get_disk_name(disks)
            files = file_actions.get_disk_files(disk_name)
            return files
        else:
            csv = file_actions.read_csv()
            files = file_actions.get_disk_files(csv['disk'])
            return files
    else:
        reset_disk()
        files = manage_disk_actions()
        return files

def manage_drive_actions():
    """This function manages the google drive selection it works with
    2 cases
    1) If there is a file defaults.csv it either asks the user to chosse a disk
    and returns a list of the files in the disk chossen or just returns the list of the
    files chossen before and registered in the disk.csv
    2) If there is not a file disk.csv it creates it and asks the user to chosse a disk
    (The No string in the csv file indicates that there is not a file chossen)"""
    if os.path.exists('defaults.csv') and 'id' in file_actions.read_csv().keys():
        if 'No' in file_actions.read_csv()['id']:
            folder_name = input('Inserte el nombre del archivo en el que se hara el respaldo: ')
            google_actions.folder_creation(folder_name)
            file_actions.write_csv({'folder_name':folder_name})
            folder_id = google_actions.get_id(folder_name)
            file_actions.write_csv({'id':folder_id})
            children_files = google_actions.get_children_files(folder_id)
            return children_files
        else:
            folder_id = file_actions.read_csv()['id']
            children_files = google_actions.get_children_files(folder_id)
            return children_files
    else:
        reset_id()
        reset_folder()
        children_files = manage_drive_actions()
        return children_files

def manage_uploads():
    """This function gets the localfiles info of the specified disk and the drive files info
    of the google drive specified folder, compares its files and uploads the new files, or updates
    the files that exist but that needs to be modified"""
    upload_count = 0
    local_files = manage_disk_actions()
    drive_files = manage_drive_actions()
    csv_file = file_actions.read_csv()
    disk = csv_file['disk']
    folder_id = csv_file['id']
    folder_name = csv_file['folder_name']
    drive_file_names = [list(x.keys())[0] for x in drive_files if drive_files != []]
    for file in local_files:
        dir_path = ''
        path = os.path.join(disk + ':/', file)
        if file_actions.file_limitter(path) > 1073741824:
            continue
        filetime = parse(time.ctime(os.path.getmtime(path)))
        utcfiletime = filetime.replace(tzinfo = timezone('UTC'))
        if os.path.isdir(path):
            dir_path = path
            path = file_actions.zip_file(file)
        if path in drive_file_names:
            drive_file = [x for x in drive_files if path in list(x.keys())][0]
            drive_file_time = parse(drive_file['modified_date'])
            #the 14400 is due to the time difference between bolivia and the location of the 
            #data in googledrive
            if utcfiletime.timestamp() + 14400 > drive_file_time.timestamp() :
                google_actions.upload_in_folder(folder_id,path)
                upload_count += 1
                print('The {} file has been updated'.format(path))
                if os.path.isdir(dir_path):
                    os.remove(path)
            elif os.path.isdir(dir_path):
                os.remove(path)
        else:
            google_actions.upload_in_folder(folder_id,path)
            upload_count += 1
            print('The {} file has been uploaded'.format(path))
            if os.path.isdir(dir_path):
                os.remove(path)
    print('{} files have been uploaded to {} folder'.format(upload_count, folder_name))

if __name__ == "__main__":
    manage_uploads()