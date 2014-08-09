#!/usr/bin/python
import sys, os;
#Setting up environment
basedir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)));
path = os.path.normpath(os.path.join(basedir,'../../..'))
sys.path.append(os.path.abspath(path))

DEBUG_MODE = True;

