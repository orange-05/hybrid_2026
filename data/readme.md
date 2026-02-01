# Agentic Financial Forensics (ICCI 2026)
METHOD1
M:
cd forensic_lcm_system
conda activate M:\forensic_lcm_system\env_windows

REM 1. Force temp files to M: drive (Crucial Step)
set TMP=M:\conda_temp
set TEMP=M:\conda_temp

REM 2. Install the missing Word tool
pip install python-docx --no-cache-dir

REM 3. Launch the App
python app.py



METHOD2
## How to Launch
1. Open Ubuntu Terminal.
2. Go to folder: `cd /mnt/m/forensic_lcm_system`
3. Activate brain: `source venv/bin/activate`
4. Launch app: `python3 app.py`
5. Open browser: http://localhost:7860

echo "alias launch_forensic='cd /mnt/m/forensic_lcm_system && source venv/bin/activate && python3 app.py'" >> ~/.bashrc && source ~/.bashrc

launch_forensic

## Critical Notes
- DO NOT update pip or python.
- DO NOT move this folder from M: drive without copying the whole 'venv'.