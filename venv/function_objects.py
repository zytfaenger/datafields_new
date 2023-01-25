def multiply(a,b):
    return a*b

print(multiply(3,4))

flist=[]

flist.append(multiply(3,4))

b=flist[0]

def f_factory(function,**args):
    def product(args):
        p=1
        for f in args:
            p=p*args[f]
        return p

    def addition(args):
        a=0
        for s in args:
            a=a+args[s]
        return a



    if function=='sum':
        return addition(args)
    elif function=='product':
        return product(args)

arg= {'0':2,'1':3,'2':5}
a=f_factory('product', **arg )
print(a)