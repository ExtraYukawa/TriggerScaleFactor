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

        self.__DiLepton_Triggers = settings['DiLepton_Triggers']
        self.__DiLep_Conditions = settings['DiLep_Conditions']
        self.__Cross_Section = settings['xs']
        self.__lumi = self.__Cross_Section['lumi']
        self.__NumberOfEvents = settings['NumberOfEvents']# # of events for Data
        
        self.__veto = settings['veto']
        if self.__veto and self.__year !='2018':
            raise ValueError('[-v/--veto] is only valid for UL2018.')
        
        self.__DataPath = settings['FilesIn']['Data'][self.__channel]
        self.__MCPath = settings['FilesIn']['MC']
        self.__Process = settings['Process']  # Sorts of Process, please see ./data/year{year}/DrellYan/path/datapath.json
        
        self.__TriggerSF= settings.get('TriggerSF',None)
        self.__LepIDSF_File = settings['LepIDSF_File']
        
        self.__histos = OrderedDict()
        self.__histos['MC'] = OrderedDict()
        self.__histos['Data'] = OrderedDict()

        self.__dfs = OrderedDict()
        self.__dfs['MC'] = OrderedDict()
        self.__dfs['Data'] = OrderedDict()
        self.__SF_mode = settings['SF_mode'] # trig_SF is applied or not
        self.__condition_weights = settings['Weights']
        self.__MET_Filters = settings['MET_Filters']
        self.__Phys_Process = settings['Phys_Process']

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
        trigSF_branchname='Default' 
        if self.__SF_mode == 2 or self.__SF_mode ==3:
            trigSF_branchname = self.__TriggerSF['branchname']
            
            trigSF_File = self.__TriggerSF['FileIn']
            #if self.__year != '2016':
            #    print(self.__TriggerSF)
            #    trigSF_File = self.__TriggerSF['FileIn']
            #else:
            #if self.__year == '2018':
            #if self.__veto:
            #    trigSF_File = self.__TriggerSF['veto'][self.__channel][trigSF_branchname]
            #else:
            #    trigSF_File = self.__TriggerSF['all'][self.__channel][trigSF_branchname]

            ROOT.gInterpreter.ProcessLine(Histogram_Definition['TrigSF'].format(trigSF_File,trigSF_branchname))
        
        #To Load IDSF function
    
        #DataFrame For Data 
        
        for dataset in self.__DataPath.keys():
            #if dataset == 'SingleEG':continue
            self.__dfs['Data'][dataset] = dict()
            for era in self.__DataPath[dataset].keys():
                settings = {
                        'channel': self.__channel,
                        'weights' : self.__condition_weights['Data'],
                        'MET_Filters' :  self.__MET_Filters['Data'],
                        #'DiLepton_Triggers' : self.__DiLepton_Triggers['Data'][self.__channel][dataset][era],
                        'Data': True,
                        'File_Paths' : self.__DataPath[dataset][era],
                        'nevents' : self.__nevents,
                        'veto':self.__veto,
                        }
                self.__dfs['Data'][dataset][era] = MyDataFrame(settings)
        #DataFrame For Simulation Events
        for process in self.__MCPath.keys():
            self.__dfs['MC'][process] = dict()
            for phys_name in self.__MCPath[process].keys():
                settings ={
                        'channel': self.__channel,
                        'Data' : False,
                        'MET_Filters' :  self.__MET_Filters['MC'][process][phys_name],
                        #'DiLepton_Triggers' : self.__DiLepton_Triggers['MC'][self.__channel][process][phys_name],
                        'weights' : self.__condition_weights['MC'],
                        'File_Paths' : self.__MCPath[process][phys_name],
                        'nevents' : self.__nevents,
                        'SF_mode':self.__SF_mode,
                        'veto':self.__veto,
                        'year':self.__year,
                        }
                
                if self.__SF_mode== 2 or self.__SF_mode==3:
                    settings['trigSF_Type']=trigSF_branchname
                self.__dfs['MC'][process][phys_name]= MyDataFrame(settings)
        for process in self.__MCPath.keys():
            for phys_name in self.__MCPath[process].keys():
                print(f"{process}:{phys_name}:Filtering")
                Filtering(self.__dfs['MC'][process][phys_name],HistSettings,self.__veto,trigSF_branchname,self.__DiLep_Conditions['MC'])
                print(f"{process}:{phys_name}:Filter equipped success")
        for dataset in self.__dfs['Data'].keys():

            for era in self.__dfs['Data'][dataset].keys():
                print(f"{dataset}:{era}:Filtering")
                Filtering(self.__dfs['Data'][dataset][era] , HistSettings,self.__veto,trigSF_branchname,self.__DiLep_Conditions["Data"][era][dataset],self.__DiLepton_Triggers[era])
                print(f"{dataset}:{era}:Filter equipped success")
        if not self.__debug:
            print('Starting to process...')
            for histname in HistSettings.keys():
                HistoGrams = OrderedDict()
                HistoGrams['MC'] = OrderedDict()
                HistoGrams['Data'] = OrderedDict()
                Temps = OrderedDict()
                Temps['Data'] = OrderedDict()
                Temps['MC'] = OrderedDict()
                for idx1 ,dataset in enumerate(self.__dfs['Data'].keys()):
                    Temps['Data'][dataset] = dict()
                    print(dataset)
                    for idx2, era in enumerate(self.__dfs['Data'][dataset].keys()):
                        h = self.__dfs['Data'][dataset][era].Hists[histname].GetValue()
                        h = overunder_flowbin(h)
                        Temps['Data'][dataset][era] = h
                        if idx1 == 0 and idx2 == 0:
                            HistoGrams['Data'] = Temps['Data'][dataset][era]
                        else:
                            HistoGrams['Data'].Add(Temps['Data'][dataset][era])
          
                for process in self.__MCPath.keys():
                    for phys_name in self.__MCPath[process].keys():
                
                        #self.__dfs['MC'][MC].Hists[histname].Draw()
                        h = self.__dfs['MC'][process][phys_name].Hists[histname].GetValue()
                        h.Scale((self.__Cross_Section[process][phys_name]*self.__lumi)/float(self.__NumberOfEvents[process][phys_name]))
                        Temps['MC'][phys_name] = overunder_flowbin(h)
                ####
                HistoGrams['MC']['DY'] = Temps['MC']['DYnlo']
                HistoGrams['MC']['WJets'] = Temps['MC']['WJets']

                if self.__year =='2018' or self.__year == '2017':
                    HistoGrams['MC']['VV'] = Temps['MC']['osWW']
                    HistoGrams['MC']['VV'].Add( Temps['MC']['ssWW'])
                    HistoGrams['MC']['VV'].Add(Temps['MC']['WWdps'])
                    HistoGrams['MC']['VV'].Add(Temps['MC']['ZG_ew'])
                    HistoGrams['MC']['VV'].Add(Temps['MC']['ZZ'])
                    if self.__year == '2018':
                        HistoGrams['MC']['VV'].Add(Temps['MC']['WZ'])
                    else:
                        HistoGrams['MC']['VV'].Add(Temps['MC']['WZ_ew'])
                        HistoGrams['MC']['VV'].Add(Temps['MC']['WZ_qcd'])
                    HistoGrams['MC']['SingleTop'] = Temps['MC']['tsch']
                    HistoGrams['MC']['SingleTop'].Add(Temps['MC']['t_tch'])
                    HistoGrams['MC']['SingleTop'].Add(Temps['MC']['tbar_tch'])
                    HistoGrams['MC']['SingleTop'].Add(Temps['MC']['tW'])
                    HistoGrams['MC']['SingleTop'].Add(Temps['MC']['tbarW'])

                    
                    
                    HistoGrams['MC']['VVV'] = Temps['MC']['WWW']
                    HistoGrams['MC']['VVV'].Add(Temps['MC']['WWZ'])
                    HistoGrams['MC']['VVV'].Add(Temps['MC']['WZZ'])
                    HistoGrams['MC']['VVV'].Add(Temps['MC']['ZZZ'])
                    

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
                else:
                    HistoGrams['MC']['VV'] = Temps['MC']['ww']
                    HistoGrams['MC']['VV'].Add(Temps['MC']['wz_qcd'])
                    HistoGrams['MC']['VV'].Add(Temps['MC']['zz2l'])
                    
                    HistoGrams['MC']['VVV'] = Temps['MC']['www1']
                    HistoGrams['MC']['VVV'].Add(Temps['MC']['wwz1'])
                    HistoGrams['MC']['VVV'].Add(Temps['MC']['wzz1'])
                    HistoGrams['MC']['VVV'].Add(Temps['MC']['zzz1'])

                    HistoGrams['MC']['SingleTop'] = Temps['MC']['tW']
                    HistoGrams['MC']['SingleTop'].Add(Temps['MC']['tW'])
                    HistoGrams['MC']['SingleTop'].Add(Temps['MC']['t_sch'])
                    HistoGrams['MC']['SingleTop'].Add(Temps['MC']['t_tch'])
                    HistoGrams['MC']['SingleTop'].Add(Temps['MC']['tbar_tch'])

                    HistoGrams['MC']['ttXorXX'] = Temps['MC']['ttH']
                    HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttW'])
                    HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttWToQQ'])
                    HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttZ'])
                    HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttZToQQ'])
                    HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttWW'])
                    HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttWZ'])
                    HistoGrams['MC']['ttXorXX'].Add(Temps['MC']['ttZZ'])

                    HistoGrams['MC']['tzq'] = Temps['MC']['tZq']

                    HistoGrams['MC']['TT'] = Temps['MC']['TTTo2L2Nu']
                    HistoGrams['MC']['TT'].Add(Temps['MC']['TTTo1L'])



                Plot(HistoGrams,x_name=histname ,lumi=self.__lumi,channel=self.__channel,year=self.__year,SF_mode=self.__SF_mode,ylog=self.__ylog,trigSF_branchname=trigSF_branchname)
            
        else:
            print("Finish Debug mode.")
