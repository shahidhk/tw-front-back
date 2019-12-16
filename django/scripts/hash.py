import csv

with open('avantis.csv', mode='r') as read_file, open('hashed_entities.csv', mode='w') as write_file:
# first read the assets into a dictionary
	reader = list(csv.reader(read_file, delimiter=','))
	line = 1
	asset_dict = {}
	for row in reader:
		asset_dict[row[0]] = f'ENT-NUM-{line}'
		line += 1
# now write the hashed file for real
	writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	line = 1
	for row in reader:
		writer.writerow([f'ENT-NUM-{line}', f'Entity Number {line} Name', 'S01', asset_dict.get(row[3], ''), 'Equipment', 'Some Other Field', row[6], f'Entity #{line} Location', row[8]])
		line += 1