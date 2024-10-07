animals = [{'hunts': 'yes', 'name': 'cat'}, 
           {'hunts': 'yes', 'name': 'cat'}, 
           {'hunts': 'maybe', 'name': 'rabbit'}, 
           {'hunts': 'no', 'name': 'horse'},
           {'hunts': 'no', 'name': 'cow'}
           ]

# Find the index where 'hunts' is 'no'
index = next((i for i, animal in enumerate(animals) if animal['hunts'] == 'no' and animal['name'] == 'cow'), None)

print(index)
