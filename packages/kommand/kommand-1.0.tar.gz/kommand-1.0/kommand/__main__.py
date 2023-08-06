from kommand import control


if __name__ == '__main__':
    control(
        name="Testing",
        version="0.1-test",
        author="kzulfazriawan",
        email="kzulfazriawan@gmail.com",
        build={
            "exec": "kommand.build",
            "help": "Generate command file json"
        }
    )
