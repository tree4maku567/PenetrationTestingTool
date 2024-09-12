import nmap
import csv
import io
import ipaddress
import time
from flask import Flask, request, render_template

app = Flask(__name__)
nm = nmap.PortScanner()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target_ip = request.form['target_ip']
    try:
        ipaddress.ip_address(target_ip)
    except ValueError:
        return "Invalid IP address.", 400

    results = {
        'progress': [],
        'scan_results': [],
        'vulnerabilities': {}
    }

    results['progress'].append("Starting scan...")
    start_time = time.time()
    try:
        scan_results = nmap_scan(target_ip)
        results['scan_results'] = scan_results
        duration = time.time() - start_time
        results['progress'].append(f"Scanning completed in {duration:.2f} seconds.")
    except Exception as e:
        results['progress'].append(f"Error during scan: {str(e)}")

    results['progress'].append("Checking for vulnerabilities...")
    try:
        vulnerabilities = check_vulnerabilities(target_ip)
        results['vulnerabilities'] = vulnerabilities
        if not vulnerabilities:
            results['progress'].append("No vulnerabilities found.")
        else:
            results['progress'].append("Vulnerabilities detected.")
    except Exception as e:
        results['progress'].append(f"Error checking vulnerabilities: {str(e)}")

    results['progress'].append("Scan completed.")

    return render_template('results.html', results=results)

def nmap_scan(ip):
    nm.scan(ip, arguments='-sV -p 1-9999 -n')
    csv_data = nm.csv()
    return parse_nmap_csv(csv_data)

def parse_nmap_csv(csv_data):
    data = io.StringIO(csv_data)
    reader = csv.DictReader(data, delimiter=';')

    results = []
    for row in reader:
        if 'state' in row and row['state'] == 'open':
            results.append({
                'host': row.get('host', 'N/A'),
                'port': row.get('port', 'N/A'),
                'name': row.get('name', 'N/A'),
                'product': row.get('product', 'N/A'),
                'version': row.get('version', 'N/A')
            })
    return results

def check_vulnerabilities(ip):
    open_ports = nm[ip]['tcp'].keys()
    vulnerabilities = {}
    for port in open_ports:
        search_results = metasploit_search(port)
        if search_results:
            vulnerabilities[port] = search_results
    return vulnerabilities

def metasploit_search(port):
    return {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
