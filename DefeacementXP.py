#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
MAGENTA='\033[1;35m'
NC='\033[0m'

if ! command -v figlet &> /dev/null
then
    echo -e "${RED}Figlet is not installed. Install with:${NC}"
    echo "sudo apt-get install figlet"
    exit 1
fi

clear
echo -e "${MAGENTA}"
figlet -f slant "DefacementXP"
echo -e "${NC}"

PASSWORD="supersecret"
echo -n "${YELLOW}Enter password to access panel: ${NC}"
read -s input_password
echo

if [ "$input_password" != "$PASSWORD" ]; then
    echo -e "${RED}Wrong password!${NC}"
    exit 1
fi

echo -e "${GREEN}Authentication successful!${NC}"

SSH_USER="root"
SSH_PORT="22"
TARGET_IP=""

menu() {
    echo -e "\n${MAGENTA}DefacementXP Panel${NC}"
    echo -e "${MAGENTA}1. Configure SSH connection"
    echo -e "2. Upload file to server"
    echo -e "3. Remove file from server"
    echo -e "4. View activity logs"
    echo -e "5. Explore server directories"
    echo -e "6. Interactive SSH access"
    echo -e "7. Execute remote command"
    echo -e "8. Transfer file via SCP"
    echo -e "9. Exit${NC}"
    echo -n "${MAGENTA}Choose an option: ${NC}"
    read option
    case $option in
        1)
            configure_ssh
            ;;
        2)
            upload_file
            ;;
        3)
            remove_file
            ;;
        4)
            view_logs
            ;;
        5)
            explore_dirs
            ;;
        6)
            ssh_access
            ;;
        7)
            remote_command
            ;;
        8)
            scp_transfer
            ;;
        9)
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option!${NC}"
            ;;
    esac
}

configure_ssh() {
    echo -e "\n${MAGENTA}SSH Configuration${NC}"
    echo -n "${MAGENTA}Target IP: ${NC}"
    read TARGET_IP
    echo -n "${MAGENTA}SSH User (default: root): ${NC}"
    read SSH_USER
    echo -n "${MAGENTA}SSH Port (default: 22): ${NC}"
    read SSH_PORT
    
    [ -z "$SSH_USER" ] && SSH_USER="root"
    [ -z "$SSH_PORT" ] && SSH_PORT="22"
    
    echo -e "${GREEN}Configuration saved:${NC}"
    echo -e "${MAGENTA}Target: ${SSH_USER}@${TARGET_IP}:${SSH_PORT}"
    echo "SSH config updated: ${SSH_USER}@${TARGET_IP}:${SSH_PORT} at $(date)" | tee -a logs.txt
}

upload_file() {
    check_config
    echo -n "${MAGENTA}Enter file path to upload: ${NC}"
    read file
    echo -n "${MAGENTA}Enter destination path on server: ${NC}"
    read destination
    scp -P $SSH_PORT "$file" "${SSH_USER}@${TARGET_IP}:${destination}"
    echo "File '$file' uploaded to '${SSH_USER}@${TARGET_IP}:${destination}'" | tee -a logs.txt
    echo -e "${GREEN}File uploaded successfully!${NC}"
}

remove_file() {
    check_config
    echo -n "${MAGENTA}Enter full file path to remove: ${NC}"
    read file_to_remove
    ssh -p $SSH_PORT "${SSH_USER}@${TARGET_IP}" "rm -v \"$file_to_remove\""
    echo "File '$file_to_remove' removed from ${TARGET_IP}" | tee -a logs.txt
    echo -e "${GREEN}File removed successfully!${NC}"
}

explore_dirs() {
    check_config
    echo -n "${MAGENTA}Enter directory path to explore: ${NC}"
    read path
    [ -z "$path" ] && path="/"
    ssh -p $SSH_PORT "${SSH_USER}@${TARGET_IP}" "ls -la \"$path\""
    echo "Explored directory $path on ${TARGET_IP}" | tee -a logs.txt
}

ssh_access() {
    check_config
    echo -e "${YELLOW}Starting interactive SSH session...${NC}"
    echo "SSH session started on ${TARGET_IP} at $(date)" | tee -a logs.txt
    ssh -p $SSH_PORT "${SSH_USER}@${TARGET_IP}"
    echo "SSH session ended on ${TARGET_IP} at $(date)" | tee -a logs.txt
    echo -e "${GREEN}SSH session ended.${NC}"
}

remote_command() {
    check_config
    echo -n "${MAGENTA}Enter command to execute on server: ${NC}"
    read command
    echo -e "${YELLOW}Executing command on server...${NC}"
    ssh -p $SSH_PORT "${SSH_USER}@${TARGET_IP}" "$command"
    echo "Command executed on ${TARGET_IP}: $command" | tee -a logs.txt
}

scp_transfer() {
    check_config
    echo -n "${MAGENTA}Enter remote file path: ${NC}"
    read remote_file
    echo -n "${MAGENTA}Enter local save path: ${NC}"
    read local_path
    scp -P $SSH_PORT "${SSH_USER}@${TARGET_IP}:${remote_file}" "$local_path"
    echo "File transferred from ${TARGET_IP}:${remote_file} to $local_path" | tee -a logs.txt
    echo -e "${GREEN}Transfer completed!${NC}"
}

view_logs() {
    echo -e "\n${MAGENTA}Activity Logs:${NC}"
    cat logs.txt 2>/dev/null || echo -e "${RED}No logs found.${NC}"
}

check_config() {
    if [ -z "$TARGET_IP" ]; then
        echo -e "${RED}Configure SSH access first (Option 1)!${NC}"
        menu
    fi
}

while true; do
    menu
done
