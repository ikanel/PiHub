from os import listdir
import datetime
from os.path import isfile, join, getsize, getmtime


def get_folder_content(path):
    for f in listdir(path):
        fullname = join(path, f)
        is_file = isfile(fullname)
        size = getsize(fullname)
        date = datetime.datetime.fromtimestamp(getmtime(fullname)).isoformat()
        filename = f
        yield {"isDirectory": not is_file, "name": filename, "date": date, "size": size}
