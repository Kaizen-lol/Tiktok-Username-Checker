import os
import requests
from colorama import init, Fore
import msvcrt
import ctypes

init(convert=True)

tag = f"""
{Fore.MAGENTA} 
 _   __      _                 _  _  _____ _____ 
| | / /     (_)              _| || ||_   _|_   _|
| |/ /  __ _ _ _______ _ __ |_  __  _|| |   | |  
|    \ / _` | |_  / _ \ '_ \ _| || |_ | |   | |  
| |\  \ (_| | |/ /  __/ | | |_  __  _|| |   | |  
\_| \_/\__,_|_/___\___|_| |_| |_||_|  \_/   \_/  
{Fore.RESET}
"""

class Checker: 
    available_count = 0
    unavailable_count = 0
    total_checks = 0
    recent_checks = []

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def create_dir(directory: str) -> bool:
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except OSError as e:
            print(f"{Fore.RED}[ERROR]{Fore.RESET} Could not create directory {directory}: {e}")
            return False

    @staticmethod
    def create_file(directory: str, filename: str) -> None:
        try:
            filepath = os.path.join(directory, filename)
            with open(filepath, 'w') as f:
                f.write('')
        except OSError as e:
            print(f"{Fore.RED}[ERROR]{Fore.RESET} Could not create file {filepath}: {e}")

    @staticmethod
    def add_username(filepath: str, username: str) -> None:
        try:
            with open(filepath, 'a') as f:
                f.write(f"{username}\n")
        except OSError as e:
            print(f"{Fore.RED}[ERROR]{Fore.RESET} Could not write to file {filepath}: {e}")
    
    @staticmethod
    def setup() -> bool:
        if Checker.create_dir("data"):
            Checker.create_file("data", "available.txt")
            Checker.create_file("data", "not_available.txt")
            return True 
        else:
            return False
        
    @staticmethod
    def check_username(username: str) -> bool: 
        try:
            url = f"https://www.tiktok.com/@{username}"
            response = requests.get(url)
            if '"followerCount":' in response.text:
                return False
            else:
                return True
        except:
            return False

    @staticmethod
    def update_title():
        title = f"Available: {Checker.available_count} | Not Available: {Checker.unavailable_count} | Checks done: {Checker.total_checks} | Press X to stop"
        ctypes.windll.kernel32.SetConsoleTitleW(title)

    @staticmethod
    def print_summary():
        print(f"\n{Fore.CYAN}Summary:")
        print(f"Total checks done: {Checker.total_checks}")
        print(f"Available usernames: {Checker.available_count}")
        print(f"Not available usernames: {Checker.unavailable_count}{Fore.RESET}")

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(tag)
        for check in Checker.recent_checks:
            print(check)

if __name__ == "__main__":
    Checker.clear_console()
    
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")
    usernames_path = os.path.join(current_dir, "usernames.txt")
    print(f"Looking for usernames.txt at: {usernames_path}")
    
    if not os.path.exists(usernames_path):
        print(f"{Fore.RED}[ERROR]{Fore.RESET} usernames.txt file does not exist at the specified location: {usernames_path}")
    else:
        Checker.setup()
        available_file = os.path.join("data", "available.txt")
        not_available_file = os.path.join("data", "not_available.txt")
        
        try:
            with open(usernames_path, "r") as f:
                lines = f.readlines()
                if not lines:
                    raise Exception(f"{Fore.RED}[ERROR]{Fore.RESET} File is empty, please add some usernames.")
                else:
                    for line in lines:
                        if msvcrt.kbhit() and msvcrt.getch().decode('utf-8').lower() == 'x':
                            print(f"{Fore.YELLOW}Exiting...{Fore.RESET}")
                            break

                        if line.strip():
                            Checker.total_checks += 1
                            result = Checker.check_username(line.strip())
                            
                            if result:
                                Checker.available_count += 1
                                check_message = f"{Fore.GREEN} https://www.tiktok.com/@{line.strip()}{Fore.RESET}"
                                Checker.add_username(available_file, line.strip())
                                
                            else:
                                Checker.unavailable_count += 1
                                check_message = f"{Fore.RED} https://www.tiktok.com/@{line.strip()}{Fore.RESET}"
                                Checker.add_username(not_available_file, line.strip())
                            
                            Checker.recent_checks.append(check_message)
                            if len(Checker.recent_checks) > 5:
                                Checker.recent_checks.pop(0)
                            
                            Checker.update_title()
                            Checker.clear_console()
                    
                    Checker.print_summary()
                                
        except FileNotFoundError:
            print(f"{Fore.RED}[ERROR]{Fore.RESET} Please create a usernames.txt file.")
