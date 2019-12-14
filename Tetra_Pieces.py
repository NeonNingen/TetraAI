# Tetra_Pieces.py

import csv

EMPTY = '0'

def csv_1(num):
	if num == 1:
		datafile = open('tetris_shapes/shapetemplate_S.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_S = []
		for row in datareader:
			shapetemplate_S.append(row)
		return shapetemplate_S[0:11]
	elif num == 2:
		datafile = open('tetris_shapes/shapetemplate_Z.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_Z = []
		for row in datareader:
			shapetemplate_Z.append(row)
		return shapetemplate_Z[0:11]
	elif num == 3:
		datafile = open('tetris_shapes/shapetemplate_I.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_I = []
		for row in datareader:
			shapetemplate_I.append(row)
		return shapetemplate_I[0:11]
	elif num == 4:
		datafile = open('tetris_shapes/shapetemplate_O.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_O = []
		for row in datareader:
			shapetemplate_O.append(row)
		return shapetemplate_O[0:6]
	elif num == 5:
		datafile = open('tetris_shapes/shapetemplate_J.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_J = []
		for row in datareader:
			shapetemplate_J.append(row)
		return shapetemplate_J[0:21]
	elif num == 6:
		datafile = open('tetris_shapes/shapetemplate_L.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_L = []
		for row in datareader:
			shapetemplate_L.append(row)
		return shapetemplate_L[0:21]
	elif num == 7:
		datafile = open('tetris_shapes/shapetemplate_T.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_T = []
		for row in datareader:
			shapetemplate_T.append(row)
		return shapetemplate_T[0:21]


class Pieces:
	def __init__(self):
		pass

	def piece_S(self):
		num = 1
		return csv_1(num)
	def piece_Z(self):
		num = 2
		return csv_1(num)
	def piece_I(self):
		num = 3
		return csv_1(num)
	def piece_O(self):
		num = 4
		return csv_1(num)
	def piece_J(self):
		num = 5
		return csv_1(num)
	def piece_L(self):
		num = 6
		return csv_1(num)
	def piece_T(self):
		num = 7
		return csv_1(num)
