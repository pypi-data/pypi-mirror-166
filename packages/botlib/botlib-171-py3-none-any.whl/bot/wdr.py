# This file is placed in the Public Domain.


"workdir"


import os


def __dir__():
    return (
            'Wd',
            'getpath'
           )


class Wd:

    "working directory."

    workdir = ""

    @staticmethod
    def get() -> None:
        "return working directory."
        return Wd.workdir

    @staticmethod
    def set(val: str) -> None:
        "set working directory."
        Wd.workdir = val


def getpath(path: str) -> str:
    "return a store's path."
    return os.path.join(Wd.workdir, "store", path)
