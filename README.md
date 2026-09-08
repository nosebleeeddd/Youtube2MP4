## 1. Create Virtual Environment for clean install:
> **Reminder:** The '.venv' is the config file name. Dot files are files hidden
> by the file-system. '.venv' can be named anything and without the '.' to
> unhide it. (e.g python3 -m venv virtual_environment)

### Linux
-  python3 -m venv .venv
-  source .venv/bin/activate   

### Windows(powershell)
-  py -m venv .venv
-  .venv\Scripts\Activate.ps1

### Windows(CMD)
-  python -m venv .venv
-  .venv\Scripts\activate.bat

## 2. Install to your Virtual Environment:
python3 -m pip install -U pytubefix

## 3. Install to Convert Stream Audio/Video(our script uses this):
sudo apt install ffmpeg

## 4. Run Script and select output destination:
python3 main.py

# Virtual Environment needs to be activated before running script! 
