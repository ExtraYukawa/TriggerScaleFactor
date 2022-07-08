import ROOT,json
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile
from array import array
from ROOT import kFALSE
import numpy as np
import math
from math import sqrt
from multiprocessing import Queue, Manager
from PhysProcessRECO.ScaleFactors import *


class RDataFrameStab(object):
    def __init__(self,settings:dict) -> None:
        '''
        '''
        self.__IsData = settings.get('IsData')
        self.__channel = settings.get('channel')
        self.__year = settings.get('year')
        self.__veto = settings.get('veto')
        self.__MET_Filters =' && '.join(settings.get('MET_Filters'))
        
        self.__region = settings.get('region')
        Nevents =  settings.get('nevents')      

        self.__IsFake = settings.get('IsFake')
        self.__FakeRateOn = settings.get('FakeRateOn')

        
        if self.__channel == 'DoubleElectron':
            channel_phys_region = 3
        elif self.__channel == 'DoubleMuon':
            channel_phys_region = 1
        else:
            channel_phys_region = 2
        self.__phys_region =None
        
        if self.__region =='SignalRegion':
            self.__phys_region = 'ttc'
            
            
            if not self.__IsFake:
                if self.__IsData:
                    if self.__channel == 'DoubleElectron':
                        region_selection = f'ttc_jets&& ttc_region=={channel_phys_region} && (ttc_mll<60 || ttc_mll>120)&&ttc_mll >20&&ttc_2P0F   && ttc_l1_pt>30 && ttc_met>30 && ttc_drll > 0.3 && nHad_tau==0  && {self.__MET_Filters} '
                    elif self.__channel == 'DoubleMuon':
                        region_selection = f"ttc_jets && ttc_region=={channel_phys_region} && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && ttc_2P0F  && {self.__MET_Filters}"
                    else:
                        region_selection = f'ttc_jets&& ttc_region=={channel_phys_region} && ttc_2P0F  && (ttc_l1_pt>30||ttc_l2_pt>30) && ttc_met>30 && ttc_drll > 0.3 && nHad_tau==0  && {self.__MET_Filters} '
                else: 
                    if self.__channel == 'DoubleElectron':
                        #region_selection = 'true'
                        #region_selection = f'ttc_jets &&lhe_nlepton>1&& ttc_region=={channel_phys_region} && ttc_2P0F && (ttc_mll<60 || ttc_mll>120) &&ttc_mll >20  && n_tight_jet < 3 && ttc_l1_pt>30 && ttc_met>30 && ttc_drll > 0.3 && nHad_tau==0  && {self.__MET_Filters} '
                        region_selection = f'ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && {self.__MET_Filters}&& lhe_nlepton>1 && nHad_tau==0 && ttc_2P0F && (ttc_mll<60 || ttc_mll>120)'
                    elif self.__channel == 'DoubleMuon':
                        region_selection = f"ttc_jets && ttc_region== {channel_phys_region} && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && lhe_nlepton>1 && nHad_tau==0 && ttc_2P0F && {self.__MET_Filters} "
                    else:
                        region_selection = f'ttc_jets &&lhe_nlepton>1&& ttc_region=={channel_phys_region} && ttc_2P0F && (ttc_l1_pt>30||ttc_l2_pt>30) && ttc_met>30 && ttc_drll > 0.3 && nHad_tau==0  && {self.__MET_Filters}  && ttc_mll>20'
            else:

                if self.__IsData:
                    if self.__channel == 'DoubleElectron':
                        region_selection = f'ttc_jets&& ttc_region=={channel_phys_region} && (ttc_1P1F || ttc_0P2F) && (ttc_mll<60 || ttc_mll>120)&&ttc_mll >20 && ttc_l1_pt>30 && ttc_met>30 && ttc_drll > 0.3 && nHad_tau==0  && {self.__MET_Filters} '       
                    elif self.__channel == 'DoubleMuon':
                        region_selection = f"ttc_jets && ttc_region=={channel_phys_region} && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && (ttc_1P1F || ttc_0P2F) && {self.__MET_Filters}"
                    else:
                        region_selection = f'ttc_jets&& ttc_region=={channel_phys_region} && (ttc_1P1F || ttc_0P2F) && (ttc_l1_pt>30||ttc_l2_pt>30) && ttc_met>30 && ttc_drll > 0.3 && nHad_tau==0  && {self.__MET_Filters} && ttc_mll>20 '
                else: 
                    if self.__channel == 'DoubleElectron':
                        region_selection = f'ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && {self.__MET_Filters}&& lhe_nlepton>1 && nHad_tau==0 && (ttc_1P1F || ttc_0P2F) && (ttc_mll<60 || ttc_mll>120)'
                    elif self.__channel == 'DoubleMuon':
                        region_selection = f"ttc_jets && ttc_region=={channel_phys_region} && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && lhe_nlepton>1 && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)  && {self.__MET_Filters}"
                    else:
                        region_selection = f'ttc_jets &&lhe_nlepton>1&& ttc_region=={channel_phys_region} && (ttc_1P1F || ttc_0P2F) && (ttc_l1_pt>30||ttc_l2_pt>30) && ttc_met>30 && ttc_drll > 0.3 && nHad_tau==0  && {self.__MET_Filters} '
        elif self.__region =='ChargeFlipRegion':
            self.__phys_region = 'ttc'
            if self.__IsData:
                region_selection = f'ttc_region=={channel_phys_region} && ttc_2P0F && ttc_mll>60 && ttc_mll<120&&MET_T1_pt >50  && n_tight_jet < 3 && ttc_l1_pt>20 && ttc_l2_pt>20 && abs(ttc_l1_eta)<2.5 && abs(ttc_l2_eta)<2.5 && nHad_tau==0  && {self.__MET_Filters} && ttc_drll>0.3'
            else:
                region_selection = f'ttc_region=={channel_phys_region} && ttc_2P0F && ttc_mll>60 && ttc_mll<120&&MET_T1Smear_pt >50  && n_tight_jet < 3 && ttc_l1_pt>20 && ttc_l2_pt>20 && abs(ttc_l1_eta)<2.5 && abs(ttc_l2_eta)<2.5 && nHad_tau==0  && {self.__MET_Filters} '

        elif self.__region =='DrellYan':
            self.__phys_region ='OPS'
            if self.__channel !='ElectronMuon':
                region_selection = f'OPS_region=={channel_phys_region} && OPS_z_mass > 60 && OPS_z_mass<120 && OPS_2P0F &&OPS_l1_pt>30 && OPS_l2_pt>20 && OPS_drll>0.3 && {self.__MET_Filters} && nHad_tau==0'
            else:
                region_selection = f'OPS_region=={channel_phys_region} && OPS_z_mass > 60 && OPS_z_mass<120 && OPS_2P0F &&( OPS_l1_pt>30 ||  OPS_l2_pt>20) && OPS_drll>0.3 && {self.__MET_Filters} && nHad_tau==0 '

        else:
            raise ValueError(f'No such region: {self.__region} yet!')
        
        self.__Hists = Manager().dict()
        File_Paths = settings.get('File_Paths')
        self.__File_Paths = ROOT.std.vector('string')()
        
        self.__File_Paths.push_back(File_Paths)
        
        #self.__Trigger_Condition = settings.get('DiLepton_Triggers')
        
        if self.__IsData and Nevents != -1:
            self.__df = ROOT.RDataFrame('Events',self.__File_Paths).Range(0,Nevents)
        else: 
            self.__df = ROOT.RDataFrame('Events',self.__File_Paths)
        
        self.__df = self.__df.Filter(region_selection) 
    @property
    def year(self)->str:
        return self.__year

    @property
    def DataFrame(self) ->ROOT.RDataFrame.Filter:
        return self.__df
    @property
    def IsData(self) ->bool:
        return self.__IsData
    @property
    def channel(self)->str:
        return self.__channel
    @channel.setter
    def channel(self,channel:str)->str:
        self.__channel = channel
    @DataFrame.setter
    def Tree(self, df:ROOT.RDataFrame):
        self.__df = df
    @property
    def Hists(self) ->dict():
        return self.__Hists
    @Hists.setter
    def Hists(self, Hists:dict):
        self.__Hists =Hists
    @property
    def PhysRegion(self)->str:
        return self.__phys_region 
    @property
    def Region(self)->str:
        return self.__region 
    @property
    def IsFake(self)->bool:
        return self.__IsFake

def Millstone(DF:RDataFrameStab,HistSettings:dict,SF_Config:dict,DiLepton_Triggers_Condition:str,Run_List=[]):

    
    PR = DF.PhysRegion
    if DF.channel != 'ElectronMuon':

        df = DF.DataFrame.Define('l1pt',f'if({PR}_l1_pt > {PR}_l2_pt) return {PR}_l1_pt;else return {PR}_l2_pt')\
                .Define('l2pt',f'if({PR}_l1_pt > {PR}_l2_pt) return {PR}_l2_pt;else return {PR}_l1_pt')\
                .Define('l1eta',f'if({PR}_l1_pt > {PR}_l2_pt) return {PR}_l1_eta;else return {PR}_l2_eta')\
                .Define('l2eta',f'if({PR}_l1_pt > {PR}_l2_pt) return {PR}_l2_eta;else return {PR}_l1_eta')\
                .Define('l1_id',f'if({PR}_l1_pt > {PR}_l2_pt) return {PR}_l1_id;else return {PR}_l2_id')\
                .Define('l2_id',f'if({PR}_l1_pt > {PR}_l2_pt) return {PR}_l2_id;else return {PR}_l1_id')
    else:
        df = DF.DataFrame.Define('l1pt',f'return {PR}_l1_pt')\
                .Define('l2pt',f'{PR}_l2_pt')\
                .Define('l1eta',f'{PR}_l1_eta')\
                .Define('l2eta',f'{PR}_l2_eta')\
                .Define('l1_id',f'return {PR}_l1_id')\
                .Define('l2_id',f'return {PR}_l2_id')

    if DF.IsData:
        DiLepton_slc_run = dict()
        for Name in Run_List.keys():
            DiLepton_slc_run[Name] = ROOT.std.vector('int')()
            for i in Run_List[Name]:
                DiLepton_slc_run[Name].push_back(i)
        df = df.Filter(eval(f"f'{DiLepton_Triggers_Condition}'"))

        df = df.Define('fr_w',f"{FakeRate(activate=SF_Config['FakeRate']['activate'], IsData=True,IsFake=SF_Config['FakeRate']['IsFake'],phys_region=PR,channel=DF.channel)}")

    else:
        df = df.Filter(DiLepton_Triggers_Condition)
        if DF.IsFake:
            df = df.Define('PreFireWeight',f"{PreFireWeight(activate=SF_Config['PreFireWeight']['activate'],year =DF.year)}")\
                    .Define('fr_w',f"{FakeRate(activate=SF_Config['FakeRate']['activate'], IsData=False,IsFake=SF_Config['FakeRate']['IsFake'],phys_region=PR,channel=DF.channel)}")\
                    .Define('genweight','genWeight/abs(genWeight) *  puWeight *PreFireWeight * fr_w')
        else:
            df = df.Define('DiLeptons_TrigSF',f"{TrigSF(activate= SF_Config['TrigSF']['activate'],Type = SF_Config['TrigSF']['Type'])}")\
                    .Define('DiLeptons_IDSF',f"{DiLeptons_IDSF(activate = SF_Config['IDSF']['activate'],channel =DF.channel)}")\
                    .Define('DiLeptons_RECOSF',f"{DiLeptons_RECOSF(activate = SF_Config['RECOSF']['activate'],channel =DF.channel)}")\
                    .Define('PreFireWeight',f"{PreFireWeight(activate=SF_Config['PreFireWeight']['activate'],year =DF.year)}")\
                    .Define('K_region',f"kinematic({SF_Config['kinematic']['activate']},l1pt,l2pt,l1eta,l2eta)")\
                    .Define('ChargeFlipSF',f"{ChargeFlipSF(activate= SF_Config['cf_SF']['activate'],channel=DF.channel,Same_Sign=SF_Config['cf_SF']['Same_Sign'],sigma = SF_Config['cf_SF']['sigma'])}")\
                    .Define('genweight','genWeight/abs(genWeight) * DiLeptons_TrigSF * DiLeptons_IDSF * puWeight*PreFireWeight * DiLeptons_RECOSF * ChargeFlipSF')





    Hists =dict()
    for name in HistSettings[DF.Region].keys():
        setting = HistSettings[DF.Region][name]
        if DF.IsData != None:
            if DF.IsData :
                Hists[name] = df.Histo1D((setting['name'],'',setting['nbins'],setting['lowedge'],setting['highedge']),setting['name'],'fr_w')

            else:
                Hists[name] = df.Histo1D((setting['name'],'',setting['nbins'],setting['lowedge'],setting['highedge']),setting['name'],'genweight')
        else:
            raise ValueError
    DF.Hists = Hists

def test():
    SF_Config = dict()
    SF_Config['TrigSF'] = dict()
    SF_Config['TrigSF']['activate'] = True
    SF_Config['TrigSF']['Type'] = 1

    SF_Config['IDSF'] = dict()
    SF_Config['IDSF']['activate'] = True
    SF_Config['RECOSF'] = dict()
    SF_Config['RECOSF']['activate'] = True
    SF_Config['PreFireWeight'] = dict()
    SF_Config['PreFireWeight']['activate'] = True
    SF_Config['kinematic'] = dict()
    SF_Config['kinematic']['activate'] = 'true'
    SF_Config['cf_SF'] = dict()
    SF_Config['cf_SF']['activate'] = 'true'
    SF_Config['cf_SF']['sigma'] =  0
    SF_Config['cf_SF']['Same_Sign'] = True

    channel = 'DoubleElectron'
    year = '2017'



    print(f"{TrigSF(activate= SF_Config['TrigSF']['activate'],Type = SF_Config['TrigSF']['Type'])}")
    print(f"{DiLeptons_IDSF(activate = SF_Config['IDSF']['activate'] , channel = channel)}")
    channel = 'DoubleMuon'
    print(f"{DiLeptons_RECOSF(activate = SF_Config['RECOSF']['activate'] , channel = channel)}")

    print(f"{PreFireWeight(activate=SF_Config['PreFireWeight']['activate'],year =year)}")
    
    channel = 'DoubleElectron'
    print(f"kinematic({SF_Config['kinematic']['activate']},l1pt,l2pt,l1eta,l2eta)")
    print(f"{ChargeFlipSF(activate= SF_Config['cf_SF']['activate'],channel=channel,Same_Sign=SF_Config['cf_SF']['Same_Sign'],sigma = SF_Config['cf_SF']['sigma'])}")
#test()

























