#!/usr/bin/python3
import os
print("select build target...")
print("1. android (apk)")
print("2. web")
print("3. pack")
sel = input("[1-3]:")
if sel in ["1","2","3"]:
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
    pass
elif int(sel) == 3:
    os.system("flet pack main.py")