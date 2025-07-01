# Gluon Application Compilation Module (`compileapp.py`)

## Overview
This module provides comprehensive application compilation functionality for the web2py framework, handling the execution of application components including models, views, and controllers. It supports both interpreted and pre-compiled code execution with sophisticated caching and optimization features.

## Architecture

### Core Dependencies
```python
import copy, fnmatch, imp, marshal, os, py_compile, random, re, shutil, sys, types
from functools import reduce
from os.path import exists, join as pjoin
from pydal.base import BaseAdapter
from gluon import html, rewrite, validators
from gluon._compat import (PY2, basestring, builtin, integer_types, iteritems,
                           reload, to_bytes, to_native, unicodeT, xrange)
from gluon.cache import Cache
from gluon.cfs import getcfs
from gluon.dal import DAL, Field
from gluon.globals import Response, current
from gluon.http import HTTP, redirect
from gluon.restricted import compile2, restricted
from gluon.template import parse_template
```

### Global Configuration
```python
CACHED_REGEXES = {}
CACHED_REGEXES_MAX_SIZE = 1000
```

## Regular Expression Caching

### `re_compile(regex)`
Intelligent regex compilation with LRU-style caching.

```python
def re_compile(regex):
    try:
        return CACHED_REGEXES[regex]
    except KeyError:
        if len(CACHED_REGEXES) >= CACHED_REGEXES_MAX_SIZE:
            CACHED_REGEXES.clear()
        compiled_regex = CACHED_REGEXES[regex] = re.compile(regex)
        return compiled_regex
```

**Features:**
- **Cache Hit**: Returns pre-compiled regex
- **Cache Miss**: Compiles and stores regex
- **Memory Management**: Clears cache when size limit reached
- **Performance**: Avoids repeated regex compilation

## Component Loading System

### `LOAD()` Function
Comprehensive component loading with AJAX and embedded support.

```python
def LOAD(c=None, f="index", args=None, vars=None, extension=None,
         target=None, ajax=False, ajax_trap=False, url=None,
         user_signature=False, timeout=None, times=1,
         content="loading...", post_vars=Storage(), **attr):
```

#### Parameters
- **c** (str): Controller name
- **f** (str): Function name
- **args** (tuple/list): Function arguments
- **vars** (dict): URL variables
- **extension** (str): File extension
- **target** (str): HTML target element ID
- **ajax** (bool): Enable AJAX behavior
- **ajax_trap** (bool): Trap forms and links within target
- **url** (str): Override URL construction
- **user_signature** (bool): Add HMAC signature
- **timeout** (int): Request timeout in milliseconds
- **times** (int/str): Request frequency ("infinity" for continuous)

#### AJAX Mode Implementation
```python
if url or ajax:
    url = url or html.URL(request.application, c, f, r=request,
                         args=args, vars=vars, extension=extension,
                         user_signature=user_signature)
    
    # Timing configuration
    if isinstance(times, basestring):
        if times.upper() in ("INFINITY", "CONTINUOUS"):
            times = "Infinity"
    
    if timeout is not None:
        statement = "$.web2py.component('%s','%s', %s, %s);" % (
            url, target, timeout, times)
        attr["_data-w2p_timeout"] = timeout
        attr["_data-w2p_times"] = times
    else:
        statement = "$.web2py.component('%s','%s');" % (url, target)
    
    attr["_data-w2p_remote"] = url
    return html.DIV(content, **attr)
```

#### Embedded Mode Implementation
```python
else:
    # Create isolated request/response environment
    other_request = Storage(request)
    other_request["env"] = Storage(request.env)
    other_request.controller = c
    other_request.function = f
    other_request.extension = extension or request.extension
    other_request.args = List(args)
    other_request.vars = vars
    other_request.get_vars = vars
    other_request.post_vars = post_vars
    other_response = Response()
    
    # Environment setup
    other_environment = copy.copy(current.globalenv)
    other_response._view_environment = other_environment
    other_environment["request"] = other_request
    other_environment["response"] = other_response
    
    # Context switching
    original_request, current.request = current.request, other_request
    original_response, current.response = current.response, other_response
    
    # Execute component
    page = run_controller_in(c, f, other_environment)
    if isinstance(page, dict):
        other_response._vars = page
        other_response._view_environment.update(page)
        page = run_view_in(other_response._view_environment)
    
    # Restore context
    current.request, current.response = original_request, original_response
```

### `LoadFactory` Class
Experimental component loading factory with environment isolation.

```python
class LoadFactory(object):
    def __init__(self, environment):
        self.environment = environment
    
    def __call__(self, c=None, f="index", args=None, vars=None, 
                 extension=None, target=None, ajax=False, ajax_trap=False,
                 url=None, user_signature=False, content="loading...", **attr):
        # Similar to LOAD() but uses stored environment
```

## Module Import System

### `local_import_aux(name, reload_force=False, app="welcome")`
Secure local module importing for web2py applications.

```python
def local_import_aux(name, reload_force=False, app="welcome"):
    """
    Import local modules from applications/app/modules/
    
    Usage:
        d = local_import('a.b.c')           # Import module
        d = local_import('a.b.c', reload=True)  # Force reload
    """
    items = name.replace("/", ".")
    name = "applications.%s.modules.%s" % (app, items)
    module = __import__(name)
    for item in name.split(".")[1:]:
        module = getattr(module, item)
    if reload_force:
        reload(module)
    return module
```

**Features:**
- **Namespace Isolation**: Prevents application conflicts
- **Path Conversion**: Handles slash/dot notation
- **Reload Support**: Force module reloading
- **Security**: Restricts imports to application modules

## Environment Management

### Base Environment Setup
```python
_base_environment_ = dict((k, getattr(html, k)) for k in html.__all__)
_base_environment_.update((k, getattr(validators, k)) for k in validators.__all__)
_base_environment_["__builtins__"] = __builtins__
_base_environment_["HTTP"] = HTTP
_base_environment_["redirect"] = redirect
_base_environment_["DAL"] = DAL
_base_environment_["Field"] = Field
_base_environment_["SQLDB"] = DAL  # backward compatibility
_base_environment_["SQLField"] = Field  # backward compatibility
_base_environment_["SQLFORM"] = SQLFORM
_base_environment_["SQLTABLE"] = SQLTABLE
_base_environment_["LOAD"] = LOAD
# Python 3 migration helpers
_base_environment_["PY2"] = PY2
_base_environment_["to_native"] = to_native
_base_environment_["to_bytes"] = to_bytes
_base_environment_["iteritems"] = iteritems
_base_environment_["reduce"] = reduce
_base_environment_["xrange"] = xrange
```

### `build_environment(request, response, session, store_current=True)`
Constructs execution environment for web2py applications.

```python
def build_environment(request, response, session, store_current=True):
    environment = dict(_base_environment_)
    
    if not request.env:
        request.env = Storage()
    
    # Conditional model loading patterns
    response.models_to_run = [
        r"^\w+\.py$",  # All models
        r"^%s/\w+\.py$" % request.controller,  # Controller-specific
        r"^%s/%s/\w+\.py$" % (request.controller, request.function),  # Function-specific
    ]
    
    # Internationalization
    T = environment["T"] = TranslatorFactory(
        pjoin(request.folder, "languages"), 
        request.env.http_accept_language
    )
    
    # Caching
    c = environment["cache"] = Cache(request)
    
    # Validator configuration
    Validator.translator = staticmethod(
        lambda text: None if text is None else str(T(text))
    )
    
    # Global context setup
    if store_current:
        current.globalenv = environment
        current.request = request
        current.response = response
        current.session = session
        current.T = T
        current.cache = c
```

## Compilation System

### Python Bytecode Compilation

#### `save_pyc(filename)`
Compiles Python files to bytecode.

```python
def save_pyc(filename):
    cfile = "%sc" % filename
    py_compile.compile(filename, cfile=cfile)
```

#### `read_pyc(filename)`
Reads and validates compiled bytecode files.

```python
def read_pyc(filename):
    data = read_file(filename, "rb")
    if not global_settings.web2py_runtime_gae and not data.startswith(imp.get_magic()):
        raise SystemError("compiled code is incompatible")
    return marshal.loads(data[MARSHAL_HEADER_SIZE:])
```

**Features:**
- **Magic Number Validation**: Ensures bytecode compatibility
- **GAE Support**: Special handling for Google App Engine
- **Version Compatibility**: Handles Python version differences
- **Error Handling**: Raises SystemError for incompatible bytecode

### View Compilation

#### `compile_views(folder, skip_failed_views=False)`
Compiles all view templates in application.

```python
def compile_views(folder, skip_failed_views=False):
    path = pjoin(folder, "views")
    failed_views = []
    for fname in listdir(path, REGEX_VIEW_PATH, followlinks=True):
        try:
            data = parse_template(fname, path)
        except Exception as e:
            if skip_failed_views:
                failed_views.append(fname)
            else:
                raise Exception("%s in %s" % (e, fname))
        else:
            filename = "views.%s.py" % fname.replace(os.sep, ".")
            filename = pjoin(folder, "compiled", filename)
            write_file(filename, data)
            save_pyc(filename)
            os.unlink(filename)  # Remove source after compilation
    return failed_views or None
```

### Model Compilation

#### `compile_models(folder)`
Compiles all model files in application.

```python
def compile_models(folder):
    path = pjoin(folder, "models")
    for fname in listdir(path, REGEX_MODEL_PATH, followlinks=True):
        data = read_file(pjoin(path, fname))
        modelfile = "models." + fname.replace(os.sep, ".")
        filename = pjoin(folder, "compiled", modelfile)
        mktree(filename)
        write_file(filename, data)
        save_pyc(filename)
        os.unlink(filename)
```

### Controller Compilation

#### `find_exposed_functions(data)`
Extracts exposed function names from controller code.

```python
REGEX_LONG_STRING = re.compile('(""".*?"""|' "'''.*?''')", re.DOTALL)
REGEX_EXPOSED = re.compile(r"^def\s+(_?[a-zA-Z0-9]\w*)\( *\)\s*:", re.MULTILINE)

def find_exposed_functions(data):
    data = REGEX_LONG_STRING.sub("", data)  # Remove docstrings
    return REGEX_EXPOSED.findall(data)
```

#### `compile_controllers(folder)`
Compiles controller functions as separate bytecode files.

```python
def compile_controllers(folder):
    path = pjoin(folder, "controllers")
    for fname in listdir(path, REGEX_CONTROLLER, followlinks=True):
        data = read_file(pjoin(path, fname))
        exposed = find_exposed_functions(data)
        for function in exposed:
            command = data + "\nresponse._vars=response._caller(%s)\n" % function
            filename = pjoin(folder, "compiled", 
                           "controllers.%s.%s.py" % (fname[:-3], function))
            write_file(filename, command)
            save_pyc(filename)
            os.unlink(filename)
```

## Runtime Execution

### Model Execution

#### `run_models_in(environment)`
Executes application models with conditional loading.

```python
def run_models_in(environment):
    request = current.request
    folder = request.folder
    response = current.response
    
    path = pjoin(folder, "models")
    cpath = pjoin(folder, "compiled")
    compiled = exists(cpath)
    
    # Sort models by dependency order
    if PY2:
        models = sorted(listdir(cpath if compiled else path, 
                              REGEX_COMPILED_MODEL if compiled else REGEX_MODEL, 
                              0), model_cmp)
    else:
        models = sorted(listdir(cpath if compiled else path,
                              REGEX_COMPILED_MODEL if compiled else REGEX_MODEL,
                              0, sort=False),
                       key=lambda f: "{0:03d}".format(f.count("." if compiled else os.sep)) + f)
    
    # Execute models based on patterns
    models_to_run = None
    for model in models:
        if response.models_to_run != models_to_run:
            regex = models_to_run = response.models_to_run[:]
            if isinstance(regex, list):
                regex = re_compile("|".join(regex))
        
        if models_to_run:
            # Determine filename for pattern matching
            if compiled:
                n = len(cpath) + 8
                fname = model[n:-4].replace(".", "/") + ".py"
            else:
                n = len(path) + 1
                fname = model[n:].replace(os.sep, "/")
            
            # Check if model matches execution patterns
            if not regex.search(fname) and c != "appadmin":
                continue
            
            # Prepare code for execution
            if compiled:
                f = lambda: read_pyc(model)
            else:
                f = lambda: compile2(read_file(model), model)
            
            ccode = getcfs(model, model, f)
            restricted(ccode, environment, layer=model)
```

### Controller Execution

#### `run_controller_in(controller, function, environment)`
Executes controller functions with pre-compilation support.

```python
def run_controller_in(controller, function, environment):
    folder = current.request.folder
    cpath = pjoin(folder, "compiled")
    badc = "invalid controller (%s/%s)" % (controller, function)
    badf = "invalid function (%s/%s)" % (controller, function)
    
    if exists(cpath):
        # Try pre-compiled version
        filename = pjoin(cpath, "controllers.%s.%s.pyc" % (controller, function))
        try:
            ccode = getcfs(filename, filename, lambda: read_pyc(filename))
        except IOError:
            raise HTTP(404, rewrite.THREAD_LOCAL.routes.error_message % badf, 
                      web2py_error=badf)
    elif function == "_TEST":
        # Special testing function
        filename = pjoin(folder, "controllers/%s.py" % controller)
        if not exists(filename):
            raise HTTP(404, rewrite.THREAD_LOCAL.routes.error_message % badc,
                      web2py_error=badc)
        environment["__symbols__"] = list(environment.keys())
        code = read_file(filename) + TEST_CODE
        ccode = compile2(code, filename)
    else:
        # Regular controller execution
        filename = pjoin(folder, "controllers/%s.py" % controller)
        try:
            code = getcfs(filename, filename, lambda: read_file(filename))
        except IOError:
            raise HTTP(404, rewrite.THREAD_LOCAL.routes.error_message % badc,
                      web2py_error=badc)
        
        # Verify function is exposed
        exposed = find_exposed_functions(code)
        if function not in exposed:
            raise HTTP(404, rewrite.THREAD_LOCAL.routes.error_message % badf,
                      web2py_error=badf)
        
        # Prepare execution code
        code = "%s\nresponse._vars=response._caller(%s)" % (code, function)
        layer = "%s:%s" % (filename, function)
        ccode = getcfs(layer, filename, lambda: compile2(code, filename))
    
    # Execute and process response
    restricted(ccode, environment, layer=filename)
    response = environment["response"]
    vars = response._vars
    
    # Apply postprocessing
    if response.postprocessing:
        vars = reduce(lambda vars, p: p(vars), response.postprocessing, vars)
    
    # Handle different return types
    if isinstance(vars, unicodeT):
        vars = to_native(vars)
    elif hasattr(vars, "xml") and callable(vars.xml):
        vars = vars.xml()
    
    return vars
```

### View Execution

#### `run_view_in(environment)`
Executes view templates with fallback to generic views.

```python
def run_view_in(environment):
    request = current.request
    response = current.response
    view = environment["response"].view
    folder = request.folder
    cpath = pjoin(folder, "compiled")
    badv = "invalid view (%s)" % view
    
    # Generic view pattern matching
    patterns = response.get("generic_patterns")
    if patterns:
        regex = re_compile("|".join(fnmatch.translate(p) for p in patterns))
        short_action = "%(controller)s/%(function)s.%(extension)s" % request
        allow_generic = regex.search(short_action)
    else:
        allow_generic = False
    
    # Handle different view types
    if not isinstance(view, str):
        # File stream view
        ccode = parse_template(view, pjoin(folder, "views"), context=environment)
        layer = "file stream"
    else:
        filename = pjoin(folder, "views", view)
        layer = None
        
        # Try compiled views first
        if exists(cpath):
            x = view.replace("/", ".")
            files = ["views.%s.pyc" % x]
            is_compiled = exists(pjoin(cpath, files[0]))
            
            if is_compiled or (not is_compiled and not exists(filename)):
                if allow_generic:
                    files.append("views.generic.%s.pyc" % request.extension)
                # Backward compatibility
                if request.extension == "html":
                    files.append("views.%s.pyc" % x[:-5])
                    if allow_generic:
                        files.append("views.generic.pyc")
                
                # Try each compiled view file
                for f in files:
                    compiled = pjoin(cpath, f)
                    if exists(compiled):
                        ccode = getcfs(compiled, compiled, lambda: read_pyc(compiled))
                        layer = compiled
                        break
        
        # Fall back to source view
        if not layer:
            if not exists(filename) and allow_generic:
                view = "generic." + request.extension
                filename = pjoin(folder, "views", view)
            
            if not exists(filename):
                raise HTTP(404, rewrite.THREAD_LOCAL.routes.error_message % badv,
                          web2py_error=badv)
            
            # Parse and compile template
            scode = parse_template(view, pjoin(folder, "views"), context=environment)
            ccode = compile2(scode, filename)
            layer = filename
    
    # Execute view
    restricted(ccode, environment, layer=layer, scode=scode)
    return environment["response"].body.getvalue()
```

## Application Management

### `compile_application(folder, skip_failed_views=False)`
Compiles entire application for production deployment.

```python
def compile_application(folder, skip_failed_views=False):
    remove_compiled_application(folder)
    os.mkdir(pjoin(folder, "compiled"))
    compile_models(folder)
    compile_controllers(folder)
    failed_views = compile_views(folder, skip_failed_views)
    return failed_views
```

### `remove_compiled_application(folder)`
Removes compiled application files.

```python
def remove_compiled_application(folder):
    try:
        shutil.rmtree(pjoin(folder, "compiled"))
        path = pjoin(folder, "controllers")
        for file in listdir(path, REGEX_COMPILED_CONTROLLER, drop=False):
            os.unlink(file)
    except OSError:
        pass
```

## Testing Framework

### Integrated Testing Support
```python
TEST_CODE = r"""
def _TEST():
    import doctest, sys, cStringIO, types, gluon.fileutils
    if not gluon.fileutils.check_credentials(request):
        raise HTTP(401, web2py_error='invalid credentials')
    
    stdout = sys.stdout
    html = '<h2>Testing controller "%s.py" ... done.</h2><br/>\n' % request.controller
    
    for key in sorted([key for key in globals() if not key in __symbols__+['_TEST']]):
        eval_key = eval(key)
        if type(eval_key) == types.FunctionType:
            number_doctests = sum([len(ds.examples) for ds in doctest.DocTestFinder().find(eval_key)])
            if number_doctests > 0:
                sys.stdout = cStringIO.StringIO()
                name = '%s/controllers/%s.py in %s.__doc__' % (request.folder, request.controller, key)
                doctest.run_docstring_examples(eval_key, globals(), False, name=name)
                report = sys.stdout.getvalue().strip()
                
                if report:
                    pf = 'failed'
                else:
                    pf = 'passed'
                
                html += '<h3 class="%s">Function %s [%s]</h3>\n' % (pf, key, pf)
                if report:
                    html += CODE(report, language='web2py', link='/examples/global/vars/').xml()
                html += '<br/>\n'
            else:
                html += '<h3 class="nodoctests">Function %s [no doctests]</h3><br/>\n' % key
    
    response._vars = html
    sys.stdout = stdout

_TEST()
"""
```

This comprehensive module provides the foundation for web2py's application execution system, supporting both development and production scenarios with sophisticated compilation, caching, and execution capabilities.