import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import ROOT,json

from Drell_Yan.DY_Analyzer import *


def Drell_Yan_Reconstruction(year:str,channel:str,nevents:int,trig_SF_on:bool):
    if year is None:
        raise ValueError('Arguments [year] must be speicified.')
    settings = dict()
    settings['year'] = year
    settings['channel'] = channel
    settings['nevents'] = nevents
    settings['trig_SF_on']  = trig_SF_on
    
    with open(f'./data/year{year}/DrellYan/configuration/HLTTriggerCondition.json','rb') as f:
        settings['HLT_Path'] = json.load(f)
    with open(f'./data/year{year}/DrellYan/configuration/data_xs.json','rb') as f:
        structure = json.load(f)
        settings['xs'] = structure['xs']
        settings['NumberOfEvents'] = structure['NumberOfEvents']     
    with open(f'./data/year{year}/DrellYan/path/datapath.json','rb') as f :
        settings['FilesIn'] = json.load(f)
    

    with open(f'./data/year{year}/DrellYan/path/triggerSF.json','rb') as f:
        settings['TriggerSF'] = json.load(f)


    Analyzer = DrellYanRDataFrame(settings)
    Analyzer.Run()
