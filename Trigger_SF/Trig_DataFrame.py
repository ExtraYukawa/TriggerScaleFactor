import ROOT
import sys
import os
import json
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from ROOT import TH2D,TFile,TEfficiency
from array import array

from Utils.RDataFrame import *
from Utils.General_Tool import *
import warnings
import Utils.plot_settings as plt_set
from Utils.Header import Histogram_Definition




class TrigRDataFrame(MyDataFrame):
    def __init__(self,settings:dict)->None:
        super().__init__(settings)
        self.__Leptons_Informations = settings.get('Leptons_Information',None)
        self.__HLT_LEP_slcRun_List = settings.get('HLT_LEP',None)
        #self.__HLT_LEP = self.__HLT_LEP_slcRun_List.keys()
        
        self.__HLT_MET = settings.get('HLT_MET',None)
        self.__MET_Filters = settings.get('MET_Filters',None)
        self.__Year = settings.get('Year',None) 
        self.__LepSF_File = settings.get('LepSF_File',None)
        self.__DirOut = settings.get('DirOut',None)
        self.__Type = settings.get('Type',None)
        self.__channel = settings.get('channel',None)
        self.__FileIn = settings.get('FileIn',None)
        self.__nEvents = settings.get('nevents',None)
        self.__Condition_Weights = '*'.join(settings.get('Condition_Weights',None))
        self.__debug = settings.get('debug',None)
        self.__veto = settings.get('veto',None)
        self.__year = settings.get('year',None)

        if self.__veto:
            if self.__year != '2018':
                raise ValueError('HEM issue "Only" occured in year2018 data/MC sample')

        
        #self.__EventsInfo_FileName = os.path.join(self.__DirOut,'Info.json')
        



        self.__FileIn_vecstr= ROOT.std.vector('string')()
        for file_path in self.__FileIn:
            self.__FileIn_vecstr.push_back(file_path)
        
        self.__Histogram = dict()
        self.__Histogram['1D'] = dict()
        self.__Histogram['1D']['pt'] = dict()
        self.__Histogram['1D']['eta'] = dict()
        self.__Histogram['1D']['njet'] = dict()
        self.__Histogram['1D']['met'] = dict()
        
        
        self.__Histogram['2D'] = dict()
        self.__Histogram['2D']['pteta'] = dict()
        self.__Histogram['2D']['pt'] = dict()
        self.__Histogram['2D']['eta'] = dict()
        
        self.__Histogram['1D']['HLT'] = dict()
    @property
    def FileOutName()->str:
        return self.__FileOutName
    def Init_Histogram(self,**args):
        df = args.get('df',None)
        name = args.get('name',None)
        dim = args.get('dim',None)
        tag = args.get('tag',None)
        xtitle = args.get('xtitle',None)
        ytitle = args.get('ytitle',None)
        content = args.get('content',None)
        weight = args.get('weight','weight')
        lep_type = args.get('lep_type',None)

        #lep_type -> l1,l2,l1l2

        if df == None:
            raise ValueError('Should Specify RDataframe')
        if dim == None:
            raise ValueError('Should Specify Histogram')
        if content == None:
            raise ValueError('Should Specify Filled Value')
        if tag == None:
            raise ValueError('Should Speicify What is the tag of the Histogram.')
        if xtitle == None:
            warnings.warn('Should Speicify xtitle!')
        if ytitle == None:
            warnings.warn('Should Speicify ytitle!')
        if dim == '1D':
            if tag == 'pt':
                if lep_type=='l1':
                    xbin = plt_set.l1ptbin
                elif lep_type=='l2':
                    xbin = plt_set.l2ptbin
                else:
                    raise ValueError(f'Error.')

            elif tag == 'eta':
                xbin = plt_set.etabin
            elif tag == 'njet':
                xbin = plt_set.njetbin
            elif tag == 'met':
                xbin = plt_set.metbin
            else:
                raise ValueError(f'Tag{f} is not in the list.')
            nxbin = len(xbin) -1 
            self.__Histogram[dim][tag][name] = df.Histo1D((name,f"{name};{xtitle};{ytitle}",nxbin,xbin),*content,weight)
            self.__Histogram[dim][tag][name].Sumw2()
            self.__Histogram[dim][tag][name].SetMinimum(0)
        if dim == '2D':
            if tag == 'pt':
                xbin = plt_set.l1ptbin
                ybin = plt_set.l2ptbin
            elif tag == 'eta':
                xbin = plt_set.abs_etabin
                ybin = plt_set.abs_etabin
            elif tag == 'pteta':
                if lep_type=='l1':
                    xbin = plt_set.l1ptbin
                elif lep_type=='l2':
                    xbin = plt_set.l2ptbin
                else:
                    raise ValueError(f'Error.')
                ybin = plt_set.abs_etabin
            else:
                raise ValueError(f'Tag{tag} is not in the list.')
            nxbin = len(xbin) -1 
            nybin = len(ybin) -1 
            self.__Histogram[dim][tag][name] = df.Histo2D((name,f"{name};{xtitle};{ytitle}",nxbin,xbin,nybin,ybin),*content,weight)
            self.__Histogram[dim][tag][name].Sumw2()

        self.__Histogram[dim][tag][name].SetStats(0)
        self.__Histogram[dim][tag][name] = self.__Histogram[dim][tag][name].GetValue()
    def Save_Histogram(self,name:str,dim:str,tag:str):
        if name == None:
            raise ValueError('Should Specify Name of Histogram')
        if dim == None:
            raise ValueError('Should Specify Histogram')
        if tag == None:
            raise ValueError('Should Speicify What is the tag of the Histogram.')
        self.__Histogram[dim][tag][name].Write()
    def Counter_Hist(self,dim:str,tag,name:str):
        #count number in the bin.
        self.__Histogram[dim][tag][name].SetTitle(f'Count {name}')
        self.__Histogram[dim][tag][name].SetName(f'Count_{name}')
        self.__Histogram[dim][tag][name].Write()
    @property
    def Histogram(self):
        return self.__Histogram
    
    def Correct_VarName(self,name:list,process:str,tag:str)->list:
        
        corrected_name = []
        if process == 'OPS':
            for n in name:
                print(n)
                corrected_name.append(n+'[OPS_'+tag+'_id]')
        
        return corrected_name

    def Run(self):
       #ROOT.ROOT.EnableImplicitMT()
        if not self.__debug:
            print(f"Start to Analyze Trigger Efficiency of {self.__Type} for {self.__channel} ...")
        else:
            print('Debug Mode')
            print(f"Start to Analyze Trigger Efficiency of {self.__Type} for {self.__channel} ...")
        if self.__nEvents == -1:
            df = ROOT.RDataFrame("Events",self.__FileIn_vecstr)
        else:
            print(f'Only {self.__nEvents} events will be dumped into Analyzer.')
            df = ROOT.RDataFrame("Events",self.__FileIn_vecstr).Range(0,self.__nEvents)
        if self.__veto:
            ROOT.gInterpreter.ProcessLine('#include "./include/HEM_veto.h"')
            ROOT.gSystem.Load('./myLib/HEM_veto_cpp.so')
            print('Kind Warning: You start to veto HEM region.')
            if self.__Type == 'Data':
                veto = 'veto_hemregion(run,Jet_phi,Jet_eta)'
            else:
                ROOT.gInterpreter.Declare('#include <time.h>;srand(12345);')
                with open('./data/year2018/TriggerSF/configuration/MET_vetoHEM_rate.json','r') as f:
                    CD_ratio = json.load(f)
                veto = f'veto_hemregion_sim(prob(),Jet_phi,Jet_eta,{CD_ratio})'
            df = df.Filter(veto) 


        print('MET Filters: '+' && '.join(self.__MET_Filters)+'\n') 
        
        df_flag_trig = df.Filter(' && '.join(self.__MET_Filters),"Flag Cut")
        if self.__channel == 'ElectronMuon': 
            
            l1_IDSF_Name = self.__LepSF_File['name']['Muon'][0]
            l1_RECO_Name = self.__LepSF_File['name']['Muon'][1]

            l1_IDSF_File = self.__LepSF_File['path']['Muon']
            
            l2_IDSF_type = self.__LepSF_File['name']['Electron']
            l2_IDSF_File = self.__LepSF_File['path']['Electron']
            print(Histogram_Definition['ElectronMuon'].format(l1_IDSF_File,l2_IDSF_File,l1_IDSF_Name,l2_IDSF_type,l1_RECO_Name)) 
            ROOT.gInterpreter.ProcessLine(Histogram_Definition['ElectronMuon'].format(l1_IDSF_File,l2_IDSF_File,l1_IDSF_Name,l2_IDSF_type,l1_RECO_Name))
        elif self.__channel == 'DoubleElectron':
            l1_IDSF_type = self.__LepSF_File['name']
            l1_IDSF_File = self.__LepSF_File['path']
            
            l2_IDSF_type = l1_IDSF_type 
            l2_IDSF_File = ""
            ROOT.gInterpreter.ProcessLine(Histogram_Definition['DoubleElectron'].format(l1_IDSF_File,l1_IDSF_type))
            
        
        elif self.__channel == 'DoubleMuon':
            RECOWeight_LEP_TTC = '1.'
            RECOWeight_LEP_OPS = '1.'
            l1_IDSF_type = self.__LepSF_File['name'][0]
            RECO_IDSF_type = self.__LepSF_File['name'][1]
            l1_IDSF_File = self.__LepSF_File['path']
            
            l2_IDSF_type = l1_IDSF_type 
            l2_IDSF_File = ""
            ROOT.gInterpreter.ProcessLine(Histogram_Definition['DoubleMuon'].format(l1_IDSF_File,l1_IDSF_type,RECO_IDSF_type))
        
        
        #ttc_Flag -> Used to judge whether the region of events is ttc.
        #OPS_Flag -> Used to judge whetehr the region of events is OPS.
        

        df_region_trig = df_flag_trig\
                .Define("ttc_Flag",f'Region_FLAG(ttc_region,{self.__Leptons_Informations["region"]})')\
                .Define("OPS_Flag",f'Region_FLAG(OPS_region,{self.__Leptons_Informations["region"]})')\
                .Filter('ttc_Flag || OPS_Flag')\
                .Define("l1p4",f'LeptonP4(ttc_Flag,OPS_Flag,{self.__Leptons_Informations["ttc_p4"]["l1"][0]}\
                ,{self.__Leptons_Informations["ttc_p4"]["l1"][1]},{self.__Leptons_Informations["ttc_p4"]["l1"][2]}\
                ,{self.__Leptons_Informations["ttc_p4"]["l1"][3]},{self.__Leptons_Informations["OPS_p4"]["l1"][0]}\
                ,{self.__Leptons_Informations["OPS_p4"]["l1"][1]},{self.__Leptons_Informations["OPS_p4"]["l1"][2]},\
                {self.__Leptons_Informations["OPS_p4"]["l1"][3]})')\
                .Define("l2p4",f'LeptonP4(ttc_Flag,OPS_Flag,{self.__Leptons_Informations["ttc_p4"]["l2"][0]}\
                ,{self.__Leptons_Informations["ttc_p4"]["l2"][1]},{self.__Leptons_Informations["ttc_p4"]["l2"][2]}\
                ,{self.__Leptons_Informations["ttc_p4"]["l2"][3]},{self.__Leptons_Informations["OPS_p4"]["l2"][0]}\
                ,{self.__Leptons_Informations["OPS_p4"]["l2"][1]},{self.__Leptons_Informations["OPS_p4"]["l2"][2]},\
                {self.__Leptons_Informations["OPS_p4"]["l2"][3]})')\
                .Define("flag_2P0F",'if(ttc_Flag) return ttc_2P0F;else if(OPS_Flag) return OPS_2P0F;throw "Contraction Region!";')\
                .Filter('flag_2P0F')
                #.Define("IDsf",f'IDScaleFact("{self._channel}",h1_IDSF,h2_IDSF,l1pt,l2pt,l1eta,l2eta)')\
        if self.__channel !='ElectronMuon':
                df_region_trig=df_region_trig\
                    .Define("l1pt_tmp","if (l1p4.Pt() < 200) return l1p4.Pt();else return 199.;")\
                    .Define("l2pt_tmp","if (l2p4.Pt() < 200) return l2p4.Pt();else return 199.;")\
                    .Define("l1pt","if(l1pt_tmp > l2pt_tmp) return l1pt_tmp;else return l2pt_tmp")\
                    .Define("l2pt","if(l1pt_tmp > l2pt_tmp) return l2pt_tmp;else return l1pt_tmp")\
                    .Define("l1eta","if(l1pt_tmp > l2pt_tmp) return l1p4.Eta();else return l2p4.Eta();")\
                    .Define("l2eta","if(l1pt_tmp > l2pt_tmp) return l2p4.Eta();else return l1p4.Eta();")\
                    .Define("l1_iD","if(ttc_Flag) return ttc_l1_id;else return OPS_l1_id;")\
                    .Define("l2_iD","if(ttc_Flag) return ttc_l2_id;else return OPS_l2_id;")\
                    .Define("l1_ID","if(l1pt_tmp > l2pt_tmp) return l1_iD;else return l2_iD;")\
                    .Define("l2_ID","if(l1pt_tmp > l2pt_tmp) return l2_iD;else return l1_iD;")\
                    .Define("l1_abseta","abs(l1eta)")\
                    .Define("l2_abseta","abs(l2eta)")
        else:
                df_region_trig=df_region_trig\
                    .Define("l1pt","l1p4.Pt()")\
                    .Define("l2pt","l2p4.Pt()")\
                    .Define("l1eta","l1p4.Eta()")\
                    .Define("l2eta","l2p4.Eta()")\
                    .Define("l1_ID","if(ttc_Flag) return ttc_l1_id;else return OPS_l1_id;")\
                    .Define("l2_ID","if(ttc_Flag) return ttc_l2_id;else return OPS_l2_id;")\
                    .Define("l1_abseta","abs(l1eta)")\
                    .Define("l2_abseta","abs(l2eta)")




        if self.__channel =='ElectronMuon':

            df_region_trig = df_region_trig.Define("RECO_SFs","RECO_Muon_SF(h_RECOSF,l1pt,l1eta) * Electron_RECO_SF[l2_ID]")\
                    .Define("IDsf","Muon_IDSF(h1_IDSF,l1pt,l1eta) * Electron_IDSF(h2_IDSF,l2pt,l2eta)")
        elif self.__channel == 'DoubleElectron':

            df_region_trig = df_region_trig.Define("RECO_SFs","Electron_RECO_SF[l1_ID]*Electron_RECO_SF[l2_ID]")\
                    .Define("IDsf","Electron_IDSF(h1_IDSF,l1pt,l1eta) * Electron_IDSF(h2_IDSF,l2pt,l2eta)")
        else:
            df_region_trig = df_region_trig.Define("RECO_SFs","RECO_Muon_SF(h_RECOSF,l1pt,l1eta) * RECO_Muon_SF(h_RECOSF,l2pt,l2eta)")\
                    .Define("IDsf","Muon_IDSF(h1_IDSF,l1pt,l1eta) * Muon_IDSF(h2_IDSF,l2pt,l2eta)")


        if self.__Type=='Data':

            MET = 'MET_T1_pt'
        else:
            MET = 'MET_T1Smear_pt'
        df_Offline_Selection = df_region_trig\
            .Define("met",f"{MET}")\
            .Filter('(l1p4+l2p4).M() >=20 && (l1pt >= 30 || l2pt >= 20) && TMath::Abs(l1p4.DeltaR(l2p4)) >= 0.3 && met >=100 && nHad_tau == 0 ')\
            .Define('no_HLT','0.5')

        if self.__Type == 'Data':
            df_Offline_Selection = df_Offline_Selection\
                    .Define("weight",'1.')
        #self.__Condition_Weights -> puWeight * PrefireWeight for UL2017 / PrefireWeight for UL2018
        #RECOWeight_LEP_OPS -> Ele_RECO_SF[l1_id] * Ele_RECO_SF[l2_id] for double electron, 1 for double muon, Ele_RECO_SF[l2_id] for emu.
        else:
            df_Offline_Selection = df_Offline_Selection.\
                    Define("weight",f'{self.__Condition_Weights}*RECO_SFs*genWeight/abs(genWeight)*IDsf')
                   # else if(ttc_Flag) return {self.__Condition_Weights}*{RECOWeight_LEP_TTC}*IDsf*genWeight/abs(genWeight);\
                   # else if(OPS_Flag) return {self.__Condition_Weights}*IDsf*{RECOWeight_LEP_OPS}*genWeight/abs(genWeight);')
            #df_Offline_Selection = df_Offline_Selection.Define("weight",'1.')
        #print('High-Level Trigger For DiLepton Channel: '+' || '.join(self.__HLT_LEP)+'\n') 
        df_HLT_LEP = df_Offline_Selection\
                .Filter(LEP_Triggers(self.__HLT_LEP_slcRun_List,self.__Type,True))\
                .Define('HLT_LEP_pass','0.5')
        print('High-Level Trigger For MET: '+' || '.join(self.__HLT_MET)+'\n')
        df_HLT_MET = df_Offline_Selection\
                .Filter(" || ".join(self.__HLT_MET))\
                .Define('HLT_MET_pass','0.5')
        df_HLT_MET_highjet = df_HLT_MET\
                .Filter('n_tight_jet >=3','pre_high_jet')
        df_HLT_MET_lowjet = df_HLT_MET\
                .Filter('n_tight_jet <3','pre_low_jet')
        df_HLT_MET_highpv = df_HLT_MET\
                .Filter('PV_npvs >=30','pre_high_pv')
        df_HLT_MET_lowpv = df_HLT_MET\
                .Filter('PV_npvs <30','pre_low_pv')
        df_HLT_MET_highmet = df_HLT_MET\
                .Filter('met >=150','pre_high_met')
        df_HLT_MET_lowmet = df_HLT_MET\
                .Filter('met <150','pre_low_met')
        df_HLT_LEPMET = df_HLT_MET\
                .Filter(LEP_Triggers(self.__HLT_LEP_slcRun_List,self.__Type))\
                .Define('HLT_LEPMET_pass','0.5')
        df_HLT_LEPMET_highjet = df_HLT_LEPMET\
                .Filter('n_tight_jet >=3','high_jet')
        df_HLT_LEPMET_lowjet = df_HLT_LEPMET\
                .Filter('n_tight_jet <3','low_jet')
        df_HLT_LEPMET_highpv = df_HLT_LEPMET\
                .Filter('PV_npvs >=30','high_pv')
        df_HLT_LEPMET_lowpv = df_HLT_LEPMET\
                .Filter('PV_npvs <30','low_pv')
        df_HLT_LEPMET_highmet = df_HLT_LEPMET\
                .Filter('met >=150','high_met')
        df_HLT_LEPMET_lowmet = df_HLT_LEPMET\
                .Filter('met <150','low_met')
        weight_all = df_Offline_Selection.Sum("weight")
        weight_lep = df_HLT_LEP.Sum("weight")
        weight_met = df_HLT_MET.Sum("weight")
        weight_lepmet = df_HLT_LEPMET.Sum("weight")
        test_1 = df_HLT_LEPMET_lowmet.Sum("weight")
        test_2 = df_HLT_LEPMET_highmet.Sum("weight")
        test_3 = df_HLT_LEPMET_lowpv.Sum("weight")
        test_4 = df_HLT_LEPMET_highpv.Sum("weight")
        if not self.__debug:

            self.__Histogram['1D']['HLT']['No_HLT'] = df_Offline_Selection.Histo1D(("No_HLT","No_HLT",1,0,1),"no_HLT","weight").GetValue()
            self.__Histogram['1D']['HLT']['HLT_LEP'] = df_HLT_LEP.Histo1D(("HLT_LEP_pass","HLT_LEP_pass",1,0,1),"HLT_LEP_pass","weight").GetValue()
            self.__Histogram['1D']['HLT']['HLT_MET'] = df_HLT_MET.Histo1D(("HLT_MET_pass","HLT_MET_pass",1,0,1),"HLT_MET_pass","weight").GetValue()
            self.__Histogram['1D']['HLT']['HLT_LEPMET'] = df_HLT_LEPMET.Histo1D(("HLT_LEPMET_pass","HLT_LEPMET_pass",1,0,1),"HLT_LEPMET_pass","weight").GetValue()
            
            ###1D Histogram
        
            ##PT
            self.Init_Histogram(name='pre_l1pt',df=df_HLT_MET,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            self.Init_Histogram(name='pre_l1pt_lowjet',df=df_HLT_MET_lowjet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            self.Init_Histogram(name='pre_l1pt_highjet',df=df_HLT_MET_highjet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            self.Init_Histogram(name='pre_l1pt_lowpv',df=df_HLT_MET_lowpv,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            self.Init_Histogram(name='pre_l1pt_highpv',df=df_HLT_MET_highpv,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            self.Init_Histogram(name='pre_l1pt_lowmet',df=df_HLT_MET_lowmet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            self.Init_Histogram(name='pre_l1pt_highmet',df=df_HLT_MET_highmet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            
            self.Init_Histogram(name='l1pt',df=df_HLT_LEPMET,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            self.Init_Histogram(name='l1pt_lowjet',df=df_HLT_LEPMET_lowjet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            self.Init_Histogram(name='l1pt_highjet',df=df_HLT_LEPMET_highjet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            self.Init_Histogram(name='l1pt_lowpv',df=df_HLT_LEPMET_lowpv,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            self.Init_Histogram(name='l1pt_highpv',df=df_HLT_LEPMET_highpv,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            self.Init_Histogram(name='l1pt_lowmet',df=df_HLT_LEPMET_lowmet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            self.Init_Histogram(name='l1pt_highmet',df=df_HLT_LEPMET_highmet,dim='1D',xtitle='Leading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l1pt'],lep_type='l1')
            
            
            self.Init_Histogram(name='pre_l2pt',df=df_HLT_MET,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            self.Init_Histogram(name='pre_l2pt_lowjet',df=df_HLT_MET_lowjet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            self.Init_Histogram(name='pre_l2pt_highjet',df=df_HLT_MET_highjet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            self.Init_Histogram(name='pre_l2pt_lowpv',df=df_HLT_MET_lowpv,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            self.Init_Histogram(name='pre_l2pt_highpv',df=df_HLT_MET_highpv,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            self.Init_Histogram(name='pre_l2pt_lowmet',df=df_HLT_MET_lowmet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            self.Init_Histogram(name='pre_l2pt_highmet',df=df_HLT_MET_highmet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            
            self.Init_Histogram(name='l2pt',df=df_HLT_LEPMET,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            self.Init_Histogram(name='l2pt_lowjet',df=df_HLT_LEPMET_lowjet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            self.Init_Histogram(name='l2pt_highjet',df=df_HLT_LEPMET_highjet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            self.Init_Histogram(name='l2pt_lowpv',df=df_HLT_LEPMET_lowpv,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            self.Init_Histogram(name='l2pt_highpv',df=df_HLT_LEPMET_highpv,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            self.Init_Histogram(name='l2pt_lowmet',df=df_HLT_LEPMET_lowmet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            self.Init_Histogram(name='l2pt_highmet',df=df_HLT_LEPMET_highmet,dim='1D',xtitle='Subleading Lepton P_{T} [GeV]',ytitle='Efficiency',tag = 'pt',content=['l2pt'],lep_type='l2')
            
            ##ETA
            self.Init_Histogram(name='pre_l1eta',df=df_HLT_MET,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            self.Init_Histogram(name='pre_l1eta_lowjet',df=df_HLT_MET_lowjet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            self.Init_Histogram(name='pre_l1eta_highjet',df=df_HLT_MET_highjet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            self.Init_Histogram(name='pre_l1eta_lowpv',df=df_HLT_MET_lowpv,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            self.Init_Histogram(name='pre_l1eta_highpv',df=df_HLT_MET_highpv,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            self.Init_Histogram(name='pre_l1eta_lowmet',df=df_HLT_MET_lowmet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            self.Init_Histogram(name='pre_l1eta_highmet',df=df_HLT_MET_highmet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            
            self.Init_Histogram(name='l1eta',df=df_HLT_LEPMET,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            self.Init_Histogram(name='l1eta_lowjet',df=df_HLT_LEPMET_lowjet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            self.Init_Histogram(name='l1eta_highjet',df=df_HLT_LEPMET_highjet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            self.Init_Histogram(name='l1eta_lowpv',df=df_HLT_LEPMET_lowpv,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            self.Init_Histogram(name='l1eta_highpv',df=df_HLT_LEPMET_highpv,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            self.Init_Histogram(name='l1eta_lowmet',df=df_HLT_LEPMET_lowmet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            self.Init_Histogram(name='l1eta_highmet',df=df_HLT_LEPMET_highmet,dim='1D',xtitle='Leading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l1eta'])
            
            
            self.Init_Histogram(name='pre_l2eta',df=df_HLT_MET,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            self.Init_Histogram(name='pre_l2eta_lowjet',df=df_HLT_MET_lowjet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            self.Init_Histogram(name='pre_l2eta_highjet',df=df_HLT_MET_highjet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            self.Init_Histogram(name='pre_l2eta_lowpv',df=df_HLT_MET_lowpv,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            self.Init_Histogram(name='pre_l2eta_highpv',df=df_HLT_MET_highpv,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            self.Init_Histogram(name='pre_l2eta_lowmet',df=df_HLT_MET_lowmet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            self.Init_Histogram(name='pre_l2eta_highmet',df=df_HLT_MET_highmet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            
            self.Init_Histogram(name='l2eta',df=df_HLT_LEPMET,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            self.Init_Histogram(name='l2eta_lowjet',df=df_HLT_LEPMET_lowjet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            self.Init_Histogram(name='l2eta_highjet',df=df_HLT_LEPMET_highjet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            self.Init_Histogram(name='l2eta_lowpv',df=df_HLT_LEPMET_lowpv,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            self.Init_Histogram(name='l2eta_highpv',df=df_HLT_LEPMET_highpv,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            self.Init_Histogram(name='l2eta_lowmet',df=df_HLT_LEPMET_lowmet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            self.Init_Histogram(name='l2eta_highmet',df=df_HLT_LEPMET_highmet,dim='1D',xtitle='Subleading Lepton #eta',ytitle='Efficiency',tag = 'eta',content=['l2eta'])
            
            ##others
            self.Init_Histogram(name='pre_njet',df=df_HLT_MET,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
            self.Init_Histogram(name='pre_njet_lowmet',df=df_HLT_MET_lowmet,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
            self.Init_Histogram(name='pre_njet_highmet',df=df_HLT_MET_highmet,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
            self.Init_Histogram(name='pre_njet_lowpv',df=df_HLT_MET_lowpv,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
            self.Init_Histogram(name='pre_njet_highpv',df=df_HLT_MET_highpv,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
            
            self.Init_Histogram(name='njet',df=df_HLT_LEPMET,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
            self.Init_Histogram(name='njet_lowmet',df=df_HLT_LEPMET_lowmet,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
            self.Init_Histogram(name='njet_highmet',df=df_HLT_LEPMET_highmet,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
            self.Init_Histogram(name='njet_lowpv',df=df_HLT_LEPMET_lowpv,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
            self.Init_Histogram(name='njet_highpv',df=df_HLT_LEPMET_highpv,dim='1D',xtitle='N_{jets}',ytitle='Efficiency',tag = 'njet',content=['n_tight_jet'])
            
            self.Init_Histogram(name='pre_met',df=df_HLT_MET,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
            self.Init_Histogram(name='pre_met_lowjet',df=df_HLT_MET_lowjet,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
            self.Init_Histogram(name='pre_met_highjet',df=df_HLT_MET_highjet,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
            self.Init_Histogram(name='pre_met_lowpv',df=df_HLT_MET_lowpv,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
            self.Init_Histogram(name='pre_met_highpv',df=df_HLT_MET_highpv,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
            
            self.Init_Histogram(name='met',df=df_HLT_LEPMET,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
            self.Init_Histogram(name='met_lowjet',df=df_HLT_LEPMET_lowjet,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
            self.Init_Histogram(name='met_highjet',df=df_HLT_LEPMET_highjet,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
            self.Init_Histogram(name='met_lowpv',df=df_HLT_LEPMET_lowpv,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
            self.Init_Histogram(name='met_highpv',df=df_HLT_LEPMET_highpv,dim='1D',xtitle='MET [GeV]',ytitle='Efficiency',tag = 'met',content=['met'])
            
            ###2D Histogram
            self.Init_Histogram(name='pre_l1l2pt',df=df_HLT_MET,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            self.Init_Histogram(name='pre_l1l2pt_lowjet',df=df_HLT_MET_lowjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            self.Init_Histogram(name='pre_l1l2pt_highjet',df=df_HLT_MET_highjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            self.Init_Histogram(name='pre_l1l2pt_lowpv',df=df_HLT_MET_lowpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            self.Init_Histogram(name='pre_l1l2pt_highpv',df=df_HLT_MET_highpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            self.Init_Histogram(name='pre_l1l2pt_lowmet',df=df_HLT_MET_lowmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            self.Init_Histogram(name='pre_l1l2pt_highmet',df=df_HLT_MET_highmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            
            self.Init_Histogram(name='pre_l1l2eta',df=df_HLT_MET,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1eta','l2eta'])
            self.Init_Histogram(name='pre_l1l2eta_lowjet',df=df_HLT_MET_lowjet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
            self.Init_Histogram(name='pre_l1l2eta_highjet',df=df_HLT_MET_highjet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
            self.Init_Histogram(name='pre_l1l2eta_lowpv',df=df_HLT_MET_lowpv,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
            self.Init_Histogram(name='pre_l1l2eta_highpv',df=df_HLT_MET_highpv,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
            self.Init_Histogram(name='pre_l1l2eta_lowmet',df=df_HLT_MET_lowmet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
            self.Init_Histogram(name='pre_l1l2eta_highmet',df=df_HLT_MET_highmet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
            
            self.Init_Histogram(name='pre_l1pteta',df=df_HLT_MET,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            self.Init_Histogram(name='pre_l1pteta_lowjet',df=df_HLT_MET_lowjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            self.Init_Histogram(name='pre_l1pteta_highjet',df=df_HLT_MET_highjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            self.Init_Histogram(name='pre_l1pteta_lowpv',df=df_HLT_MET_lowpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            self.Init_Histogram(name='pre_l1pteta_highpv',df=df_HLT_MET_highpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            self.Init_Histogram(name='pre_l1pteta_lowmet',df=df_HLT_MET_lowmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            self.Init_Histogram(name='pre_l1pteta_highmet',df=df_HLT_MET_highmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            
            self.Init_Histogram(name='pre_l2pteta',df=df_HLT_MET,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            self.Init_Histogram(name='pre_l2pteta_lowjet',df=df_HLT_MET_lowjet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            self.Init_Histogram(name='pre_l2pteta_highjet',df=df_HLT_MET_highjet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            self.Init_Histogram(name='pre_l2pteta_lowpv',df=df_HLT_MET_lowpv,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            self.Init_Histogram(name='pre_l2pteta_highpv',df=df_HLT_MET_highpv,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            self.Init_Histogram(name='pre_l2pteta_lowmet',df=df_HLT_MET_lowmet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            self.Init_Histogram(name='pre_l2pteta_highmet',df=df_HLT_MET_highmet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            #After LEPMET
            self.Init_Histogram(name='l1l2pt',df=df_HLT_LEPMET,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            self.Init_Histogram(name='l1l2pt_lowjet',df=df_HLT_LEPMET_lowjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            self.Init_Histogram(name='l1l2pt_highjet',df=df_HLT_LEPMET_highjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            self.Init_Histogram(name='l1l2pt_lowpv',df=df_HLT_LEPMET_lowpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            self.Init_Histogram(name='l1l2pt_highpv',df=df_HLT_LEPMET_highpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            self.Init_Histogram(name='l1l2pt_lowmet',df=df_HLT_LEPMET_lowmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            self.Init_Histogram(name='l1l2pt_highmet',df=df_HLT_LEPMET_highmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Subleading lepton P_{T} [GeV]',tag = 'pt',content=['l1pt','l2pt'])
            
            self.Init_Histogram(name='l1l2eta',df=df_HLT_LEPMET,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1eta','l2eta'])
            self.Init_Histogram(name='l1l2eta_lowjet',df=df_HLT_LEPMET_lowjet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
            self.Init_Histogram(name='l1l2eta_highjet',df=df_HLT_LEPMET_highjet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
            self.Init_Histogram(name='l1l2eta_lowpv',df=df_HLT_LEPMET_lowpv,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
            self.Init_Histogram(name='l1l2eta_highpv',df=df_HLT_LEPMET_highpv,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
            self.Init_Histogram(name='l1l2eta_lowmet',df=df_HLT_LEPMET_lowmet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
            self.Init_Histogram(name='l1l2eta_highmet',df=df_HLT_LEPMET_highmet,dim='2D',xtitle='Leading lepton #eta',ytitle='Subleading lepton #eta',tag = 'eta',content=['l1_abseta','l2_abseta'])
            
            self.Init_Histogram(name='l1pteta',df=df_HLT_LEPMET,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            self.Init_Histogram(name='l1pteta_lowjet',df=df_HLT_LEPMET_lowjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            self.Init_Histogram(name='l1pteta_highjet',df=df_HLT_LEPMET_highjet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            self.Init_Histogram(name='l1pteta_lowpv',df=df_HLT_LEPMET_lowpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            self.Init_Histogram(name='l1pteta_highpv',df=df_HLT_LEPMET_highpv,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            self.Init_Histogram(name='l1pteta_lowmet',df=df_HLT_LEPMET_lowmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            self.Init_Histogram(name='l1pteta_highmet',df=df_HLT_LEPMET_highmet,dim='2D',xtitle='Leading lepton P_{T} [GeV]',ytitle='Leading lepton #eta',tag = 'pteta',content=['l1pt','l1_abseta'],lep_type='l1')
            
            self.Init_Histogram(name='l2pteta',df=df_HLT_LEPMET,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            self.Init_Histogram(name='l2pteta_lowjet',df=df_HLT_LEPMET_lowjet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            self.Init_Histogram(name='l2pteta_highjet',df=df_HLT_LEPMET_highjet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            self.Init_Histogram(name='l2pteta_lowpv',df=df_HLT_LEPMET_lowpv,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            self.Init_Histogram(name='l2pteta_highpv',df=df_HLT_LEPMET_highpv,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            self.Init_Histogram(name='l2pteta_lowmet',df=df_HLT_LEPMET_lowmet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
            self.Init_Histogram(name='l2pteta_highmet',df=df_HLT_LEPMET_highmet,dim='2D',xtitle='Subleading lepton P_{T} [GeV]',ytitle='Subleading lepton #eta',tag = 'pteta',content=['l2pt','l2_abseta'],lep_type='l2')
def Data_Processor(trig_dfs:dict,DirOut:str,Type:str,veto:bool):
    
    if veto:
        FileOutName = os.path.join(DirOut,f'EfficiencyFor{Type}_vetoHEM.root')
    else:
        FileOutName = os.path.join(DirOut,f'EfficiencyFor{Type}.root')
    FileOut = TFile.Open(FileOutName,"RECREATE") 

    FileOut.cd()
    print('Histogramming now...') 
    for name in ['l1pt','l1pt_highjet','l1pt_lowjet','l1pt_lowmet','l1pt_highmet','l1pt_lowpv','l1pt_highpv'\
            ,'l2pt','l2pt_highjet','l2pt_lowjet','l2pt_lowmet','l2pt_highmet','l2pt_lowpv','l2pt_highpv']:
        h = dict()
        for idx,era in  enumerate(trig_dfs.keys()):
            if idx ==0:
                h['1'] = trig_dfs[era].Histogram['1D']['pt'][name].Clone()
                h['2'] = trig_dfs[era].Histogram['1D']['pt']['pre_'+name].Clone()
            else:
                h['1'].Add(trig_dfs[era].Histogram['1D']['pt'][name].Clone())
                h['2'].Add(trig_dfs[era].Histogram['1D']['pt']['pre_'+name].Clone())
        Merge_Hist(h['1'],h['2'],dim='1D',title=name) 
    for name in ['l1eta','l1eta_highjet','l1eta_lowjet','l1eta_lowmet','l1eta_highmet','l1eta_lowpv','l1eta_highpv'\
            ,'l2eta','l2eta_highjet','l2eta_lowjet','l2eta_lowmet','l2eta_highmet','l2eta_lowpv','l2eta_highpv']:
        h = dict()
        for idx,era in  enumerate(trig_dfs.keys()):
            if idx ==0:
                h['1'] = trig_dfs[era].Histogram['1D']['eta'][name].Clone()
                h['2'] = trig_dfs[era].Histogram['1D']['eta']['pre_'+name].Clone()
            else:
                h['1'].Add(trig_dfs[era].Histogram['1D']['eta'][name].Clone())
                h['2'].Add(trig_dfs[era].Histogram['1D']['eta']['pre_'+name].Clone())
        Merge_Hist(h['1'],h['2'],dim='1D',title=name) 
    for name in ['l1pteta','l1pteta_highjet','l1pteta_lowjet','l1pteta_lowmet','l1pteta_highmet','l1pteta_lowpv','l1pteta_highpv'\
            ,'l2pteta','l2pteta_highjet','l2pteta_lowjet','l2pteta_lowmet','l2pteta_highmet','l2pteta_lowpv','l2pteta_highpv']:
        h = dict()
        for idx,era in  enumerate(trig_dfs.keys()):
            if idx ==0:
                h['1'] = trig_dfs[era].Histogram['2D']['pteta'][name].Clone()
                h['2'] = trig_dfs[era].Histogram['2D']['pteta']['pre_'+name].Clone()
            else:
                h['1'].Add(trig_dfs[era].Histogram['2D']['pteta'][name].Clone())
                h['2'].Add(trig_dfs[era].Histogram['2D']['pteta']['pre_'+name].Clone())
        Merge_Hist(h['1'],h['2'],dim='2D',title=name) 
    for name in ['l1l2pt','l1l2pt_highjet','l1l2pt_lowjet','l1l2pt_lowmet','l1l2pt_highmet','l1l2pt_lowpv','l1l2pt_highpv']:
        h = dict()
        for idx,era in  enumerate(trig_dfs.keys()):
            if idx ==0:
                h['1'] = trig_dfs[era].Histogram['2D']['pt'][name].Clone()
                h['2'] = trig_dfs[era].Histogram['2D']['pt']['pre_'+name].Clone()
            else:
                h['1'].Add(trig_dfs[era].Histogram['2D']['pt'][name].Clone())
                h['2'].Add(trig_dfs[era].Histogram['2D']['pt']['pre_'+name].Clone())
        Merge_Hist(h['1'],h['2'],dim='2D',title=name) 

    for name in ['l1l2eta','l1l2eta_highjet','l1l2eta_lowjet','l1l2eta_lowmet','l1l2eta_highmet','l1l2eta_lowpv','l1l2eta_highpv']:
        h = dict()
        for idx,era in  enumerate(trig_dfs.keys()):
            if idx ==0:
                h['1'] = trig_dfs[era].Histogram['2D']['eta'][name].Clone()
                h['2'] = trig_dfs[era].Histogram['2D']['eta']['pre_'+name].Clone()
            else:
                h['1'].Add(trig_dfs[era].Histogram['2D']['eta'][name].Clone())
                h['2'].Add(trig_dfs[era].Histogram['2D']['eta']['pre_'+name].Clone())
        Merge_Hist(h['1'],h['2'],dim='2D',title=name) 
    for name in ['HLT_MET','HLT_LEP','HLT_LEPMET']:
        h = dict()
        for idx,era in  enumerate(trig_dfs.keys()):
            if idx ==0:
                h['1'] = trig_dfs[era].Histogram['1D']['HLT'][name].Clone()
                h['2'] = trig_dfs[era].Histogram['1D']['HLT']['No_HLT'].Clone()
            else:
                h['1'].Add(trig_dfs[era].Histogram['1D']['HLT'][name].Clone())
                h['2'].Add(trig_dfs[era].Histogram['1D']['HLT']['No_HLT'].Clone())
        Merge_Hist(h['1'],h['2'],dim='1D',title=name) 
    h = dict()
    for idx,era in enumerate(trig_dfs.keys()):
        if idx ==0:
            h['1'] = trig_dfs[era].Histogram['1D']['HLT']['HLT_LEPMET'].Clone()
            h['2'] = trig_dfs[era].Histogram['1D']['HLT']['HLT_MET'].Clone()
        else:
            h['1'].Add(trig_dfs[era].Histogram['1D']['HLT']['HLT_LEPMET'].Clone())
            h['2'].Add(trig_dfs[era].Histogram['1D']['HLT']['HLT_MET'].Clone())
    Merge_Hist(h['1'],h['2'],dim='1D',title='Integrated') 
    FileOut.Close()
    print(f'You could see Efficiency of {Type}: {FileOutName}')
def Merge_Hist(Hist1,Hist2,dim:str,title='default'):
    if dim == '1D':
        eff = TEfficiency(Hist1,Hist2)
        eff.SetTitle(f'Eff {title}')
        eff.SetName(f'Eff_{title}')
        eff.Write()
    elif dim == '2D':
        Hist1.Divide(Hist2)
        Hist1.Write()
    else:
        raise ValueError('Dimension {dim} is not in the list.')

