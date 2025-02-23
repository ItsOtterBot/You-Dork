This tool was designed for OSINT investigators and in support for Hackers Guild. Amazing company offering bounties
to help find missing people, items, etc. Highly recommend checking them out at: https://hackers-guild.tech/

#####################################################################################################################################################################

HOW TO INSTALL (Windows):
1. Make sure Python 3.8 or later is installed.
    Download: https://www.python.org/downloads/

2. Download Google Chorme.
    Download: https://www.google.com/chrome/index.html

3. Download GoogleDriver (must match your Chrome version).
    Download: https://developer.chrome.com/docs/chromedriver/downloads
    Extract chromedriver.exe and move it to the You Dork folder.

4. Clone or Download the Repository.
    git clone https://github.com/YOUR_GITHUB_USERNAME/YouDork.git
    cd YouDork
   (If you don’t have Git, manually download and extract the ZIP file.)

5. Install Dependencies.
    pip install -r requirements.txt

6. python youdork.py
    (add --help or -h to python youdork.py get back to README for help)

For updates, use:
    git pull

HOW TO INTALL (Linux):
1. Check if Python is installed and if it's at least version 3.8 or later.
    python3 --version
   If not, install it:
    sudo apt update && sudo apt install python3 python3-pip -y  # Debian/Ubuntu
    sudo dnf install python3 python3-pip -y  # Fedora

2. Install Google Chrome.
    For Debian/Ubuntu:
        wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        sudo dpkg -i google-chrome-stable_current_amd64.deb
        sudo apt --fix-broken install -y
    For Fedora:
        sudo dnf install google-chrome-stable -y

3. Install ChromeDriver.
    CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1)
    wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0.0/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    sudo mv chromedriver /usr/local/bin/
    chmod +x /usr/local/bin/chromedriver

4. Install Dependencies.
    pip3 install -r requirements.txt

5. python youdork.py
    (add --help or -h to python youdork.py get back to README for help)

For updates, use:
    git pull

#####################################################################################################################################################################

Troubleshooting:

Issue: chromedriver Not Found:
    which chromedriver  # Check if it's installed
    sudo mv chromedriver /usr/local/bin/

Issue: ModuleNotFoundError: No module named 'selenium':
    pip install selenium

#####################################################################################################################################################################

Use:
Option [1]: Generate Google Dorks
    This will generate Google Dorks custom to the information you will provide it. This will be Name, Username, eMail, Phone Number, File Type, etc.
    If you do not know/ don't want to add information in the feild pressing Enter will allow you to skip it without affecting the script. Once you have
    entered all information you will be asked if you would like to log your custom dorks (logging is OFF by default), if you choose to log then you can
    locate them in the logs folder saved under the date you ran the command.

Option [2]: Toggle Logging
    Logging is OFF by default, selecting this option will toggle it ON or OFF depending on it's current state. After generation, it will promt you 
    everytime it's done; However, if you turn ON logging then it will bypass this and log your dorks automaticly. 

Option [3]: Update Database
    **YOU MUST RUN THIS IF IT IS YOUR FIRST TIME USING THE SCRIPT, IF YOU DON'T NOTHING WILL GENERATE, THIS IS FOR THE INITAL DATABASE POPULATION.**
    This allows you to manually update the scripts database, the script doesn't update on it's own as it in all transparency takes a good amount of time. 
    If you run this, know it's pulling the entire expliot-db database, as of writing this thats 7950 different expliots so it will take sometime. 

Option [4]: Help
    Simple, brings you back here, surprise! 

Option [5]: Support Author
    This is just to help support me and my work to keep me off the streets, figuratively and literally. If you are so kind to do so I will leave a 
    couple donation options and ways to reach out if you would like. If you do, it means alot, but also thank you for even taking the time to give it 
    a thought. 

Option [0]: Exit
    Closes the application.
