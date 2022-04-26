import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import ROOT
import numpy as np

from ROOT import kFALSE

from array import array
lumi =41480.

ptbin = array('d',[20,40,50,65,80,100,200])
l1ptbin=array('d',[20,40,42,44,46,48,50, 65, 80, 100, 200])
l2ptbin=array('d',[20,25,28,31,33,36,40,50, 65, 80, 100, 200])
etabin=array('d',[-2.5,-2.1,-1.8,-1.5,-1.2,-0.9,-0.6,-0.3,-0.25,-0.2,-0.15,-0.1,-0.05,0,0.05,0.1,0.15,0.2,0.25,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5])
njetbin=array('d',[0,1,2,3,4,5,6,7,8,9,10])
metbin=array('d',[100,110,120,130,140,160,180,200,250])
abs_etabin=array('d',[0,0.1,0.2,0.3,0.5,0.7,0.9,1.5,2.5])

fr_ptbin= array('d',[20, 30, 40, 60, 80])
fr_etabin=array('d',[0, 0.5,1.0,1.5,2.0,2.5])

