import os
import subprocess
import configparser
import shutil
import time
import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

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
       shutil.copy(src=os.path.join(base_path, 'template.txt'),dst=todaynote)
       file.write('Date: '+time.strftime("%d.%m.%Y")+'\n')
       file.close()
    
    subprocess.Popen(
        ["notepad.exe", todaynote],
        shell=False,
        creationflags=subprocess.CREATE_NO_WINDOW
    )   
    mail_prompter(todaynote)

def send_mail(file):
    print("Button clicked!")
    sender = config['DEFAULT']['MAIL_FROM']
    reciever =config['DEFAULT']['MAIL_TO']
    senderpass = config['DEFAULT']['MAIL_FROM_PASSWORD']
    smtp_host=config['DEFAULT']['SMTP_HOST']
    smtp_port=config['DEFAULT']['SMTP_PORT']
    loading_window = tk.Toplevel()
    loading_window.title("Sending Email")
    loading_label = tk.Label(loading_window, text="Sending email, please wait...")
    loading_label.pack(pady=10)
    if(config['DEFAULT']['SEND_MAIL']=='TRUE' and sender and reciever and senderpass):
        try:
            s = smtplib.SMTP(smtp_host, smtp_port)
            s.starttls()
            s.ehlo()
            s.login(sender,senderpass)
            msg = EmailMessage()
            msg['Subject'] = 'Notes for the day: '+time.strftime("%d.%m.%Y")
            msg['From'] = sender
            msg['To'] = reciever
            with open(file, 'r+') as fp:
                notes_data = fp.read()
                msg.add_attachment(notes_data,subtype='plain',filename=os.path.basename(file))
            
            s.send_message(msg,sender,reciever)
            time.sleep(2)
            s.quit()
            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")
        finally:
            loading_window.destroy()    
    else:
        messagebox.showerror("Error", "Email configuration is incomplete!")


def send_selected_file():
    file = filedialog.askopenfilename(initialdir=RECALL_FOLDER, title="Select a file",filetypes=[("Text files","*.txt")])
    if file:
        send_mail(file)
    else:
        messagebox.showwarning("No File", "No file selected!")

def mail_prompter(todaynote):
    root = tk.Tk()
    root.title("Mail sender")
    send_button = tk.Button(root, text="Save and send today's note?", command=lambda: send_mail(todaynote), width=40,)
    send_selected_button = tk.Button(root, text="Send Selected File", command=send_selected_file, width=40,)
    send_selected_button.pack(pady=5)
    send_button.pack(pady=5)
    root.mainloop()
    
def main():
    close_everything_else()
    time.sleep(2)
    open_note()