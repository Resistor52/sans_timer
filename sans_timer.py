#!/usr/bin/env python3
"""
SANS Timer - A timer application for teaching environments
"""

import sys
import time
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QTimeEdit, 
                            QRadioButton, QButtonGroup, QSpinBox, QGroupBox,
                            QGridLayout, QSizePolicy, QDesktopWidget, QColorDialog,
                            QFormLayout, QDialog, QScrollArea, QTextBrowser)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont, QIcon, QColor


class TimerDisplay(QMainWindow):
    """Window that displays the countdown timer"""
    
    def __init__(self):
        super().__init__()
        # Default colors
        self.normal_color = QColor(255, 255, 255)  # White
        self.warning_color = QColor(255, 0, 0)     # Red
        self.background_color = QColor(0, 0, 0)    # Black
        self.current_time_str = "00:00:00"
        self.is_warning_state = False
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle('Timer Display')
        
        # Keep the window frameless and on top
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)  # Add some padding
        
        # Create timer display label
        self.timer_label = QLabel('00:00:00')
        self.timer_label.setFont(QFont('Arial', 48, QFont.Bold))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet(f"color: {self.normal_color.name()};")
        layout.addWidget(self.timer_label)
        
        # Set window size to fit content
        self.adjustSize()
        self.setStyleSheet(f"background-color: {self.background_color.name()};")
    
    def showEvent(self, event):
        """Handle the window show event to ensure proper positioning"""
        super().showEvent(event)
        # Ensure the window size is correct
        self.adjustSize()
        # Position the window on the correct monitor
        self.move_to_secondary_monitor()
    
    def move_to_secondary_monitor(self):
        """Position the window on the secondary monitor if available"""
        desktop = QDesktopWidget()
        
        # First, ensure the window size is properly calculated
        self.adjustSize()
        
        if desktop.screenCount() > 1:
            # Use second monitor
            screen_geometry = desktop.screenGeometry(1)
            
            # Calculate position to ensure window is fully on the secondary monitor
            x = screen_geometry.left() + screen_geometry.width() - self.width() - 20
            y = screen_geometry.top() + screen_geometry.height() - self.height() - 20
            
            # Ensure x coordinate is within the secondary monitor bounds
            if x < screen_geometry.left():
                x = screen_geometry.left() + 20
                
            self.move(x, y)
            
            # Double-check that we're on the right monitor and adjust if needed
            if self.frameGeometry().left() < screen_geometry.left():
                # If still not on secondary monitor, force it there
                self.move(screen_geometry.left() + 50, y)
        else:
            # Only one monitor, position on the lower right corner
            screen_geometry = desktop.screenGeometry(0)
            x = screen_geometry.width() - self.width() - 20
            y = screen_geometry.height() - self.height() - 20
            self.move(x, y)
    
    def update_display(self, time_str, is_warning=False):
        """Update the timer display with the given time string"""
        self.current_time_str = time_str
        self.is_warning_state = is_warning
        self.timer_label.setText(time_str)
        
        # Change color based on time remaining
        if is_warning:
            self.timer_label.setStyleSheet(f"color: {self.warning_color.name()};")
        else:
            self.timer_label.setStyleSheet(f"color: {self.normal_color.name()};")
        
        # Adjust size to fit content
        self.adjustSize()
    
    def set_colors(self, normal_color, warning_color, background_color):
        """Set the colors for the timer display"""
        self.normal_color = normal_color
        self.warning_color = warning_color
        self.background_color = background_color
        
        # Update the display with the new colors
        self.setStyleSheet(f"background-color: {self.background_color.name()};")
        
        # Check if we're in warning mode by looking at the current text color
        current_style = self.timer_label.styleSheet()
        if "red" in current_style or self.warning_color.name() in current_style:
            self.timer_label.setStyleSheet(f"color: {self.warning_color.name()};")
        else:
            self.timer_label.setStyleSheet(f"color: {self.normal_color.name()};")
    
    def mousePressEvent(self, event):
        """Enable dragging the window when clicked"""
        self.oldPos = event.globalPos()
        
    def mouseMoveEvent(self, event):
        """Move the window when dragged"""
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


class HelpDialog(QDialog):
    """Dialog to display help information"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SANS Timer Help")
        self.setMinimumSize(500, 400)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Create scroll area for help text
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Create text browser for formatted text
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        
        # Use the built-in help text for better compatibility with single file executables
        help_text = self.get_default_help_text()
        text_browser.setMarkdown(help_text)
        
        # Add text browser to scroll area
        scroll_area.setWidget(text_browser)
        
        # Add scroll area to layout
        layout.addWidget(scroll_area)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
    
    def get_default_help_text(self):
        """Return help text for the application"""
        return """# SANS Timer Help

## Usage

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

## Timer Modes

- Time until 8:30 AM, 9:00 AM, 10:50 AM, 1:30 PM, 3:20 PM: Calculates time until the specified time today (or tomorrow if the time has already passed)
- Time until custom time: Allows you to set any target time
- 20, 30, 45 Minute Timer: Fixed duration countdown timers
- Custom Timer: Set your own hours, minutes, and seconds for the countdown

Created by: Kenneth G. Hartman (ken@kennethghartman.com)
Source code available at: https://github.com/resistor52/sans_timer

"""

class ControlPanel(QMainWindow):
    """Window for controlling the timer settings"""
    
    def __init__(self, timer_display):
        super().__init__()
        self.timer_display = timer_display
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.end_time = None
        self.timer_mode = "Not started"
        self.timer_window_visible = False  # Start with timer window hidden
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle('SANS Timer Control Panel')
        
        # Set window icon if available
        icon_path = "timer_icon.ico"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.resize(400, 450)  # Adjusted height
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create top bar with quit button
        top_bar = QHBoxLayout()
        
        # Add title to the left
        title_label = QLabel("SANS Timer")
        title_label.setFont(QFont('Arial', 12, QFont.Bold))
        top_bar.addWidget(title_label)
        
        # Add spacer to push buttons to the right
        top_bar.addStretch()
        
        # Add help button
        self.help_button = QPushButton("?")
        self.help_button.setFixedSize(24, 24)
        self.help_button.setFont(QFont('Arial', 12, QFont.Bold))
        self.help_button.clicked.connect(self.show_help)
        self.help_button.setStyleSheet("""
            QPushButton {
                background-color: #4a86e8; 
                color: white; 
                font-weight: bold;
                border-radius: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2a66c8;
            }
        """)
        top_bar.addWidget(self.help_button)
        
        # Add quit button to the top right
        self.quit_button = QPushButton("×")  # Unicode × character
        self.quit_button.setFixedSize(24, 24)
        self.quit_button.setFont(QFont('Arial', 14, QFont.Bold))
        self.quit_button.clicked.connect(self.quit_application)
        self.quit_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6b6b; 
                color: white; 
                font-weight: bold;
                border-radius: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #ff4040;
            }
        """)
        top_bar.addWidget(self.quit_button)
        
        main_layout.addLayout(top_bar)
        
        # Add timer display in control panel
        self.control_timer_display = QLabel('00:00:00')
        self.control_timer_display.setFont(QFont('Arial', 24, QFont.Bold))
        self.control_timer_display.setAlignment(Qt.AlignCenter)
        self.control_timer_display.setStyleSheet(f"color: {self.timer_display.normal_color.name()}; background-color: {self.timer_display.background_color.name()}; padding: 5px; border-radius: 5px;")
        main_layout.addWidget(self.control_timer_display)
        
        # Create timer mode selection group
        mode_group = QGroupBox("Timer Mode")
        mode_layout = QVBoxLayout()
        
        # Create radio buttons for timer modes
        self.mode_group = QButtonGroup(self)
        
        # Time until specific time modes
        self.radio_830am = QRadioButton("Time until 8:30 AM")
        self.radio_9am = QRadioButton("Time until 9:00 AM")
        self.radio_1050am = QRadioButton("Time until 10:50 AM")
        self.radio_130pm = QRadioButton("Time until 1:30 PM")
        self.radio_320pm = QRadioButton("Time until 3:20 PM")
        self.radio_custom_time = QRadioButton("Time until custom time")
        
        # Custom time selection
        time_layout = QHBoxLayout()
        self.custom_time_edit = QTimeEdit()
        self.custom_time_edit.setDisplayFormat("hh:mm")
        self.custom_time_edit.setTime(QTime(9, 0))
        time_layout.addWidget(QLabel("Custom time:"))
        time_layout.addWidget(self.custom_time_edit)
        
        # Countdown timer modes
        self.radio_20min = QRadioButton("20 Minute Timer")
        self.radio_30min = QRadioButton("30 Minute Timer")
        self.radio_45min = QRadioButton("45 Minute Timer")
        self.radio_custom_duration = QRadioButton("Custom Timer")
        
        # Custom duration selection
        duration_layout = QHBoxLayout()
        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(0, 23)
        self.hours_spin.setSuffix(" hours")
        
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0, 59)
        self.minutes_spin.setSuffix(" minutes")
        
        self.seconds_spin = QSpinBox()
        self.seconds_spin.setRange(0, 59)
        self.seconds_spin.setSuffix(" seconds")
        
        duration_layout.addWidget(self.hours_spin)
        duration_layout.addWidget(self.minutes_spin)
        duration_layout.addWidget(self.seconds_spin)
        
        # Add radio buttons to the button group
        self.mode_group.addButton(self.radio_830am)
        self.mode_group.addButton(self.radio_9am)
        self.mode_group.addButton(self.radio_1050am)
        self.mode_group.addButton(self.radio_130pm)
        self.mode_group.addButton(self.radio_320pm)
        self.mode_group.addButton(self.radio_custom_time)
        self.mode_group.addButton(self.radio_20min)
        self.mode_group.addButton(self.radio_30min)
        self.mode_group.addButton(self.radio_45min)
        self.mode_group.addButton(self.radio_custom_duration)
        
        # Add widgets to the mode layout
        mode_layout.addWidget(self.radio_830am)
        mode_layout.addWidget(self.radio_9am)
        mode_layout.addWidget(self.radio_1050am)
        mode_layout.addWidget(self.radio_130pm)
        mode_layout.addWidget(self.radio_320pm)
        mode_layout.addWidget(self.radio_custom_time)
        mode_layout.addLayout(time_layout)
        mode_layout.addWidget(self.radio_20min)
        mode_layout.addWidget(self.radio_30min)
        mode_layout.addWidget(self.radio_45min)
        mode_layout.addWidget(self.radio_custom_duration)
        mode_layout.addLayout(duration_layout)
        
        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)
        
        # Create color configuration group
        color_group = QGroupBox("Color Settings")
        color_layout = QFormLayout()
        
        # Normal color button
        self.normal_color_button = QPushButton("Choose")
        self.normal_color_button.clicked.connect(self.choose_normal_color)
        self.normal_color_preview = QLabel()
        self.normal_color_preview.setFixedSize(20, 20)
        self.normal_color_preview.setStyleSheet(f"background-color: {self.timer_display.normal_color.name()}; border: 1px solid black;")
        normal_color_layout = QHBoxLayout()
        normal_color_layout.addWidget(self.normal_color_button)
        normal_color_layout.addWidget(self.normal_color_preview)
        color_layout.addRow("Normal Text Color:", normal_color_layout)
        
        # Warning color button
        self.warning_color_button = QPushButton("Choose")
        self.warning_color_button.clicked.connect(self.choose_warning_color)
        self.warning_color_preview = QLabel()
        self.warning_color_preview.setFixedSize(20, 20)
        self.warning_color_preview.setStyleSheet(f"background-color: {self.timer_display.warning_color.name()}; border: 1px solid black;")
        warning_color_layout = QHBoxLayout()
        warning_color_layout.addWidget(self.warning_color_button)
        warning_color_layout.addWidget(self.warning_color_preview)
        color_layout.addRow("Warning Text Color:", warning_color_layout)
        
        # Background color button
        self.background_color_button = QPushButton("Choose")
        self.background_color_button.clicked.connect(self.choose_background_color)
        self.background_color_preview = QLabel()
        self.background_color_preview.setFixedSize(20, 20)
        self.background_color_preview.setStyleSheet(f"background-color: {self.timer_display.background_color.name()}; border: 1px solid black;")
        background_color_layout = QHBoxLayout()
        background_color_layout.addWidget(self.background_color_button)
        background_color_layout.addWidget(self.background_color_preview)
        color_layout.addRow("Background Color:", background_color_layout)
        
        color_group.setLayout(color_layout)
        main_layout.addWidget(color_group)
        
        # Create control buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Timer")
        self.start_button.clicked.connect(self.start_timer)
        
        self.stop_button = QPushButton("Stop Timer")
        self.stop_button.clicked.connect(self.stop_timer)
        self.stop_button.setEnabled(False)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)
        
        # Add toggle timer window button
        self.toggle_timer_button = QPushButton("Show Timer Window")  # Changed default text
        self.toggle_timer_button.clicked.connect(self.toggle_timer_window)
        self.toggle_timer_button.setEnabled(True)  # Always enabled
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)
        
        main_layout.addLayout(button_layout)
        
        # Add toggle timer window button in its own row
        main_layout.addWidget(self.toggle_timer_button)
        
        # Current timer display
        self.current_timer_label = QLabel("Timer not started")
        self.current_timer_label.setAlignment(Qt.AlignCenter)
        self.current_timer_label.setFont(QFont('Arial', 14))
        main_layout.addWidget(self.current_timer_label)
        
        # Set default selection
        self.radio_30min.setChecked(True)
        
        # Position on primary monitor
        self.move_to_primary_monitor()
    
    def closeEvent(self, event):
        """Handle the window close event to close both windows"""
        self.quit_application()
        event.accept()
    
    def choose_normal_color(self):
        """Open color dialog to choose normal text color"""
        try:
            color = QColorDialog.getColor(self.timer_display.normal_color, self, "Choose Normal Text Color")
            if color.isValid():
                self.timer_display.normal_color = color
                self.normal_color_preview.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
                self.update_timer_display_colors()
        except Exception as e:
            print(f"Error selecting color: {e}")
    
    def choose_warning_color(self):
        """Open color dialog to choose warning text color"""
        try:
            color = QColorDialog.getColor(self.timer_display.warning_color, self, "Choose Warning Text Color")
            if color.isValid():
                self.timer_display.warning_color = color
                self.warning_color_preview.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
                self.update_timer_display_colors()
        except Exception as e:
            print(f"Error selecting color: {e}")
    
    def choose_background_color(self):
        """Open color dialog to choose background color"""
        try:
            color = QColorDialog.getColor(self.timer_display.background_color, self, "Choose Background Color")
            if color.isValid():
                self.timer_display.background_color = color
                self.background_color_preview.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
                self.update_timer_display_colors()
        except Exception as e:
            print(f"Error selecting color: {e}")
    
    def update_timer_display_colors(self):
        """Update the timer display with the current colors"""
        try:
            self.timer_display.set_colors(
                self.timer_display.normal_color,
                self.timer_display.warning_color,
                self.timer_display.background_color
            )
            
            # Update control panel timer colors too
            if self.timer_display.is_warning_state:
                self.control_timer_display.setStyleSheet(f"color: {self.timer_display.warning_color.name()}; background-color: {self.timer_display.background_color.name()}; padding: 5px; border-radius: 5px;")
            else:
                self.control_timer_display.setStyleSheet(f"color: {self.timer_display.normal_color.name()}; background-color: {self.timer_display.background_color.name()}; padding: 5px; border-radius: 5px;")
                
        except Exception as e:
            print(f"Error updating colors: {e}")
    
    def move_to_primary_monitor(self):
        """Position the window on the primary monitor"""
        desktop = QDesktopWidget()
        screen_geometry = desktop.screenGeometry(0)  # Primary monitor
        
        # Ensure the window fits within the primary monitor
        window_width = min(self.width(), screen_geometry.width() - 40)
        window_height = min(self.height(), screen_geometry.height() - 40)
        
        if window_width < self.width() or window_height < self.height():
            self.resize(window_width, window_height)
        
        # Calculate centered position
        x = screen_geometry.left() + (screen_geometry.width() - self.width()) // 2
        y = screen_geometry.top() + (screen_geometry.height() - self.height()) // 2
        
        # Ensure the window is fully on the primary monitor
        if x < screen_geometry.left():
            x = screen_geometry.left() + 20
        if y < screen_geometry.top():
            y = screen_geometry.top() + 20
            
        # Make sure the right and bottom edges are on screen too
        if x + self.width() > screen_geometry.right():
            x = screen_geometry.right() - self.width() - 20
        if y + self.height() > screen_geometry.bottom():
            y = screen_geometry.bottom() - self.height() - 20
            
        self.move(x, y)
    
    def quit_application(self):
        """Quit the application"""
        # Close the timer display window first
        if self.timer_display:
            self.timer_display.close()
        # Then close this window and exit the application
        self.close()
        QApplication.quit()
    
    def toggle_timer_window(self):
        """Toggle the visibility of the timer display window"""
        if self.timer_window_visible:
            self.timer_display.hide()
            self.timer_window_visible = False
            self.toggle_timer_button.setText("Show Timer Window")
        else:
            self.timer_display.show()
            self.timer_window_visible = True
            self.toggle_timer_button.setText("Hide Timer Window")
    
    def start_timer(self):
        """Start the timer based on the selected mode"""
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        now = datetime.now()
        
        # Determine the end time based on the selected mode
        if self.radio_830am.isChecked():
            target_time = now.replace(hour=8, minute=30, second=0, microsecond=0)
            if target_time < now:
                # If 8:30 AM has already passed today, use tomorrow
                target_time = target_time + timedelta(days=1)
            self.end_time = target_time
            self.timer_mode = "Until 8:30 AM"
            self.current_timer_label.setText(f"Timer until 8:30 AM")
            
        elif self.radio_9am.isChecked():
            target_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
            if target_time < now:
                # If 9:00 AM has already passed today, use tomorrow
                target_time = target_time + timedelta(days=1)
            self.end_time = target_time
            self.timer_mode = "Until 9:00 AM"
            self.current_timer_label.setText(f"Timer until 9:00 AM")
            
        elif self.radio_1050am.isChecked():
            target_time = now.replace(hour=10, minute=50, second=0, microsecond=0)
            if target_time < now:
                # If 10:50 AM has already passed today, use tomorrow
                target_time = target_time + timedelta(days=1)
            self.end_time = target_time
            self.timer_mode = "Until 10:50 AM"
            self.current_timer_label.setText(f"Timer until 10:50 AM")
            
        elif self.radio_130pm.isChecked():
            target_time = now.replace(hour=13, minute=30, second=0, microsecond=0)
            if target_time < now:
                # If 1:30 PM has already passed today, use tomorrow
                target_time = target_time + timedelta(days=1)
            self.end_time = target_time
            self.timer_mode = "Until 1:30 PM"
            self.current_timer_label.setText(f"Timer until 1:30 PM")
            
        elif self.radio_320pm.isChecked():
            target_time = now.replace(hour=15, minute=20, second=0, microsecond=0)
            if target_time < now:
                # If 3:20 PM has already passed today, use tomorrow
                target_time = target_time + timedelta(days=1)
            self.end_time = target_time
            self.timer_mode = "Until 3:20 PM"
            self.current_timer_label.setText(f"Timer until 3:20 PM")
            
        elif self.radio_custom_time.isChecked():
            custom_time = self.custom_time_edit.time()
            target_time = now.replace(
                hour=custom_time.hour(),
                minute=custom_time.minute(),
                second=0,
                microsecond=0
            )
            if target_time < now:
                # If the custom time has already passed today, use tomorrow
                target_time = target_time + timedelta(days=1)
            self.end_time = target_time
            time_str = self.custom_time_edit.time().toString("hh:mm")
            self.timer_mode = f"Until {time_str}"
            self.current_timer_label.setText(f"Timer until {time_str}")
            
        elif self.radio_20min.isChecked():
            self.end_time = now + timedelta(minutes=20)
            self.timer_mode = "20 Minute Timer"
            self.current_timer_label.setText("20 Minute Timer")
            
        elif self.radio_30min.isChecked():
            self.end_time = now + timedelta(minutes=30)
            self.timer_mode = "30 Minute Timer"
            self.current_timer_label.setText("30 Minute Timer")
            
        elif self.radio_45min.isChecked():
            self.end_time = now + timedelta(minutes=45)
            self.timer_mode = "45 Minute Timer"
            self.current_timer_label.setText("45 Minute Timer")
            
        elif self.radio_custom_duration.isChecked():
            hours = self.hours_spin.value()
            minutes = self.minutes_spin.value()
            seconds = self.seconds_spin.value()
            
            if hours == 0 and minutes == 0 and seconds == 0:
                # Default to 1 minute if no time is specified
                self.end_time = now + timedelta(minutes=1)
                self.timer_mode = "1 Minute Timer"
                self.current_timer_label.setText("1 Minute Timer")
            else:
                self.end_time = now + timedelta(
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds
                )
                time_parts = []
                if hours > 0:
                    time_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
                if minutes > 0:
                    time_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
                if seconds > 0:
                    time_parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")
                
                time_str = " ".join(time_parts)
                self.timer_mode = f"{time_str} Timer"
                self.current_timer_label.setText(f"{time_str} Timer")
        
        # Start the timer to update every second
        self.timer.start(1000)
        self.update_timer()
    
    def update_timer(self):
        """Update the timer display"""
        now = datetime.now()
        
        if self.end_time is None:
            return
        
        # Calculate the remaining time
        if now >= self.end_time:
            # Timer has ended
            self.timer_display.update_display("00:00:00", is_warning=True)
            self.control_timer_display.setText("00:00:00")
            self.control_timer_display.setStyleSheet(f"color: {self.timer_display.warning_color.name()}; background-color: {self.timer_display.background_color.name()}; padding: 5px; border-radius: 5px;")
            self.current_timer_label.setText("Timer Ended!")
            self.stop_timer()
            return
        
        # Calculate the time difference
        time_diff = self.end_time - now
        
        # Convert to hours, minutes, seconds
        total_seconds = int(time_diff.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Format the time string
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Update the displays
        is_warning = time_diff.total_seconds() < 300  # Warning if less than 5 minutes
        self.timer_display.update_display(time_str, is_warning)
        
        # Update control panel timer display
        self.control_timer_display.setText(time_str)
        if is_warning:
            self.control_timer_display.setStyleSheet(f"color: {self.timer_display.warning_color.name()}; background-color: {self.timer_display.background_color.name()}; padding: 5px; border-radius: 5px;")
        else:
            self.control_timer_display.setStyleSheet(f"color: {self.timer_display.normal_color.name()}; background-color: {self.timer_display.background_color.name()}; padding: 5px; border-radius: 5px;")
    
    def stop_timer(self):
        """Stop the timer"""
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    
    def reset_timer(self):
        """Reset the timer"""
        self.stop_timer()
        self.timer_display.update_display("00:00:00")
        self.control_timer_display.setText("00:00:00")
        self.control_timer_display.setStyleSheet(f"color: {self.timer_display.normal_color.name()}; background-color: {self.timer_display.background_color.name()}; padding: 5px; border-radius: 5px;")
        self.current_timer_label.setText("Timer not started")
        self.end_time = None
        self.timer_mode = "Not started"
    
    def show_help(self):
        """Show the help dialog"""
        help_dialog = HelpDialog(self)
        help_dialog.exec_()


def main():
    app = QApplication(sys.argv)
    
    # Set application icon if available
    icon_path = "timer_icon.ico"
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
        # Set the taskbar icon (Windows specific)
        try:
            import ctypes
            myappid = 'kennethghartman.sanstimer.1.0'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print(f"Warning: Could not set taskbar icon: {e}")
    
    # Create the timer display window
    timer_display = TimerDisplay()
    
    # Create the control panel window
    control_panel = ControlPanel(timer_display)
    
    # Show only the control panel initially
    control_panel.show()
    
    # Force proper positioning after windows are shown
    timer_display.move_to_secondary_monitor()
    control_panel.move_to_primary_monitor()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 