# Penetration Testing Tool

Requirements:
- Python
- Nmap
- Metasploit
- Flask

This tool performs basic penetration testing by scanning a specified host to identify running services and their versions. It then cross-references these findings with the Metasploit database to check for potential vulnerabilities.

Installation:
- Clone the repository to your server with: `git clone https://github.com/Red-Blink/PenetrationTestingTool.git`
- Navigate to the directory with: `cd PenetrationTestingTool`
- Start the app by running: `python3 -m app`
- Open a web browser and go to `http://PUBLIC_IP:5000`

Notes:
- The app allows external access via your public IP address.
- It operates on port 5000. Ensure this port is open in your firewall settings if applicable.
- The tool scans ports up to 9999 by default. To increase this limit, edit the `app.py` file.
