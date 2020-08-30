import asyncio
import time

async def foo(n):
    a = await asyncio.sleep(n)
    print(n)
    return n

async def bar():

    tasks = []
    for n in range(0, 3):
        tasks.append(asyncio.create_task(foo(n)))
        # tasks.append(foo(n))
    
    results = []

    for task in tasks:
        results.append(await task)
    
    return results

time_1 = time.time()
a = asyncio.run(bar(), debug=True)
print(a)
print(f'Han pasado {time.time()-time_1} segundos')

async def nested():
    return 10

async def main():
    # Nothing happens if we just call "nested()".
    # A coroutine object is created but not awaited,
    # so it *won't run at all*.

    # Let's do it differently now and await it:
    print(await nested())  # will print "42".

# asyncio.run(main(), debug=True)