# from django.test import TestCase
import csv

# Create your tests here.


def print_tree(level, parent_str, things):
    if parent_str in things.keys():
        print(('--' * level) + parent_str + ' *')
        for child in things[parent_str]:
            print_tree(level+1, child[0], things)
    else:
        print(('--' * level) + parent_str)


parent = {}
with open('avantis.csv', mode='r') as csv_f:
    csv_r = csv.reader(csv_f, delimiter=',')
    for row in csv_r:
        if row[3] in parent.keys():
            parent[row[3]].append(row)
        else:
            parent[row[3]] = [row]
print_tree(0, 'SITE', parent)
