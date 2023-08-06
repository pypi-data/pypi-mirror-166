import unittest as _
from kommand.ansi_text import AnsiText
from kommand import control


class AppTest(_.TestCase):
    def testParseAnsi(self):
        code = "<[bold|black|white]>Black on White"
        ansi = AnsiText.parse(code).__eq__("\033[1;30;47mBlack on White")

        self.assertTrue(ansi)
        self.assertFalse(not ansi)


if __name__ == "__main__":
    _.main()
