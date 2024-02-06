#!/usr/bin/python3
import os
import requests
import pathlib
import zipfile
import io
print("select option...")
print("1. android (apk)")
print("2. web")
print("3. pack")
print("4. download dependancys")
sel = input("[1-4]:")
if sel in ["1","2","3","4"]:
    pass
else:
    print("bad selection!")
    exit()
if int(sel) == 1:
    print("read version...")
    f = open("version")
    version = f.read()
    f.close()
    command = "".join([
        "flet build apk ",
        "--project Toonify ",
        "--product Toonify ",
        "--copyright mitLicense ",
        "-vv ",
        f"--build-version {version} ",
        "--org ca.hugie999"
    ])
    os.system(command)
elif int(sel) == 2:
    raise NotImplementedError
elif int(sel) == 3:
    os.system("flet pack main.py")
elif int(sel) == 4:
    print("not implemented yet sorry")
    raise NotImplementedError
    #fix later
    print("please wait...")
    tempdir = pathlib.Path("./temp/")
    if not tempdir.is_dir():
        tempdir.mkdir()
    print("getting FletNavigator... (v2.5.5) (https://github.com/xzripper/flet_navigator/archive/refs/tags/v2.5.5.zip)")
    req = requests.get("https://github.com/xzripper/flet_navigator/archive/refs/tags/v2.5.5.zip").content
    zip = zipfile.ZipFile(io.BytesIO(req))
    print(zip.filelist)
    print("extract...")
    zip.extract(zip.getinfo("flet_navigator-2.5.5/flet_navigator/__init__.py"),"./extradepends/flet_navigator/")
    
    