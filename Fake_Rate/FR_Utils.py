import json
import os 
import ROOT
from ROOT import *
class  MyDataFrame(object):
    def __init__(self,**settings)->None:
        self.__IsData = settings.get('IsData',None)
        if self.__IsData == None:
            raise ValueError('You need to Specifiy whether the files is Data or MC by Bool [IsData]')
        
        self.__FilesIn = settings.get('FilesIn',None)
        if self.__FilesIn == None:
            raise ValueError('You need to Specifiy Input Files Path!')

        self.__Files_Containter = ROOT.std.vector('string')()
        if self.__IsData:
            for File in self.__FilesIn:
                self.__Files_Containter.push_back(File)
        else:
            self.__Files_Containter.push_back(self.__FilesIn)
        
        nevents = settings.get('nevents',None)
        if nevents == -1:
            self.__DataFrame = ROOT.RDataFrame('Events',self.__Files_Containter)
        else:
            self.__DataFrame = ROOT.RDataFrame('Events',self.__Files_Containter).Range(0,nevents)


        self.__general_filters = settings.get('General_Filters',None)
        if self.__general_filters != None:
            self.__DataFrame.Filter(self.__general_filters) 
        self.__Histo2D = None
    def Filter(self,condition:str):
        self.__DataFrame = self.__DataFrame.Filter(condition)
    def Define(self,name:str,definition:str):
        self.__DataFrame = self.__DataFrame.Define(name,definition)
    @property
    def DataFrame(self):
        return self.__DataFrame
    
    @property
    def Histo2D(self):
        return self.__Histo2D
    
    def SetHisto2D(self,Model,x:str,y:str,genweight=None):

        if genweight != None:
            self.__Histo2D = self.__DataFrame.Histo2D(Model,x,y,genweight)
        else:
            self.__Histo2D = self.__DataFrame.Histo2D(Model,x,y)



def FakeRate_Histo(df:MyDataFrame,Model:ROOT.RDF.TH2DModel,channel:str,Filters:dict,trigSF_on:bool,IsData:bool,IsNume:bool,weight_set=[])->MyDataFrame.Histo2D:

    df.Define(name="abs_l1eta",definition="abs(l1_eta)")
    df.Filter(Filters['All'])
    if IsData == None:
        raise ValueError("You need to specifiy 'IsData' For [FakeRate_Histo] function")
    elif not IsData:
        df.Define(name="eff_lumi",definition=f'MC_eff_lumi(l1_pt,"{channel}")')
        
        if trigSF_on == None:
            raise ValueError("You need to specifiy 'trigSF_on' For [FakeRate_Histo] function")
        
        elif trigSF_on:
            trigSF = "Trigger_sf(h1,l1_pt,l1_eta)"
        else:
            trigSF = "1."
        
        df.Define(name='triggerSF',definition=trigSF)
        df.Define(name='genweight',definition=f'{weight_set}*eff_lumi*triggerSF*genWeight/abs(genWeight)')
        
        if IsNume == None:
            raise ValueError("You need to specifiy 'IsNume' For [FakeRate_Histo] function")
        
        elif IsNume:

            df.Filter(Filters['numerator'])
        else:
            
            df.Filter(Filters['denominator'])
        
        df.SetHisto2D(Model=Model, x ="abs_l1eta",y = "l1_pt",genweight='genweight' )
    else:
        if IsNume == None:
            raise ValueError("You need to specifiy 'IsNume' For [FakeRate_Histo] function")
        elif IsNume:
            df.Filter(Filters['numerator'])
        else:
            df.Filter(Filters['denominator'])
        df.SetHisto2D(Model=Model, x ="abs_l1eta",y = "l1_pt")
    return df.Histo2D

import ROOT
import numpy as np


from array import array
from  Utils.CMSTDRStyle import setTDRStyle
import Utils.CMSstyle as CMSstyle
from Utils.General_Tool import Hist2D_to_Binx_Equal
def Plot(Histogram:dict, IsLepton:bool,year:str , channel:str,trigSF_on:bool):
    
    with open(f'./data/year{year}/FakeRate/User.json','rb') as f:
        DirOut = json.load(f)['DirOut'][channel]

    
    if IsLepton:
        pre_fix = 'Lepton'
    else:
        pre_fix = 'QCD'
    if trigSF_on:
        pre_fix += '_trigSF'


    Hist_File = ROOT.TFile(os.path.join(DirOut['files'],pre_fix+'_Histo.root'),'RECREATE')

    Hist_File.cd()
    
    Out_Histo= dict()
    
    if IsLepton:
        Out_Histo['nume'] = Histogram['Data']['nume'].Clone()
        Out_Histo['deno'] = Histogram['Data']['deno'].Clone()
    else:
        if channel == 'Electron':
            Out_Histo['nume'] = Histogram['QCDEM15to20']['nume'].Clone()
            Out_Histo['deno'] = Histogram['QCDEM15to20']['deno'].Clone()
        else:
            Out_Histo['nume'] = Histogram['QCD15to20']['nume'].Clone()
            Out_Histo['deno'] = Histogram['QCD15to20']['deno'].Clone()

    for i in Histogram.keys():
        for j in Histogram[i].keys():
            Histogram[i][j].SetName(i+'_'+j)
            Histogram[i][j].Write()
            if i == 'Data' or i == 'QCDEM15to20' or i == 'QCD15to20':
                pass
            else:
                Out_Histo[j].Add(Histogram[i][j])
    
    Out_Histo['nume'].Divide(Out_Histo['deno'])
    Out_Histo['nume'].SetName('FakeRate')
    Out_Histo['nume'].GetXaxis().SetTitle("#||{#eta}")
    Out_Histo['nume'].GetYaxis().SetTitle("cone-P_{T} [GeV]")
    Out_Histo['nume'].GetXaxis().SetTitleSize(0.05)
    Out_Histo['nume'].GetYaxis().SetTitleSize(0.05)
    

    TS = setTDRStyle()
    TS.cd()
    c = ROOT.TCanvas('','',800,600)
    c.cd()
    pad = ROOT.TPad()
    pad.Draw()
    
    Out_Histo['nume'] = Hist2D_to_Binx_Equal(Out_Histo['nume'],True) 

    CMSstyle.SetStyle(gPad=pad,year=year)
    pad.SetRightMargin(0.15)
    c.SetGridx(False);
    c.SetGridy(False);
    c.Update()
    
    
    c.SaveAs(os.path.join(DirOut['plots'],f'{pre_fix}_fakerate_data.pdf'))
    c.SaveAs(os.path.join(DirOut['plots'],f'{pre_fix}_fakerate_data.png'))
    FakeRate_File = ROOT.TFile(os.path.join(DirOut['files'],pre_fix+'_FakeRate.root'),'RECREATE')
    FakeRate_File.cd()
    Out_Histo['nume'].Write()
    FakeRate_File.Close()
    Hist_File.Close()
    return c
    pad.Close()

    











