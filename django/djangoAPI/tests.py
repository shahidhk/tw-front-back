# from django.test import TestCase
import csv
from django.db import transaction
from graphql import GraphQLError
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


class abc():
    def __init__(self, a='a', b='b', c='c'):
        self.a = a
        self.b = b
        self.c = c

    def name(self):
        print('name is abc')

    # def new(self):
    #     print(self.d)


class abcd(abc):
    def __init__(self, a='a', b='b', c='c', d='d'):
        super().__init__(a, b, c)
        self.d = d

    def long_name(self):
        print('name is abcd')


def thing():
    with transaction.atomic():
        raise GraphQLError('there is an error')
