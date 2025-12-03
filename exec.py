import subprocess
from pathlib import Path
import sys
import getpass

def find_driver_on_remote(remote_pc, driver_name, psexec_path, username, password):
    """Query remote PC for specific driver using provided credentials"""
    try:
        result = subprocess.run(
            [
                str(psexec_path),
                "-accepteula",
                f"\\\\{remote_pc}",
                "-u", username,
                "-p", password,
                "driverquery"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return False, f"Error: {result.stderr}"
        
        if driver_name.lower() in result.stdout.lower():
            return True, result.stdout
        return False, result.stdout
        
    except PermissionError:
        return False, "Permission denied. Check credentials and try again."
    except subprocess.TimeoutExpired:
        return False, "Timeout connecting to remote PC"
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    script_dir = Path(__file__).parent
    psexec_path = script_dir / "tools" / "PsExec64.exe"
    
    if not psexec_path.exists():
        print(f"Error: PsExec64.exe not found at {psexec_path}")
        print("Please download from https://docs.microsoft.com/en-us/sysinternals/downloads/psexec")
        sys.exit(1)
    
    # Prompt for credentials
    print("Enter your Active Directory credentials:")
    username = input("Username (format: DOMAIN\\username or username@domain.com): ").strip()
    password = getpass.getpass("Password: ")
    
    # Validate username format
    if not username:
        print("Error: Username cannot be empty")
        sys.exit(1)
    
    # Add domain prefix if not provided
    if "\\" not in username and "@" not in username:
        domain = input("Enter domain (e.g., 'ad'): ").strip()
        username = f"{domain}\\{username}"
    
    remote_pc = input("\nEnter remote PC name or IP: ")
    driver_name = input("Enter driver name to search for (default: HID-Compliant Touch Driver): ").strip()
    
    if not driver_name:
        driver_name = "HID-Compliant Touch Driver"
    
    print(f"\nSearching for '{driver_name}' on {remote_pc}...")
    print(f"{username} \n")
    print(f"{password}")
#    exit()


    found, output = find_driver_on_remote(remote_pc, driver_name, psexec_path, username, password)
    
    if found:
        print(f"✓ Driver '{driver_name}' FOUND on {remote_pc}")
    else:
        print(f"✗ Driver '{driver_name}' NOT FOUND on {remote_pc}")
    
    show_full = input("\nShow full driver list? (y/n): ").lower()
    if show_full == 'y':
        print("\n" + output)

if __name__ == "__main__":
    main()
