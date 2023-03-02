
import inspect

class divider():

    def __init__(self):
        self.a=0
        self.b=1

    def division (self, a,b):
        self.a=a
        self.b=b
        try:
            return self.a/self.b
        except ZeroDivisionError:
            c=inspect.getmembers(self)
            print(c.__module__)



a=divider()
a.division(1,0)