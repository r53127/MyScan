def _odd_iter():
    n= 1
    i=1
    while True:
        n = n + 2
        i=i+1
        yield n


def _not_divisible(n):
    result=lambda x: x % n > 0
    print('返回函数',result)
    return result#返回的是一个内联函数

def primes():
    yield 2
    it = _odd_iter() # 初始序列
    while True:
        n = next(it) # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it) # 构造新序列，过滤函数，为真保留，为假去除

# 打印1000以内的素数:
# for n in primes():
#     if n < 100:
#         print(n)
#     else:
#         break

# m=primes()
# print(m)
# n = next(m)
# while True:
#     print(n)
#     if n>100:
#         break
#     else:
#         n=next(m)



# def count():
#     fs = []
#     for i in range(1, 4):
#         print('i',i)
#         def f():
#             print(i)
#             return i*i
#         fs.append(f)
#         print(id(fs))
#     return fs
#
# f1, f2, f3 = count()
# f1()
# print(id(f1),id(f2),id(f3))


def now(*kv,**kwargs):
    if 'test' in kwargs:
        print('test arg is:',kwargs['test'])
    print('2015-3-25')

def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

# @log
# def now(**kwargs):
#     print('2015-3-25')
# class Chain(object):
#
#     def __init__(self, path=''):
#         self._path = path
#
#     def __getattr__(self, path):
#         return Chain('%s/%s' % (self._path, path))
#
#     def __str__(self):
#         return self._path
#
#     __repr__ = __str__
#
# print(Chain().status.user.timeline.list)

class Chain(object):
    def __init(self, path=''):
        self.path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self.path, path))

    def __call__(self, username):
        return Chain('%s/%s' % (self.path, username))

    def __str__(self):
        return self.path
    __repr__ = __str__

print(Chain().users('Michael').repos)