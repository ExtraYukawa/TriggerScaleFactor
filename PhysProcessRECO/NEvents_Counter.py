import ROOT
import json
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile
from PhysProcessRECO.Utils import  Plot
from PhysProcessRECO.DF_NEventCalc import DF_NEventCalc
import PhysProcessRECO.Utils as Utils
from PhysProcessRECO.HistogramSetting import HistSettings
from collections import OrderedDict
from Utils.General_Tool import overunder_flowbin
from Utils.Header import Histogram_Definition

from PhysProcessRECO.Skip_MCSample import Skip_MC
from PhysProcessRECO.ReadScaleFactors import Claim
#import multiprocessing
#from multiprocessing import Queue, Process, Manager, Pool


class NEvents_Counter():
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
        
        self.__FakeRateFiles = settings['FakeRateFiles']


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
        self.__FakeRate = settings['FakeRate']
        if self.__FakeRate:
            print('Fake Rate Estimation: Activate')
        else:
            print('Fake Rate Estimation: Deactivate')


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
            self.__channel_rep='2'
            if self.__FakeRate:
                ROOT.gInterpreter.ProcessLine(Claim['FakeRate']['ElectronMuon'].format(self.__FakeRateFiles['muon'],self.__FakeRateFiles['electron']))
            
            if self.__IDSF or self.__RECOSF:
            
            
                l1_IDSF_Name = self.__LepSF_File['name']['Muon'][0]
                l1_RECO_Name = self.__LepSF_File['name']['Muon'][1]

                l1_IDSF_File = self.__LepSF_File['path']['Muon']
                
                l2_IDSF_type = self.__LepSF_File['name']['Electron']
                l2_IDSF_File = self.__LepSF_File['path']['Electron']
                
                ROOT.gInterpreter.ProcessLine(Claim['IDSF']['ElectronMuon'].format(l1_IDSF_File,l2_IDSF_File,l1_IDSF_Name,l2_IDSF_type,l1_RECO_Name))
            
        elif self.__channel == 'DoubleElectron':
            self.__channel_rep='3'
            if self.__FakeRate:
                ROOT.gInterpreter.ProcessLine(Claim['FakeRate']['DoubleElectron'].format(self.__FakeRateFiles['electron']))
            
            if self.__IDSF:
                l1_IDSF_type = self.__LepSF_File['name']
                l1_IDSF_File = self.__LepSF_File['path']
                
                l2_IDSF_type = l1_IDSF_type 
                l2_IDSF_File = ""
                ROOT.gInterpreter.ProcessLine(Claim['IDSF']['DoubleElectron'].format(l1_IDSF_File,l1_IDSF_type))


                with open(f'./data/year{self.__year}/PhysProcessRECO/path/ChargeFlipFiles.json','r') as f:
                    cf_Info = json.load(f)
            
            if self.__CFSF:
                ROOT.gInterpreter.ProcessLine(Claim['ChargeFlipSF'].format(cf_Info['SF'],cf_Info['prob_MLE']))



        elif self.__channel == 'DoubleMuon':
            self.__channel_rep='1'
            if self.__FakeRate:
                ROOT.gInterpreter.ProcessLine(Claim['FakeRate']['DoubleElectron'].format(self.__FakeRateFiles['muon']))
            if self.__IDSF or self.__RECOSF:
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
        else:pass
        
        #DataFrame For Simulation Events
        self.__NCounter = dict()

        self.__NCounter['Data'] = dict()
        self.__NCounter['MC'] = dict()
        if self.__FakeRate:
            self.__NCounter['FakeRate'] = dict()
        else:
            pass
        for idx,era in enumerate(self.__Eras):
            self.__dfs['Data'][era] = dict()
            for idx1,dataset in enumerate(self.__DataPath.keys()):
                print(f'Set up dataset: {dataset}')
                settings = {
                        'channel': self.__channel,
                        'IsData': True,
                        'File_Paths' : self.__DataPath[dataset][era],
                        'nevents' : self.__nevents,
                        'veto':self.__veto,
                        'year':self.__year,
                        'region':self.__region,
                        }
        
                SF_Config = dict()
                SF_Config['FakeRate'] = dict()
                print(f"{dataset}:{era}:Filtering")
                if self.__FakeRate:
                    self.__dfs['Data'][era][dataset] =dict()
                    SF_Config['FakeRate']['activate']= True
                    SF_Config['FakeRate']['IsFake'] = True

                    self.__dfs['Data'][era][dataset]['IsFake']= DF_NEventCalc(settings,SF_Config)

                    SF_Config['FakeRate']['IsFake'] = False
                    self.__dfs['Data'][era][dataset]['NotFake']= DF_NEventCalc(settings,SF_Config)
                    if idx == 0 and idx1 ==0:
                        self.__NCounter['Data']['PhysRegionCut'] = self.__dfs['Data'][era][dataset]['NotFake'].NEvents
                        self.__NCounter['FakeRate']['PhysRegionCut'] = self.__dfs['Data'][era][dataset]['IsFake'].NEvents
                    else:
                        self.__NCounter['Data']['PhysRegionCut'] += self.__dfs['Data'][era][dataset]['NotFake'].NEvents
                        self.__NCounter['FakeRate']['PhysRegionCut'] += self.__dfs['Data'][era][dataset]['IsFake'].NEvents
                else:
                    SF_Config['FakeRate']['activate']= False
                    SF_Config['FakeRate']['IsFake'] = False
                    self.__dfs['Data'][era][dataset]= DF_NEventCalc(settings,SF_Config)
                
                self.Filter(idx = idx,idx1=idx1,Cut_Name='lhe_nleptonCut',Cut='true',IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate) 
                self.Filter(idx = idx,idx1=idx1,Cut_Name='nHad_tau_Cut',Cut='nHad_tau==0',IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate) 
                self.Filter(idx=idx,idx1=idx1,Cut_Name='ttcRegion_Cut',Cut=f'ttc_region=={self.__channel_rep}',IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate)
                METFilters = ' && '.join(self.__MET_Filters['Data']) 
                self.Filter(idx=idx,idx1=idx1,Cut_Name='METFilters_Cut',Cut=f'{METFilters}',IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate)
                DiLepton_slc_run = dict()
                for Name in self.__DiLepton_Triggers[era].keys():
                    DiLepton_slc_run[Name] = ROOT.std.vector('int')()
                    for i in self.__DiLepton_Triggers[era][Name]:
                        DiLepton_slc_run[Name].push_back(i)
                DiLepton_Triggers_Condition = self.__DiLep_Conditions["Data"][era][dataset]
                self.Filter(idx = idx,idx1=idx1,Cut_Name='Triggers_Cut',Cut=eval(f"f'{DiLepton_Triggers_Condition}'"),IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate) 
                self.Filter(idx = idx,idx1=idx1,Cut_Name='ttcjets_Cut',Cut='ttc_jets',IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate) 
                self.Filter(idx = idx,idx1=idx1,Cut_Name='mll_Cut_20',Cut='ttc_mll>20',IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate) 
                if self.__channel == 'DoubleElectron':
                    self.Filter(idx = idx,idx1=idx1,Cut_Name='ttc_l1pt',Cut='l1pt>30',IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate) 
                    self.Filter(idx = idx,idx1=idx1,Cut_Name='mll_Cut_60_120',Cut='(ttc_mll>120 || ttc_mll<60)',IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate) 
                elif self.__channel == 'DoubleMuon':
                    self.Filter(idx = idx,idx1=idx1,Cut_Name='ttc_l1pt',Cut='l1pt>30',IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate) 
                else:
                    self.Filter(idx = idx,idx1=idx1,Cut_Name='ttc_dl_pt',Cut='l1pt>30 || l2pt>30',IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate) 

                self.Filter(idx = idx,idx1=idx1,Cut_Name='ttc_met_Cut',Cut='ttc_met>30',IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate) 
                self.Filter(idx = idx,idx1=idx1,Cut_Name='ttc_drll_Cut',Cut='ttc_drll>0.3',IsData=True,key1=era,key2=dataset,FakeRateOn=self.__FakeRate) 
        
                print(f"{dataset}:{era}:Filter equipped success")
        



        for idx,process in enumerate(self.__MCPath.keys()):
            self.__dfs['MC'][process] = dict()
            for idx1,phys_name in enumerate(self.__MCPath[process].keys()):
                if self.__FakeRate:
                    if Skip_MC(phys_name,self.__year,Skip_Sample=True): continue
                settings ={
                        'channel': self.__channel,
                        'IsData' : False,
                        'File_Paths' : self.__MCPath[process][phys_name],
                        'nevents' : self.__nevents,
                        'veto':self.__veto,
                        'year':self.__year,
                        'region':self.__region,
                        'scale':(self.__Cross_Section[process][phys_name]*self.__lumi)/float(self.__NumberOfEvents[process][phys_name])
                        }
                SF_Config = dict()                
                SF_Config['IsData'] = False 
                SF_Config['TrigSF'] = dict()
                SF_Config['IDSF'] = dict()
                SF_Config['RECOSF'] = dict()
                SF_Config['PreFireWeight'] = dict()
                SF_Config['kinematic'] = dict()
                SF_Config['cf_SF'] = dict()
                SF_Config['FakeRate'] = dict()
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
                    SF_Config['cf_SF']['activate'] = True
                    
                    if self.__region == 'SignalRegion' or self.__region =='ChargeFlipRegion': 
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

                SF_Config['FakeRate'] = dict()

                print(f"{process}:{phys_name}:Filtering")
                if self.__FakeRate:
                    if Skip_MC(phys_name,self.__year,Skip_Sample=True): continue
                    self.__dfs['MC'][process][phys_name]= dict()
                    SF_Config['FakeRate']['activate']= True
                    SF_Config['FakeRate']['IsFake'] =True
                    SF_Config['FakeRate']['IsFake'] =True
                    self.__dfs['MC'][process][phys_name]['IsFake']= DF_NEventCalc(settings,SF_Config)
                    SF_Config['FakeRate']['IsFake'] =False
                    self.__dfs['MC'][process][phys_name]['NotFake']= DF_NEventCalc(settings,SF_Config)
                    if idx == 0 and idx1 ==0:
                        self.__NCounter['MC']['PhysRegionCut'] = self.__dfs['MC'][process][phys_name]['NotFake'].NEvents
                    else:
                        self.__NCounter['MC']['PhysRegionCut'] += self.__dfs['MC'][process][phys_name]['NotFake'].NEvents
                    self.__NCounter['FakeRate']['PhysRegionCut'] += self.__dfs['MC'][process][phys_name]['IsFake'].NEvents
                    
                else:
                    SF_Config['FakeRate']['activate']= False
                    SF_Config['FakeRate']['IsFake'] =False
                    self.__dfs['MC'][process][phys_name]= DF_NEventCalc(settings,SF_Config)
                    if idx == 0 and idx1 ==0:
                        self.__NCounter['MC']['PhysRegionCut'] = self.__dfs['MC'][process][phys_name].NEvents
                    else:
                        self.__NCounter['MC']['PhysRegionCut'] += self.__dfs['MC'][process][phys_name].NEvents
                
                self.Filter(idx=idx,idx1=idx1,Cut_Name='lhe_nleptonCut',Cut='lhe_nlepton>1',IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate)
                self.Filter(idx = idx,idx1=idx1,Cut_Name='nHad_tau_Cut',Cut='nHad_tau==0',IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate) 
                self.Filter(idx=idx,idx1=idx1,Cut_Name='ttcRegion_Cut',Cut=f'ttc_region=={self.__channel_rep}',IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate)
                METFilters = ' && '.join(self.__MET_Filters['MC'][process][phys_name]) 
                self.Filter(idx=idx,idx1=idx1,Cut_Name='METFilters_Cut',Cut=f'{METFilters}',IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate)
                self.Filter(idx = idx,idx1=idx1,Cut_Name='Triggers_Cut',Cut=f"{self.__DiLep_Conditions['MC']}",IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate) 
                self.Filter(idx = idx,idx1=idx1,Cut_Name='ttcjets_Cut',Cut='ttc_jets',IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate) 
                self.Filter(idx = idx,idx1=idx1,Cut_Name='mll_Cut_20',Cut='ttc_mll>20',IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate) 
                if self.__channel == 'DoubleElectron':
                    self.Filter(idx = idx,idx1=idx1,Cut_Name='ttc_l1pt',Cut='l1pt>30',IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate) 
                    self.Filter(idx = idx,idx1=idx1,Cut_Name='mll_Cut_60_120',Cut='(ttc_mll>120 || ttc_mll<60)',IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate) 
                elif self.__channel == 'DoubleMuon':
                    self.Filter(idx = idx,idx1=idx1,Cut_Name='ttc_l1pt',Cut='l1pt>30',IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate) 
                else:
                    self.Filter(idx = idx,idx1=idx1,Cut_Name='ttc_dl_pt',Cut='l1pt>30 || l2pt>30',IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate) 

                self.Filter(idx = idx,idx1=idx1,Cut_Name='ttc_met_Cut',Cut='ttc_met>30',IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate) 
                self.Filter(idx = idx,idx1=idx1,Cut_Name='ttc_drll_Cut',Cut='ttc_drll>0.3',IsData=False,key1=process,key2=phys_name,FakeRateOn=self.__FakeRate) 

                print(f"{process}:{phys_name}:Filter equipped success")
        if self.__channel =='DoubleElectron':
            Cuts_List =  ['PhysRegionCut','lhe_nleptonCut','nHad_tau_Cut','ttcRegion_Cut','METFilters_Cut','Triggers_Cut','ttcjets_Cut','mll_Cut_20','ttc_l1pt','mll_Cut_60_120','ttc_met_Cut','ttc_drll_Cut']
        elif self.__channel =='DoubleMuon':
            Cuts_List =  ['PhysRegionCut','lhe_nleptonCut','nHad_tau_Cut','ttcRegion_Cut','METFilters_Cut','Triggers_Cut','ttcjets_Cut','mll_Cut_20','ttc_l1pt','ttc_met_Cut','ttc_drll_Cut']
        else:
            Cuts_List =  ['PhysRegionCut','lhe_nleptonCut','nHad_tau_Cut','ttcRegion_Cut','METFilters_Cut','Triggers_Cut','ttcjets_Cut','mll_Cut_20','ttc_dl_pt','ttc_met_Cut','ttc_drll_Cut']

        for i in ['Data','FakeRate','MC']:
            for j in Cuts_List:    
                print(f'{i},{j}: {self.__NCounter[i][j]}')


    def Filter(self,idx:int,idx1:int,Cut_Name:str,Cut:str,IsData:bool,key1:str,key2:str,FakeRateOn=True):
        if IsData ==None:
            raise ValueError('You need to specify Data or MC.')
        elif not IsData:
            NAME = 'MC'
        else :
            NAME ='Data'
        if FakeRateOn:
            self.__dfs[NAME][key1][key2]['NotFake'].Filter(Cut)
            self.__dfs[NAME][key1][key2]['IsFake'].Filter(Cut)
            if idx == 0 and idx1 ==0:
                self.__NCounter[NAME][Cut_Name] = self.__dfs[NAME][key1][key2]['NotFake'].NEvents
                if IsData:
                    self.__NCounter['FakeRate'][Cut_Name] = self.__dfs[NAME][key1][key2]['IsFake'].NEvents
                else:
                    self.__NCounter['FakeRate'][Cut_Name] += self.__dfs[NAME][key1][key2]['IsFake'].NEvents
            else:
                self.__NCounter[NAME][Cut_Name] += self.__dfs[NAME][key1][key2]['NotFake'].NEvents
                self.__NCounter['FakeRate'][Cut_Name] += self.__dfs[NAME][key1][key2]['IsFake'].NEvents

        else:
            self.__dfs[NAME][key1][key2].Filter(Cut)
            if idx == 0 and idx1 ==0:
                self.__NCounter[NAME][Cut_Name] = self.__dfs[NAME][key1][key2].NEvents
            else:
                self.__NCounter[NAME][Cut_Name] += self.__dfs[NAME][key1][key2].NEvents



