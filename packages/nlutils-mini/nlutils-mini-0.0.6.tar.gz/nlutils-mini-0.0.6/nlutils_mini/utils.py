import os
import inspect
import subprocess
from hashlib import md5

## CONSTANTS
DEFAULT_LOG_PATH = "nlutils/logs"


def convert_tolistible_object_to_list(obj):
    for k, v in obj.items():
        if type(v) is dict:
            obj[k] = convert_tolistible_object_to_list(v)
        else:
            if "tolist" in dir(v):
                obj[k] = v.tolist()
    return obj


def merge_files():
    whole_text = "["
    for root, _, files in os.walk(DEFAULT_LOG_PATH):
        for file in files:
            if file.endswith(".json"):
                if "fail" not in os.path.abspath(os.path.join(root, file)):
                    with open(os.path.join(root, file), "r") as f:
                        whole_text += f.read() + ","
    whole_text = whole_text[:-1] + "]"
    with open("all_log.json", "w") as f:
        f.write(whole_text)


def generate_MD5(obj):
    md5_obj = md5()
    md5_obj.update(obj.encode("utf8"))
    return md5_obj.hexdigest()


def retrieve_var_name(var):
    for fi in reversed(inspect.stack()):
        names = [
            var_name
            for var_name, var_val in fi.frame.f_locals.items()
            if var_val is var
        ]
        if len(names) > 0:
            return names[0]


def retrieve_commit_id():
    return subprocess.getoutput("git log -1 | grep commit | awk '{print $2}'")
