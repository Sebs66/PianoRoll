def func(*args,**kwargs):
    print('type(*args)',type(args))
    print('*args',args)
    print('type(**kwargs)',type(kwargs))
    print('**kwargs',kwargs)


func('hola','chao',keyword1='keyword1',otro='keyword2')