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


class DF_NEventCalc(object):
    def __init__(self,settings:dict,SF_Config:dict)->None:
        self.__IsData = settings.get('IsData')
        self.__channel = settings.get('channel')
        self.__year = settings.get('year')
        self.__veto = settings.get('veto')
        self.__region = settings.get('region')
        self.__scale = settings.get('scale')        
        Nevents =  settings.get('nevents')      
        if self.__channel == 'DoubleElectron':
            channel_phys_region = 3
        elif self.__channel == 'DoubleMuon':
            channel_phys_region = 1
        else:
            channel_phys_region = 2
        self.__phys_region =None

        if self.__region == 'SignalRegion' or self.__region == 'ChargeFlipRegion':
            self.__phys_region = 'ttc'
            self.__bkg_region ='OPS'
        elif self.__region == 'DrellYan':
            self.__phys_region =='OPS'
            self.__bkg_region ='ttc'
        else:
            raise ValueError('No such region:{self.__region}')
        File_Paths = settings.get('File_Paths')
        self.__File_Paths = ROOT.std.vector('string')()
        self.__File_Paths.push_back(File_Paths)
        
        self.__df = ROOT.RDataFrame('Events',self.__File_Paths)
    
        PR = self.__phys_region 
        if self.__channel == 'DoubleElectron':
            self.__region = 3
        elif self.__channel =='DoubleMuon':
            self.__region =1
        else:
            self.__region =2
        
        
        self.__df = self.__df.Filter(f'ttc_region=={self.__region} or OPS_region == {self.__region}')\
                .Define('Flag',f'{self.__phys_region}_region=={self.__region}')
        

        self.__df = self.__df\
                .Define('l1pt_tmp',f'if(Flag) return {self.__phys_region}_l1_pt;else return {self.__bkg_region}_l1_pt')\
                .Define('l2pt_tmp',f'if(Flag) return {self.__phys_region}_l2_pt;else return {self.__bkg_region}_l2_pt')\
                .Define('l1eta_tmp',f'if(Flag) return {self.__phys_region}_l1_eta;else return {self.__bkg_region}_l1_eta')\
                .Define('l2eta_tmp',f'if(Flag) return {self.__phys_region}_l2_eta;else return {self.__bkg_region}_l2_eta')\
                .Define('l1id_tmp',f'if(Flag) return {self.__phys_region}_l1_id;else return {self.__bkg_region}_l1_id')\
                .Define('l2id_tmp',f'if(Flag) return {self.__phys_region}_l2_id;else return {self.__bkg_region}_l2_id')\

        

        if self.__channel != 'ElectronMuon':
            
            self.__df = self.__df\
                    .Define('l1pt','if(l1pt_tmp > l2pt_tmp) return l1pt_tmp;else return l2pt_tmp;')\
                    .Define('l2pt','if(l1pt_tmp > l2pt_tmp) return l2pt_tmp;else return l1pt_tmp;')\
                    .Define('l1eta','if(l1pt_tmp > l2pt_tmp) return l1eta_tmp;else return l2eta_tmp;')\
                    .Define('l2eta','if(l1pt_tmp > l2pt_tmp) return l2eta_tmp;else return l1eta_tmp;')\
                    .Define('l1_id','if(l1pt_tmp > l2pt_tmp) return l1id_tmp;else return l2id_tmp;')\
                    .Define('l2_id','if(l1pt_tmp > l2pt_tmp) return l2id_tmp;else return l1id_tmp;')
        else:
            self.__df = self.__df.Define('l1pt','l1pt_tmp')\
                    .Define('l2pt','l1pt_tmp')\
                    .Define('l1eta','l1eta_tmp')\
                    .Define('l2eta','l2eta_tmp')\
                    .Define('l1_id','l1id_tmp')\
                    .Define('l2_id','l2id_tmp')        
            

        
        if self.__IsData:
            if SF_Config['FakeRate']['IsFake']:
                self.__df = self.__df.Filter('ttc_1P1F || ttc_0P2F || OPS_1P1F || OPS_0P2F')
            else :
                self.__df = self.__df.Filter('ttc_2P0F || OPS_2P0F')
            self.__df = self.__df.Define('fr_w',f"if (Flag) return {FakeRate(activate=SF_Config['FakeRate']['activate'], IsData=True,IsFake=SF_Config['FakeRate']['IsFake'],phys_region=PR,channel=self.__channel)};else return {FakeRate(activate=SF_Config['FakeRate']['activate'], IsData=True,IsFake=SF_Config['FakeRate']['IsFake'],phys_region=self.__bkg_region,channel=self.__channel)}")
        else:
            if SF_Config['FakeRate']['IsFake']:
                self.__df = self.__df.Filter('ttc_1P1F || ttc_0P2F || OPS_1P1F || OPS_0P2F')
                self.__df = self.__df.Define('PreFireWeight',f"{PreFireWeight(activate=SF_Config['PreFireWeight']['activate'],year =self.__year)}")\
                        .Define('fr_w',f"if (Flag) return {FakeRate(activate=SF_Config['FakeRate']['activate'], IsData=False,IsFake=SF_Config['FakeRate']['IsFake'],phys_region=PR,channel=self.__channel)};else return {FakeRate(activate=SF_Config['FakeRate']['activate'], IsData=False,IsFake=SF_Config['FakeRate']['IsFake'],phys_region=self.__bkg_region,channel=self.__channel)}")\
                        .Define('genweight','genWeight/abs(genWeight) * puWeight *PreFireWeight *fr_w')
            else:
                self.__df = self.__df.Filter('ttc_2P0F || OPS_2P0F')
                self.__df = self.__df.Define('DiLeptons_TrigSF',f"{TrigSF(activate= SF_Config['TrigSF']['activate'],Type = SF_Config['TrigSF']['Type'],IsFake=SF_Config['FakeRate']['IsFake'])}")\
                        .Define('DiLeptons_IDSF',f"{DiLeptons_IDSF(activate = SF_Config['IDSF']['activate'],channel =self.__channel,IsFake=SF_Config['FakeRate']['IsFake'])}")\
                        .Define('DiLeptons_RECOSF',f"{DiLeptons_RECOSF(activate = SF_Config['RECOSF']['activate'],channel = self.__channel,IsFake=SF_Config['FakeRate']['IsFake'])}")\
                        .Define('PreFireWeight',f"{PreFireWeight(activate=SF_Config['PreFireWeight']['activate'],year =self.__year)}")\
                        .Define('K_region',f"kinematic({SF_Config['kinematic']['activate']},l1pt,l2pt,l1eta,l2eta)")\
                        .Define('ChargeFlipSF',f"if (Flag ) return {ChargeFlipSF(activate= SF_Config['cf_SF']['activate'],channel=self.__channel,Same_Sign=SF_Config['cf_SF']['Same_Sign'],sigma = SF_Config['cf_SF']['sigma'],IsFake=SF_Config['FakeRate']['IsFake'])};else return {ChargeFlipSF(activate= SF_Config['cf_SF']['activate'],channel=self.__channel,Same_Sign=False,sigma = SF_Config['cf_SF']['sigma'],IsFake=SF_Config['FakeRate']['IsFake'])}")\
                        .Define('genweight','genWeight/abs(genWeight) * DiLeptons_TrigSF * DiLeptons_IDSF * puWeight*PreFireWeight * DiLeptons_RECOSF * ChargeFlipSF')

        if self.__IsData:
            if SF_Config['FakeRate']['IsFake']:
                self.__NEvents = self.__df.Sum('fr_w').GetValue()
            else:
                self.__NEvents = self.__df.Count().GetValue()
        else:
            self.__NEvents = self.__df.Sum('genweight').GetValue()*self.__scale

        self.__IsFake = SF_Config['FakeRate']['IsFake']
    def Filter(self,Selection:str)->None:
        self.__df = self.__df.Filter(Selection)
        if self.__IsData:
            if self.__IsFake:
                self.__NEvents = self.__df.Sum('fr_w').GetValue()
            else:
                self.__NEvents = self.__df.Count().GetValue()
        else:
            self.__NEvents =self.__df.Sum('genweight').GetValue()*self.__scale

    @property
    def NEvents(self):
        return self.__NEvents

    @property
    def channel(self):
        return self.__channel
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
    @DataFrame.setter
    def Tree(self, df:ROOT.RDataFrame):
        self.__df = df
    @property
    def Hists(self) ->dict():
        return self.__Hists
    @property
    def PhysRegion(self)->str:
        return self.__phys_region 
    @property
    def Region(self)->str:
        return self.__region 
    @property
    def IsFake(self)->bool:
        return self.__IsFake




