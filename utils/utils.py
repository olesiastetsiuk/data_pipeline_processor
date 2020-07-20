import hashlib
import json


def get_image_meta_files_path(folder_path, name):
    """
    Gets path to image and meta file
    """
    images = ''
    metas_files = ''
    return meta_file_path, image_file_path



def read_chunks(f, chunk_size=8192):
    """ 
    Reads potentially big file by chunks
    
    """
    while True:
        data = f.read(chunk_size)
        if not data:
            break
        yield data

def md5(f):
    """
    Obtains md5 hash function of file-like object
    
    """

    h = hashlib.md5()
    h.update(f)
    return h.hexdigest()


def parse_meta_json(f):
    """
    Gets meta data for an image, returns fields for statistics
    """
    pass


def update_json(data, meta_file_name):
    """
    Updates meta-file with new data
    """
    pass