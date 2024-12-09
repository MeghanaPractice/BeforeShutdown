import os
import subprocess
import configparser
import shutil
import time

base_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_path, 'config.txt')
config = configparser.ConfigParser()
config.read_file(open(config_path))
RECALL_FOLDER = os.path.expandvars(config['DEFAULT']['RECALLFOLDER'])

def close_everything_else():
    ps1_script_path = os.path.join(
    base_path,
    "closeall.ps1"
   )
    try:
        powershell_command = [
        "powershell.exe",
        "-ExecutionPolicy", "Bypass",
        "-File", ps1_script_path,
        "-Verb RunAs"
        ]
        
        proc = subprocess.Popen(powershell_command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT
        )
        output, error = proc.communicate()
        print(output.decode('utf-8'))
    except Exception:
        print("Exception ",error.decode('utf-8'))
    
    finally:    
        if proc.returncode == 0:
         print("Closed everything else")
        else:
         print(f"Error with exit code {proc.returncode}")

def open_note():
    todaynote = RECALL_FOLDER+f'{time.strftime("%d_%m_%Y")}.txt'
    
    if(not os.path.exists(todaynote)):
       file = open(todaynote,mode='x+')
       shutil.copy(src='before_shutdown/template.txt',dst=todaynote)
       file.write('Date: '+time.strftime("%d.%m.%Y")+'\n')
       file.close()
    
    subprocess.Popen(
        ["notepad.exe", todaynote],
        shell=False,
        creationflags=subprocess.CREATE_NO_WINDOW
    )   
    #os.system("notepad.exe "+todaynote)



def main():
    close_everything_else()
    time.sleep(2)
    open_note()