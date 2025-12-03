#!/usr/bin/env python3
"""
Simple PsExec Wrapper for Windows
Direct subprocess call to PsExec
"""
import subprocess
import getpass
import sys
import os

def check_driver_simple(remote_pc, driver_name, username, password):
    """
    Directly call PsExec from Python
    """
    psexec_path = ".\\tools\\PsExec64.exe"
    
    if not os.path.exists(psexec_path):
        print(f"[✗] PsExec not found at {psexec_path}")
        return False
    
    # Build the command
    command = [
        psexec_path,
        "-accepteula",
        f"\\\\{remote_pc}",
        "-u", username,
        "-p", password,
        "driverquery", "/v", "/fo", "csv"
    ]
    
    print(f"[*] Running: {' '.join(command[:6])} ... [credentials hidden]")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout + result.stderr
        
        # Search for driver
        found = driver_name.lower() in output.lower()
        
        if result.returncode == 0:
            if found:
                print(f"\n[✓] Driver '{driver_name}' FOUND on {remote_pc}")
                # Print matching lines
                for line in output.split('\n'):
                    if driver_name.lower() in line.lower():
                        print(f"    {line}")
            else:
                print(f"\n[✗] Driver '{driver_name}' NOT FOUND on {remote_pc}")
        else:
            print(f"\n[✗] PsExec failed with exit code {result.returncode}")
            print(f"Error: {output}")
        
        return found
        
    except subprocess.TimeoutExpired:
        print("[✗] Command timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"[✗] Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Simple Remote Driver Checker")
    print("=" * 60)
    
    if sys.platform != "win32":
        print("[!] This script requires Windows")
        sys.exit(1)
    
    username = input("Username (DOMAIN\\username): ").strip()
    password = getpass.getpass("Password: ")
    remote_pc = input("Remote PC: ").strip()
    driver_name = input("Driver name (default: Touch): ").strip() or "Touch"
    
    check_driver_simple(remote_pc, driver_name, username, password)

if __name__ == "__main__":
    main()

