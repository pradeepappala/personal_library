# personal_library
Simple Single use library

# install required softwares - git
$ sudo apt-get update 
$ sudo apt-get install git python3-venv
$ git clone https://github.com/pradeepappala/personal_library.git

# dir structure
- personal_library
   - src
   - main.py
   - tests/unittests

# create venv (python on windows/ python3 on linux)
cd to repo dir
python -m venv library_venv

# activate venv
library_venv\Scripts\activate
# linux
source library_venv/bin/activate 

# install requirements
pip install -r requirements.txt

# start app_notification
python -m main

# run app from vs code
open workspace in vs code
ctrl+shift+p select python from the venv created (library_venv\Scripts\python.exe)
Run (F5/ctrl+F5)


# build apk using buildozer
create wsl (windows subsystem for linux)
create venv 
https://www.youtube.com/watch?v=6gNpSuE01qE&t=14s

https://buildozer.readthedocs.io/en/latest/installation.html

https://buildozer.readthedocs.io/en/latest/quickstart.html

# steps followed
open wsl (ubuntu)
cd GitHub\my-finance
source GitHub\my-finance\finance_venv_wsl\bin\activate
cd GitHub\my-finance\my_android_app
Edit the buildozer.spec according to the Specifications. You should at least change the title, package.name and package.domain in the [app] section.
buildozer -v android debug
apk will be available in my_android_app\bin
copy apk to mobile and install