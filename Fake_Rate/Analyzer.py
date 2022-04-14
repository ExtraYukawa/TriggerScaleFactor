import ROOT
import json
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)

from Fake_Rate.FR_Utils import *
from Utils.plot_settings import *

from Utils.General_Tool import *
from Utils.Header import *


def FakeRateAnalyzer(settings:dict):
    
    ROOT.gInterpreter.ProcessLine(Histogram_Definition['Single'].format(settings['path']['l1'],settings['branchname']['l1']))
    

    DF = dict() #DF -> DataFrame Dicitionary

    DF['Lepton'] = dict()  # The 'data' Lepton dataframe
    
    for sample in ['Data','DY','WJets','TTTo1L','TTTo2L']:
        DF['Lepton'][sample] = dict()
        if sample == 'Data':
            DF['Lepton'][sample]['nume'] = MyDataFrame(IsData=True,FilesIn=settings['Data_FilesIn'],nevents=settings['nevents'])
            DF['Lepton'][sample]['deno'] = MyDataFrame(IsData=True,FilesIn=settings['Data_FilesIn'],nevents=settings['nevents'])
        else:
            DF['Lepton'][sample]['nume'] = MyDataFrame(IsData=False,FilesIn=settings['MC_Lepton'][sample]['path'],nevents=settings['nevents'])
            DF['Lepton'][sample]['deno'] = MyDataFrame(IsData=False,FilesIn=settings['MC_Lepton'][sample]['path'],nevents=settings['nevents'])


    DF['background'] = dict()  # Non-prompt background
    
    for sample in settings['MC_QCD'].keys():
        DF['background'][sample] = dict()
        DF['background'][sample]['nume'] = MyDataFrame(IsData=False,FilesIn=settings['MC_QCD'][sample]['path'],nevents=settings['nevents'])
        DF['background'][sample]['deno'] = MyDataFrame(IsData=False,FilesIn=settings['MC_QCD'][sample]['path'],nevents=settings['nevents'])


    
    h2_deno=ROOT.TH2D('','',5,fr_etabin,4,fr_ptbin)
    h2_nume=ROOT.TH2D('','',5,fr_etabin,4,fr_ptbin)
    h2_deno_model=ROOT.RDF.TH2DModel(h2_deno)
    h2_nume_model=ROOT.RDF.TH2DModel(h2_nume)
    
    
    H = dict()
    H['Lepton'] = dict()
    H['background'] = dict()
    
    for sample in DF['Lepton'].keys():
        H['Lepton'][sample] =dict()
        if sample == 'Data':
            trigSF_on = False
            IsData = True
            weight_set = None
        else:
            trigSF_on = settings['trigSF_on']
            IsData = False
            weight_set = settings['weight_set']
        H['Lepton'][sample]['deno'] = FakeRate_Histo(DF['Lepton'][sample]['deno'],Model=h2_deno_model,channel=settings['channel'],Filters=settings['LeptonFilters'],trigSF_on=trigSF_on,IsData=IsData,IsNume=False,weight_set=weight_set)
        H['Lepton'][sample]['nume'] = FakeRate_Histo(DF['Lepton'][sample]['nume'],Model=h2_nume_model,channel=settings['channel'],Filters=settings['LeptonFilters'],trigSF_on=trigSF_on,IsData=IsData,IsNume=True,weight_set=weight_set)
            
    h2_deno=ROOT.TH2D('','',5,fr_etabin,4,fr_ptbin)
    h2_nume=ROOT.TH2D('','',5,fr_etabin,4,fr_ptbin)
    h2_deno_model=ROOT.RDF.TH2DModel(h2_deno)
    h2_nume_model=ROOT.RDF.TH2DModel(h2_nume)
    
    for sample in DF['background'].keys():
        H['background'][sample] =dict()
        H['background'][sample]['deno'] = FakeRate_Histo(DF['background'][sample]['deno'],Model=h2_deno_model,channel=settings['channel'],Filters=settings['QCDFilters'],trigSF_on=settings['trigSF_on'],IsData=False,IsNume=False,weight_set=settings['weight_set'])
        H['background'][sample]['nume'] = FakeRate_Histo(DF['background'][sample]['nume'],Model=h2_nume_model,channel=settings['channel'],Filters=settings['QCDFilters'],trigSF_on=settings['trigSF_on'],IsData=False,IsNume=True,weight_set=settings['weight_set'])

    for sample in  ['Data','DY','WJets','TTTo1L','TTTo2L']:
        for key in ['deno','nume'] :
            H['Lepton'][sample][key].Draw()
            H['Lepton'][sample][key] =  H['Lepton'][sample][key].GetValue()
            if sample != 'Data': ####Scale up Monte Carlo
                H['Lepton'][sample][key].Scale(-1*settings['MC_Lepton'][sample]['xs']/settings['MC_Lepton'][sample]['nevents'])
            H['Lepton'][sample][key] = overunder_flowbin(h = H['Lepton'][sample][key], Hist_dim='2D')
    
    for sample in DF['background'].keys():
        for key in ['deno','nume'] :
            H['background'][sample][key].Draw()
            H['background'][sample][key] =  H['background'][sample][key].GetValue()
            H['background'][sample][key].Scale(settings['MC_QCD'][sample]['xs']/settings['MC_QCD'][sample]['nevents']) 
            H['background'][sample][key] = overunder_flowbin(h = H['background'][sample][key], Hist_dim='2D')
    
    
    Plot(Histogram = H['Lepton'],IsLepton= True, year = settings['year'], channel = settings['channel'],trigSF_on=settings['trigSF_on'])
    #Plot(Histogram = H['background'],IsLepton= False, year = settings['year'], channel = settings['channel'],trigSF_on=settings['trigSF_on'])








