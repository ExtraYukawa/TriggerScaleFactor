import json
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from Utils.General_Tool import get_NumberOfEvent,getNumberofEventsInDataSet

import ROOT

def CalculateVetoRatio(year:str):

    if year == '2018':
        
        with open('./data/year2018/DrellYan/path/datapath.json','r') as f:
            Data = json.load(f)['Data']

        TotalEvents = dict()
        
        #TotalEvents['DoubleElectron']['EGamma'] = get_NumberOfEvent(Data = json.load(f)['Data']['DoubleElectron']['EGamma']) 
        #getNumberofEventsInDataSet(Data['DoubleElectron']['EGamma'])


#CalculateVetoRatio('2018')
def veto_Prob(File_List:list):
    veto_func = 'valid_region_hem(run)'
    FileIn_vecstr= ROOT.std.vector('string')()
    for f in File_List:
        FileIn_vecstr.push_back(f)

    df = ROOT.RDataFrame("Events",FileIn_vecstr)

    df = df.Define('Count','1')
    df_total = df
    df_veto_hem = df.Define('Veto_hem',veto_func).Filter('Veto_hem')

    c_veto_hem = df_veto_hem.Sum('Count')
    c_total = df_total.Sum('Count')
    prob = c_veto_hem.GetValue() / c_total.GetValue()
    return prob
def TestRatio(year:str):
    '''
    Calculate the probability for events pass MET filters that also pass veto HEM region
    '''
    ROOT.gInterpreter.ProcessLine('#include "./include/HEM_veto.h"')
    ROOT.gSystem.Load('./myLib/HEM_veto_cpp.so')
    prob = dict()
    File_List = dict() 
    
    #ROOT.gInterpreter.Declare('#include <time.h>;srand(12345);')
    with open(f'./data/year{year}/TriggerSF/path/filein.json','rb') as f:
        File_List['MET'] = json.load(f)['Data']
    
    #
    v = ROOT.std.vector('string')()
    for f in File_List['MET']:
        v.push_back(f)
    df = ROOT.RDataFrame("Events",v)
    df = df.Define('Count','test_prob(prob())').Define('count','1.')
    print(df.Sum('Count').GetValue()/df.Sum('count').GetValue())


def CalculateHEM_Valid_Ratio(year:str):
    '''
    Calculate the probability for events pass MET filters that also pass veto HEM region
    '''
    ROOT.gInterpreter.ProcessLine('#include "./include/HEM_veto.h"')
    ROOT.gSystem.Load('./myLib/HEM_veto_cpp.so')
    prob = dict()
    File_List = dict() 
    
    #ROOT.gInterpreter.Declare('#include <time.h>;srand(12345);')
    with open(f'./data/year{year}/TriggerSF/path/filein.json','rb') as f:
        File_List['MET'] = json.load(f)['Data']
    
    
    with open(f'./data/year{year}/DrellYan/path/datapath.json','rb') as f:
        FilesIn = json.load(f)["Data"]
    
    for channel in FilesIn.keys():
        File_List[channel] = []
        for dataset in FilesIn[channel]:
            for path in FilesIn[channel][dataset]:
                File_List[channel].append(path)
     
    for data in File_List.keys():
        prob[data] = veto_Prob(File_List[data])

    with open(f'./data/year{year}/TriggerSF/configuration/veto_prob.json','w') as f:
        json.dump(prob,f,indent=4)


def Calculate_vetoHEM_retio(year:str):
    ROOT.gInterpreter.ProcessLine('#include "./include/HEM_veto.h"')
    ROOT.gSystem.Load('./myLib/HEM_veto_cpp.so')
    prob = dict()
    File_List = dict() 
    
    #ROOT.gInterpreter.Declare('#include <time.h>;srand(12345);')
    with open(f'./data/year{year}/TriggerSF/path/filein.json','rb') as f:
        File_List['MET'] = json.load(f)['Data']
    
    
    with open(f'./data/year{year}/DrellYan/path/datapath.json','rb') as f:
        FilesIn = json.load(f)["Data"]
    veto_func = 'not_hem_event(run,Jet_phi,Jet_eta)'
    
    ratio_veto_to_total = dict()

    for channel in FilesIn.keys():
        File_List[channel] = []
        for dataset in FilesIn[channel]:
            #FileIn_vecstr= ROOT.std.vector('string')()
            for path in FilesIn[channel][dataset]:      
                File_List[channel].append(path)
                #FileIn_vecstr.push_back(path)
    
    for DATA in File_List.keys():
        FileIn_vecstr= ROOT.std.vector('string')()
        for path in File_List[DATA]:
            FileIn_vecstr.push_back(path)


        df =  ROOT.RDataFrame("Events",FileIn_vecstr).Define('Count','1').Define('Count_notveto',veto_func)
        ratio_veto_to_total[DATA] = df.Sum('Count_notveto').GetValue()/df.Sum('Count').GetValue()
    
    with open('./data/year2018/DrellYan/configuration/veto_ratio.json','w') as f:

        json.dump(ratio_veto_to_total,f,indent=4)



def Calculate_HEM_ratio(Dataset:str):
    ROOT.gInterpreter.ProcessLine('#include "./include/HEM_veto.h"')
    ROOT.gSystem.Load('./myLib/HEM_veto_cpp.so')
    eras = ["A","B","C","D_0","D_1"] 
    folder = "/eos/cms/store/group/phys_top/ExtraYukawa/2018/"
    df = dict()
    df_CD = dict() 
    if Dataset == 'MET':
        Fileout = './data/year2018/TriggerSF/configuration/MET_vetoHEM_rate.json'
    else:
        Fileout = f'./data/year2018/DrellYan/configuration/{Dataset}_vetoHEM_rate.json'
        
        
        
    total = 0
    n_CD = 0
    
    
    for era in eras:
        FileIn_vecstr= ROOT.std.vector('string')()
        print(f'{folder}/{Dataset}{era}.root')
        FileIn_vecstr.push_back(f'{folder}/{Dataset}{era}.root')
        df[era] = ROOT.RDataFrame("Events",FileIn_vecstr).Define('Count','1')
        df_CD[era]=df[era].Filter('run >319077')
        
        total += df[era].Sum('Count').GetValue()
        n_CD += df_CD[era].Sum('Count').GetValue()
        
    with open(Fileout,'w') as f:

        json.dump(n_CD/total,f,indent=4)
        
Calculate_HEM_ratio('MET')
Calculate_HEM_ratio('EGamma')  
Calculate_HEM_ratio('DoubleMuon')  
Calculate_HEM_ratio('SingleMuon')  
Calculate_HEM_ratio('MuonEG')  









#Calculate_vetoHEM_retio('2018')
