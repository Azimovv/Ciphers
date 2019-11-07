import time

start_time = time.time()
for trial in range(10000):
    building = ''
    for i in range(10000):
        building += 'x'
print(f"String concatenation: {time.time() - start_time}")

start_time = time.time()
for trial in range(10000):
    building = []
    for i in range(10000):
        building.append('x')
    building = ''.join(building)
print(f"List appending: {time.time() - start_time}")