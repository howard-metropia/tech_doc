# Gluon MessageBox Handler Module Technical Documentation

## Module: `messageboxhandler.py`

### Overview
The `messageboxhandler` module provides logging handlers that display log messages through GUI dialogs and desktop notifications. It includes two handler classes: `MessageBoxHandler` for Tkinter-based modal dialogs and `NotifySendHandler` for Linux desktop notifications using the `notify-send` command.

### Table of Contents
1. [Dependencies](#dependencies)
2. [Handler Classes](#handler-classes)
3. [GUI Integration](#gui-integration)
4. [Desktop Notifications](#desktop-notifications)
5. [Usage Examples](#usage-examples)
6. [Cross-Platform Support](#cross-platform-support)
7. [Error Handling](#error-handling)

### Dependencies

#### Required Imports
```python
import logging
import subprocess
import sys

# Conditional Tkinter import with Python 2/3 compatibility
try:
    if sys.version_info[0] == 2:
        import Tkinter as tkinter
    else:
        import tkinter
except ImportError:
    tkinter = None
```

### Handler Classes

#### `MessageBoxHandler`
A logging handler that displays log messages in Tkinter message boxes.

**Class Definition:**
```python
class MessageBoxHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        if tkinter:
            msg = self.format(record)
            root = tkinter.Tk()
            root.wm_title("web2py logger message")
            text = tkinter.Text()
            text["height"] = 12
            text.insert(0.1, msg)
            text.pack()
            button = tkinter.Button(root, text="OK", command=root.destroy)
            button.pack()
            root.mainloop()
```

**Features:**
- Modal dialog display
- Scrollable text area (12 lines high)
- OK button to close dialog
- Automatic message formatting
- Cross-platform GUI support

#### `NotifySendHandler`
A logging handler that sends desktop notifications using the Linux `notify-send` command.

**Class Definition:**
```python
class NotifySendHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        if tkinter:  # Note: This appears to be a bug - should check for notify-send availability
            msg = self.format(record)
            subprocess.run(["notify-send", msg], check=False, timeout=2)
```

**Features:**
- Non-blocking desktop notifications
- 2-second timeout for safety
- Linux desktop environment integration
- Minimal system resource usage

### GUI Integration

#### Tkinter Message Box Setup
```python
def setup_gui_logging():
    """Setup GUI-based logging for desktop applications"""
    
    # Create logger
    logger = logging.getLogger('web2py.gui')
    logger.setLevel(logging.INFO)
    
    # Add MessageBox handler
    if tkinter:
        mb_handler = MessageBoxHandler()
        mb_handler.setLevel(logging.WARNING)  # Only warnings and errors
        
        # Custom formatter for GUI display
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s\n\n%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        mb_handler.setFormatter(formatter)
        
        logger.addHandler(mb_handler)
    else:
        logger.warning("Tkinter not available - GUI logging disabled")
    
    return logger
```

#### Message Box Customization
```python
class CustomMessageBoxHandler(MessageBoxHandler):
    """Enhanced message box handler with customization options"""
    
    def __init__(self, title="Application Message", width=600, height=400):
        super(CustomMessageBoxHandler, self).__init__()
        self.title = title
        self.width = width
        self.height = height
    
    def emit(self, record):
        if not tkinter:
            return
        
        msg = self.format(record)
        
        # Create main window
        root = tkinter.Tk()
        root.wm_title(self.title)
        root.geometry(f"{self.width}x{self.height}")
        
        # Create scrollable text widget
        frame = tkinter.Frame(root)
        frame.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tkinter.Scrollbar(frame)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        
        text = tkinter.Text(frame, yscrollcommand=scrollbar.set, wrap=tkinter.WORD)
        text.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        
        scrollbar.config(command=text.yview)
        
        # Insert message
        text.insert(tkinter.END, msg)
        text.config(state=tkinter.DISABLED)  # Read-only
        
        # Add buttons
        button_frame = tkinter.Frame(root)
        button_frame.pack(pady=10)
        
        ok_button = tkinter.Button(
            button_frame, 
            text="OK", 
            command=root.destroy,
            width=10
        )
        ok_button.pack(side=tkinter.LEFT, padx=5)
        
        copy_button = tkinter.Button(
            button_frame,
            text="Copy",
            command=lambda: self.copy_to_clipboard(root, msg),
            width=10
        )
        copy_button.pack(side=tkinter.LEFT, padx=5)
        
        # Center window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (self.width // 2)
        y = (root.winfo_screenheight() // 2) - (self.height // 2)
        root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        root.mainloop()
    
    def copy_to_clipboard(self, root, text):
        """Copy message to clipboard"""
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()  # Required for clipboard to work
```

### Desktop Notifications

#### Enhanced Notification Handler
```python
class EnhancedNotifySendHandler(logging.Handler):
    """Enhanced notification handler with better error handling and features"""
    
    def __init__(self, urgency='normal', timeout=5000, icon=None):
        super(EnhancedNotifySendHandler, self).__init__()
        self.urgency = urgency  # low, normal, critical
        self.timeout = timeout  # milliseconds
        self.icon = icon
        self._notify_available = self._check_notify_send()
    
    def _check_notify_send(self):
        """Check if notify-send is available"""
        try:
            subprocess.run(['which', 'notify-send'], 
                         check=True, 
                         capture_output=True, 
                         timeout=1)
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def emit(self, record):
        if not self._notify_available:
            return
        
        try:
            msg = self.format(record)
            title = f"web2py - {record.levelname}"
            
            # Build notify-send command
            cmd = ['notify-send']
            
            # Add urgency
            cmd.extend(['--urgency', self.urgency])
            
            # Add timeout
            cmd.extend(['--expire-time', str(self.timeout)])
            
            # Add icon if specified
            if self.icon:
                cmd.extend(['--icon', self.icon])
            
            # Add title and message
            cmd.extend([title, msg])
            
            # Send notification
            subprocess.run(cmd, check=False, timeout=3)
            
        except Exception as e:
            # Silently fail - don't break logging
            pass
```

#### Notification Levels
```python
def setup_notification_logging():
    """Setup notifications with different styles per log level"""
    
    logger = logging.getLogger('web2py.notifications')
    
    # Error notifications (critical urgency, red icon)
    error_handler = EnhancedNotifySendHandler(
        urgency='critical',
        timeout=10000,  # 10 seconds
        icon='dialog-error'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter('%(message)s'))
    
    # Warning notifications (normal urgency, yellow icon)
    warning_handler = EnhancedNotifySendHandler(
        urgency='normal',
        timeout=5000,   # 5 seconds
        icon='dialog-warning'
    )
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(logging.Formatter('%(message)s'))
    
    # Info notifications (low urgency, blue icon)
    info_handler = EnhancedNotifySendHandler(
        urgency='low',
        timeout=3000,   # 3 seconds
        icon='dialog-information'
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter('%(message)s'))
    
    logger.addHandler(error_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(info_handler)
    
    return logger
```

### Usage Examples

#### Basic Setup
```python
import logging
from gluon.messageboxhandler import MessageBoxHandler, NotifySendHandler

# Setup basic GUI logging
def setup_basic_gui_logging():
    logger = logging.getLogger('myapp')
    
    # Add message box handler for errors
    if tkinter:
        mb_handler = MessageBoxHandler()
        mb_handler.setLevel(logging.ERROR)
        logger.addHandler(mb_handler)
    
    # Add notification handler for warnings
    notify_handler = NotifySendHandler()
    notify_handler.setLevel(logging.WARNING)
    logger.addHandler(notify_handler)
    
    return logger

# Usage
logger = setup_basic_gui_logging()
logger.error("This will show in a message box")
logger.warning("This will show as a notification")
```

#### Web2py Integration
```python
def setup_web2py_gui_logging():
    """Setup GUI logging for web2py development"""
    
    # Get web2py logger
    logger = logging.getLogger('web2py')
    
    # Add GUI handlers only in development mode
    if request.is_local:
        # Message boxes for critical errors
        if tkinter:
            mb_handler = MessageBoxHandler()
            mb_handler.setLevel(logging.CRITICAL)
            
            # Format for development
            formatter = logging.Formatter(
                'WEB2PY ERROR\n\n'
                'Time: %(asctime)s\n'
                'Level: %(levelname)s\n'
                'Module: %(name)s\n\n'
                'Message:\n%(message)s'
            )
            mb_handler.setFormatter(formatter)
            logger.addHandler(mb_handler)
        
        # Notifications for other messages
        notify_handler = NotifySendHandler()
        notify_handler.setLevel(logging.WARNING)
        
        notify_formatter = logging.Formatter('%(levelname)s: %(message)s')
        notify_handler.setFormatter(notify_formatter)
        logger.addHandler(notify_handler)
```

#### Development Tools Integration
```python
class DevelopmentLogHandler:
    """Combined handler for development environment"""
    
    def __init__(self):
        self.logger = logging.getLogger('development')
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all development logging handlers"""
        
        # Console handler (always available)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # GUI message box for errors (if available)
        if tkinter:
            gui_handler = CustomMessageBoxHandler(
                title="Development Error",
                width=800,
                height=600
            )
            gui_handler.setLevel(logging.ERROR)
            gui_formatter = logging.Formatter(
                'ERROR DETAILS\n'
                '=============\n\n'
                'Time: %(asctime)s\n'
                'Logger: %(name)s\n'
                'Function: %(funcName)s\n'
                'Line: %(lineno)d\n\n'
                'Message:\n%(message)s\n\n'
                'Full Path: %(pathname)s'
            )
            gui_handler.setFormatter(gui_formatter)
            self.logger.addHandler(gui_handler)
        
        # Desktop notifications (if available)
        notify_handler = EnhancedNotifySendHandler(
            urgency='normal',
            timeout=4000,
            icon='applications-development'
        )
        notify_handler.setLevel(logging.WARNING)
        notify_formatter = logging.Formatter(
            'DEV: %(levelname)s in %(funcName)s()\n%(message)s'
        )
        notify_handler.setFormatter(notify_formatter)
        self.logger.addHandler(notify_handler)
    
    def log_exception(self, exc_info=None):
        """Log exception with full traceback"""
        self.logger.error("Exception occurred", exc_info=exc_info or True)
    
    def log_debug_point(self, message, **context):
        """Log debug checkpoint with context"""
        context_str = ', '.join(f"{k}={v}" for k, v in context.items())
        self.logger.debug(f"DEBUG: {message} | Context: {context_str}")
```

### Cross-Platform Support

#### Platform Detection
```python
import platform

def get_platform_handlers():
    """Get appropriate handlers for current platform"""
    
    handlers = []
    
    # GUI handler (cross-platform)
    if tkinter:
        gui_handler = MessageBoxHandler()
        handlers.append(('gui', gui_handler))
    
    # Platform-specific notification handlers
    system = platform.system().lower()
    
    if system == 'linux':
        # Linux: notify-send
        notify_handler = NotifySendHandler()
        handlers.append(('notification', notify_handler))
        
    elif system == 'darwin':  # macOS
        # macOS: osascript for notifications
        class MacNotificationHandler(logging.Handler):
            def emit(self, record):
                try:
                    msg = self.format(record)
                    script = f'display notification "{msg}" with title "web2py"'
                    subprocess.run(['osascript', '-e', script], 
                                 check=False, timeout=2)
                except:
                    pass
        
        handlers.append(('notification', MacNotificationHandler()))
        
    elif system == 'windows':
        # Windows: toast notifications (if available)
        try:
            import win10toast
            
            class WindowsNotificationHandler(logging.Handler):
                def __init__(self):
                    super().__init__()
                    self.toaster = win10toast.ToastNotifier()
                
                def emit(self, record):
                    try:
                        msg = self.format(record)
                        self.toaster.show_toast(
                            "web2py",
                            msg,
                            duration=5,
                            threaded=True
                        )
                    except:
                        pass
            
            handlers.append(('notification', WindowsNotificationHandler()))
            
        except ImportError:
            # Fallback to message box only
            pass
    
    return handlers
```

### Error Handling

#### Safe Handler Implementation
```python
class SafeMessageBoxHandler(MessageBoxHandler):
    """Message box handler with comprehensive error handling"""
    
    def __init__(self, fallback_handler=None):
        super(SafeMessageBoxHandler, self).__init__()
        self.fallback_handler = fallback_handler or logging.StreamHandler()
    
    def emit(self, record):
        try:
            if not tkinter:
                self.fallback_handler.emit(record)
                return
            
            # Attempt to show GUI dialog
            super(SafeMessageBoxHandler, self).emit(record)
            
        except Exception as e:
            # If GUI fails, use fallback
            try:
                self.fallback_handler.emit(record)
                
                # Log the GUI error to stderr
                import sys
                sys.stderr.write(f"GUI logging failed: {e}\n")
                
            except Exception:
                # Last resort - just print to stderr
                import sys
                sys.stderr.write(f"Logging failed completely: {record.getMessage()}\n")
```

### Best Practices

1. **Graceful Degradation**: Always provide fallbacks when GUI isn't available
2. **Performance**: Use notifications for non-critical messages, dialogs for errors only
3. **User Experience**: Don't overwhelm users with too many notifications
4. **Platform Support**: Test on all target platforms
5. **Error Handling**: Never let logging handlers break the application
6. **Formatting**: Use appropriate message formatting for GUI display
7. **Threading**: Consider thread safety for GUI operations

### Limitations and Considerations

1. **Tkinter Availability**: Not always available in server environments
2. **Desktop Environment**: Notifications require desktop environment
3. **User Interaction**: Message boxes block execution until dismissed
4. **Platform Dependencies**: Different notification systems per platform
5. **Resource Usage**: GUI dialogs consume more resources than console logging

### Module Metadata

- **License**: Part of web2py framework (LGPLv3)
- **Platform**: Cross-platform with platform-specific features
- **Dependencies**: tkinter (optional), subprocess
- **Thread Safety**: Varies by platform and GUI toolkit
- **Python**: 2.7+, 3.x compatible