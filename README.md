# SANS Timer

> **Note:** If you only need the timer application without building it yourself, you can download the ready-to-use Windows executable (`SANS_Timer.exe`) from the `dist` folder.

A timer application designed for teaching environments, allowing instructors to easily track time until class resumes for the start of class, lunch break, labs, etc.

## Features

- Multiple preset timer modes:
  - Time until 8:30 AM
  - Time until 9:00 AM
  - Time until 10:50 AM
  - Time until 1:30 PM
  - Time until 3:20 PM
  - Time until custom time
  - 20 Minute countdown
  - 30 Minute countdown
  - 45 Minute countdown
  - Custom countdown

- Flexible dual-display interface:
  - Control panel with built-in timer display
  - Optional floating timer window that can be shown/hidden as needed
  - Both displays use the same customizable color scheme

- Customization options:
  - Configurable text colors for normal and warning states
  - Configurable background color
  - Warning color activates when less than 5 minutes remain

- User-friendly controls:
  - Show/hide the floating timer window at any time
  - Compact interface with timer display in both windows
  - Small quit button in the top-right corner
  - Help button for quick access to instructions

- Optimized UI design:
  - Frameless floating timer window for minimal screen space usage
  - Control panel appears in the taskbar with a digital timer icon
  - Floating timer window stays on top of other windows

## Requirements

- Python 3.6+
- PyQt5
- python-dateutil
- Pillow (for icon creation)

## Installation

1. Ensure Python is installed on your system
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application with:
```
python sans_timer.py
```

### Basic Operation

1. Select a timer mode from the options
2. Click "Start Timer" to begin the countdown
3. Use "Stop Timer" to pause and "Reset" to clear the timer
4. Click "Show Timer Window" to display the floating timer when needed
5. Click "Hide Timer Window" to hide the floating timer

### Multi-Monitor Support

- The control panel appears on your primary monitor
- The floating timer window (when shown) appears on your secondary monitor
- If only one monitor is available, both windows will appear on that monitor

### Color Customization

1. Click the "Choose" buttons in the Color Settings section
2. Select your preferred colors for normal text, warning text, and background
3. Changes apply immediately to both displays

## Building a Standalone Executable

### Prerequisites
- Windows operating system
- Python 3.6 or higher installed
- PyInstaller (`pip install pyinstaller`)
- Pillow (`pip install pillow`)

### Building with the Provided Scripts

#### Using build_exe.bat
1. Run the `build_exe.bat` script by double-clicking it
2. The script will:
   - Create a digital timer icon showing "00:14:23"
   - Generate a spec file for PyInstaller
   - Build the executable
3. The executable will be created in the `dist` folder
4. You can distribute `SANS_Timer.exe` to users who don't have Python installed

### Custom Icon
The build script automatically generates a digital timer icon with "00:14:23" displayed in white text on a black background.

## License

MIT

## Author

Created by: Kenneth G. Hartman (ken@kennethghartman.com)  
Source code available at: https://github.com/resistor52/sans_timer 