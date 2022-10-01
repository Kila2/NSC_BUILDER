# coding=utf-8
from logging import root
import re
import os
import subprocess2
import ztools.lib.nutdb as nutdb

root_dir = os.path.dirname(__file__)
squirrel = os.path.join(root_dir, "ztools", "squirrel.py")
nutdb_dir = os.path.join(root_dir, "zconfig", "DB")
output_info_dir = os.path.join(root_dir, "INFO")


def get_contentname(app_id):
    regions = ["", "_America", "_Japan", "_Asia", "_Europe"]
    for region in regions:
        (name, publisher) = nutdb.get_contentname(
            app_id, nutdbfile=os.path.join(nutdb_dir, f"nutdb{region}.json"), roman=False)
        if name:
            return (name, publisher)
    return (False, False)


def get_dlcData(content_id):
    regions = ["", "_America", "_Japan", "_Asia", "_Europe"]
    for region in regions:
        (name, editor) = nutdb.get_dlcData(
            content_id, nutdbfile=os.path.join(nutdb_dir, f"nutdb{region}.json"))
        if name and editor:
            return (name, editor)
    return (False, False)


def get_info(file):
    ret = {}
    stdout = subprocess2.capture(
        f"set PYTHONIOENCODING=utf8 && python \"{squirrel}\" -o \"{output_info_dir}\" --translate TRUE --fw_req \"{file}\"").decode('utf-8')
    # print(stdout)
    # content_id
    match = re.search('CONTENT ID: (.*)\r\n', stdout)
    content_id = match.group(1)
    ret["content_id"] = content_id
    # base_id
    base_id = nutdb.get_baseid(content_id)
    ret["base_id"] = base_id
    # content_type
    match = re.search('Content type: (.*)\r\n', stdout)
    content_type = match.group(1)
    ret["content_type"] = content_type
    # name
    (name, publisher) = get_contentname(base_id)
    if name:
        ret["name"] = name
    if publisher:
        ret["editor"] = publisher
    if content_type == "DLC":
        match = re.search(r'- DLC number: (.*) \r\n', stdout)
        # dlc_number
        if match:
            ret["dlc_number"] = match.group(1)
    elif content_type == "Base Game or Application":
        # name
        if not name:
            match = re.search(r'- Name: (.*)\r\n', stdout)
            if match:
                ret["name"] = match.group(1)
    elif content_type == "Update":
        # name
        if not name:
            match = re.search(r'- Name: (.*)\r\n', stdout)
            if match:
                ret["name"] = match.group(1)
        # version
        match = re.search(r'- Version: (.*) \r\n', stdout)
        if match:
            ret["version"] = match.group(1)
        # display_version
        match = re.search(r'- Display Version: (.*)\r\n', stdout)
        if match:
            ret["display_version"] = match.group(1)
    else:
        os._exit(111)
    # editor
    if "editor" not in ret:
        match = re.search(r'- Editor: (.*)\r\n', stdout)
        if match:
            ret["editor"] = match.group(1)
    return ret


def verify(target):
    verfiy_result_path = f"{target}.verify"
    if not os.path.exists(verfiy_result_path):
        stdout = subprocess2.capture(
            f"set PYTHONIOENCODING=utf8 && python \"{squirrel}\" -o \"{output_info_dir}\" -v \"{target}\"").decode('utf-8')
        if str(stdout).find("CORRUPT") != -1:
            print(f"check ok {target}")
            with open(verfiy_result_path, encoding='utf-8',mode="w+") as filehandler:
                filehandler.write(stdout)
        else:
            print(f"check failed {target}")
            print(stdout)