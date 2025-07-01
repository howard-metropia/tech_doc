# Gluon Debug Module Documentation

## Overview
The `debug.py` module provides comprehensive debugging infrastructure for the Gluon web framework. It implements both traditional PDB-based debugging and a modern web-based debugging interface, supporting remote debugging, thread-safe debugging sessions, and interactive debugging capabilities.

## Module Information
- **File**: `allrepo/connectsmart/hybrid/gluon/debug.py`
- **Component**: Web2py Framework Debug Infrastructure
- **Purpose**: Interactive debugging, remote debugging, and web-based debug interfaces
- **Dependencies**: logging, pdb, sys, threading, Queue, gluon.contrib.dbg
- **Integration**: ConnectSmart platform development tools

## Key Components

### Legacy PDB Implementation

#### Pipe Class
```python
class Pipe(Queue.Queue):
    """Thread-safe communication pipe for debugger interaction"""
    
    def __init__(self, name, mode="r", *args, **kwargs):
        self.__name = name
        Queue.Queue.__init__(self, *args, **kwargs)
```

**Features:**
- **Thread Safety**: Built on Queue.Queue for safe inter-thread communication
- **Bidirectional**: Supports both input and output pipes
- **Blocking I/O**: Implements blocking read/write operations
- **Logging**: Comprehensive debug logging for all operations

#### Pipe Operations
```python
def write(self, data):
    """Write data to the pipe with logging"""
    logger.debug("debug %s writing %s" % (self.__name, data))
    self.put(data)

def read(self, count=None, timeout=None):
    """Read data from pipe with timeout support"""
    logger.debug("debug %s reading..." % (self.__name,))
    data = self.get(block=True, timeout=timeout)
    self.task_done()
    logger.debug("debug %s read %s" % (self.__name, data))
    return data

def flush(self):
    """Flush pipe and wait for processing completion"""
    logger.debug("debug %s flushing..." % self.__name)
    self.put(None)  # Mark checkpoint
    self.join()     # Wait for processing
    logger.debug("debug %s flush done" % self.__name)
```

#### PDB Integration
```python
pipe_in = Pipe("in")
pipe_out = Pipe("out")

debugger = pdb.Pdb(
    completekey=None,
    stdin=pipe_in,
    stdout=pipe_out,
)
```

### Modern Web Debugger

#### WebDebugger Class
```python
class WebDebugger(c_dbg.Frontend):
    """Qdb web2py interface with thread-safe interaction"""
    
    def __init__(self, pipe, completekey="tab", stdin=None, stdout=None):
        c_dbg.Frontend.__init__(self, pipe)
        self.clear_interaction()
```

**State Management:**
- **filename**: Current file being debugged
- **lineno**: Current line number
- **exception_info**: Exception details if debugging an error
- **context**: Debug context including stack and variables

#### Thread Safety
```python
from threading import RLock

interact_lock = RLock()
run_lock = RLock()

@check_interaction
def do_continue(self):
    """Thread-safe continue operation"""
    c_dbg.Frontend.do_continue(self)
```

**Locking Strategy:**
- **interact_lock**: Protects interaction state
- **run_lock**: Protects debugger execution
- **check_interaction**: Decorator for safe method calls

### Debugging Commands

#### Core Debug Operations
```python
@check_interaction
def do_step(self):
    """Step into next statement"""
    c_dbg.Frontend.do_step(self)

@check_interaction  
def do_next(self):
    """Step over next statement"""
    c_dbg.Frontend.do_next(self)

@check_interaction
def do_return(self):
    """Continue until function returns"""
    c_dbg.Frontend.do_return(self)

@check_interaction
def do_quit(self):
    """Quit debugger session"""
    c_dbg.Frontend.do_quit(self)
```

#### Code Execution
```python
def do_exec(self, statement):
    """Execute code in debugger context"""
    interact_lock.acquire()
    try:
        if self.filename:
            # Avoid spurious interaction notifications
            self.set_burst(2)
            # Execute in remote debugger
            return c_dbg.Frontend.do_exec(self, statement)
    finally:
        interact_lock.release()
```

### Communication Infrastructure

#### Queue-Based Communication
```python
parent_queue, child_queue = Queue.Queue(), Queue.Queue()
front_conn = c_dbg.QueuePipe("parent", parent_queue, child_queue)
child_conn = c_dbg.QueuePipe("child", child_queue, parent_queue)
```

**Architecture:**
- **Frontend**: Web interface running in main thread
- **Backend**: Debugger running in application thread
- **Bidirectional**: Commands and responses flow both ways
- **Decoupled**: Frontend and backend operate independently

#### Debugger Instances
```python
web_debugger = WebDebugger(front_conn)  # Frontend
dbg_debugger = c_dbg.Qdb(pipe=child_conn, redirect_stdio=False, skip=None)  # Backend
dbg = dbg_debugger  # Convenient alias
```

### Interaction Management

#### State Tracking
```python
def interaction(self, filename, lineno, line, **context):
    """Store current debugging state"""
    interact_lock.acquire()
    try:
        self.filename = filename
        self.lineno = lineno  
        self.context = context
    finally:
        interact_lock.release()
```

#### Exception Handling
```python
def exception(self, title, extype, exvalue, trace, request):
    """Store exception information for debugging"""
    self.exception_info = {
        "title": title,
        "extype": extype,
        "exvalue": exvalue,
        "trace": trace,
        "request": request,
    }
```

### Usage Examples

#### Basic Debugging
```python
from gluon.debug import set_trace

def my_function():
    x = 10
    set_trace()  # Breakpoint here
    y = x * 2
    return y
```

#### Remote Debugging Session
```python
# Start debugging session
from gluon.debug import communicate

# Send commands to debugger
result = communicate("l")  # List current code
result = communicate("p x")  # Print variable x
result = communicate("n")  # Next statement
result = communicate("c")  # Continue execution
```

#### Web-Based Debugging
```python
from gluon.debug import web_debugger

# Check if debugging session is active
if web_debugger.filename:
    print(f"Debugging {web_debugger.filename}:{web_debugger.lineno}")
    
# Execute code in debug context
result = web_debugger.do_exec("print(locals())")

# Control execution
web_debugger.do_step()  # Step into
web_debugger.do_next()  # Step over
web_debugger.do_continue()  # Continue
```

### Legacy PDB Functions

#### set_trace()
```python
def set_trace():
    """Breakpoint shortcut (like pdb)"""
    logger.info("DEBUG: set_trace!")
    debugger.set_trace(sys._getframe().f_back)
```

#### communicate()
```python
def communicate(command=None):
    """Send command to debugger, wait result"""
    if command is not None:
        logger.info("DEBUG: sending command %s" % command)
        pipe_in.write(command)
    
    result = []
    while True:
        data = pipe_out.read()
        if data is None:
            break
        result.append(data)
    
    logger.info("DEBUG: result %s" % repr(result))
    return "".join(result)
```

#### stop_trace()
```python
def stop_trace():
    """Stop waiting for the debugger (called atexit)"""
    logger.info("DEBUG: stop_trace!")
    pipe_out.write("debug finished!")
    pipe_out.write(None)
```

### Decorator System

#### check_interaction Decorator
```python
def check_interaction(fn):
    """Decorator to clean and prevent interaction when not available"""
    
    def check_fn(self, *args, **kwargs):
        interact_lock.acquire()
        try:
            if self.filename:
                self.clear_interaction()
                return fn(self, *args, **kwargs)
        finally:
            interact_lock.release()
    
    return check_fn
```

**Purpose:**
- **State Validation**: Ensures debugger is in valid state
- **Resource Cleanup**: Clears interaction state after use
- **Thread Safety**: Protects operations with locks
- **Error Prevention**: Prevents invalid operations

### Configuration

#### Debugger Parameters
```python
# Enable context information
dbg_debugger.set_params(dict(
    call_stack=True,    # Include call stack
    environment=True,   # Include variable environment
))
```

#### Global Settings Integration
```python
import gluon.main
gluon.main.global_settings.debugging = True
```

### Performance Considerations

#### Development Mode
- **Full Debugging**: All features enabled
- **Context Capture**: Stack and environment information
- **Interactive Response**: Real-time debugging capabilities

#### Production Considerations
- **Debugging Disabled**: No performance impact when not debugging
- **Conditional Activation**: Debug features only when needed
- **Resource Management**: Proper cleanup of debug resources

### Security Considerations

#### Debug Access Control
- **Development Only**: Debug features should be disabled in production
- **Code Execution**: Debug interface allows arbitrary code execution
- **Session Isolation**: Each debug session is isolated

#### Information Disclosure
- **Variable Inspection**: Full access to application state
- **Stack Traces**: Complete execution context available
- **File Access**: Debug interface can access application files

### Integration Points

#### Web2py Framework
- **Global Settings**: Integrates with framework configuration
- **Request Context**: Accesses web2py request/response objects
- **Exception Handling**: Hooks into web2py error handling

#### ConnectSmart Platform
- **Development Tools**: Enhanced debugging for API development
- **Error Tracking**: Integration with error monitoring systems
- **Performance Debugging**: Analysis of request processing

### Advanced Features

#### Context Capture
```python
# Debugger captures comprehensive context
context = {
    'locals': frame.f_locals,
    'globals': frame.f_globals,
    'stack': traceback.extract_stack(),
    'variables': inspect.currentframe()
}
```

#### Burst Mode
```python
# Prevent excessive interaction notifications
self.set_burst(2)  # Skip next 2 interactions
```

#### Queue Management
```python
# Proper queue lifecycle management
self.task_done()  # Signal task completion
self.join()       # Wait for queue processing
```

This debug module provides comprehensive debugging infrastructure for the Gluon framework, supporting both traditional command-line debugging and modern web-based debugging interfaces, with robust thread safety and extensive integration capabilities for the ConnectSmart platform development environment.