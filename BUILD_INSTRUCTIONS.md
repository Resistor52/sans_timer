# Building SANS Timer Executable

This document provides instructions for building a standalone Windows executable for the SANS Timer application.

## Prerequisites

- Windows operating system
- Python 3.6 or higher installed
- pip package manager

## Building the Executable

### Automatic Method (Recommended)

1. Simply double-click the `build_exe.bat` file
2. Wait for the build process to complete
3. The executable will be created in the `dist` folder as `SANS_Timer.exe`

### Manual Method

If you prefer to build the executable manually:

1. Install PyInstaller if not already installed:
   ```
   pip install pyinstaller
   ```

2. Run PyInstaller with the spec file:
   ```
   pyinstaller --clean sans_timer.spec
   ```

3. The executable will be created in the `dist` folder

## Custom Icon (Optional)

To use a custom icon for the executable:

1. Create or obtain an .ico file
2. Name it `timer_icon.ico` and place it in the same directory as `sans_timer.py`
3. Rebuild the executable

## Troubleshooting

If you encounter any issues during the build process:

1. Ensure all required Python packages are installed:
   ```
   pip install -r requirements.txt
   ```

2. Try running PyInstaller with the --debug option:
   ```
   pyinstaller --debug sans_timer.spec
   ```

3. Check the PyInstaller documentation for more troubleshooting tips:
   https://pyinstaller.org/en/stable/when-things-go-wrong.html

## Distribution

After building, you can distribute the `SANS_Timer.exe` file from the `dist` folder. Users will not need to have Python installed to run the application. 