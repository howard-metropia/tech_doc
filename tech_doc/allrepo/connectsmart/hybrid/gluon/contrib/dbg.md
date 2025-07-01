# dbg.py

🔍 **Quick Summary (TL;DR)**
- Advanced remote Python debugger with queue-based bidirectional communication, providing comprehensive debugging capabilities for Web2py applications
- Core functionality: remote debugging | queue-based communication | breakpoint management | variable inspection | call stack analysis | post-mortem debugging
- Primary use cases: Production debugging, remote development, complex application troubleshooting, multi-threaded debugging
- Quick compatibility: Python 2.7+/3.x, multiprocessing support, Web2py framework, network connectivity for remote debugging

❓ **Common Questions Quick Index**
- Q: How to start remote debugging? A: [Usage Methods](#usage-methods) - Use set_trace() or debug() functions
- Q: What debugging commands are available? A: [Detailed Code Analysis](#detailed-code-analysis) - Step, next, continue, breakpoints, eval
- Q: How to connect debugger frontend? A: [Technical Specifications](#technical-specifications) - Use start() function with host/port
- Q: Can this debug production code? A: [Important Notes](#important-notes) - Yes, but use cautiously with proper security
- Q: How to set breakpoints remotely? A: [Usage Methods](#usage-methods) - Use do_set_breakpoint() method
- Q: What's the communication protocol? A: [Detailed Code Analysis](#detailed-code-analysis) - JSON-RPC like messaging
- Q: How to inspect variables? A: [Output Examples](#output-examples) - Use do_eval() and do_environment()
- Q: How to troubleshoot connection issues? A: [Important Notes](#important-notes) - Check network, authentication, and firewall

📋 **Functionality Overview**
- **Non-technical explanation:** Like having a remote control for debugging code that's running anywhere - imagine being able to pause a program running on a server, look at what's happening inside, step through the code line by line, and even change values, all from your local computer. It's like having X-ray vision and remote control for software problems.
- **Technical explanation:** Queue-based remote debugger implementing bidirectional RPC communication, providing full debugging capabilities including breakpoint management, variable inspection, call stack analysis, and post-mortem debugging for distributed applications.
- Business value: Enables debugging of production systems without disruption, reduces downtime through remote troubleshooting, accelerates problem resolution
- Context: Advanced debugging tool for Web2py applications requiring remote debugging capabilities, particularly useful for production environments and distributed systems

🔧 **Technical Specifications**
- File: dbg.py, /gluon/contrib/, Python, Debugging utility, ~35KB, Very high complexity
- Dependencies: bdb (Python debugger base), threading, multiprocessing, collections, json (communication)
- Compatibility: Python 2.7+/3.x, multiprocessing support, network connectivity, Web2py framework
- Configuration: Host/port for connections, authentication key, stdio redirection options
- System requirements: Network access, proper firewall configuration, multiprocessing support
- Security: Authentication key based access, configurable stdio redirection, connection encryption

📝 **Detailed Code Analysis**
```python
class Qdb(bdb.Bdb):
    """Queue-based debugger backend with RPC communication"""
    
    def __init__(self, pipe, redirect_stdio=True, allow_interruptions=False):
        bdb.Bdb.__init__(self)
        self.pipe = pipe  # Communication channel
        self.waiting = False
        self.frame = None
        
        # Replace stdio for remote communication
        if redirect_stdio:
            sys.stdin = self
            sys.stdout = self
            sys.stderr = self
```

**RPC Communication Protocol:**
```python
def pull_actions(self):
    """Process remote procedure calls from frontend"""
    request = self.pipe.recv()
    response = {'version': '1.1', 'id': request.get('id'), 
                'result': None, 'error': None}
    try:
        # Dispatch method call
        method = getattr(self, request['method'])
        response['result'] = method(*request['args'], 
                                   **request.get('kwargs', {}))
    except Exception as e:
        response['error'] = {'code': 0, 'message': str(e)}
    
    # Send response for normal calls, not notifications
    if request.get('id'):
        self.pipe.send(response)
```

**Debugging Commands:**
```python
def do_step(self):
    """Execute current line, stop at first possible occasion"""
    self.set_step()
    self.waiting = False

def do_next(self):
    """Execute current line, don't stop at function calls"""
    self.set_next(self.frame)
    self.waiting = False

def do_continue(self):
    """Continue execution until breakpoint"""
    self.set_continue()
    self.waiting = False
    self.fast_continue = self.use_speedups

def do_eval(self, arg, safe=True):
    """Evaluate expression in current frame"""
    if self.frame:
        ret = eval(arg, self.frame.f_globals, self.frame_locals)
        if safe:
            ret = pydoc.cram(repr(ret), 255)
        return ret
```

**Breakpoint Management:**
```python
def do_set_breakpoint(self, filename, lineno, temporary=0, cond=None):
    global breaks  # Speed optimization
    breaks.append((filename.replace("\\", "/"), int(lineno)))
    return self.set_break(filename, int(lineno), temporary, cond)

def do_list_breakpoint(self):
    breaks = []
    for bp in bdb.Breakpoint.bpbynumber:
        if bp:
            breaks.append((bp.number, bp.file, bp.line, 
                         bp.temporary, bp.enabled, bp.hits, bp.cond))
    return breaks
```

**Design Patterns:** Command pattern for debugging actions, Observer pattern for frame events, RPC pattern for communication
**Performance:** Speed optimizations with fast_continue mode, global breakpoint list for performance
**Communication:** JSON-RPC like protocol with bidirectional messaging, authentication support

🚀 **Usage Methods**
```python
# Basic remote debugging setup
from gluon.contrib.dbg import set_trace, debug, start

# Start debugging immediately
set_trace(host='localhost', port=6000, authkey='secret')

# Start debugging without immediate stop
debug(host='localhost', port=6000, authkey='secret')

# Start debugger server (on debugging machine)
start(host='localhost', port=6000, authkey='secret')

# In application code - set breakpoint
import gluon.contrib.dbg as dbg
dbg.set_trace()  # Immediate debugging

# Command line debugging
python -m gluon.contrib.dbg script.py
```

**Remote Debugging Session:**
```python
# On server (target application)
from gluon.contrib.dbg import debug
debug(host='debugger-machine', port=6000)

# Your application code continues here
def complex_function(data):
    # This will hit the debugger if breakpoint is set
    result = process_data(data)
    return result

# On debugger machine (developer's computer)
from gluon.contrib.dbg import start
start(host='0.0.0.0', port=6000)  # Wait for connection
```

**Interactive Debugging Commands:**
```python
# In debugger frontend
(Qdb) l                    # List source code
(Qdb) n                    # Next line
(Qdb) s                    # Step into
(Qdb) c                    # Continue
(Qdb) b filename:line      # Set breakpoint
(Qdb) p variable_name      # Print variable
(Qdb) w                    # Show call stack
(Qdb) eval expression      # Evaluate expression
(Qdb) !statement          # Execute statement
```

**Post-mortem Debugging:**
```python
# Automatic post-mortem on exceptions
try:
    risky_operation()
except Exception:
    import gluon.contrib.dbg as dbg
    dbg.qdb.post_mortem()  # Debug the exception
```

📊 **Output Examples**
**Debugger Session:**
```
qdb debugger backend: waiting for connection at ('localhost', 6000)
qdb debugger backend: connected to ('192.168.1.100', 45678)

> /app/mymodule.py(42)
-> result = calculate_value(input_data)
(Qdb) l
  37    def process_request(self, data):
  38        print("Processing:", data)
  39        input_data = self.validate_input(data)
  40        if input_data:
  41            # Complex calculation
  42 ->         result = calculate_value(input_data)
  43            return self.format_result(result)
  44        return None

(Qdb) p input_data
{'id': 123, 'value': 45.7, 'type': 'calculation'}

(Qdb) s
> /app/mymodule.py(15)
-> def calculate_value(data):
```

**Variable Inspection:**
```
(Qdb) eval len(data_list)
25

(Qdb) eval data_dict.keys()
dict_keys(['id', 'name', 'values', 'metadata'])

(Qdb) w
/app/main.py(67)<module>()
-> main()
/app/main.py(45)main()
-> process_batch(batch_data)
/app/mymodule.py(23)process_batch()
-> result = calculate_value(item)
```

**Breakpoint Management:**
```
(Qdb) b mymodule.py:50
(Qdb) b
Num File                          Line Temp Enab Hits Cond
1   /app/mymodule.py                50 False True    0 None
2   /app/helpers.py                 123 False True    3 x > 10
```

**Exception Handling:**
```
Exception occurred: ValueError
Traceback (most recent call last):
  File "/app/mymodule.py", line 67, in calculate
    result = int(value) / divisor
ValueError: invalid literal for int() with base 10: 'abc'

> /app/mymodule.py(67)
-> result = int(value) / divisor
(Qdb) p value
'abc'
(Qdb) p divisor
0
```

⚠️ **Important Notes**
- **Security Risk:** Remote debugging opens network ports, use strong authentication keys in production
- **Performance Impact:** Debugging adds overhead, use sparingly in production environments
- **Network Requirements:** Requires open network connections, configure firewalls appropriately
- **Thread Safety:** Handles multi-threaded applications but may affect thread timing
- **Production Usage:** Exercise extreme caution when debugging production systems
- **Connection Management:** Ensure proper cleanup of debugging connections

**Common Troubleshooting:**
- Connection refused → Check network connectivity, firewall rules, and port availability
- Authentication failed → Verify authkey matches between client and server
- Debugging not stopping → Check breakpoint placement and code execution path
- Variable not found → Verify variable scope and frame context
- Performance degradation → Disable debugging in production or use conditional breakpoints

🔗 **Related File Links**
- Python bdb module documentation for debugging concepts
- Multiprocessing documentation for communication pipes
- Web2py deployment guides for production debugging
- Network security documentation for remote debugging
- Threading documentation for multi-threaded debugging
- Exception handling best practices for production systems

📈 **Use Cases**
- **Production Debugging:** Troubleshoot issues in live systems without disruption
- **Remote Development:** Debug applications running on remote servers
- **Complex Bug Investigation:** Deep dive into hard-to-reproduce issues
- **Performance Analysis:** Analyze execution flow and variable states
- **Integration Testing:** Debug interactions between distributed components
- **Exception Analysis:** Post-mortem debugging of crashed applications

🛠️ **Improvement Suggestions**
- **Security Enhancement:** Implement SSL/TLS encryption for communication
- **Performance Monitoring:** Add debugging overhead metrics and monitoring
- **Session Management:** Implement session persistence and reconnection
- **Visual Frontend:** Develop GUI frontend for better debugging experience
- **Log Integration:** Combine with application logging for comprehensive debugging
- **Conditional Debugging:** Add smart breakpoints based on conditions or metrics
- **Documentation Generation:** Auto-generate debugging sessions for knowledge sharing

🏷️ **Document Tags**
- Keywords: remote debugging, Python debugger, RPC communication, breakpoint management, production debugging, post-mortem analysis, variable inspection, call stack, Web2py debugging
- Technical tags: #remote-debugging #python-debugger #rpc-communication #production-debugging #web2py-contrib
- Target roles: Senior developers (expert), DevOps engineers (advanced), System administrators (intermediate)
- Difficulty level: ⭐⭐⭐⭐⭐ - Requires deep understanding of debugging, networking, and system administration
- Maintenance level: High - Complex system requiring updates for Python versions and security patches
- Business criticality: High - Critical for production issue resolution and system maintenance
- Related topics: Python debugging, remote development, production monitoring, distributed systems, network programming