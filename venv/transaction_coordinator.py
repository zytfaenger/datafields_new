class ta_mon():
    def __init__(self):
        self.ta_list = []

    def add_ta(self,function):
        self.ta_list.append(function)

    def exec_ta(self):

        if len(self.ta_list)>0:
            self.ta_list(0)
            self.ta_list.pop(0)
