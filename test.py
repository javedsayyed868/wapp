#!/usr/bin/python

'''import os
dirname = os.path.dirname(__file__)
print "dirname : " + dirname'''
import os.path
my_path = os.path.abspath(os.path.dirname(__file__))
print my_path

