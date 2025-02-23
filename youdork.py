import os
import json
import sys
import time
import platform
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore, Style

DATABASE_FILE = "dork_database.json"
LOG_DIR = "logs"
LOGGING = False 

CATEGORY_MAPPING = {
    "name": ["Files Containing Juicy Info", "Files Containing Usernames", "Sensitive Directories"],
    "username": ["Files Containing Usernames", "Files Containing Juicy Info", "Sensitive Directories"],
    "email": ["Files Containing Email Addresses", "Files Containing Juicy Info", "Sensitive Directories"],
    "phone": ["Files Containing Juicy Info", "Sensitive Directories"],
    "filetype": ["Files Containing Juicy Info", "Sensitive Directories"],
    "ip": ["Network or Vulnerability Data"],
    "domain": ["Sensitive Directories"],
    "crypto": ["Files Containing Juicy Info"],
    "social": ["Files Containing Usernames"],
    "tech": ["Web Server Detection"],
    "address": ["Files Containing Juicy Info", "Files Containing Personal Information"],
    "cve": ["Advisories and Vulnerabilities"]
}


init(autoreset=True) 

GREEN = "\033[38;2;119;221;119m"  
BLUE = "\033[38;2;136;209;241m"  
RED = "\033[38;2;255;0;0m"  
WHITE = "\033[38;2;255;255;255m" 
RESET = "\033[0m" 

HEADER = f"""
{WHITE}██╗   ██╗ ██████╗ ██╗   ██╗    {BLUE}██████╗  ██████╗ ██████╗ ██╗  ██╗
{WHITE}╚██╗ ██╔╝██╔═══██╗██║   ██║    {BLUE}██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝
 {WHITE}╚████╔╝ ██║   ██║██║   ██║    {BLUE}██║  ██║██║   ██║██████╔╝█████╔╝ 
  {WHITE}╚██╔╝  ██║   ██║██║   ██║    {BLUE}██║  ██║██║   ██║██╔══██╗██╔═██╗ 
   {WHITE}██║   ╚██████╔╝╚██████╔╝    {BLUE}██████╔╝╚██████╔╝██║  ██║██║  ██╗
   {WHITE}╚═╝    ╚═════╝  ╚═════╝     {BLUE}╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
{Style.RESET_ALL}
{BLUE}by{WHITE}: OtterBot
{BLUE}Last Modified{WHITE}: 02/23/25
{BLUE}Version{WHITE}: 1.0.0
{RED}Disclaimer: The author is not responsible for any actions you do, use at your own risk.{Style.RESET_ALL}
"""

def loading_bar(duration=3):
    """Simulate a loading bar for realism."""
    print("[*] Generating Google Dorks...", end="", flush=True)
    for _ in range(30):
        time.sleep(duration / 30)
        sys.stdout.write(".")
        sys.stdout.flush()
    print(" [✔] Done!\n")

def get_chromedriver_path():
    """Automatically find ChromeDriver for Windows/Linux, and fix permissions if needed."""

    user_defined_path = os.getenv("CHROMEDRIVER_PATH")
    if user_defined_path and os.path.exists(user_defined_path):
        return user_defined_path

    script_dir = os.path.dirname(os.path.abspath(__file__))

    if platform.system() == "Windows":
        win_path = os.path.join(script_dir, "chromedriver-win64", "chromedriver.exe")
        if os.path.exists(win_path):
            return win_path
    elif platform.system() == "Linux":
        linux_path = os.path.join(script_dir, "chromedriver-linux64", "chromedriver")
        if os.path.exists(linux_path):
            os.chmod(linux_path, 0o755)
            return linux_path

    if shutil.which("chromedriver"):
        return shutil.which("chromedriver")

    print("[!] ChromeDriver not found. Set CHROMEDRIVER_PATH or place it in the script directory.")
    return None

def scrape_exploitdb():
    """Scrape ALL pages from Exploit-DB and save Google Dorks."""
    print("[*] Scraping Exploit-DB for Google Dorks...")

    driver_path = get_chromedriver_path()
    if not driver_path:
        print("[!] No valid ChromeDriver found. Please download it and place it in the script folder.")
        return False

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 🛠️ **Anti-Bot Detection Bypass - Hides Selenium from detection**
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        url = "https://www.exploit-db.com/google-hacking-database"
        driver.get(url)
        time.sleep(5)  
        dorks = {}

        while True:  
            try:
                table = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.ID, "exploits-table"))
                )
                rows = table.find_elements(By.TAG_NAME, "tr")[1:]  

                if not rows:
                    print("[!] No rows found on this page.")
                    break

                print(f"[✔] Found {len(rows)} rows on this page!")

                for row in rows:
                    columns = row.find_elements(By.TAG_NAME, "td")
                    if len(columns) < 3:
                        continue

                    dork_text = columns[1].text.strip()
                    category = columns[2].text.strip()

                    if category not in dorks:
                        dorks[category] = []
                    dorks[category].append(dork_text)

                try:
                    next_button = driver.find_element(By.ID, "exploits-table_next")
                    if "disabled" in next_button.get_attribute("class"):
                        print("[✔] No more pages. Scraping complete.")
                        break  

                    print("[*] Moving to the next page...")
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(3)  
                except:
                    print("[✔] No more pages. Scraping complete.")
                    break  

            except Exception as e:
                print(f"[!] Error on this page: {e}")
                break

        with open(DATABASE_FILE, "w") as f:
            json.dump(dorks, f, indent=4)

        print("[✔] Database updated successfully!")

    except Exception as e:
        print(f"[!] Error scraping Exploit-DB: {e}")

    finally:
        driver.quit()

def load_database():
    """Load Google Dorks database, ask user to update if missing."""
    if not os.path.exists(DATABASE_FILE) or os.stat(DATABASE_FILE).st_size == 0:
        choice = input("[?] Database missing or empty. Would you like to update it now? (y/n): ").strip().lower()
        if choice != "y":
            print("[!] No database loaded. Exiting...")
            sys.exit(0)  

        print("[*] Fetching fresh data from Exploit-DB...")
        if not scrape_exploitdb():
            print("[!] Failed to update database. Exiting...")
            sys.exit(1)

    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("[!] Database file is corrupted. Re-downloading...")
        if not scrape_exploitdb():
            print("[!] Using fallback database.")
            return {"General": ["site:pastebin.com", "site:github.com"]}

        with open(DATABASE_FILE, "r") as f:
            return json.load(f)

def interactive_input():
    """Interactive menu for selecting user inputs with a cleaner interface."""
def interactive_input():
    """Interactive menu for selecting user inputs with a cleaner interface."""
    user_inputs = {
        "name": "", "username": "", "email": "", "phone": "", "filetype": "",
        "ip": "", "domain": "", "crypto": "", "social": "", "tech": "", "address": "", "cve": ""
    }

    options = {
        "1": ("Name", "name"),
        "2": ("Username", "username"),
        "3": ("Email", "email"),
        "4": ("Phone Number", "phone"),
        "5": ("File Type", "filetype"),
        "6": ("IP Address", "ip"),
        "7": ("Domain/Website", "domain"),
        "8": ("Cryptocurrency Wallet", "crypto"),
        "9": ("Social Media Handle", "social"),
        "10": ("Technology Stack", "tech"),
        "11": ("Physical Address", "address"),
        "12": ("CVE/Vulnerability", "cve"),
        "0": ("Done", None)  
    }
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n[?] Select information type to enter:\n")
        for key, (display_name, dict_key) in options.items():
            entered_value = f" ({user_inputs[dict_key]})" if dict_key and user_inputs[dict_key] else ""
            print(f"[{key}] {display_name}{entered_value}")

        choice = input("\n[*] Select an option: ").strip()

        if choice == "0":
            break
        elif choice in options and options[choice][1] is not None:
            dict_key = options[choice][1]
            user_inputs[dict_key] = input(f"[?] Enter {options[choice][0]}: ").strip()

    return user_inputs

def generate_dorks():
    """Generate Google Dorks based on user input and return the best results dynamically."""
    database = load_database()
    user_inputs = interactive_input()

    generated_dorks = {}

    for input_type, user_value in user_inputs.items():
        if user_value:
            if input_type not in generated_dorks:
                generated_dorks[input_type] = {}

            for category in CATEGORY_MAPPING.get(input_type, []):
                if category in database:
                    if category not in generated_dorks[input_type]:
                        generated_dorks[input_type][category] = []

                    dorks_list = insert_smartly(database[category], user_value)

                    best_dorks = dorks_list[:min(len(dorks_list), 10)]  
                    generated_dorks[input_type][category].extend(best_dorks)

    loading_bar()

    print("\n[✔] Google Dorks Generated:\n")

    if not generated_dorks:
        print("[!] No Google Dorks found for the provided inputs.\n")
    else:
        for input_type, categories in generated_dorks.items():
            print(f"{GREEN}[{input_type.capitalize()}]{RESET}")
            for category, dorks in categories.items():
                print(f"    {BLUE}[{category}]{RESET}")
                for dork in dorks:
                    time.sleep(0.2)
                    print(f"        {dork}") 
                print("")

    if LOGGING:
        save_to_log(generated_dorks)
    else:
        log_choice = input("[?] Would you like to log this? (y/n): ").strip().lower()
        if log_choice == "y":
            save_to_log(generated_dorks)

def insert_smartly(dork_list, user_input):
    """Insert user input into Google Dorks while ranking the most effective ones first."""
    modified_dorks = []

    ranking_weights = {
        "password": 10, "login": 9, "index of": 8, "database": 7,
        "admin": 6, "confidential": 6, "secret": 5, "filetype:xls": 5,
        "inurl:ftp": 4, "intitle:login": 4, "site:pastebin.com": 3,
        "wallet.dat": 9, "cve": 9, "exploit": 8, "security": 7
    }

    for dork in dork_list:
        dork_lower = dork.lower()
        modified_dork = dork

        user_input_quoted = f'"{user_input}"' if " " in user_input else user_input

        if user_input_quoted not in dork:
            if "intext:" in dork_lower:
                modified_dork = dork.replace("intext:", f'intext:{user_input_quoted} ')
            elif "intitle:" in dork_lower:
                modified_dork = dork.replace("intitle:", f'intitle:{user_input_quoted} ')
            elif "site:" in dork_lower:
                modified_dork = dork.replace("site:", f'site:{user_input_quoted} ')
            elif "filetype:" in dork_lower:
                modified_dork = dork.replace("filetype:", f'filetype:{user_input_quoted} ')
            elif "ext:" in dork_lower:
                modified_dork = dork.replace("ext:", f'ext:{user_input_quoted} ')
            elif "inurl:" in dork_lower:
                modified_dork = dork.replace("inurl:", f'inurl:{user_input_quoted} ')
            else:
                modified_dork = f"{dork} {user_input_quoted}"

        rank_score = sum(ranking_weights[keyword] for keyword in ranking_weights if keyword in dork_lower)

        modified_dorks.append((modified_dork, rank_score))

    modified_dorks.sort(key=lambda x: x[1], reverse=True)

    return [dork[0] for dork in modified_dorks]

def save_to_log(generated_dorks):
    """Save generated dorks to a log file."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    date_str = time.strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_DIR, f"{date_str}.txt")

    with open(log_file, "w", encoding="utf-8") as f:
        for input_type, categories in generated_dorks.items():
            f.write(f"[{input_type.capitalize()}]\n")
            for category, dorks in categories.items():
                f.write(f"    [{category}]\n")
                for dork in dorks:
                    f.write(f"        {dork}\n")
                f.write("\n")

    print(f"[✔] Saved to {log_file}")

def toggle_logging():
    """Toggle logging and update the menu in place without reprinting it."""
    global LOGGING
    LOGGING = not LOGGING

    sys.stdout.write("\033[F" * 10)  
    sys.stdout.write("\033[J") 
    
def show_help():
    """Display the help menu from README.txt in the assets folder."""
    help_file = os.path.join("assets", "README.txt")

    if os.path.exists(help_file):
        with open(help_file, "r", encoding="utf-8") as f:
            print("\n" + f.read())  
    else:
        print("\n[!] Help file (README.txt) not found in assets folder.\n")

def show_support():
    """Display the support information from SUPPORT.txt in the assets folder."""
    support_file = os.path.join("assets", "SUPPORT.txt")

    if os.path.exists(support_file):
        with open(support_file, "r", encoding="utf-8") as f:
            print("\n" + f.read())  
    else:
        print("\n[!] Support file (SUPPORT.txt) not found in assets folder.\n")

def show_menu():
    """Display the main menu with updated logging status."""
    print("\n[*] You Dork Menu")
    print(f"[1] Generate Google Dorks")
    print(f"[2] Toggle Logging (Currently: {'ON' if LOGGING else 'OFF'})")
    print("[3] Update Database")
    print("[4] Help")
    print("[5] Support Author")
    print("[0] Exit")

def main():
    global LOGGING  

    print(HEADER) 

    while True:
        show_menu() 
        choice = input("\n[*] Select an option: ").strip()

        if choice == "1":
            generate_dorks()
        elif choice == "2":
            toggle_logging() 
        elif choice == "3":
            scrape_exploitdb()
        elif choice == "4":
            show_help()
        elif choice == "5":
            show_support()
        elif choice == "0":
            print("[✔] Exiting You Dork...")
            break
        else:
            print("[!] Invalid option, try again.")

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()  
    else:
        main()