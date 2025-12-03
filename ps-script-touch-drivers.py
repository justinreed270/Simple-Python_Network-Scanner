from pypsrp.client import Client
import getpass
import csv

def check_touch_drivers(computer_name, username, password):
    try:
        client = Client(computer_name, username=username, password=password, ssl=False)
        
        # PowerShell script to check for touch drivers
        ps_script = """
        $drivers = Get-CimInstance Win32_PnPSignedDriver | Where-Object {$_.DeviceName -like '*touch*' -or $_.DeviceName -like '*HID*'}
        if($drivers){
            $drivers | Select-Object DeviceName, DriverVersion, Manufacturer | ConvertTo-Json
        } else {
            '[]'
        }
        """
        
        output, streams, had_errors = client.execute_ps(ps_script)
        
        if output:
            import json
            drivers = json.loads(output)
            return {
                'computer': computer_name,
                'status': 'success',
                'drivers': drivers
            }
        else:
            return {
                'computer': computer_name,
                'status': 'no_drivers',
                'drivers': []
            }
    except Exception as e:
        return {
            'computer': computer_name,
            'status': 'error',
            'error': str(e)
        }

# Prompt user for credentials
print("=== Touch Driver Check Tool ===\n")
username = input("Enter AD username (e.g., AD\\username): ")
password = getpass.getpass("Enter password: ")

# Get list of computers to check
print("\nEnter computer names (one per line, press Enter twice when done):")
computers = []
while True:
    computer = input()
    if computer == "":
        break
    computers.append(computer)

if not computers:
    print("No computers entered. Exiting.")
    exit()

# Check each computer
print(f"\nChecking {len(computers)} computer(s)...\n")
print("-" * 80)

results = []
for computer in computers:
    print(f"Checking {computer}...", end=" ")
    result = check_touch_drivers(computer, username, password)
    results.append(result)
    
    if result['status'] == 'success':
        print(f"✓ Found {len(result['drivers'])} touch driver(s)")
        for driver in result['drivers']:
            print(f"  • {driver.get('DeviceName', 'Unknown')}")
            print(f"    Version: {driver.get('DriverVersion', 'N/A')}")
            print(f"    Manufacturer: {driver.get('Manufacturer', 'N/A')}")
    elif result['status'] == 'no_drivers':
        print("✗ No touch drivers found")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")
    
    print()

# Summary
print("-" * 80)
print("\nSummary:")
success_count = sum(1 for r in results if r['status'] == 'success')
no_drivers_count = sum(1 for r in results if r['status'] == 'no_drivers')
error_count = sum(1 for r in results if r['status'] == 'error')

print(f"  Successful checks: {success_count}")
print(f"  No drivers found: {no_drivers_count}")
print(f"  Errors: {error_count}")

# Export to CSV
print("\nExporting results to CSV...")
with open('touch_drivers_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Computer', 'Status', 'Driver Count', 'Drivers'])
    for result in results:
        driver_names = '; '.join([d.get('DeviceName', '') for d in result.get('drivers', [])])
        writer.writerow([
            result['computer'],
            result['status'],
            len(result.get('drivers', [])),
            driver_names
        ])

print("✓ Results exported to touch_drivers_results.csv")
print("\nDone!")
