from AcademicObjects import Subject, Group
from IncludingObjects import Schedule
from AppUtils import Logger
import time
import os
import asyncio
import requests

loop = asyncio.get_event_loop()

equations = Subject(22956)

time_1 = time.time()
paralel = equations.import_groups()
time_2 = time.time()
print(f'Con paralelismo: {time_2-time_1} segundos')
# sequential = equations.import_groups_b()
# print(len(sequential))
# print(f'Sin paralelismo: {time.time()-time_2} segundos')

f = 5

# a = loop.run_until_complete(asyncio.gather(*[loop.run_in_executor(None, requests.get, 'http://127.0.0.1:8888/') for i in range(10)]))

# print(a)