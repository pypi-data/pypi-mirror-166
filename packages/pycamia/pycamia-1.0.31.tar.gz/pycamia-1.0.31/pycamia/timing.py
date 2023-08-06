
from .manager import info_manager

__info__ = info_manager(
    project = "PyCAMIA",
    package = "<main>",
    author = "Yuncheng Zhou",
    create = "2021-12",
    fileinfo = "File to record time."
)

__all__ = """
    time_this
    Timer
    Jump
    scope
    jump
    Workflow
    periodic
    periodic_run
    periodic_call
""".split()

import time
from functools import wraps
from threading import Timer as tTimer

from .environment import get_environ_vars

def time_this(func):
    """
    A function wrapper of function `func` that outputs the time used to run it. 

    Example:
    ----------
    @timethis
    >>> def func_to_run(*args):
    ...     # inside codes
    ... 
    >>> func_to_run(*input_args)
    # some outputs
    [func_to_run takes 0.001s]
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        if hasattr(getattr(func, '__wrapped__', func), '__name__'):
            print("[%s takes %lfs]"%(func.__name__, end-start))
        else:
            print("[%s takes %lfs]"%(func.__class__.__name__, end-start))
        return result
    return wrapper

class Timer(object):
    """
    An environment that outputs the time used to run codes within. 

    Example:
    ----------
    >>> with Timer("test"):
    ...     # inside codes
    ... 
    # some outputs
    [test takes 0.001s]
    """
    def __init__(self, name='', timing=True):
        if not timing: name = ''
        self.name = name
        self.nround = 0
        self.prevrecord = None
    @property
    def recorded_time(self): return self.prevrecord
    def __enter__(self):
        self.start = time.time()
        self.prevtime = self.start
        return self
    def round(self, name = ''):
        self.nround += 1
        self.end = time.time()
        if self.name:
            if not name: name = "%s(round%d)"%(self.name, self.nround)
            self.prevrecord = self.end - self.prevtime
            print(f"[{name} takes {self.prevrecord}s]")
        self.prevtime = self.end
    def exit(self): raise RuntimeError("JUMP")
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type == RuntimeError and str(exc_value) == "JUMP": return True
        if self.name:
            self.prevrecord = time.time() - self.start
            print(f"[{self.name}{'' if self.nround == 0 else '(all)'} takes {self.prevrecord}s]")

class Jump(object):
    """
    Creates a Jump RuntimeError, designed for instance `jump`. 
    """
    def __init__(self, jump=None): self.jump = True if jump is None else jump
    def __enter__(self):
        def dojump(): raise RuntimeError("JUMP")
        if self.jump: dojump()
        else: return dojump
    def __exit__(self, *args): pass
    def __call__(self, condition): return Jump(condition)
    
def scope(name, timing=True):
    """
    An allias of timer to better organize the codes. 
    
    Inputs:
        name (str): the name of the scope, used to display. 
        timing (bool): whether to show the time span or not. 

    Example:
    ----------
    >>> with scope("test"):
    ...     # inside codes
    ... 
    # some outputs
    [scope test takes 0.001s]
    """
    return Timer("scope " + str(name), timing)

jump = Jump()
"""
The jumper, one can use it along with `scope`(or `Timer`) to jump a chunk of codes. 

Example:
----------
>>> with scope("test"), jump:
...     # inside codes
... 
# nothing, the inside codes do not run
>>> with scope("test"), jump as stop:
...     print('a')
...     stop()
...     print('b')
... 
a
"""

class Workflow:
    """
    A structure to create a series of workflow. 
    
    Note:
        Remember to manually add `, {workflow_name}.jump` after `with` so that 
        we can control it. See the example. 
    
    Args:
        *args: the list of scope names to run. 

    Example:
    ----------
    >>> run = Workflow("read data", "run method", "visualization")
    ... with run("read data"), run.jump:
    ...     print(1, end='')
    ... with run("pre-processing"), run.jump:
    ...     print(2, end='')
    ... with run("run method"), run.jump:
    ...     print(3, end='')
    ... with run("visualization"), run.jump:
    ...     print(4, end='')
    ... 
    1[read data takes 0.000022s]
    3[run method takes 0.000008s]
    4[visualization takes 0.000006s]
    """
    def __init__(self, *args, verbose=True): self.workflow = args; self.verbose=verbose
    def __call__(self, *keys):
        if len(keys) == 1 and isinstance(keys[0], (list, tuple)): keys = keys[0]
        self.keys=keys
        return Timer(','.join(keys), timing=self.verbose)
    def __getattr__(self, *k): return self(*k)
    def __getitem__(self, *k): return self(*k)
    @property
    def j(self): return self.jump
    @property
    def jump(self):
        if len(self.keys) > 1: raise TypeError("Trying to use workflow.jump for section with multiple keys, please use 'jump_or' or 'jump_and' instead. ")
        return Jump(self.keys[0] not in self.workflow)
    @property
    def jump_and(self): return Jump(any(k not in self.workflow for k in self.keys))
    @property
    def jump_or(self): return Jump(all(k not in self.workflow for k in self.keys))

class TimerCtrl(tTimer):
    """
    Creates a Time Handler, designed for function `periodic`. 
    """

    def __init__(self, seconds, function):
        tTimer.__init__(self, seconds, function)
        self.isCanceled = False
        self.seconds = seconds
        self.function = function
        self.funcname = function.__name__
        self.startTime = time.time()

    def cancel(self):
        tTimer.cancel(self)
        self.isCanceled = True

    def is_canceled(self): return self.isCanceled

    def setFunctionName(self, funcname): self.funcname = funcname

    def __str__(self):
        return "%5.3fs to run next "%(self.seconds + self.startTime -
                                      time.time()) + self.funcname

class STOP:
    def __init__(self): self.stopped = False; self.index = 0
    def __bool__(self): return self.stopped
    def set_index(self, index): self.index = index
    def stop(self): self.stopped = True
    def resume(self): self.stopped = False

def periodic(period, maxiter=float('Inf'), wait_return=False):
    """
    A function wrapper to repeatedly run the wrapped function `period`.
    The return of function being False means the periodic process should stop.
    
    Args:
        maxiter (int): the number of iterations. 
        wait_return (bool): If True, the next iteration starts when the current is over, the gap is period.
            If False, the next iteration starts right after 'period' seconds.
        Note: if wait_return is False, function should accept a timer controler timer as the first argument just like 'self'.

    Example:
    ----------
    >>> i = 1
    ... @periodic(1)
    ... def func(timer):
    ...     print(i)
    ...     i+= 1
    ...     timer.stop()
    ...     timer.resume()
    ... 
    1
    2
    3
    [Output every 1s, and GO ON...]
    """
    def wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global count, stopped
            if 'count' not in globals(): count = 1
            if 'stopped' not in globals(): stopped = STOP()
            if stopped: return
            timer_ctrl = TimerCtrl(period, lambda : wrapper(*args, **kwargs))
            timer_ctrl.setFunctionName(func.__name__)
            if not wait_return:
                timer_ctrl.start()
                stopped.set_index(count)
                ret = func(stopped, *args, **kwargs)
                count += 1
                if count >= maxiter: return ret
                return ret
            else:
                ret = func(*args, **kwargs)
                count += 1
                if count >= maxiter: return
                if ret == False: return
                timer_ctrl.start()
        return wrapper
    return wrap

def periodic_run(period, maxiter=float('Inf')):
    return periodic(period, maxiter=maxiter, wait_return=True)

def periodic_call(period, maxiter=float('Inf')):
    return periodic(period, maxiter=maxiter, wait_return=False)
