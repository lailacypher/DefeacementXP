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

def check_ssh_connection():
    try:
        # Test SSH connection with a simple command that should work on any Linux
        result = subprocess.run(
            f"ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} 'echo \"Testing connection\"'",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        if result.returncode == 0:
            print(f"{GREEN}Access Granted{NC}")
            return True
        else:
            print(f"{RED}Access Denied{NC}")
            return False
    except:
        print(f"{RED}Access Denied{NC}")
        return False

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

# Hardcoded SSH credentials (change these to your actual credentials)
SSH_USER = "root"
SSH_PORT = "22"
TARGET_IP = "192.168.1.100"  # Change to your target IP

# Verify SSH connection immediately after authentication
print(f"\n{YELLOW}Testing SSH connection to {SSH_USER}@{TARGET_IP}:{SSH_PORT}...{NC}")
if not check_ssh_connection():
    print(f"{RED}Cannot continue without SSH access.{NC}")
    sys.exit(1)

def upload_file():
    file = input(f"{MAGENTA}Enter file path to upload: {NC}")
    destination = input(f"{MAGENTA}Enter destination path on server: {NC}")
    if check_ssh_connection():
        os.system(f"scp -P {SSH_PORT} {file} {SSH_USER}@{TARGET_IP}:{destination}")
        with open("logs.txt", "a") as log_file:
            log_file.write(f"File '{file}' uploaded to '{SSH_USER}@{TARGET_IP}:{destination}'\n")
        print(f"{GREEN}File uploaded successfully!{NC}")

def remove_file():
    file_to_remove = input(f"{MAGENTA}Enter full file path to remove: {NC}")
    if check_ssh_connection():
        os.system(f'ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} "rm -v \\"{file_to_remove}\\""')
        with open("logs.txt", "a") as log_file:
            log_file.write(f"File '{file_to_remove}' removed from {TARGET_IP}\n")
        print(f"{GREEN}File removed successfully!{NC}")

def explore_dirs():
    path = input(f"{MAGENTA}Enter directory path to explore: {NC}") or "/"
    if check_ssh_connection():
        os.system(f'ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} "ls -la \\"{path}\\""')
        with open("logs.txt", "a") as log_file:
            log_file.write(f"Explored directory {path} on {TARGET_IP}\n")

def ssh_access():
    print(f"{YELLOW}Starting interactive SSH session...{NC}")
    if check_ssh_connection():
        with open("logs.txt", "a") as log_file:
            log_file.write(f"SSH session started on {TARGET_IP} at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}\n")
        os.system(f"ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP}")
        with open("logs.txt", "a") as log_file:
            log_file.write(f"SSH session ended on {TARGET_IP} at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}\n")
        print(f"{GREEN}SSH session ended.{NC}")

def remote_command():
    command = input(f"{MAGENTA}Enter command to execute on server: {NC}")
    if check_ssh_connection():
        print(f"{YELLOW}Executing command on server...{NC}")
        os.system(f'ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} "{command}"')
        with open("logs.txt", "a") as log_file:
            log_file.write(f"Command executed on {TARGET_IP}: {command}\n")

def scp_transfer():
    remote_file = input(f"{MAGENTA}Enter remote file path: {NC}")
    local_path = input(f"{MAGENTA}Enter local save path: {NC}")
    if check_ssh_connection():
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

def menu():
    while True:
        print(f"\n{MAGENTA}DefacementXP Panel{NC}")
        print(f"{MAGENTA}Target: {SSH_USER}@{TARGET_IP}:{SSH_PORT}")
        print("1. Upload file to server")
        print("2. Remove file from server")
        print("3. Explore server directories")
        print("4. Interactive SSH access")
        print("5. Execute remote command")
        print("6. Transfer file via SCP")
        print("7. View activity logs")
        print("8. Exit{NC}")
        option = input(f"{MAGENTA}Choose an option: {NC}")
        if option == "1":
            upload_file()
        elif option == "2":
            remove_file()
        elif option == "3":
            explore_dirs()
        elif option == "4":
            ssh_access()
        elif option == "5":
            remote_command()
        elif option == "6":
            scp_transfer()
        elif option == "7":
            view_logs()
        elif option == "8":
            sys.exit(0)
        else:
            print(f"{RED}Invalid option!{NC}")

if __name__ == "__main__":
    menu()
