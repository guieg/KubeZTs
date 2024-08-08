class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Report(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.report = ""

    def append_to_report(self, text):
        self.report += ("\n" + text)

    def print_report(self):
        print(self.report)

    def get_report(self):
        return self.report
