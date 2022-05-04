import os,sys,json
import ROOT
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import math
from math import sqrt

def get_NumberOfEvent(filename:str) -> float:
    ftemp = ROOT.TFile.Open(filename)
    htemp = ftemp.Get('nEventsGenWeighted')
    return  htemp.GetBinContent(1)
def getNumberofEventsInDataSet(DataSet:list,FilterSet:list):

    for filename in DataSet:
        ftemp = ROOT.TFile.Open(filename)
        Events = ftemp.Get('Events')
        print(Events.GetEntries())



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





def Hist2D_to_Binx_Equal(h_original:ROOT.TH2D,IsFakeRate=False,axis='Default')->ROOT.TH2D:


    nx = h_original.GetXaxis().GetNbins()
    ny = h_original.GetYaxis().GetNbins()
    xmax = h_original.GetXaxis().GetXmax()
    ymax = h_original.GetYaxis().GetXmax()
    xmin = h_original.GetXaxis().GetXmin()
    ymin = h_original.GetYaxis().GetXmin()
    xtitle = h_original.GetXaxis().GetTitle()
    ytitle = h_original.GetYaxis().GetTitle()
    
    h_new = ROOT.TH2D("new_h","",nx,xmin,xmax,ny,ymin,ymax)

    h_new.GetXaxis().SetTitle(xtitle)
    h_new.GetYaxis().SetTitle(ytitle)
    
    
    for i in range(1,nx+1):
        for j in range(1,ny+1):
            BinContent= h_original.GetBinContent(i,j)
            BinError = h_original.GetBinError(i,j)
            h_new.SetBinContent(i,j,BinContent)
            h_new.SetBinError(i,j,BinError)
    h_new.GetXaxis().SetLabelOffset(999)
    h_new.GetYaxis().SetLabelOffset(999)

#    h_new.Draw('COLZ TEXT E')


    label = ROOT.TText()
    label.SetTextFont(42)
    label.SetTextSize(0.04)
    label.SetTextAlign(22)
    ylabel = h_new.GetYaxis().GetBinLowEdge(1) - 0.15*h_new.GetYaxis().GetBinWidth(1)
    xlabel = h_new.GetXaxis().GetBinLowEdge(1) - 0.25*h_new.GetXaxis().GetBinWidth(1)
    h_new.SetEntries(h_original.GetEntries())

    h_new.Draw('COLZ TEXT E')
    if not IsFakeRate:
        for i in range(nx+1):
            xlow = h_original.GetXaxis().GetBinUpEdge(i)
            xnew = h_new.GetXaxis().GetBinLowEdge(i+1)
            if axis =='Default' or axis == 'ptpt' or axis =='pteta':
                label.DrawText(xnew,ylabel,f"{int(xlow)}")
            else:
                label.DrawText(xnew,ylabel,f"{xlow:.1f}")
        for i in range(ny+1):
            ylow = h_original.GetYaxis().GetBinUpEdge(i)
            ynew = h_new.GetYaxis().GetBinLowEdge(i+1)
            if axis =='Default' or axis =='etaeta' or axis == 'pteta':
                label.DrawText(xlabel,ynew,f"{ylow:.1f}")
            else:
                label.DrawText(xlabel,ynew,f"{int(ylow)}")
    else:
        for i in range(nx+1):
            xlow = h_original.GetXaxis().GetBinUpEdge(i)
            xnew = h_new.GetXaxis().GetBinLowEdge(i+1)
            label.DrawText(xnew,ylabel,f"{xlow:.1f}")
        for i in range(ny+1):
            ylow = h_original.GetYaxis().GetBinUpEdge(i)
            ynew = h_new.GetYaxis().GetBinLowEdge(i+1)
            label.DrawText(xlabel,ynew,f"{int(ylow)}")
    #mypalette.colorPalette()
    return h_new


def OpenAndWrite(path:str,Key:str,Value:float):

    if not os.path.isfile(path):
        Content = dict()
    else:
        with open(path,'r') as f:
            Content = json.load(f)

    Content[Key] = Value

    with open(path,'w') as f:
        json.dump(Content,f,indent=4)


















