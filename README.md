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


# setup buildozer (one time)
https://www.youtube.com/watch?v=6gNpSuE01qE&t=14s
https://buildozer.readthedocs.io/en/latest/installation.html
create wsl (windows subsystem for linux)
cd ~
python3 -m venv buildozer_env
source buildozer_env/bin/activate
pip3 install --upgrade buildozer
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo6 cmake libffi-dev libssl-dev
pip3 install --upgrade Cython==0.29.33 virtualenv
pip3 install setuptools

# add the following line at the end of your ~/.bashrc file
export PATH=$PATH:~/buildozer_env/bin

# build apk
https://buildozer.readthedocs.io/en/latest/quickstart.html
cd ~
source buildozer_env/bin/activate
cd ~/android_app
buildozer init
Edit the buildozer.spec according to the Specifications. You should at least change the title, package.name and package.domain in the [app] section.
buildozer -v android debug

# path of apk
~/buildozer_env/bin