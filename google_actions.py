from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def login():
    """This function needs the credentials_module.json file created
    as the module pydrive states or as needed, in this case what we did
    with the file is to keep us loged in. The function will then ask for 
    google drive credentials, if the credentials were given it returns them."""
    credentials_file = 'credentials_module.json'
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = credentials_file
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credentials_file)
    if gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile(credentials_file)
    credentials = GoogleDrive(gauth)
    return credentials

def folder_creation(name):
    """This function assumes name, the parameter, as a string and creates a file with the
    parameter given in google drive"""
    credentials = login()
    folder = credentials.CreateFile({'title':name, 'mimeType' : 'application/vnd.google-apps.folder'})
    folder.Upload()

def get_id(name):
    """Asumes name as a string with the name of the file
    and returns the id of the specified file"""
    query = "title = '{}' and trashed = false".format(name)
    credentials = login()
    file_list = credentials.ListFile({'q': query}).GetList()
    if file_list == []:
        return []
    return file_list[0]['id']

def get_children_files(id):
    """Asumes id as a string with the id of the folder, the function returns as a list of
    dictionaries all the children files and folders of the folder previusly mentioned"""
    result = []
    credentials = login()
    query = "\'" + id + "\'" + " in parents and trashed=false"
    file_list = credentials.ListFile({'q': query}).GetList()
    for file in file_list:
        result.append({file['title']: file['id'], 'modified_date': file['modifiedDate']})
    return result

#print(list(get_children_files('1nOekW95qI6CU7Cu0G9BMYyYks-ajNkup')[0].keys())[0][:-4])

def upload_in_folder(id, path):
    """Receives the id of the google drive folder and the local file path to upload
    as strings, it uploads the file or overwrites it if the file name already exits in the
    google drive folder"""
    file_id = get_id(path)
    credentials = login()
    if file_id == []:    
        file = credentials.CreateFile({'parents': [{'id': id}]})
        file.SetContentFile(path)
        file.Upload()
        return file
    else:
        file = credentials.CreateFile({'id':file_id})
        file.SetContentFile(path)
        file.Upload()
        return file

