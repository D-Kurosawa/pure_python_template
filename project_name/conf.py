"""Load application configure file"""
import json
import sys
from pathlib import Path

from .mypkg import mputil


class ConfigLoader:
    """
    :type setting: Setting
    :type loads: Loads
    :type saves: Saves
    """

    def __init__(self):
        conf = JsonCmdLineArg.load()
        self.setting = Setting(conf["set"])
        self.loads = Loads(conf["load"])
        self.saves = Saves(conf["save"])

    def load(self):
        pass

    def walk(self):
        for key, val in self._walk_generator(self.__dict__):
            print(f"{key:<40}: {val}")

    def _walk_generator(self, dic):
        """
        :type dic: dict
        """
        for key, val in dic.items():
            yield key, val
            try:
                nest_value = val.__dict__  # type: dict
            except AttributeError:
                pass
            else:
                for child_key, child_val in self._walk_generator(nest_value):
                    yield key + " -> " + child_key, child_val


class Setting:
    """
    :type cpu: int
    """

    def __init__(self, dic):
        self.cpu = mputil.MpCPU(dic["cpu"]).get()


class Loads:
    """
    :type foo: Loads.Foo
    :type bar: Loads.Bar
    """

    def __init__(self, dic):
        self.foo = Loads.Foo(dic["foo"])
        self.bar = Loads.Bar(dic["bar"])

    class Foo:
        """
        :type foo_a: Path
        :type foo_b: list[Path]
        """

        def __init__(self, dic):
            self.foo_a = FileMaker.load(dic["foo_A"])
            self.foo_b = FileMaker.find(dic["foo_B"])

    class Bar:
        """
        :type bar_a: Path
        :type bar_b: list[Path]
        """

        def __init__(self, dic):
            self.bar_a = FileMaker.load(dic["bar_A"])
            self.bar_b = FileMaker.find(dic["bar_B"])


class Saves:
    """
    :type foo: Saves.Foo
    :type bar: Saves.Bar

    def __init__(self, dic):
        self.foo = Saves.Foo(dic["foo"])
        self.bar = Saves.Bar(dic["bar"])

    class Foo:
        """
        :type foo_a: Path
        :type foo_b: Path
        """

        def __init__(self, dic):
            self.foo_a = FileMaker.save(dic["foo_A"])
            self.foo_b = FileMaker.base(dic["foo_B"])

    class Bar:
        """
        :type bar_a: Path
        :type bar_b: Path
        """

        def __init__(self, dic):
            self.bar_a = FileMaker.save(dic["bar_A"])
            self.bar_b = FileMaker.base(dic["bar_B"])


class JsonCmdLineArg:
    @staticmethod
    def _get_cmd_line_arg():
        """
        :rtype: str
        """
        try:
            arg = sys.argv[1]
        except IndexError:
            raise IndexError("Not found command line arguments")
        except Exception:
            raise Exception
        return arg

    @classmethod
    def load(cls):
        """
        :rtype: dict
        """
        with open(cls._get_cmd_line_arg(), "r", encoding="utf-8") as j:
            return json.load(j)


class FileMaker:
    @staticmethod
    def _has_key(dic, *args):
        """
        :type dic: dict
        """
        for arg in args:
            if arg not in dic:
                raise KeyError(f"Not in key : {arg}")

    @staticmethod
    def _exists_path(path):
        """
        :type path: str
        :rtype: Path
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(path)

        return p

    @classmethod
    def load(cls, dic):
        """
        :type dic: dict
        :rtype: Path
        """
        cls._has_key(dic, "path", "file")

        p = cls._exists_path(dic["path"])
        file = p / dic["file"]

        if not file.exists():
            raise FileNotFoundError(dic["file"])

        return file

    @classmethod
    def find(cls, dic):
        """
        :type dic: dict
        :rtype: list[Path]
        """
        cls._has_key(dic, "path", "pattern")

        p = cls._exists_path(dic["path"])
        files = [f for f in p.glob(f"**/{dic['pattern']}")]

        if not files:
            raise FileNotFoundError(files)

        return files

    @classmethod
    def save(cls, dic):
        """
        :type dic: dict
        :rtype: Path
        """
        cls._has_key(dic, "path", "file")

        p = cls._exists_path(dic["path"])
        return p / dic["file"]

    @classmethod
    def base(cls, dic):
        """
        :type dic: dict
        :rtype: Path
        """
        cls._has_key(dic, "path", "base_name")

        p = cls._exists_path(dic["path"])
        return p / dic["base_name"]


if __name__ == "__main__":

    def _main():
        conf = ConfigLoader()
        conf.load()
        conf.walk()

    _main()
