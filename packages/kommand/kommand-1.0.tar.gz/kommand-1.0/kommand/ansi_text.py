class AnsiText:
    __prefix = "\033["
    __style  = {
        "normal"   : 0,
        "bold"     : 1,
        "italic"   : 2,
        "underline": 3
    }
    __color = {
        "black" : 30,
        "red"   : 31,
        "green" : 32,
        "yellow": 33,
        "blue"  : 34,
        "purple": 35,
        "cyan"  : 36,
        "white" : 37
    }
    __background = {
        "black" : 40,
        "red"   : 41,
        "green" : 42,
        "yellow": 44,
        "blue"  : 44,
        "purple": 45,
        "cyan"  : 46,
        "white" : 47
    }
    __bracket = ["<[", "]>"]

    @staticmethod
    def compile(parse: str):
        parse   = parse.split("|")
        _result = f"{AnsiText.__prefix}"
        _sort   = [AnsiText.__style, AnsiText.__color, AnsiText.__background]

        for k, v in enumerate(parse):
            _result += f"{_sort[k][v]}"
            _result += ";" if(k < len(parse) - 1) else "m"
        return _result

    @staticmethod
    def parse(code: str) -> str:
        _text   = []
        _parsed = 0

        for item in AnsiText.__bracket:
            _text.append(code.index(item))
            _parsed += len(item)

        _codec = code[_text[0] + (len(AnsiText.__bracket[0]) - 1) + 1: _text[1]]
        _parsed += len(_codec)

        return f"{AnsiText.compile(_codec)}{code[_parsed: len(code)]}"
