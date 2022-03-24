import os,sys,json
import ROOT
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import math
from math import sqrt

def get_NumberOfEvent(filename:str) -> int:
    ftemp = ROOT.TFile.Open(filename)
    htemp = ftemp.Get('nEventsGenWeighted')
    return  htemp.GetBinContent(1)

def MakeDir(Root:str,ChildName:str):

    if not os.path.isdir(Root):
        raise ValueError(f'No such Root Directory: {Root}!')
    else:
        DIR = os.path.join(Root,ChildName)
    if os.path.isdir(DIR):
        print(DIR + ' exist')
    else:
        print('Create '+ DIR)
        os.mkdir(DIR)

def Trigger(df:ROOT.RDataFrame,Trigger_condition:str) -> ROOT.RDataFrame.Filter:
    '''
    Trigger_conidtion -> Trigger For Leptons
    return dataframe with triggered condition
    '''
    return df.Filter(Trigger_condition)

def Trig_Cond(flag:str,joint:str) -> str:
    '''
    Return Trig_Condition
    '''
    return joint.join(flag)

def overunder_flowbin(h=None,Hist_dim='1D'):
    if Hist_dim =='1D':
        h.SetBinContent(1,h.GetBinContent(0)+h.GetBinContent(1))
        h.SetBinError(1,sqrt(h.GetBinError(0)*h.GetBinError(0)+h.GetBinError(1)*h.GetBinError(1)))
        h.SetBinContent(h.GetNbinsX(),h.GetBinContent(h.GetNbinsX())+h.GetBinContent(h.GetNbinsX()+1))
        h.SetBinError(h.GetNbinsX(),sqrt(h.GetBinError(h.GetNbinsX())*h.GetBinError(h.GetNbinsX())+h.GetBinError(h.GetNbinsX()+1)*h.GetBinError(h.GetNbinsX()+1)))
    
    elif Hist_dim=='2D':
        binx = h.GetNbinsX()
        biny = h.GetNbinsY()
        for i in range(1 , 1+ binx):
            h.SetBinContent(i , 1 , h.GetBinContent( i , 0 ) + h.GetBinContent( i , 1 ) )
            h.SetBinError(i , 1 , sqrt(h.GetBinError( i , 0 )*h.GetBinError( i , 0 ) + h.GetBinError( i , 1 )*h.GetBinError( i , 1 )))
            h.SetBinContent(i , biny , h.GetBinContent( i , biny ) + h.GetBinContent( i , biny + 1 ) )
            h.SetBinError(i , biny , sqrt(h.GetBinError( i , biny )*h.GetBinError( i , biny ) + h.GetBinError( i ,biny + 1 )*h.GetBinError( i , biny + 1 )))
        for i in range(1 , 1+ biny):
            h.SetBinContent(1 , i , h.GetBinContent( 0 , i ) + h.GetBinContent( 1 , i ) )
            h.SetBinError(1 , i , sqrt(h.GetBinError( 0 , i )*h.GetBinError( 0 , i ) + h.GetBinError( 1 , i )*h.GetBinError( 1 , i )))
            h.SetBinContent( binx , i , h.GetBinContent( binx , i ) + h.GetBinContent( binx + 1 , i ) )
            h.SetBinError(binx , i , sqrt(h.GetBinError( binx , i )*h.GetBinError( binx , i ) + h.GetBinError( binx + 1 , i )*h.GetBinError( binx + 1  , i )))
    
    else:
        raise ValueError(f'Dim: {Hist_dim} is not specified.')
    return h

