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

m=primes()
n = next(m)
while True:
    print(n)
    if n>100:
        break
    else:
        n=next(m)



