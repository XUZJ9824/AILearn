'''
Created on Mar 25, 2017

@author: e427632
'''

import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget


if __name__ == '__main__':
    flist = os.listdir( 'c:/' )
    print( flist )
    flist_map = list( map( lambda x: os.path.splitext( x )[0] , flist ) )
    print( flist_map )

    #map1
    a = ['1', '2', '3', '4', '5']
    print( list(map(list, a) ) )
    print( list(map(int, a) ) )
    print ( list(map(lambda x:int(x)+2, a) ) )

    #zip
    l1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    t = list(zip(*l1))
    print (t)

    t2 = list(map(lambda x:[x[0]+1, x[1]+2,x[2]+3], zip(*l1)))
    print(t2)
    pass

    #zip & unzip
    r1 = ['r11', 'r12', 'r13']
    r2 = ['r21', 'r22', 'r23']
    r3 = ['r31', 'r32', 'r33']
    matrix = zip(r1,r2,r3)
    row1, row2, row3 = zip(*matrix)

    lmatrix = list(matrix)
    print(lmatrix)


    print(row1)
    print(row2)
    print(row3)


    all={"jack":2001,"beginman":2003,"sony":2005,"pcky":2000}
    for i in all.keys():
        print(i,all[i])

    name = ('jack', 'beginman', 'sony', 'pcky')
    age = (2001, 2003, 2005, 2000)
    for a, n in zip(name, age):
        print(a, n)

    #matrix row col exchange
    m3X4 = [['r11', 'r12', 'r13', 'r14'], ['r21','r22','r23','r24'], ['r31','r32','r33','r34']]
    lm4X3 = list(zip(*m3X4))
    print(lm4X3)
    lm4X3_2 = list(map(list,zip(*m3X4)))
    print(lm4X3_2)

    #QT5
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
