#!/usr/bin/python
import sys

c=int(sys.argv[2])
r=int(sys.argv[1])
print r,c
m1 = [[0 for x in range(c)] for y in range(r)]
print m1

print "Enter Values for Array 1"
for x in range(r):
	for y in range(c):
		m1[x][y]=int(raw_input("Enter Value column %d for line %d"%(x,y)))

print m1
m2 = [[0 for x in range(c)] for y in range(r)]

for i in range(r):
	for j in range(c):
		print i,j,m1[i][j]
		value=0
		if i==0:
			init_row=i
		else:
			init_row=i-1
		if i==r-1:
			max_row=i
		else:
			max_row=i+1

		while init_row <= max_row:
			if j==0:
				init_col=j
			else:
				init_col=j-1
			if j==c-1:
				max_col=j
			else:
				max_col=j+1
			print "i is %d, j is %d, init_row is %d, max_row is %d, init_col is %d, max_col is %d"%(i,j,init_row,max_row,init_col,max_col)
			while init_col <= max_col:
				print "adding m[%d][%d] which is %d to %d"%(init_row,init_col,m1[init_row][init_col],value)
				value=value+m1[init_row][init_col]
				init_col=init_col+1
			init_row=init_row+1
		print "total value for postion [%d][%d] is %d"%(i,j,value)
		m2[i][j]=value

print m1
print m2