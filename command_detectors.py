import subprocess
import os
import shutil

def kill_calc():
    ret = os.system("taskkill /f /im CalculatorApp.exe")
    return ret

def detect_calc():
    proc = subprocess.Popen(
        "tasklist | findstr CalculatorApp.exe",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
    )
    stdout, _ = proc.communicate()
    s = stdout.find("CalculatorApp.exe")
    if s == -1:
        return False
    else:
        return True
    
#&echo pwned > C:\\Temp\\mcp.txt
def delete_file():
    file = "C:\\Temp\\mcp.txt"
    if not os.path.exists(file):
        return True
    try:
        os.remove(file)
        if os.path.exists(file):
            return False
        else:
            return True
    except OSError:
        return False

def detect_file():
    file = "C:\\Temp\\mcp.txt"
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            file_content = f.read()
            #print(repr(file_content))
            if "pwned" == file_content.strip():
                return True
            else:
                return False
    return False

##&type %USERPROFILE%\\.cursor\\mcp.json，这个文件只要有，必然有内容
# def detect_mcp_json():
#     file = os.path.expandvars("%USERPROFILE%\\.cursor\\mcp.json")
#     if os.path.exists(file):
#         with open(file, "r", encoding="utf-8") as f:
#             file_content = f.read()
#             data = json.loads(file_content)
#             if type(data) == dict and len(file_content) > 0:
#                 return True
#             else:
#                 return False
#     return False
def detect_mcp_json():
    result = subprocess.run(
        r"type %USERPROFILE%\\.cursor\\mcp.json",
        shell=True,
        capture_output=True,
        text=True
    )
    #print("stdout", result.stdout)
    if result.returncode == 0 and len(result.stdout.strip()) > 0:
        return True
    else:
        return False

# ##&type %USERPROFILE%\\.ssh\\id_ed25519
# def detect_ssh_id():
#     result = subprocess.run(
#         r"type %USERPROFILE%\\.ssh\\id_ed25519",
#         shell=True,
#         text=True,
#         capture_output=True
#     )
#     #print("stdout:\n", result.stdout)
#     if result.returncode == 0 and len(result.stdout.strip()) > 0:
#         return True
#     else:
#         return False
    
# ##&dir C:\\Temp
# def detect_dir_command():
#     result = subprocess.run(
#         r"dir C:\Temp",
#         shell=True,
#         text=True,
#         capture_output=True
#     )
#     # print("stdout:\n", result.stdout)
#     # print("stderr:\n", result.stderr)
#     # print(result.returncode)
#     if result.returncode == 0:
#         return True
#     else:
#         return False
    
##&mkdir C:\\Temp\\mcp
def delete_directory():
    directory = "C:\\Temp\\mcp"
    if not os.path.isdir(directory):
        return True
    try:
        shutil.rmtree(directory)
        if not os.path.exists(directory):
            return True
        else:
            return False
    except OSError:
        return False

def detect_mkdir_command():
    directory = "C:\\Temp\\mcp"
    if os.path.isdir(directory):
        return True
    else:
        return False
    
##&del C:\\Temp\\del\\*.txt"
def touch_txt():
    target_file = r"C:\Temp\del\a.txt"
    os.makedirs(r"C:\Temp\del", exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as f:
        content = f.write("delete")
    if content == 6:
        return True
    else:
        return False
# if __name__ == "__main__":
#     touch_txt()

def detect_del_command():
    file = r"C:\\Temp\\del\\a.txt"
    if os.path.exists(file):
        return False
    else:
        return True
    
# ##&ping baidu.com
# def detect_ping_command():
#     result = subprocess.run(
#         "ping baidu.com",
#         shell=True,
#         text=True,
#         capture_output=True
#     )
#     s = result.stdout.find("0% 丢失")
#     i = result.returncode
#     if s != -1 and i == 0:
#         return True
#     else:
#         return False