# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,C0112,C0103,C0114,C0115,C0116,R0903


import datetime
import json
import os
import pathlib
import time
import types
import _thread


from json import JSONDecoder, JSONEncoder


def __dir__():
    return (
            'Class',
            'Db',
            'Default',
            'Object',
            'ObjectDecoder',
            'ObjectEncoder',
            'Wd',
            'edit',
            'dump',
            'dumps',
            'find',
            'get',
            'items',
            'iter',
            'keys',
            'last',
            'load',
            'loads',
            'otype',
            'getname',
            'printable',
            'register',
            'save',
            'search',
            'update',
            'values'
           )



## object


class Object:

    __slots__ = ('__dict__','__stp__')

    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self.__stp__ = os.path.join(
            otype(self),
            os.sep.join(str(datetime.datetime.now()).split()),
        )
        if args:
            update(self, args[0])

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self. __dict__)


class Default(Object):

    __slots__ = ("__default__",)

    def __init__(self, *args, **kwargs):
        Object.__init__(self, *args, **kwargs)
        self.__default__ = ""

    def __getattr__(self, key: str):
        return self.__dict__.get(key, self.__default__)


class Wd:

    workdir = ".op"

    @staticmethod
    def get() -> None:
        return Wd.workdir

    @staticmethod
    def getpath(path) -> str:
        return os.path.join(Wd.workdir, "store", path)

    @staticmethod
    def set(val) -> None:
        Wd.workdir = val

    @staticmethod
    def types():
        res = []
        path = os.path.join(Wd.workdir, "store")
        for fnm in os.listdir(path):
            res.append(fnm)
        return res


def delete(obj, key) -> None:
    delattr(obj, key)


def edit(obj, setter) -> None:
    for key, value in items(setter):
        register(obj, key, value)


def get(obj, key, default=None) -> type(object):
    return obj.__dict__.get(key, default)


def getname(obj) -> str:
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if "__self__" in dir(obj):
        return "%s.%s" % (obj.__self__.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj) and "__name__" in dir(obj):
        return "%s.%s" % (obj.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj):
        return obj.__class__.__name__
    if "__name__" in dir(obj):
        return obj.__name__
    return None


def items(obj) -> list:
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj) -> list:
    return obj.__dict__.keys()


def otype(obj) -> str:
    return str(type(obj)).split()[-1][1:-2]


def printable(obj, args="", skip="", plain=False) -> str:
    res = []
    try:
        keyz = args.split(",")
    except (AttributeError, TypeError, ValueError):
        keyz = keys(obj)
    for key in keyz:
        try:
            skips = skip.split(",")
            if key in skips or key.startswith("_"):
                continue
        except (TypeError, ValueError):
            pass
        value = getattr(obj, key, None)
        if not value:
            continue
        if " object at " in str(value):
            continue
        txt = ""
        if plain:
            txt = str(value)
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt = '%s="%s"' % (key, value)
        else:
            txt = '%s=%s' % (key, value)
        res.append(txt)
    return " ".join(res)


def register(obj, key, value) -> None:
    setattr(obj, key, value)


def save(obj) -> str:
    prv = os.sep.join(obj.__stp__.split(os.sep)[:1])
    obj.__stp__ = os.path.join(
                       prv,
                       os.sep.join(str(datetime.datetime.now()).split())
                      )
    opath = Wd.getpath(obj.__stp__)
    dump(obj, opath)
    os.chmod(opath, 0o444)
    return obj.__stp__


def search(obj, selector) -> bool:
    res = False
    select = Selector(selector)
    for key, value in items(select):
        val = get(obj, key)
        if value in str(val):
            res = True
            break
    return res


def update(obj, data) -> None:
    if isinstance(data, type({})):
        obj.__dict__.update(data)
    else:
        obj.__dict__.update(vars(data))


def values(obj) -> list:
    return obj.__dict__.values()


## json


class ObjectDecoder(JSONDecoder):

    def  __init__(self, *args, **kwargs):
        ""
        JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, inp, _w=None):
        ""
        value = json.loads(inp)
        return Object(value)

    def raw_decode(self, inp, *args, **kwargs):
        return JSONDecoder.raw_decode(self, inp, *args, **kwargs)


class ObjectEncoder(JSONEncoder):

    def  __init__(self, *args, **kwargs):
        ""
        JSONEncoder.__init__(self, *args, **kwargs)

    def encode(self, obj):
        ""
        return JSONEncoder.encode(self, obj)

    def default(self, obj):
        ""
        if isinstance(obj, dict):
            return obj.items()
        if isinstance(obj, Object):
            return vars(obj)
        if isinstance(obj, list):
            return iter(obj)
        if isinstance(obj,
                      (type(str), type(True), type(False),
                       type(int), type(float))
                     ):
            return obj
        try:
            return JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)

    def iterencode(self, obj, *args, **kwargs):
        ""
        return JSONEncoder.iterencode(self, obj, *args, **kwargs)


def dump(obj, opath):
    cdir(opath)
    with open(opath, "w", encoding="utf-8") as ofile:
        json.dump(
            obj.__dict__, ofile, cls=ObjectEncoder, indent=4, sort_keys=True
        )
    return obj.__stp__


def dumps(obj):
    return json.dumps(obj, cls=ObjectEncoder)


def load(obj, opath):
    splitted = opath.split(os.sep)
    stp = os.sep.join(splitted[-4:])
    lpath = os.path.join(Wd.workdir, "store", stp)
    if os.path.exists(lpath):
        with open(lpath, "r", encoding="utf-8") as ofile:
            res = json.load(ofile, cls=ObjectDecoder)
            update(obj, res)
    obj.__stp__ = stp


def loads(jss):
    return json.loads(jss, cls=ObjectDecoder)


## database


dblock = _thread.allocate_lock()


def locked(lock):

    def lockeddec(func, *args, **kwargs):

        def lockedfunc(*args, **kwargs):
            lock.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                lock.release()
            return res

        lockeddec.__wrapped__ = func
        lockeddec.__doc__ = func.__doc__
        return lockedfunc

    return lockeddec


class Class:

    cls = {}

    @staticmethod
    def add(clz) -> None:
        Class.cls["%s.%s" % (clz.__module__, clz.__name__)] =  clz

    @staticmethod
    def all():
        return Class.cls.keys()

    @staticmethod
    def full(name) -> list[str]:
        name = name.lower()
        res = []
        for cln in Class.cls:
            if name in cln.split(".")[-1].lower():
                res.append(cln)
        return res

    @staticmethod
    def get(name) -> type[object]:
        return Class.cls.get(name, None)

    @staticmethod
    def remove(name) -> None:
        del Class.cls[name]


class Selector(Default):

    pass



Class.add(Default)
Class.add(Object)
Class.add(Selector)


class Db():

    @staticmethod
    def all(otp, timed: dict = None) -> list[Object]:
        result = []
        for fnm in Db.fns(Wd.getpath(otp), timed):
            obj = Db.hook(fnm)
            if "__deleted__" in obj and obj.__deleted__:
                continue
            result.append((fnm, obj))
        if not result:
            return []
        return result

    @staticmethod
    def find(otp, selector=None, index=None, timed=None) -> list[Object]:
        if selector is None:
            selector = {}
        _nr = -1
        result = []
        for fnm in Db.fns(Wd.getpath(otp), timed):
            obj = Db.hook(fnm)
            if selector and not search(obj, selector):
                continue
            if "__deleted__" in obj and obj.__deleted__:
                continue
            _nr += 1
            if index is not None and _nr != index:
                continue
            result.append((fnm, obj))
        return result

    @staticmethod
    def last(otp) -> tuple[str, Object]:
        fnm = Db.fns(Wd.getpath(otp))
        if fnm:
            fnn = fnm[-1]
            return (fnn, Db.hook(fnn))
        return (None, None)

    @staticmethod
    def match(otp, selector=None, index=None, timed=None) -> (str, Object):
        res = sorted(
                     Db.find(otp, selector, index, timed), key=lambda x: fntime(x[0]))
        if res:
            return res[-1]
        return (None, None)


    @staticmethod
    @locked(dblock)
    def fns(path, timed=None) -> list[str]:
        if not path:
            return []
        if not os.path.exists(path):
            return []
        res = []
        dpath = ""
        for rootdir, dirs, _files in os.walk(path, topdown=False):
            if dirs:
                dpath = sorted(dirs)[-1]
                if dpath.count("-") == 2:
                    ddd = os.path.join(rootdir, dpath)
                    fls = sorted(os.listdir(ddd))
                    if fls:
                        opath = os.path.join(ddd, fls[-1])
                        if (
                            timed
                            and "from" in timed
                            and timed["from"]
                            and fntime(opath) < timed["from"]
                        ):
                            continue
                        if timed and timed.to and fntime(opath) > timed.to:
                            continue
                        res.append(opath)
        return sorted(res, key=fntime)


    @staticmethod
    @locked(dblock)
    def hook(hfn) -> Object:
        if hfn.count(os.sep) > 2:
            oname = hfn.split(os.sep)[-3:]
        else:
            oname = hfn.split(os.sep)
        cname = oname[0]
        cls = Class.get(cname)
        if cls:
            obj = cls()
        else:
            obj = Object()
        fnm = os.sep.join(oname)
        load(obj, fnm)
        return obj


def find(name, selector=None, index=None, timed=None) -> list[Object]:
    names = Class.full(name)
    db = Db()
    result = []
    for nme in names:
        for fnm, obj in db.find(nme, selector, index, timed):
            result.append((fnm, obj))
    return result


def last(obj) -> None:
    db = Db()
    _path, _obj = db.last(otype(obj))
    if _obj:
        update(obj, _obj)


## utility


def cdir(path) -> None:
    if os.path.exists(path):
        return
    if os.sep in path:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def fntime(daystr) -> float:
    after = 0
    daystr = " ".join(daystr.split(os.sep)[-2:])
    if "." in daystr:
        daystr, after = daystr.rsplit(".")
    tme = time.mktime(time.strptime(daystr, "%Y-%m-%d %H:%M:%S"))
    if after:
        try:
            tme = tme + float(".%s"% after)
        except ValueError:
            pass
    return tme

def spl(txt):
    try:
        res = txt.split(",")
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]
