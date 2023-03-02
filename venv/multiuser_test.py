import anvil.server
import anvil.tables
import time


anvil.server.connect('server_IASVRU2IQUMUDVCWBW3CVJIY-2Q3FDIYJDHS24GFZ')  #modules PDS v2

class ta_stub():
    def __init__(self):
        self.ta_list=[]

    def add_ta(self,fnkt,args):
        t_fs=(fnkt,args)
        self.ta_list.append(t_fs)

    def get_ta(self):
        print(self.ta_list,"=volle Version")
        entry = self.ta_list[0]
        return entry

    def remove_ta(self, pos):
        self.ta_list.pop(0)



ta_process = ta_stub()

def fscount(user_id):
    time.sleep(5)
    return user_id
@anvil.server.callable
def ding_dong(user_id):
    #print(user_id)
    ta_process.add_ta(fscount,user_id)
    a=ta_process.get_ta()
    print("die liste ist:", a)
    b=a[0](a[1])
    print('b ist:',b)
    ta_process.remove_ta(0)
    return "ding_dong: {}".format(b)

#fscount(10)



z=fscount
# ta_process.add_ta(fscount,[15,19])
#print(ta_process.get_ta())
# ta_process.get_ta()[0][0](ta_process.get_ta()[0][1])



anvil.server.wait_forever()
