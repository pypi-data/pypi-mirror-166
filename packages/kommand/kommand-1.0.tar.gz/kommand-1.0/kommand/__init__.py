import importlib
import json
import os
import sys

from kommand.ansi_text import AnsiText

VERSION = '1.0'
NAME = 'Kommand'
DESCRIPTION = 'Command everything with kommand'
AUTHOR = 'kzulfazriawan'
EMAIL = 'kzulfazriawan@gmail.com'


def build():
    _input = {
        "name": input(AnsiText.parse("<[normal|green]>Name:")),
        "version": input(AnsiText.parse("<[normal|green]>Version:")),
        "author": input(AnsiText.parse("<[normal|green]>Author:")),
        "email": input(AnsiText.parse("<[normal|green]>Email:")),
    }
    _data = {}

    name = f"{_input['name'].lower().replace(' ', '-')}.json"
    with open(os.path.join(os.getcwd(), name), "w") as _fl:
        for k, v in _input.items():
            _data[k] = v.strip()
        _data["your_command"] = {
            "exec": "mypackage.mymodule.myfunc",
            "help": "my help description"
        }
        json.dump(_data, _fl, indent=4)
        _fl.close()
        sys.stdout.write(AnsiText.parse(f"<[bold|black|green]>All done! file {name} created success!"))


def control(**kwargs):
    _argv = sys.argv
    _result = {"intro": None, "body": None, "command": None}
    _data = {
        "name": NAME,
        "version": VERSION,
        "author": AUTHOR,
        "email": EMAIL
    }

    try:
        if "json_file" in kwargs:
            _rootPath = os.path.dirname(sys.modules["__main__"].__file__)
            with open(os.path.join(_rootPath, kwargs["json_file"])) as fl:
                _json = json.load(fl)
                for k, v in _json.items():
                    _data[k] = v
                fl.close()
        else:
            for k, v in kwargs.items():
                _data[k] = v

    except Exception as e:
        raise e.with_traceback(e.__traceback__)

    else:
        _name = AnsiText.parse(f"<[bold|black|green]>{_data['name']}")
        _onVer = AnsiText.parse("<[normal|black|green]>on version:")
        _version = AnsiText.parse(f"<[bold|black|green]>{_data['version']}")
        _intro = " ".join([_name, _onVer, _version])

        if all(k in _data for k in ("author", "email")):
            _author = AnsiText.parse(f"<[normal|green]>{_data['author']}")
            _sepr = AnsiText.parse("<[normal|white]>|")
            _email = AnsiText.parse(f"<[normal|green]>{_data['email']}")
            _body = " ".join([_author, _sepr, _email])
            _line = "<" + ("=" * (len(_body) - 3)) + ">"
            _body = "\n".join([_body, AnsiText.parse(f"<[normal|white]>{_line}")])
        else:
            _body = ""

        _help = "\n---\n"
        _comm = _data
        for i in ("name", "version", "author", "email"):
            if i in _comm:
                del _comm[i]

        for k, v in _comm.items():
            _help += AnsiText.parse(f"<[bold|white]>{k}")
            _help += AnsiText.parse(f"<[normal|white]> {v['help']}")

        _result = [_intro, _body]

        if isinstance(_argv, list):
            del _argv[0]
            _result.append(f"Options:{_help}")

            try:
                if _argv[0] == 'help':
                    for item in _result:
                        sys.stdout.write(f"{item}\n")
                else:
                    for z in _argv:
                        _paramSplit = z.split("=")
                        _paramValue = None
                        _commandX = _paramSplit[0]
                        _result.pop()
                        _result.append(" ".join([
                            AnsiText.parse("<[normal|red]>Running command:"),
                            AnsiText.parse(f"<[bold|red]>{_commandX}")
                        ]))

                        if len(_paramSplit) > 1:
                            _paramValue = _paramSplit[1].strip('"').strip("'")

                        if _commandX in _comm:
                            _execute = _comm[_commandX]["exec"]

                            if "." in _execute:
                                _module = _execute.split(".")
                                _execute = getattr(importlib.import_module(".".join(_module[:-1])), _module[-1])
                            else:
                                raise ImportError(f"Module import Error -> {_execute}")

                            if callable(_execute):
                                try:
                                    for item in _result:
                                        sys.stdout.write(f"{item}\n")

                                    if _paramValue is not None:
                                        _execute(*_paramValue.split(","))

                                    else:
                                        _execute()
                                except KeyboardInterrupt:
                                    pass

                                except EOFError:
                                    pass
            except IndexError:
                for item in _result:
                    sys.stdout.write(f"{item}\n")
