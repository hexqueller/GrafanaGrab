import os

def create_dir(script_dir):
    folder = "/data"
    os.makedirs(script_dir+folder, exist_ok=True)
    log_file = check_log_file(script_dir+folder)
    return script_dir+folder, log_file

def check_log_file(path):
    file = "/log.txt"
    file_path = path+file
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            pass
    return file_path

def logging(log_file, string_to_append):
    with open(log_file, 'r') as file:
        file_content = file.read()

    if string_to_append not in file_content:
        with open(log_file, 'a') as file:
            file.write('\n' + string_to_append)
