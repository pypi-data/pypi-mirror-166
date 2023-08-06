import sys as _system
import inspect as _inspect
import time as _time
import os as _os

# Convert variable name to string
def nameof(var):
    callers_local_vars = _inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var][0]

def createof(Type, *args, **kwargs):
    __object__ = Type(*args, **kwargs)
    for keys, vals in Type.__dict__.items():
        if type(vals) is list: __object__[keys] = Type.__dict__[keys].copy()
        if type(vals) is dict: __object__[keys] = Type.__dict__[keys].copy()
    return __object__

class cursor:
    def __init__(self):
        self.ci = None
        if _os.name == "nt":
            self._msvcrt = __import__("msvcrt")
            self._ctypes = __import__("ctypes")
            class _CursorInfo(self._ctypes.Structure):
                _fields_ = [("size", self._ctypes.c_int), ("visible", self._ctypes.c_byte)]
            self.ci = _CursorInfo()
    def hide(self):
        if _os.name == "nt":
            handle = self._ctypes.windll.kernel32.GetStdHandle(-11)
            self._ctypes.windll.kernel32.GetConsoleCursorInfo(handle, self._ctypes.byref(self.ci))
            self.ci.visible = False
            self._ctypes.windll.kernel32.SetConsoleCursorInfo(handle, self._ctypes.byref(self.ci))
        elif _os.name == "posix":
            _system.stdout.write("\033[?25l")
            _system.stdout.flush()
    def show(self):
        if _os.name == "nt":
            handle = self._ctypes.windll.kernel32.GetStdHandle(-11)
            self._ctypes.windll.kernel32.GetConsoleCursorInfo(handle, self._ctypes.byref(self.ci))
            self.ci.visible = True
            self._ctypes.windll.kernel32.SetConsoleCursorInfo(handle, self._ctypes.byref(self.ci))
        elif _os.name == "posix":
            _system.stdout.write("\033[?25h")
            _system.stdout.flush()


class console:
    @staticmethod
    def write(content, timer: int = 0.02, skip="", end="\n"):
        for index in range(len(content)):
            _system.stdout.write(content[index])
            _system.stdout.flush()
            if type(skip) is str and content[index] != skip: _time.sleep(timer)
            if type(skip) is list and content[index] not in skip: _time.sleep(timer)
            if type(skip) is not str and type(skip) is not list: raise Exception("Error, arg skip should be \'str\' or \'list\', not " + type(skip).__name__)
        print(end=end, flush=True)
    @staticmethod
    def read(putout: str, rtype=str):
        return str(input(putout))
    @staticmethod
    def clsline(clear_char=50): _system.stdout.write("\r" + " " * clear_char + "\r"); _system.stdout.flush()
    @staticmethod
    def reline(): print(end="\033[F", flush=True)
# Any variable can be stored in the template, and can be Assgin later with the Add function
class Template:
    def __init__(self, **args):
        self.args = args
        self.assginSelf()

    def __str__(self):
        return str(self.args)

    def assginSelf(self):
        for key, value in self.args.items():
            self.__dict__[key] = value

    def Assgin(self, **arg):
        for key, value in arg.items():
            self.args[key] = value
        self.assginSelf()

    def AssginDict(self, *arg):
        for rdict in arg:
            for key, value in rdict.items():
                self.args[key] = value
            self.assginSelf()

    def delete(self, *arg_names):
        for name in arg_names:
            for vals_name, vals in self.__dict__.items():
                if vals_name == name:
                    del self.__dict__[vals_name]
                    del self.args[vals_name]

    def __add__(self, otherT):
        ReTemplate = Template()
        ReTemplate.AssginDict(self.args, otherT.args)
        return ReTemplate

    def __sub__(self, other):
        ReTemplate = Template()



