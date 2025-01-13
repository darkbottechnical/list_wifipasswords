import subprocess
import platform
import sys
import os

def getOs():
    try:
        os = platform.system()
        return os
    except Exception as e:
        print(f"Sorry, this script was designed to run on Windows.")
        sys.exit()
        
def getPass(profile):
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8').split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        return results
    except subprocess.CalledProcessError:
        print(f"Error: Could not retrieve password for profile '{profile}'.")
        return []

def getProfiles():
    try:
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
        profiles = [i.split(":")[1][1:-1] for i in result if "All User Profile" in i]
        return profiles
    except subprocess.CalledProcessError:
        print("Error: Could not retrieve Wi-Fi profiles.")
        return []

def getAllPass():
    profiles = getProfiles()
    if not profiles:
        print("No Wi-Fi profiles found.")
        return
    for profile in profiles:
        try:
            password = getPass(profile)[0]
        except IndexError:
            password = "NONE"
        print(f"""
 >> Network found: {profile}
\tPassword: {password}
""")

def getCurrentProfile():
    try:
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8').split('\n')
        profile = [i.split(":")[1][1:-1] for i in result if "Profile" in i and "Connection mode" not in i]
        return profile
    except subprocess.CalledProcessError:
        print("Error: Could not retrieve current Wi-Fi profile.")
        return []

def main():
    if not getOs() == 'Windows':
        print("Sorry, this script was designed to only run on Windows. Terminating...")
        sys.exit()
    print(
"""
██╗    ██╗██╗  ████████╗ ██████╗  ██████╗ ██╗     
██║    ██║██║  ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██║ █╗ ██║██║     ██║   ██║   ██║██║   ██║██║     
██║███╗██║██║     ██║   ██║   ██║██║   ██║██║     
╚███╔███╔╝███████╗██║   ╚██████╔╝╚██████╔╝███████╗
 ╚══╝╚══╝ ╚══════╝╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
"""
    )
    print("Stable v1.0.0 by TechnicalHazard")
    print("Type 'help' for a list of commands.")
    while True:
        cmd = input(" << ").strip().lower()
        if not cmd:
            continue
        parts = cmd.split()
        maincmd = parts[0].lower()
        if maincmd == 'exit':
            break
        elif maincmd == 'get':
            toget = parts[1] if len(parts) > 1 else None
            
            if toget is None:
                print("No action specified. Type 'help' for commands.")
            elif toget == 'keys' or toget == 'key':
                profile = parts[2] if len(parts) > 2 else None
                if profile is None:
                    print("Please provide a profile name or the SSID of the Wi-Fi network, or 'all' to get all stored Wi-Fi passwords.")
                    continue
                if profile == 'all':
                    getAllPass()
                else:
                    try:
                        password = getPass(profile)[0]
                    except IndexError:
                        password = "NONE"
                    print(f"""
 >> Network found: {profile}
\tPassword: {password}
                    """)
            elif toget == 'profile' or toget == 'profiles':
                option = parts[2] if len(parts) > 2 else None
                if option is None:
                    print("Please specify 'current' or 'all'.")
                    continue
                if option == 'current':
                    results = getCurrentProfile()
                    print(f"Current profiles: {results}")
                elif option == 'all':
                    results = getProfiles()
                    for result in results:
                        print(f"Stored profile: {result}")
        elif maincmd == 'clear':
            try:
                os.system("cls")
            except Exception as e:
                print(f"Error clearing screen: {e}")
        elif maincmd == 'help':
            print(" >> Commands:\n\tget keys <profile>|all - Gets the password for a specific profile or all.\n\tget profile <current>|all - Gets the current profiles or all.\n\thelp - Show help. \n\tclear - Clears the screen.\n\texit - Exits the program.")
            

if __name__ == '__main__':
    main()
