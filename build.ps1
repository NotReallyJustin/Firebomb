# Powershell script to build the firebomb executable using PyInstaller, clean up unnecessary files, and keep only the executable.
# Make sure you have PyInstaller installed in your Python environment

rm firebomb.ex*         # Lazy way to remove all firebomb.exe if it exists
pyinstaller --onefile --icon=./Assets/Firebomb.png --name firebomb.exe ./firebomb.py
rm -r ./build
mv ./dist/firebomb.exe ./
rm -r ./dist
rm *.spec