#!/usr/bin/env python3
import os
import sys
import subprocess
import getpass
from time import gmtime, strftime

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
PURPLE = '\033[0;35m'
CYAN = '\033[0;36m'
MAGENTA = '\033[1;35m'
NC = '\033[0m'

try:
    subprocess.check_call(["which", "figlet"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    print(f"{RED}Figlet is not installed. Install with:{NC}")
    print("sudo apt-get install figlet")
    sys.exit(1)

os.system("clear")
print(f"{MAGENTA}")
os.system('figlet -f slant "DefacementXP"')
print(f"{NC}")

PASSWORD = "supersecret"
input_password = getpass.getpass(f"{YELLOW}Enter password to access panel: {NC}")

if input_password != PASSWORD:
    print(f"{RED}Wrong password!{NC}")
    sys.exit(1)

print(f"{GREEN}Authentication successful!{NC}")

SSH_USER = "root"
SSH_PORT = "22"
TARGET_IP = ""

def configure_ssh():
    global TARGET_IP, SSH_USER, SSH_PORT
    print(f"\n{MAGENTA}SSH Configuration{NC}")
    TARGET_IP = input(f"{MAGENTA}Target IP: {NC}")
    SSH_USER = input(f"{MAGENTA}SSH User (default: root): {NC}") or "root"
    SSH_PORT = input(f"{MAGENTA}SSH Port (default: 22): {NC}") or "22"
    print(f"{GREEN}Configuration saved:{NC}")
    print(f"{MAGENTA}Target: {SSH_USER}@{TARGET_IP}:{SSH_PORT}")
    with open("logs.txt", "a") as log_file:
        log_file.write(f"SSH config updated: {SSH_USER}@{TARGET_IP}:{SSH_PORT} at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}\n")

def upload_file():
    check_config()
    file = input(f"{MAGENTA}Enter file path to upload: {NC}")
    destination = input(f"{MAGENTA}Enter destination path on server: {NC}")
    os.system(f"scp -P {SSH_PORT} {file} {SSH_USER}@{TARGET_IP}:{destination}")
    with open("logs.txt", "a") as log_file:
        log_file.write(f"File '{file}' uploaded to '{SSH_USER}@{TARGET_IP}:{destination}'\n")
    print(f"{GREEN}File uploaded successfully!{NC}")

def remove_file():
    check_config()
    file_to_remove = input(f"{MAGENTA}Enter full file path to remove: {NC}")
    os.system(f'ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} "rm -v \\"{file_to_remove}\\""')
    with open("logs.txt", "a") as log_file:
        log_file.write(f"File '{file_to_remove}' removed from {TARGET_IP}\n")
    print(f"{GREEN}File removed successfully!{NC}")

def explore_dirs():
    check_config()
    path = input(f"{MAGENTA}Enter directory path to explore: {NC}") or "/"
    os.system(f'ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} "ls -la \\"{path}\\""')
    with open("logs.txt", "a") as log_file:
        log_file.write(f"Explored directory {path} on {TARGET_IP}\n")

def ssh_access():
    check_config()
    print(f"{YELLOW}Starting interactive SSH session...{NC}")
    with open("logs.txt", "a") as log_file:
        log_file.write(f"SSH session started on {TARGET_IP} at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}\n")
    os.system(f"ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP}")
    with open("logs.txt", "a") as log_file:
        log_file.write(f"SSH session ended on {TARGET_IP} at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}\n")
    print(f"{GREEN}SSH session ended.{NC}")

def remote_command():
    check_config()
    command = input(f"{MAGENTA}Enter command to execute on server: {NC}")
    print(f"{YELLOW}Executing command on server...{NC}")
    os.system(f'ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} "{command}"')
    with open("logs.txt", "a") as log_file:
        log_file.write(f"Command executed on {TARGET_IP}: {command}\n")

def scp_transfer():
    check_config()
    remote_file = input(f"{MAGENTA}Enter remote file path: {NC}")
    local_path = input(f"{MAGENTA}Enter local save path: {NC}")
    os.system(f"scp -P {SSH_PORT} {SSH_USER}@{TARGET_IP}:{remote_file} {local_path}")
    with open("logs.txt", "a") as log_file:
        log_file.write(f"File transferred from {TARGET_IP}:{remote_file} to {local_path}\n")
    print(f"{GREEN}Transfer completed!{NC}")

def view_logs():
    print(f"\n{MAGENTA}Activity Logs:{NC}")
    try:
        with open("logs.txt", "r") as log_file:
            print(log_file.read())
    except FileNotFoundError:
        print(f"{RED}No logs found.{NC}")

def check_config():
    if not TARGET_IP:
        print(f"{RED}Configure SSH access first (Option 1)!{NC}")
        menu()

def menu():
    while True:
        print(f"\n{MAGENTA}DefacementXP Panel{NC}")
        print(f"{MAGENTA}1. Configure SSH connection")
        print("2. Upload file to server")
        print("3. Remove file from server")
        print("4. View activity logs")
        print("5. Explore server directories")
        print("6. Interactive SSH access")
        print("7. Execute remote command")
        print("8. Transfer file via SCP")
        print("9. Exit{NC}")
        option = input(f"{MAGENTA}Choose an option: {NC}")
        if option == "1":
            configure_ssh()
        elif option == "2":
            upload_file()
        elif option == "3":
            remove_file()
        elif option == "4":
            view_logs()
        elif option == "5":
            explore_dirs()
        elif option == "6":
            ssh_access()
        elif option == "7":
            remote_command()
        elif option == "8":
            scp_transfer()
        elif option == "9":
            sys.exit(0)
        else:
            print(f"{RED}Invalid option!{NC}")

if __name__ == "__main__":
    menu()
