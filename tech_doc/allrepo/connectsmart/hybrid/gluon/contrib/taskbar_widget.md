# Gluon Contrib Taskbar Widget Module

## Overview
Windows taskbar widget integration for web2py applications. Provides functionality to create system tray applications and desktop widgets that can interact with web2py applications.

## Module Information
- **Module**: `gluon.contrib.taskbar_widget`
- **Platform**: Windows desktop applications
- **Purpose**: Desktop integration utilities
- **Use Case**: System tray applications, desktop notifications

## Key Features
- **System Tray Integration**: Create system tray applications
- **Desktop Notifications**: Display desktop notifications
- **Web2py Integration**: Connect desktop apps to web2py
- **Event Handling**: Handle desktop events and interactions
- **Background Processing**: Run background tasks from desktop

## Basic Usage

### System Tray Application
```python
from gluon.contrib.taskbar_widget import TaskbarWidget

class MyAppWidget(TaskbarWidget):
    def __init__(self):
        super().__init__(
            title="MyApp Desktop",
            icon_path="static/images/app_icon.ico"
        )
        
        self.setup_menu()
    
    def setup_menu(self):
        """Setup context menu"""
        self.add_menu_item("Open Web App", self.open_webapp)
        self.add_menu_item("Check Updates", self.check_updates)
        self.add_separator()
        self.add_menu_item("Exit", self.exit_app)
    
    def open_webapp(self):
        """Open web application in browser"""
        import webbrowser
        webbrowser.open('http://localhost:8000/myapp')
    
    def check_updates(self):
        """Check for application updates"""
        # Connect to web2py app to check updates
        self.show_notification("Checking for updates...")

# Start widget
if __name__ == '__main__':
    widget = MyAppWidget()
    widget.run()
```

### Desktop Notifications
```python
def send_desktop_notification(title, message, icon=None):
    """Send desktop notification"""
    
    widget = TaskbarWidget()
    widget.show_notification(
        title=title,
        message=message,
        icon=icon,
        timeout=5000  # 5 seconds
    )
```

This module enables desktop integration for web2py applications on Windows platforms, providing system tray functionality and desktop notifications.