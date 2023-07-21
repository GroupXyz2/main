# BadIP - Version 2.0 - Creator: GroupXyz - Credit: The PC Security Channel (https://www.youtube.com/watch?v=7UWFJGeix_E)
# Blocks Botnet IPs with Windows Defender Firewall
# For Windows and Windows Server
# Windoof

import requests
import csv
import subprocess
from pathlib import Path

def backup_csv_to_file(csv_content, filename):
    try:
        print("CSV Content:")
        print(csv_content)
        file_path = Path(__file__).resolve().parent / filename
        with file_path.open('w', encoding="utf-8") as backup_file:
            backup_file.write(csv_content)
        print("Backup successful.")
    except Exception as e:
        print(f"Error while creating backup: {e}")

def download_ip_addresses():
    return requests.get("https://feodotracker.abuse.ch/downloads/ipblocklist.csv").text

def print_valid_ip_addresses(csv_content):
    print("Downloaded IP addresses:")
    mycsv = csv.reader(filter(lambda x: not x.startswith("#"), csv_content.splitlines()))
    for row in mycsv:
        ip = row[1]
        if all(c.isdigit() or c == '.' for c in ip):
            print(ip)
        else:
            print("Invalid IP address:", ip)


def delete_existing_rules():
    rule_outbound = "netsh advfirewall firewall delete rule name='BadIP_Outbound'"
    rule_inbound = "netsh advfirewall firewall delete rule name='BadIP_Inbound'"
    subprocess.run(["Powershell", "-Command", rule_outbound])
    subprocess.run(["Powershell", "-Command", rule_inbound])

def add_blocking_rules(csv_content):
    mycsv = csv.reader(filter(lambda x: not x.startswith("#"), csv_content.splitlines()))
    for row in mycsv:
        ip = row[1]
        if all(c.isdigit() or c == '.' for c in ip):
            rule_outbound = f"netsh advfirewall firewall add rule name='BadIP_Outbound' Dir=Out Action=Block RemoteIP={ip}"
            rule_inbound = f"netsh advfirewall firewall add rule name='BadIP_Inbound' Dir=In Action=Block RemoteIP={ip}"
            subprocess.run(["Powershell", "-Command", rule_outbound])
            subprocess.run(["Powershell", "-Command", rule_inbound])
            print("Added Rule to block:", ip)

def rollback_rules_from_backup():
    rollback_confirmation = input("Do you want to rollback to the previous rules? THIS OPTION IS ONLY NECESSARY IF THERE ARE ERRORS IN THE CURRENT (yes/no): ")
    if rollback_confirmation.lower() == 'yes':
        rollback_confirmation2 = input("really? THIS WILL UNDO EVERY CHANGE!!! (yes/no): ")
        if rollback_confirmation2.lower() == 'yes':
            with open('ipblocklist_backup.txt', 'r') as backup_file:
                for ip in backup_file:
                    ip = ip.strip()
                    rule_outbound = f"netsh advfirewall firewall add rule name='BadIP_Outbound' Dir=Out Action=Block RemoteIP={ip}"
                    rule_inbound = f"netsh advfirewall firewall add rule name='BadIP_Inbound' Dir=In Action=Block RemoteIP={ip}"
                    subprocess.run(["Powershell", "-Command", rule_outbound])
                    subprocess.run(["Powershell", "-Command", rule_inbound])
                    print("Added Rule to block:", ip)

def main():
    print("BadIP - Version 2.0 - Creator: GroupXyz - Credit: The PC Security Channel (https://www.youtube.com/watch?v=7UWFJGeix_E)")
    csv_content = download_ip_addresses()
    print_valid_ip_addresses(csv_content)

    confirmation = input("Do you want to proceed and add the blocking rules? (yes/no): ")
    if confirmation.lower() == 'yes':
        delete_existing_rules()
        add_blocking_rules(csv_content)

        rollback_rules_from_backup()

        backup_confirmation = input("Do you want to backup the current Rules? (yes/no): ")
        if backup_confirmation.lower() == 'yes':
            backup_csv_to_file(csv_content, 'ipblocklist_backup.txt')

        subprocess.run(["pause"], shell=True)
    else:
        print("Operation canceled. No rules were added.")
        subprocess.run(["pause"], shell=True)

if __name__ == "__main__":
    main()
