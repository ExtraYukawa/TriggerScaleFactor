import ROOT
import json
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile
from Drell_Yan.DY_utils import  Plot, MyDataFrame, Filtering
import Drell_Yan.DY_utils as DY_utils
from Drell_Yan.DY_HistogramSetting import HistSettings
from collections import OrderedDict
from Utils.General_Tool import overunder_flowbin

#import multiprocessing
#from multiprocessing import Queue, Process, Manager, Pool

class DrellYanRDataFrame():
    def __init__(self,settings:dict) -> None:
        
        self.__year  = settings['year']
        self.__channel = settings['channel']
        self.__nevents = settings['nevents'] ## of events for DataFrame to run through

        self.__HLT_Path = settings['HLT_Path']
        self.__Cross_Section = settings['xs']
        self.__lumi = self.__Cross_Section['lumi']
        self.__NumberOfEvents = settings['NumberOfEvents']# # of events for Data
        self.__FilesIn = settings['FilesIn']

        self.__TriggerSF= settings['TriggerSF']
        
        self.__histos = OrderedDict()
        self.__histos['MC'] = OrderedDict()
        self.__histos['Data'] = OrderedDict()

        self.__dfs = OrderedDict()
        self.__dfs['MC'] = OrderedDict()
        self.__dfs['Data'] = OrderedDict()
        self.__trig_SF_on = settings['trig_SF_on'] # trig_SF is applied or not
    
    def Run(self):

        ROOT.gInterpreter.ProcessLine('#include "./include/IDScaleFactor.h"')
        print('./include/IDScaleFactor.h is Loaded.')
        ROOT.gSystem.Load('./myLib/myLib.so')
        print('./myLib/myLib.so is Loaded.')
        print(f"Start to Analyze Drell-Yan Process For Channel: {self.__channel} ...")
        for MC in self.__FilesIn['MC'].keys():
            settings ={
                    'channel': self.__channel,
                    'Data' : False,
                    'Trigger_Condition': self.__HLT_Path['All'],
                    'File_Paths' : self.__FilesIn['MC'][MC],
                    'TriggerSF': self.__TriggerSF,
                    'nevents' : self.__nevents,
                    'trig_SF_on':self.__trig_SF_on
                    }
            self.__dfs['MC'][MC]= MyDataFrame(settings)
        
        
        for dilepton_type in self.__HLT_Path[self.__channel].keys():
            settings = {
                    'channel': self.__channel,
                    'Trigger_Condition' :  self.__HLT_Path[self.__channel][dilepton_type],
                    'weight' : None,
                    'Data': True,
                    'File_Paths' : self.__FilesIn['Data'][dilepton_type],
                    'nevents' : self.__nevents
                    }
            self.__dfs['Data'][dilepton_type]= MyDataFrame(settings)

        for MC in self.__FilesIn['MC'].keys():
            Filtering(self.__dfs['MC'][MC],HistSettings)
        
        for dilepton_type in self.__HLT_Path[self.__channel].keys():
            Filtering(self.__dfs['Data'][ dilepton_type] , HistSettings)


        for histname in HistSettings.keys():
            HistoGrams = OrderedDict()
            HistoGrams['MC'] = OrderedDict()
            Temps = OrderedDict()
            Temps['Data'] = OrderedDict()
            Temps['MC'] = OrderedDict()
            for MC in self.__dfs['MC'].keys():
                h = self.__dfs['MC'][MC].Hists[histname].GetValue()
                h.Scale(self.__Cross_Section[MC]/float(self.__NumberOfEvents[MC]))
                Temps['MC'][MC] = overunder_flowbin(h)
            for idx ,Data in enumerate(self.__dfs['Data'].keys()):
                h= self.__dfs['Data'][Data].Hists[histname].GetValue()
                h = overunder_flowbin(h)
                Temps['Data'][Data] = overunder_flowbin(h)
                if idx == 0:
                    HistoGrams['Data'] = Temps['Data'][Data]
                else:
                    HistoGrams['Data'].Add(Temps['Data'][Data])

            ####
            HistoGrams['MC']['DY'] = Temps['MC']['DYnlo']
            HistoGrams['MC']['WJets'] = Temps['MC']['WJets']
            
            HistoGrams['MC']['VV'] = Temps['MC']['osWW']
            HistoGrams['MC']['VV'] = Temps['MC']['ssWW']
            HistoGrams['MC']['VV'] = Temps['MC']['WWdps']
            HistoGrams['MC']['VV'].Add(Temps['MC']['WZ_ew'])
            HistoGrams['MC']['VV'].Add(Temps['MC']['WZ_qcd'])
            HistoGrams['MC']['VV'].Add(Temps['MC']['ZZ'])
            HistoGrams['MC']['VV'].Add(Temps['MC']['ZG_ew'])
            
            HistoGrams['MC']['VVV'] = Temps['MC']['WWW']
            HistoGrams['MC']['VVV'].Add(Temps['MC']['WWZ'])
            HistoGrams['MC']['VVV'].Add(Temps['MC']['WZZ'])
            HistoGrams['MC']['VVV'].Add(Temps['MC']['ZZZ'])
            
            HistoGrams['MC']['SingleTop'] = Temps['MC']['tsch']
            HistoGrams['MC']['SingleTop'].Add(Temps['MC']['t_tch'])
            HistoGrams['MC']['SingleTop'].Add(Temps['MC']['tbar_tch'])
            HistoGrams['MC']['SingleTop'].Add(Temps['MC']['tW'])
            HistoGrams['MC']['SingleTop'].Add(Temps['MC']['tbarW'])

            HistoGrams['MC']['ttXorXX'] = Temps['MC']['ttWtoLNu']
            HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttWtoQQ'])
            HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttZ'])
            HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttZtoQQ'])
            HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttH'])
            HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttWW'])
            HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttWZ'])
            HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttZZ'])
            HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttWH'])
            HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttZH'])
            HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['tttJ'])
            HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['tttW'])
            HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['tttt'])
       
            HistoGrams['MC']['tzq'] = Temps['MC']['tzq']

            HistoGrams['MC']['TT'] = Temps['MC']['TTTo1L']
            HistoGrams['MC']['TT'].Add(Temps['MC']['TTTo2L'])

            Plot(HistoGrams,x_name=histname ,lumi=self.__lumi,channel=self.__channel,year=self.__year,trig_SF_on=self.__trig_SF_on )
        


