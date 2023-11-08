ls = [10, 5, 7, 8, 9, 60, 10, 300, 40, 40, 40, 70, 70, 100, 100]

lss = ls[0:5]

print(lss)

increment = 5
start_index = len(lss); end_index = start_index + increment
print(start_index, end_index)

lss = ls[start_index:end_index]

print(lss)