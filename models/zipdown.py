# -*- coding: utf-8 -*-

import os
import zipfile

def zipdown(get_files_path, zip_file_fullname):
    f = zipfile.ZipFile(zip_file_fullname, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(get_files_path):      
        fpath = dirpath.replace(get_files_path, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames: 
            f.write(os.path.join(dirpath, filename), fpath + filename)
    f.close()
    zip_done = True
    return zip_done
    
if __name__=='__main__':
    get_files_path = "..\\static\\certification\\"
    save_files_path = "..\\static\\download\\certification.zip"
    print zipdown(get_files_path, save_files_path)