# This file is placed in the Public Domain.
# pylint: disable=C0112,C0103,C0114,C0115,C0116


"object programming (working directory)"


import os


class Wd:

    workdir = ""

    @staticmethod
    def get() -> str:
        assert Wd.workdir
        return Wd.workdir

    @staticmethod
    def getpath(path) -> str:
        assert Wd.workdir
        return os.path.join(Wd.workdir, "store", path)

    @staticmethod
    def set(val) -> None:
        Wd.workdir = val

    @staticmethod
    def types() -> list[str]:
        res = []
        path = os.path.join(Wd.workdir, "store")
        for fnm in os.listdir(path):
            res.append(fnm)
        return res
