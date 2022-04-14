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
from Utils.Header import Histogram_Definition

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
        self.__Process = settings['Process']  # Sorts of Process, please see ./data/year{year}/DrellYan/path/datapath.json
        
        self.__TriggerSF= settings['TriggerSF']
        self.__LepSF_File = settings['LepSF_File']
        
        self.__histos = OrderedDict()
        self.__histos['MC'] = OrderedDict()
        self.__histos['Data'] = OrderedDict()

        self.__dfs = OrderedDict()
        self.__dfs['MC'] = OrderedDict()
        self.__dfs['Data'] = OrderedDict()
        self.__SF_mode = settings['SF_mode'] # trig_SF is applied or not
        self.__weights = settings['Weights'] 
    
    def Run(self):

        ROOT.gInterpreter.ProcessLine('#include "./include/IDScaleFactor.h"')
        print('./include/IDScaleFactor.h is Loaded.')
        ROOT.gSystem.Load('./myLib/IDScaleFactor_cpp.so')
        print('./myLib/myLib.so is Loaded.')
        print(f"Start to Analyze Drell-Yan Process For Channel: {self.__channel} ...")
        

        if self.__channel == 'ElectronMuon': 
            RECOWeight_Mul_TTC = 'Electron_RECO_SF[ttc_l2_id]'
            RECOWeight_Mul_OPS = 'Electron_RECO_SF[OPS_l2_id]'
            l1_IDSF_type = self.__LepSF_File['name']['Muon']
            l1_IDSF_File = self.__LepSF_File['path']['Muon']
            
            l2_IDSF_type = self.__LepSF_File['name']['Electron']
            l2_IDSF_File = self.__LepSF_File['path']['Electron']
            ROOT.gInterpreter.ProcessLine(Histogram_Definition['Diff_Type'].format(l1_IDSF_File,l2_IDSF_File,l1_IDSF_type,l2_IDSF_type))
        else:
            l1_IDSF_type = self.__LepSF_File['name']
            l1_IDSF_File = self.__LepSF_File['path']
            
            l2_IDSF_type = l1_IDSF_type 
            l2_IDSF_File = ""
            ROOT.gInterpreter.ProcessLine(Histogram_Definition['Same_Type'].format(l1_IDSF_File,l1_IDSF_type))
            if self.__channel == 'DoubleElectron'  :
                RECOWeight_Mul_TTC = 'Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]'
                RECOWeight_Mul_OPS = 'Electron_RECO_SF[OPS_l1_id]*Electron_RECO_SF[OPS_l2_id]'
            elif self.__channel == 'DoubleMuon':
                RECOWeight_Mul_TTC = '1.'
                RECOWeight_Mul_OPS = '1.'

        ROOT.gInterpreter.ProcessLine(Histogram_Definition['Same_Type'].format(l1_IDSF_File,l1_IDSF_type))
        #To Load IDSF function

        for p in self.__Process:
            for MC in self.__FilesIn['MC'][p].keys():
                settings ={
                        'channel': self.__channel,
                        'Data' : False,
                        'Trigger_Condition': self.__HLT_Path['All'],
                        'weights' : self.__weights['MC'],
                        'File_Paths' : self.__FilesIn['MC'][p][MC],
                        'TriggerSF': self.__TriggerSF,
                        'nevents' : self.__nevents,
                        'SF_mode':self.__SF_mode
                        }
                self.__dfs['MC'][MC]= MyDataFrame(settings)
        
        
        for Sample_Name in self.__HLT_Path[self.__channel].keys():
            settings = {
                    'channel': self.__channel,
                    'weights' : self.__weights['Data'],
                    'Trigger_Condition' :  self.__HLT_Path[self.__channel][Sample_Name],
                    'Data': True,
                    'File_Paths' : self.__FilesIn['Data'][self.__channel][Sample_Name],
                    'nevents' : self.__nevents
                    }
            self.__dfs['Data'][Sample_Name]= MyDataFrame(settings)


        for p in self.__Process:
            for MC in self.__FilesIn['MC'][p].keys():
                Filtering(self.__dfs['MC'][MC],HistSettings)
        
        for Sample_Name in self.__HLT_Path[self.__channel].keys():
            Filtering(self.__dfs['Data'][Sample_Name] , HistSettings)


        for histname in HistSettings.keys():
            HistoGrams = OrderedDict()
            HistoGrams['MC'] = OrderedDict()
            Temps = OrderedDict()
            Temps['Data'] = OrderedDict()
            Temps['MC'] = OrderedDict()
            for p in self.__Process:
                for MC in self.__FilesIn['MC'][p].keys():
                    h = self.__dfs['MC'][MC].Hists[histname].GetValue()
                    h.Scale(self.__Cross_Section[p][MC]/float(self.__NumberOfEvents[p][MC]))
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
            if self.__year =='2017':
                HistoGrams['MC']['VV'].Add(Temps['MC']['WZ_ew'])
                HistoGrams['MC']['VV'].Add(Temps['MC']['WZ_qcd'])
            elif self.__year =='2018':
                HistoGrams['MC']['VV'].Add(Temps['MC']['WZ'])

            
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

            Plot(HistoGrams,x_name=histname ,lumi=self.__lumi,channel=self.__channel,year=self.__year,SF_mode=self.__SF_mode )
        


