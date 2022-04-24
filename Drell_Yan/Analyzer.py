import ROOT
import json
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile
from Drell_Yan.Utils import  Plot, MyDataFrame, Filtering
import Drell_Yan.Utils as DY_utils
from Drell_Yan.HistogramSetting import HistSettings
from collections import OrderedDict
from Utils.General_Tool import overunder_flowbin
from Utils.Header import Histogram_Definition

#import multiprocessing
#from multiprocessing import Queue, Process, Manager, Pool

class DrellYanRDataFrame():
    def __init__(self,settings:dict) -> None:
        '''
        self.__year -> '2017/2018/2016apv/2016postapv'
        self.__channel -> DoubleElectron/DoubleMuon/ElectronMuon
        self.__nevents -> Wanted Event rounds for Entire Analysis
        self.__HLT_Path -> HLT_Path for LEP/MET
        self.__Cross_Section -> Cross_Section Dictionary for corresponding phys. process.
        self.__lumi -> Total Luminosity for corresponding year
        self.__veto -> To veto HEM region or not, only valid in UL2018
        self.__FilesIn -> Path to Data/MC
        self.__Process -> Name or info. for MC.
        self.__TriggerSF -> Path/branchname for triggerSF 
        self.__LeptIDSF_File-> Path/branchname for LepIDSF_File
        self.__histos -> Histogram for corresponding phys. process/Data
        self.__SF_mode -> To specifiy whether to use IDSF/TrigSF, 
            - 0->no SF
            - 1->IDSF
            - 2->TrigSF
            - 3->(ID+Trig) SF
        self.__condition_weights ->
            - MC:
                - 2017 : Prefire*puWeight
                - 2018 : puWeight
            - Data:
                - 2017/2018 : 1
        '''
        self.__year  = settings['year']
        self.__channel = settings['channel']
        self.__nevents = settings['nevents'] ## of events for DataFrame to run through

        self.__HLT_Path = settings['HLT_Path']
        self.__Cross_Section = settings['xs']
        self.__lumi = self.__Cross_Section['lumi']
        self.__NumberOfEvents = settings['NumberOfEvents']# # of events for Data
        
        self.__veto = settings['veto']
        if self.__veto and self.__year !='2018':
            raise ValueError('[-v/--veto] is only valid for UL2018.')
        
        self.__FilesIn = settings['FilesIn']
        self.__Process = settings['Process']  # Sorts of Process, please see ./data/year{year}/DrellYan/path/datapath.json
        
        self.__TriggerSF= settings['TriggerSF']
        self.__LepIDSF_File = settings['LepIDSF_File']
        
        self.__histos = OrderedDict()
        self.__histos['MC'] = OrderedDict()
        self.__histos['Data'] = OrderedDict()

        self.__dfs = OrderedDict()
        self.__dfs['MC'] = OrderedDict()
        self.__dfs['Data'] = OrderedDict()
        self.__SF_mode = settings['SF_mode'] # trig_SF is applied or not
        self.__condition_weights = settings['Weights']
        self.__flag = settings['FLAG']
        self.__debug = settings['debug']
        self.__ylog = settings['ylog']
    
    def Run(self):

        ROOT.gInterpreter.ProcessLine('#include "./include/IDScaleFactor.h"')
        print('./include/IDScaleFactor.h is Loaded.')
        ROOT.gSystem.Load('./myLib/IDScaleFactor_cpp.so')
        print('./myLib/myLib.so is Loaded.')
        print(f"Start to Analyze Drell-Yan Process For Channel: {self.__channel} ...")
        
        #HEM15/16 issue for UL2018 problems
        if self.__year == '2018' and self.__veto:
            ROOT.gInterpreter.ProcessLine('#include "./include/HEM_veto.h"')
            ROOT.gSystem.Load('./myLib/HEM_veto_cpp.so')
            ROOT.gInterpreter.ProcessLine('srand(12345);')
            #Seed to offset the prob for deciding whether MC events in events which have HEM issue.

            print('Veto HEM Region For Data 2018...')
            #with open(f'./data/year{self.__year}/DrellYan/User.json','r') as f:
            #    UserName = json.load(f)["UserName"]
            #with open(f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{self.__year}/{self.__channel}/files/Info_vetohemregion.json','r') as f:
            #    Veto_Nevts = json.load(f)['Data:NumberOfEvents']
            #with open(f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{self.__year}/{self.__channel}/files/Info.json','r') as f:
            #    All_Nevts = json.load(f)['Data:NumberOfEvents']
            
            with open ("./data/year2018/TriggerSF/configuration/veto_ratio.json","r") as f :
                veto_ratio = json.load(f)[self.__channel]
            lumi = self.__lumi
            self.__lumi = veto_ratio*self.__lumi
            print(f'Total Luminosity reduce from {lumi} to {self.__lumi} due to HEM region in UL2018.')
        #Define IDSF files path and branchname
        #Define TrigSF files path and branchname
        if self.__channel == 'ElectronMuon': 
            l1_IDSF_type = self.__LepIDSF_File['name']['Muon']
            l1_IDSF_File = self.__LepIDSF_File['path']['Muon']
            
            l2_IDSF_type = self.__LepIDSF_File['name']['Electron']
            l2_IDSF_File = self.__LepIDSF_File['path']['Electron']


            ROOT.gInterpreter.ProcessLine(Histogram_Definition['Diff_Type_IDSF'].format(l1_IDSF_File,l2_IDSF_File,l1_IDSF_type,l2_IDSF_type))
        else:
            IDSF_type = self.__LepIDSF_File['name']
            IDSF_File = self.__LepIDSF_File['path']
            ROOT.gInterpreter.ProcessLine(Histogram_Definition['Same_Type_IDSF'].format(IDSF_File,IDSF_type))
        
        l1_trigSF_branchname = self.__TriggerSF['branchname']['l1']
        l2_trigSF_branchname = self.__TriggerSF['branchname']['l2']
        
        if self.__year != '2018':
            l1_trigSF_File = self.__TriggerSF['file'][self.__channel]['l1']
            l2_trigSF_File = self.__TriggerSF['file'][self.__channel]['l2']
        else:
            if self.__veto:
                l1_trigSF_File = self.__TriggerSF['file']['veto'][self.__channel]['l1']
                l2_trigSF_File = self.__TriggerSF['file']['veto'][self.__channel]['l2']
            else:
                l1_trigSF_File = self.__TriggerSF['file']['all'][self.__channel]['l1']
                l2_trigSF_File = self.__TriggerSF['file']['all'][self.__channel]['l2']

        ROOT.gInterpreter.ProcessLine(Histogram_Definition['TrigSF'].format(l1_trigSF_File,l2_trigSF_File,l1_trigSF_branchname,l2_trigSF_branchname))
        #To Load IDSF function
    
        #DataFrame For Data 
        for Sample_Name in self.__HLT_Path[self.__channel].keys():
            settings = {
                    'channel': self.__channel,
                    'weights' : self.__condition_weights['Data'],
                    'Trigger_Condition' :  self.__HLT_Path[self.__channel][Sample_Name],
                    'Data': True,
                    'File_Paths' : self.__FilesIn['Data'][self.__channel][Sample_Name],
                    'nevents' : self.__nevents,
                    'veto':self.__veto,
                    'Flag':self.__flag
                    }
            self.__dfs['Data'][Sample_Name]= MyDataFrame(settings)
        
        #DataFrame For Simulation Events
        for p in self.__Process:
            for MC in self.__FilesIn['MC'][p].keys():
                settings ={
                        'channel': self.__channel,
                        'Data' : False,
                        'Trigger_Condition': self.__HLT_Path['All'],
                        'weights' : self.__condition_weights['MC'],
                        'File_Paths' : self.__FilesIn['MC'][p][MC],
                        'TriggerSF': self.__TriggerSF,
                        'nevents' : self.__nevents,
                        'SF_mode':self.__SF_mode,
                        'veto':self.__veto,
                        'year':self.__year,
                        'Flag':self.__flag
                        }
                self.__dfs['MC'][MC]= MyDataFrame(settings)

        for p in self.__Process:
            for MC in self.__FilesIn['MC'][p].keys():
                Filtering(self.__dfs['MC'][MC],HistSettings,self.__veto)
        for Sample_Name in self.__HLT_Path[self.__channel].keys():
            Filtering(self.__dfs['Data'][Sample_Name] , HistSettings,self.__veto)

        if not self.__debug:
            for histname in HistSettings.keys():
                HistoGrams = OrderedDict()
                HistoGrams['MC'] = OrderedDict()
                Temps = OrderedDict()
                Temps['Data'] = OrderedDict()
                Temps['MC'] = OrderedDict()
                for idx ,Data in enumerate(self.__dfs['Data'].keys()):
                    h= self.__dfs['Data'][Data].Hists[histname].GetValue()
                    h = overunder_flowbin(h)
                    Temps['Data'][Data] = overunder_flowbin(h)
                    if idx == 0:
                        HistoGrams['Data'] = Temps['Data'][Data]
                    else:
                        HistoGrams['Data'].Add(Temps['Data'][Data])
          
                for p in self.__Process:
                    for MC in self.__FilesIn['MC'][p].keys():
                        h = self.__dfs['MC'][MC].Hists[histname].GetValue()
                        h.Scale(self.__Cross_Section[p][MC]/float(self.__NumberOfEvents[p][MC]))
                        Temps['MC'][MC] = overunder_flowbin(h)
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

                Plot(HistoGrams,x_name=histname ,lumi=self.__lumi,channel=self.__channel,year=self.__year,SF_mode=self.__SF_mode,ylog=self.__ylog)
            
        else:
            print("Finish Debug mode.")
