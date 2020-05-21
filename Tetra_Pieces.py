# Tetra_Pieces.py

import csv

EMPTY = '0'

class Pieces_Array:
	def __init__(self):
		pass

	def piece_S(self):
		datafile = open('tetris_shapes/shapetemplate_S.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_S = []
		for row in datareader:
			shapetemplate_S.append(row)
		return shapetemplate_S[0:11]
	def piece_Z(self):
		datafile = open('tetris_shapes/shapetemplate_Z.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_Z = []
		for row in datareader:
			shapetemplate_Z.append(row)
		return shapetemplate_Z[0:11]
	def piece_I(self):
		datafile = open('tetris_shapes/shapetemplate_I.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_I = []
		for row in datareader:
			shapetemplate_I.append(row)
		return shapetemplate_I[0:11]
	def piece_O(self):
		datafile = open('tetris_shapes/shapetemplate_O.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_O = []
		for row in datareader:
			shapetemplate_O.append(row)
		return shapetemplate_O[0:6]
	def piece_J(self):
		datafile = open('tetris_shapes/shapetemplate_J.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_J = []
		for row in datareader:
			shapetemplate_J.append(row)
		return shapetemplate_J[0:21]
	def piece_L(self):
		datafile = open('tetris_shapes/shapetemplate_L.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_L = []
		for row in datareader:
			shapetemplate_L.append(row)
		return shapetemplate_L[0:21]
	def piece_T(self):
		datafile = open('tetris_shapes/shapetemplate_T.csv', 'r')
		datareader = csv.reader(datafile, delimiter=',')
		shapetemplate_T = []
		for row in datareader:
			shapetemplate_T.append(row)
		return shapetemplate_T[0:21]

