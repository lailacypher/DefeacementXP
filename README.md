# DefeacementXP - Advanced Web Defacement Tool
  
## By: Laila19

### Features

- Web crawling and image scanning
- SQL injection testing
- SSH brute force attacks (for password auditing)
- Web shell upload capabilities
- Port scanning
- Website backup and restoration
- Comprehensive activity logging
- Multi-threaded operations
- Both SSH and web-based access methods

## Installation

### Prerequisites

- Python 3.6+
- Linux or macOS (Windows support via WSL)
- SSH client installed
- figlet for banner display

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DefaceMaster.git
cd DefaceMaster
```
Install required Python packages:

```bash
pip3 install -r requirements.txt
```
Install system dependencies (Debian/Ubuntu):

```bash
sudo apt-get install figlet sshpass
```
Prepare the environment:

```bash
chmod +x defacemaster.py
mkdir -p backups downloads uploads
```
Usage
Basic Operation
Start the tool:

```bash
./defacemaster.py
```
Enter the default password: supersecret (change this in the code before production use)

### Configure your target:

For SSH access: Use menu option 1

For web access: Use menu option 2

Common Workflows
Web Scanning and Defacement
Configure web target (menu option 2)

Crawl website to find images (menu option 4)

Replace identified images (menu option 5)

### SSH Access and Server Management

Configure SSH access (menu option 1)

Backup the website (menu option 8)

Upload a web shell (menu option 6)

Restore the website when done (menu option 9)

Security Testing
Perform SQL injection tests (menu option 5)

Run port scans (menu option 7)

Audit SSH credentials (menu option 3)

### Tutorial: Basic Website Assessment
Configure your target:

Select option 2 from main menu

Enter the target URL (e.g., http://testphp.vulnweb.com)

Skip authentication if not needed

### Scan for vulnerabilities:

Select option 4 to crawl the website

Select option 5 to test for SQL injection

Review results:

Check sql_injection.txt for vulnerabilities

Examine crawled_urls.txt for site structure

Clean up:

All activities are logged in various .txt files

Remove any test files uploaded during assessment

### Security Considerations
Always change the default password in the code

Use only on authorized systems

Remove all testing files after assessment

Review local laws before conducting any security testing

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
