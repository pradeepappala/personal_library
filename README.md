# personal_library
Simple Single use library

## Install Required Software
```sh
sudo apt-get update
sudo apt-get install git python3-venv
git clone https://github.com/pradeepappala/personal_library.git
```

## Directory Structure
- personal_library/
   - src/
   - main.py
   - tests/unittests/

## Create and Activate Virtual Environment
```sh
cd personal_library
python -m venv library_venv
# Windows
library_venv\Scripts\activate
# Linux
source library_venv/bin/activate
```

## Install Requirements
```sh
pip install -r requirements.txt
```

## Start Main UI
```sh
python -m main
```

## Run App from VS Code
Open workspace in VS Code
Select Python interpreter from venv (`library_venv\Scripts\python.exe`)
Run (F5 / Ctrl+F5)

## Build Android APK (Kivy UI)

### Setup Buildozer (one time)
- [Buildozer Installation Guide](https://buildozer.readthedocs.io/en/latest/installation.html)
- [Video Tutorial](https://www.youtube.com/watch?v=6gNpSuE01qE&t=14s)

#### 1. Install WSL (Windows Subsystem for Linux)
	```bash
	wsl --install
	```

#### 2. Create and activate Python venv
	```bash
	cd ~
	python3 -m venv buildozer_env
	source buildozer_env/bin/activate
	```

#### 3. Install Buildozer and dependencies
	```bash
	pip3 install --upgrade buildozer
	sudo apt update
	sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo6 cmake libffi-dev libssl-dev autopoint
	pip3 install --upgrade Cython==0.29.33 virtualenv
	pip3 install setuptools
	```

#### 4. Add venv to PATH (append to ~/.bashrc)
	```bash
	export PATH=$PATH:~/buildozer_env/bin
	```

### Creating APK
- [Buildozer Quickstart](https://buildozer.readthedocs.io/en/latest/quickstart.html)

#### 5. Start Ubuntu (WSL) from Start Menu

#### 6. Activate buildozer venv
	```bash
	cd ~
	source buildozer_env/bin/activate
	```

#### 7. Prepare your app source files
	```bash
	cd ~/android_app
	```
	- Backup old files: `mv <old app src files>, buildozer.spec ../old_android_app/<app_name>`
	- Create a list of files to copy (e.g., `list.txt` with `main.py, personal_library.py, buildozer.spec`)
	- Copy new files:
	  ```bash
	  rsync -arv --files-from='list.txt' /mnt/c/Users/prade/work/GitHub/personal_library/ /home/pradeep/android_app/
	  ```

#### 8. Initialize and edit buildozer.spec
	```bash
	buildozer init
	# Edit buildozer.spec: set title, package.name, package.domain, permissions and requirements
	# Example requirements:
	requirements = python3,kivy,db-sqlite3
	android.permissions = android.permission.INTERNET
	```

#### 9. Build APK
	```bash
	buildozer -v android debug
	```

#### 10. Find generated APK
	- APK will be in `bin/` (e.g., `bin/mylibraryapp-0.1-arm64-v8a_armeabi-v7a-debug.apk`)

### Test APK
	```bash
	cp bin/mylibraryapp-0.1-arm64-v8a_armeabi-v7a-debug.apk /mnt/c/Users/prade/work/GitHub/android_apps/
	```
	- Transfer to phone using Wifi File Transfer app or USB cable, install and test