import ROOT
import json
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile
from PhysProcessRECO.Utils import  Plot
from PhysProcessRECO.RDataFrameStab import RDataFrameStab,Millstone 
import PhysProcessRECO.Utils as Utils
from PhysProcessRECO.HistogramSetting import HistSettings
from collections import OrderedDict
from Utils.General_Tool import overunder_flowbin
from Utils.Header import Histogram_Definition

from PhysProcessRECO.ReadScaleFactors import Claim
#import multiprocessing
#from multiprocessing import Queue, Process, Manager, Pool

class Analyzer():
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
        self.__region = settings['region']        
        
        if settings['lumi'] == -1:
        
            self.__lumi = self.__Cross_Section['lumi']
        else:
            self.__lumi = settings['lumi']
        
        
        self.__NumberOfEvents = settings['NumberOfEvents']# # of events for Data
        
        self.__veto = settings['veto']
        if self.__veto and self.__year !='2018':
            raise ValueError('[-v/--veto] is only valid for UL2018.')
        
        self.__DataPath = settings['FilesIn']['Data'][self.__channel]
        self.__MCPath = settings['FilesIn']['MC']
        self.__Process = settings['Process']  # Sorts of Process, please see ./data/year{year}/DrellYan/path/datapath.json
        
        self.__TriggerSF= settings.get('TriggerSF',None)
        self.__LepSF_File = settings['LepIDSF_File']
        
        self.__histos = OrderedDict()
        self.__histos['MC'] = OrderedDict()
        self.__histos['Data'] = OrderedDict()

        self.__dfs = OrderedDict()
        self.__dfs['MC'] = OrderedDict()
        self.__dfs['Data'] = OrderedDict()
        self.__TrigSF = settings['TrigSF'] # trig_SF is applied or not
        if self.__TrigSF != 0:
            print('TrigSF: Activate')
            print(f'TrigSF Type -> {self.__TrigSF}')
        else:
            print('TrigSF: Deactivate')

        self.__IDSF = settings['IDSF'] # IDSF is applied or not
        if self.__IDSF:
            print('IDSF: Activate')
        else:
            print('IDSF: Deactivate')
        self.__RECOSF = settings['RECOSF'] # RECOSF is applied or not
        if self.__RECOSF:

            print('RECOSF: Activate')
        else:
            print('RECOSF: Deactivate')
        self.__CFSF = settings['CFSF'] # CFSF is applied or not
        if self.__CFSF:
            print('Charge Flip Scale Factors: Activate')
        else:
            print('Charge Flip Scale Factors: Deactivate')
        #self.__condition_weights = settings['Weights']
        self.__MET_Filters = settings['MET_Filters']
        #self.__Phys_Process = settings['Phys_Process']

        self.__debug = settings['debug']
        self.__ylog = settings['ylog']

        self.__Eras = settings['Eras']
        
        if self.__Eras ==['']:
            self.__Eras = -1


        self.__trigSFInfo = settings['trigSFInfo']

    def Run(self):
        print(f"Start to Analyze {self.__region} Process For Channel: {self.__channel} ...")
        
        #HEM15/16 issue for UL2018 problems
        #Define IDSF files path and branchname
        #Define TrigSF files path and branchname
        if self.__channel == 'ElectronMuon': 
            
            l1_IDSF_Name = self.__LepSF_File['name']['Muon'][0]
            l1_RECO_Name = self.__LepSF_File['name']['Muon'][1]

            l1_IDSF_File = self.__LepSF_File['path']['Muon']
            
            l2_IDSF_type = self.__LepSF_File['name']['Electron']
            l2_IDSF_File = self.__LepSF_File['path']['Electron']
            
            ROOT.gInterpreter.ProcessLine(Claim['IDSF']['ElectronMuon'].format(l1_IDSF_File,l2_IDSF_File,l1_IDSF_Name,l2_IDSF_type,l1_RECO_Name))
            
            
            #ROOT.gInterpreter.ProcessLine(Histogram_Definition['ElectronMuon'].format(l1_IDSF_File,l2_IDSF_File,l1_IDSF_Name,l2_IDSF_type,l1_RECO_Name))
        elif self.__channel == 'DoubleElectron':
            l1_IDSF_type = self.__LepSF_File['name']
            l1_IDSF_File = self.__LepSF_File['path']
            
            l2_IDSF_type = l1_IDSF_type 
            l2_IDSF_File = ""
            #ROOT.gInterpreter.ProcessLine(Histogram_Definition['DoubleElectron'].format(l1_IDSF_File,l1_IDSF_type))
            ROOT.gInterpreter.ProcessLine(Claim['IDSF']['DoubleElectron'].format(l1_IDSF_File,l1_IDSF_type))


            with open(f'./data/year{self.__year}/PhysProcessRECO/path/ChargeFlipFiles.json','r') as f:
                cf_Info = json.load(f)
            ROOT.gInterpreter.ProcessLine(Claim['ChargeFlipSF'].format(cf_Info['prob_MLE'],cf_Info['SF']))



        elif self.__channel == 'DoubleMuon':
            RECOWeight_LEP_TTC = '1.'
            RECOWeight_LEP_OPS = '1.'
            l1_IDSF_type = self.__LepSF_File['name'][0]
            RECO_IDSF_type = self.__LepSF_File['name'][1]
            l1_IDSF_File = self.__LepSF_File['path']
            
            l2_IDSF_type = l1_IDSF_type 
            l2_IDSF_File = ""
            ROOT.gInterpreter.ProcessLine(Claim['IDSF']['DoubleMuon'].format(l1_IDSF_File,l1_IDSF_type,RECO_IDSF_type)) 
        if self.__TrigSF != 0:
            if self.__TrigSF==1:
                branchName = 'l1pteta'
            elif self.__TrigSF == 2:
                branchName = 'l2pteta'
            elif self.__TrigSF == 3:
                branchName = 'l1l2pt'
            else:
                branchName = 'l1l2eta'
            
            with open('./data/year2017/PhysProcessRECO/path/triggerSF.json','r') as f:
                TrigSFInfo = json.load(f)
            TrigSF_FileIn = TrigSFInfo['file'][self.__channel][branchName]
            
            ROOT.gInterpreter.ProcessLine(Claim['TrigSF'].format(TrigSF_FileIn,branchName))

        
        
        
        #To Load IDSF function
    
        #DataFrame For Data 
        
        if self.__Eras == -1:
            for i in self.__DataPath.keys() :
                self.__Eras = self.__DataPath[i].keys()
                break 

        for era in self.__Eras:
            self.__dfs['Data'][era] = dict()
            for dataset in self.__DataPath.keys():
                settings = {
                        'channel': self.__channel,
                        'MET_Filters' :  self.__MET_Filters['Data'],
                        'IsData': True,
                        'File_Paths' : self.__DataPath[dataset][era],
                        'nevents' : self.__nevents,
                        'veto':self.__veto,
                        'year':self.__year,
                        'region':self.__region,
                        }
        
                self.__dfs['Data'][era][dataset] = RDataFrameStab(settings)
         
        
        #DataFrame For Simulation Events
        for process in self.__MCPath.keys():
            self.__dfs['MC'][process] = dict()
            for phys_name in self.__MCPath[process].keys():
                settings ={
                        'channel': self.__channel,
                        'MET_Filters' :  self.__MET_Filters['MC'][process][phys_name],
                        'IsData' : False,
                        'File_Paths' : self.__MCPath[process][phys_name],
                        'nevents' : self.__nevents,
                        'veto':self.__veto,
                        'year':self.__year,
                        'region':self.__region,
                        }
                
                self.__dfs['MC'][process][phys_name]= RDataFrameStab(settings)
        for process in self.__MCPath.keys():
            for phys_name in self.__MCPath[process].keys():
                print(f"{process}:{phys_name}:Filtering")
                SF_Config = dict()
                
                SF_Config['TrigSF'] = dict()
                SF_Config['IDSF'] = dict()
                SF_Config['RECOSF'] = dict()
                SF_Config['PreFireWeight'] = dict()
                SF_Config['kinematic'] = dict()
                SF_Config['cf_SF'] = dict()

                if self.__IDSF:
                    SF_Config['IDSF']['activate'] = True

                else:
                    SF_Config['IDSF']['activate'] = False
                if self.__RECOSF:
                    SF_Config['RECOSF']['activate'] = True
                else:
                    SF_Config['RECOSF']['activate'] = False
                if self.__CFSF:
                    SF_Config['cf_SF']['sigma'] = 0
                    SF_Config['kinematic']['activate'] = 'true'
                    if phys_name =='TTTo1L':
                        SF_Config['cf_SF']['activate'] = False

                    else:
                        SF_Config['cf_SF']['activate'] = True
                    
                    if self.__region == 'SignalRegion': 
                        SF_Config['cf_SF']['Same_Sign'] = True
                    else:
                        SF_Config['cf_SF']['Same_Sign'] = False
                else:
                    SF_Config['cf_SF']['activate'] = False
                    SF_Config['kinematic']['activate'] ='false'
                    SF_Config['cf_SF']['sigma'] = None
                    SF_Config['cf_SF']['Same_Sign'] = None
                
                if self.__TrigSF != 0:
                    SF_Config['TrigSF']['activate'] = True
                else:
                    SF_Config['TrigSF']['activate'] = False
                SF_Config['TrigSF']['Type']  = self.__TrigSF
                SF_Config['PreFireWeight']['activate']   = True 



                #print(self.__DiLep_Conditions['MC'])
                Millstone(self.__dfs['MC'][process][phys_name],HistSettings=HistSettings,SF_Config=SF_Config,DiLepton_Triggers_Condition = self.__DiLep_Conditions['MC'],Run_List=[])
                
                print(f"{process}:{phys_name}:Filter equipped success")
        
        
        for era in self.__Eras:
            for dataset in self.__DataPath.keys():
                SF_Config = dict()
                print(f"{dataset}:{era}:Filtering")
                Millstone(self.__dfs['Data'][era][dataset] , HistSettings=HistSettings,SF_Config=SF_Config,DiLepton_Triggers_Condition =self.__DiLep_Conditions["Data"][era][dataset],Run_List =self.__DiLepton_Triggers[era])
                print(f"{dataset}:{era}:Filter equipped success")
        if not self.__debug:
            print('Starting to plotting...')
            for histname in HistSettings[self.__region].keys():
                HistoGrams = OrderedDict()
                HistoGrams['MC'] = OrderedDict()
                HistoGrams['Data'] = OrderedDict()
                Temps = OrderedDict()
                Temps['Data'] = OrderedDict()
                Temps['MC'] = OrderedDict()
                for idx1 ,era in enumerate(self.__dfs['Data'].keys()):
                    Temps['Data'][era] = dict()
                    for idx2, dataset in enumerate(self.__dfs['Data'][era].keys()):
                        h = self.__dfs['Data'][era][dataset].Hists[histname].GetValue()
                        h = overunder_flowbin(h)
                        Temps['Data'][era][dataset] = h
                        if idx1 == 0 and idx2 == 0:
                            HistoGrams['Data'] = Temps['Data'][era][dataset]
                        else:
                            HistoGrams['Data'].Add(Temps['Data'][era][dataset])
          
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

                Plot(HistoGrams,x_name=histname ,lumi=self.__lumi,channel=self.__channel,year=self.__year,ylog=self.__ylog,TrigSF_On = self.__TrigSF, IDSF_On= self.__IDSF,RECOSF_On =self.__RECOSF,CFSF_On =self.__CFSF,eras = self.__Eras,region=self.__region)
