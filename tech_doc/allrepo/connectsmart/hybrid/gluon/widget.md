# Widget Module

## Overview
The widget module provides GUI and service management capabilities for web2py applications. It includes a Tkinter-based graphical interface for starting/stopping the web server, scheduler management, taskbar integration, and command-line service controls. This module is primarily used for development environments and desktop deployments of web2py.

## Core Components

### web2pyDialog Class
Main GUI window for web2py server management.

```python
class web2pyDialog(object):
    """Main window dialog for web2py server control"""
    
    def __init__(self, root, options):
        self.root = tkinter.Toplevel(root, bg="white")
        self.options = options
        self.scheduler_processes = OrderedDict()
        # Initialize GUI components
```

**Key Features:**
- Server start/stop controls
- IP address and port configuration
- Password management
- Application browser menu
- Scheduler process management
- System tray integration

## GUI Components

### Server Configuration
```python
# IP Address Selection
self.selected_ip = tkinter.StringVar()
ips = [
    ("127.0.0.1", "Local (IPv4)"),
    ("::1", "Local (IPv6)"),
    ("0.0.0.0", "Public")
]

for ip, legend in ips:
    self.ips[ip] = tkinter.Radiobutton(
        text="%s (%s)" % (legend, ip),
        variable=self.selected_ip,
        value=ip
    )
```

### Password Entry
```python
# Password Configuration
self.password = tkinter.Entry(show="*")
self.password.bind("<Return>", lambda e: self.start())
self.password.focus_force()
```

### Control Buttons
```python
# Start/Stop Buttons
self.button_start = tkinter.Button(
    text="start server", 
    command=self.start
)

self.button_stop = tkinter.Button(
    text="stop server", 
    command=self.stop
)
```

## Menu System

### Server Menu
```python
servermenu = tkinter.Menu(self.menu, tearoff=0)

# View logs
httplog = os.path.join(options.folder, options.log_filename)
servermenu.add_command(
    label="View httpserver.log", 
    command=lambda: start_browser(httplog)
)

# Quit option
servermenu.add_command(
    label="Quit (pid:%i)" % os.getpid(), 
    command=self.quit
)
```

### Application Pages Menu
```python
def connect_pages(self):
    """Populate pages menu with available applications"""
    self.pagesmenu.delete(0, "end")
    
    applications_folder = os.path.join(self.options.folder, "applications")
    available_apps = [
        app for app in os.listdir(applications_folder)
        if os.path.exists(os.path.join(applications_folder, app, "__init__.py"))
    ]
    
    for app in available_apps:
        url = self.url + app
        self.pagesmenu.add_command(
            label=url,
            command=lambda a=app: self.try_start_browser(a)
        )
```

### Scheduler Menu
```python
def update_schedulers(self, start=False):
    """Update scheduler menu with available applications"""
    with self.scheduler_processes_lock:
        self.schedmenu.delete(0, "end")
        
        for app in available_apps:
            if app not in self.scheduler_processes:
                # Add start option
                self.schedmenu.add_command(
                    label="start %s" % app,
                    command=lambda a=app: self.try_start_scheduler(a)
                )
            else:
                # Add stop option
                self.schedmenu.add_command(
                    label="stop %s" % app,
                    command=lambda a=app: self.try_stop_scheduler(a)
                )
```

## Server Management

### Server Startup
```python
def start(self):
    """Start web2py server with current configuration"""
    password = self.password.get()
    ip = self.selected_ip.get()
    port = int(self.port_number.get())
    
    # Validate configuration
    if not password:
        self.error("no password, no web admin interface")
        return
    
    if not is_valid_ip_address(ip):
        return self.error("invalid host ip address")
    
    # Create server instance
    self.server = main.HttpServer(
        ip, port, password,
        pid_filename=options.pid_filename,
        log_filename=options.log_filename,
        ssl_certificate=options.server_cert,
        ssl_private_key=options.server_key,
        min_threads=options.min_threads,
        max_threads=options.max_threads,
        timeout=options.timeout,
        path=options.folder
    )
    
    # Start in separate thread
    threading.Thread(target=self.server.start).start()
```

### Server Shutdown
```python
def stop(self):
    """Stop web2py server"""
    self.button_start.configure(state="normal")
    self.button_stop.configure(state="disabled")
    self.password.configure(state="normal")
    
    # Re-enable configuration controls
    for ip in self.ips.values():
        ip.configure(state="normal")
    self.port_number.configure(state="normal")
    
    # Stop server
    self.server.stop()
```

## Scheduler Management

### Process Lifecycle
```python
def start_schedulers(self, app):
    """Start scheduler process for application"""
    from multiprocessing import Process
    
    code = "from gluon.globals import current;current._scheduler.loop()"
    args = (app, True, True, None, False, code, False, True)
    
    p = Process(target=run, args=args)
    
    with self.scheduler_processes_lock:
        self.scheduler_processes[app] = p
        self.update_schedulers()
    
    p.start()

def try_stop_scheduler(self, app, skip_update=False):
    """Stop scheduler process for application"""
    p = None
    with self.scheduler_processes_lock:
        if app in self.scheduler_processes:
            p = self.scheduler_processes[app]
            del self.scheduler_processes[app]
    
    if p is not None:
        p.terminate()
        p.join()
    
    if not skip_update:
        self.update_schedulers()
```

### Scheduler Control
```python
def get_code_for_scheduler(applications_parent, app_groups):
    """Generate scheduler startup code"""
    app = app_groups[0]
    
    if not is_appdir(applications_parent, app):
        print("Application '%s' doesn't exist, skipping" % app)
        return None, None
    
    code = "from gluon.globals import current;"
    
    if len(app_groups) > 1:
        # Add group names
        code += "current._scheduler.group_names=['%s'];" % "','".join(app_groups[1:])
    
    code += "current._scheduler.loop()"
    return app, code
```

## System Tray Integration

### Taskbar Widget
```python
if options.taskbar:
    import gluon.contrib.taskbar_widget
    self.tb = gluon.contrib.taskbar_widget.TaskBarIcon()
    self.checkTaskBar()

def checkTaskBar(self):
    """Monitor taskbar status and handle events"""
    tb = self.tb
    if tb.status:
        st0 = tb.status[0]
        EnumStatus = tb.EnumStatus
        
        if st0 == EnumStatus.QUIT:
            self.quit()
        elif st0 == EnumStatus.TOGGLE:
            if self.root.state() == "withdrawn":
                self.root.deiconify()
            else:
                self.root.withdraw()
        elif st0 == EnumStatus.START:
            self.start()
        elif st0 == EnumStatus.STOP:
            self.stop()
        
        del tb.status[0]
    
    self.root.after(1000, self.checkTaskBar)
```

## Monitoring and Visualization

### Server Activity Graph
```python
def update_canvas(self):
    """Update activity visualization canvas"""
    httplog = os.path.join(self.options.folder, self.options.log_filename)
    canvas = self.canvas
    
    try:
        t1 = os.path.getsize(httplog)
        
        # Read new log data
        with open(httplog, "r") as fp:
            fp.seek(self.t0)
            data = fp.read(t1 - self.t0)
        
        # Calculate activity level
        activity = 10 + 90.0 / math.sqrt(1 + data.count("\n"))
        self.p0 = self.p0[1:] + [activity]
        
        # Update graph lines
        for i in range(len(self.p0) - 1):
            c = canvas.coords(self.q0[i])
            canvas.coords(self.q0[i], (c[0], self.p0[i], c[2], self.p0[i + 1]))
        
        self.t0 = t1
        
    except AttributeError:
        # Initialize graph
        points = 400
        self.t0 = t1
        self.p0 = [100] * points
        self.q0 = [
            canvas.create_line(i, 100, i + 1, 100, fill="green")
            for i in range(points - 1)
        ]
    
    canvas.after(1000, self.update_canvas)
```

## Command Line Interface

### Main Start Function
```python
def start():
    """Main entry point for web2py widget"""
    # Parse command line options
    options = console(version=ProgramVersion)
    
    # Handle special modes
    if options.gae:
        setup_gae_deployment(options)
        return
    
    if options.run_system_tests:
        run_system_tests(options)
        return
    
    if options.shell:
        run_shell_mode(options)
        return
    
    # Setup logging
    logger = logging.getLogger("web2py")
    logger.setLevel(options.log_level)
    
    # Create welcome application if needed
    create_welcome_w2p()
    
    # Start GUI or command line server
    if should_start_gui(options):
        start_gui(options)
    else:
        start_command_line_server(options)
```

### GUI Decision Logic
```python
def should_start_gui(options):
    """Determine if GUI should be started"""
    return (
        (not options.no_gui and options.password == "<ask>") 
        or options.taskbar
    ) and tkinter_available()

def start_gui(options):
    """Start GUI interface"""
    try:
        import tkinter
        root = tkinter.Tk()
        root.focus_force()
        
        # macOS specific window raising
        if os.path.exists("/usr/bin/osascript"):
            applescript = """
tell application "System Events"
    set proc to first process whose unix id is %d
    set frontmost of proc to true
end tell
""" % os.getpid()
            os.system("/usr/bin/osascript -e '%s'" % applescript)
        
        # Create main dialog
        master = web2pyDialog(root, options)
        signal.signal(signal.SIGTERM, lambda a, b: master.quit())
        
        root.mainloop()
        
    except (ImportError, OSError):
        logger.warn("GUI not available because Tk library is not installed")
        start_command_line_server(options)
```

## Utility Functions

### URL Generation
```python
def get_url(host, path="/", proto="http", port=80):
    """Generate proper URL from components"""
    if ":" in host:
        host = "[%s]" % host  # IPv6
    elif host == "0.0.0.0":
        host = "127.0.0.1"
    
    if path.startswith("/"):
        path = path[1:]
    
    if proto.endswith(":"):
        proto = proto[:-1]
    
    if not port or port == 80:
        port = ""
    else:
        port = ":%s" % port
    
    return "%s://%s%s/%s" % (proto, host, port, path)
```

### Browser Integration
```python
def start_browser(url, startup=False):
    """Launch web browser with specified URL"""
    if startup:
        print("please visit:")
        print("\t" + url)
        print("starting browser...")
    
    try:
        import webbrowser
        webbrowser.open(url)
    except:
        print("warning: unable to detect your browser")
```

### System Testing
```python
def run_system_tests(options):
    """Execute web2py system tests"""
    call_args = ["-m", "unittest", "-c", "gluon.tests"]
    
    if options.verbose:
        call_args.insert(-1, "-v")
    
    if options.with_coverage:
        # Setup coverage testing
        coverage_config_file = os.path.join("gluon", "tests", "coverage.ini")
        run_args = ["coverage", "run", "--rcfile=%s" % coverage_config_file]
        os.execvpe(run_args[0], run_args + call_args, os.environ)
    else:
        run_args = [sys.executable]
        os.execv(run_args[0], run_args + call_args)
```

## Configuration Management

### Option Processing
```python
def process_options():
    """Process command line options and environment"""
    options = console()
    
    # Validate scheduler requirements
    if options.with_scheduler or len(options.schedulers) > 1:
        try:
            from multiprocessing import Process
        except ImportError:
            die("Sorry, -K/--scheduler only supported for Python 2.6+")
    
    # Handle password prompt
    if options.password == "<ask>":
        import getpass
        options.password = getpass.getpass("choose a password:")
    
    return options
```

### Environment Setup
```python
def setup_environment(options):
    """Configure runtime environment"""
    # Set up cron thread pools
    newcron.dancer_size(options.min_threads)
    newcron.launcher_size(options.cron_threads)
    
    # Configure cron type
    if options.with_cron:
        if options.soft_cron:
            global_settings.web2py_crontype = "soft"
        else:
            global_settings.web2py_crontype = "hard"
            newcron.hardcron(options.folder, apps=options.crontabs).start()
```

## Error Handling and Cleanup

### Graceful Shutdown
```python
def quit(self, justHide=False):
    """Clean shutdown of all services"""
    if justHide:
        self.root.withdraw()
    else:
        try:
            # Stop all scheduler processes
            with self.scheduler_processes_lock:
                scheds = list(self.scheduler_processes.keys())
            for t in scheds:
                self.try_stop_scheduler(t, skip_update=True)
        except:
            pass
        
        # Stop cron if running
        if self.options.with_cron and not self.options.soft_cron:
            try:
                newcron.stopcron()
            except:
                pass
        
        # Stop HTTP server
        try:
            self.server.stop()
        except:
            pass
        
        # Clean up taskbar
        try:
            self.tb.Destroy()
        except:
            pass
        
        self.root.destroy()
        sys.exit(0)
```

### Error Display
```python
def error(self, message):
    """Display error message in GUI"""
    import tkinter.messagebox as messagebox
    messagebox.showerror("web2py start server", message)
```

## Integration Examples

### Custom Widget Extension
```python
class CustomWeb2pyDialog(web2pyDialog):
    """Extended dialog with custom features"""
    
    def __init__(self, root, options):
        super().__init__(root, options)
        self.add_custom_menu()
    
    def add_custom_menu(self):
        """Add custom application management menu"""
        custommenu = tkinter.Menu(self.menu, tearoff=0)
        
        custommenu.add_command(
            label="Backup Database",
            command=self.backup_database
        )
        
        custommenu.add_command(
            label="Clear Cache",
            command=self.clear_cache
        )
        
        self.menu.add_cascade(label="Tools", menu=custommenu)
    
    def backup_database(self):
        """Perform database backup"""
        # Implementation here
        pass
    
    def clear_cache(self):
        """Clear application cache"""
        # Implementation here
        pass
```

### Headless Server Management
```python
def run_headless_server():
    """Run server without GUI"""
    options = process_options()
    
    # Force command line mode
    options.no_gui = True
    options.password = options.password or "admin"
    
    server = main.HttpServer(
        ip=options.ip,
        port=options.port,
        password=options.password,
        path=options.folder
    )
    
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
```

## Best Practices

### GUI Development
1. Handle threading properly for server operations
2. Provide clear user feedback
3. Implement proper error handling
4. Support keyboard shortcuts
5. Follow platform UI conventions

### Process Management
1. Clean up child processes on exit
2. Handle process failures gracefully
3. Provide process monitoring
4. Implement proper signal handling

### Configuration
1. Validate user input
2. Provide sensible defaults
3. Store user preferences
4. Support command line overrides

## See Also
- Tkinter documentation
- Web2py server configuration
- Python multiprocessing guide
- System tray integration patterns