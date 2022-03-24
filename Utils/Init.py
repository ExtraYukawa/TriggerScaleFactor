import os,sys 
import json
import fnmatch 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from Utils.General_Tool import get_NumberOfEvent


def GenPaths_HLTTrigger_File(year:str):
    '''
    
    Build JSON file to record trigger conditions for Each particular channels.
    
    '''
    trigger = dict()
    if year=='2017' or year=='2018':
    
        trigger['DoubleElectron'] = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_passEle32WPTight", "HLT_Ele35_WPTight_Gsf"]
        trigger['DoubleMuon'] = ["HLT_IsoMu27", "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"]
        trigger["ElectronMuon"] = ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_IsoMu27", "HLT_passEle32WPTight", "HLT_passEle32WPTight"]
        trigger['MET'] = ["HLT_PFMET120_PFMHT120_IDTight", "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight", "HLT_PFHT500_PFMET100_PFMHT100_IDTight", "HLT_PFHT700_PFMET85_PFMHT85_IDTight", "HLT_PFHT800_PFMET75_PFMHT75_IDTight"]

    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/configuration/HLTTrigger.json','w')  as f:
        json.dump(trigger,f,indent=4)

def GenPaths_HLTTriggerCondition_ForAnalyzer_File(year:str):
    '''
    
    Build JSON file to record trigger conditions for Each particular channels used in Analyzer condition.
    
    '''

    trigger =dict()

    if year=='2017' or year=='2018':
        trigger['All'] = 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf'

        trigger['DoubleElectron'] =dict()

        trigger['DoubleElectron']['DoubleElectron'] = 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'
        trigger['DoubleElectron']['SingleElectron'] = '!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)'

        trigger['DoubleMuon'] = dict()
        trigger['DoubleMuon']['DoubleMuon'] = '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8)'
        trigger['DoubleMuon']['SingleMuon'] = '!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8) && HLT_IsoMu27'

        trigger['ElectronMuon'] = dict()
        trigger['ElectronMuon']['SingleElectron'] = '!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)'
        trigger['ElectronMuon']['SingleMuon'] = '!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && HLT_IsoMu27'
        trigger['ElectronMuon']['ElectronMuon'] = '(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)'
    
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/configuration/HLTTriggerCondition.json','wt')  as f:
        json.dump(trigger,f,indent=4)


def GenTrigEffInput_File(year:str):
    '''
    
    Build JSON file to record Input path for TriggerEfficiency Calculation Stage.
    
    '''
    if year=='2017' :
        path = {
                "Data":['/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METB.root'
                    ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METC.root'
                    ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METD.root'
                    ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METE.root'
                    ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METF.root'],
                "MC":['/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/TTTo2L.root']
                }
    elif year=='2018':
        path = {
                "Data":['/eos/cms/store/group/phys_top/ExtraYukawa/2018/MET_A.root',
                    '/eos/cms/store/group/phys_top/ExtraYukawa/2018/MET_B.root',
                    '/eos/cms/store/group/phys_top/ExtraYukawa/2018/MET_C.root',
                    '/eos/cms/store/group/phys_top/ExtraYukawa/2018/MET_D_0.root',
                    '/eos/cms/store/group/phys_top/ExtraYukawa/2018/MET_D_1.root'
                    ],
                "MC":['/eos/cms/store/group/phys_top/ExtraYukawa/2018/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root']
                
                }
    
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/path/filein.json','w') as f:
        json.dump(path,f,indent=4)

def GenMCWeightsName_File(year:str):
    if year == '2017':
        weights={
                'Data':'1.',
                'MC':['puWeight','PrefireWeight']
                }
    elif year =='2018':
        weights={
                'Data':'1.',
                'MC':['puWeight']
                }
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/configuration/weights.json','w') as f:
        json.dump(weights,f,indent=4)


def GenLeptonIDSF_File(year:str):
    if year=='2017' or year == '2018':
        path = {
                'DoubleElectron':{ 
                    'path':f'/afs/cern.ch/user/m/melu/public/eleIDSF_{year}.root',
                        'name':'EleIDDataEff'},
                'DoubleMuon':{
                    'path':f'/eos/user/t/tihsu/share/muonID_SF/{year}UL/muonIdSF_{year}UL.root',
                    'name':'muIdSF'
                    },
                'ElectronMuon':{
                    'path':{
                        'Muon':f'/eos/user/t/tihsu/share/muonID_SF/{year}UL/muonIdSF_{year}UL.root',
                        'Electron':f'/afs/cern.ch/user/m/melu/public/eleIDSF_{year}.root'
                    },
                    'name':{
                        'Muon':'muIdSF',
                        'Electron':'EleIDDataEff'
                        }

                    }
        }
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/path/LeptonsID_SF.json','w') as f:
        json.dump(path,f,indent=4)



def GenVariableNames_File(year:str):
    '''
    
    Build JSON file to record Variable names.
    
    '''
    channels = ['DoubleElectron','DoubleMuon','ElectronMuon']

    property_name = dict()
    if year=='2017' or year =='2018':

        for channel in channels:
            property_name[channel] = dict()

        property_name['DoubleElectron']['region']=3
        property_name['DoubleElectron']['weight'] = {'l1':'Electron_RECO_SF','l2':'Electron_RECO_SF'}

        property_name['DoubleElectron']['OPS_p4'] = {'l1':['OPS_l1_pt','OPS_l1_eta','OPS_l1_phi','OPS_l1_mass'],'l2':['OPS_l2_pt','OPS_l2_eta','OPS_l2_phi','OPS_l2_mass']}

        property_name['DoubleMuon']['region']=1
        property_name['DoubleMuon']['weight'] = {'l1':None,'l2':None}
        property_name['DoubleMuon']['OPS_p4'] = {'l1':['OPS_l1_pt','OPS_l1_eta','OPS_l1_phi','OPS_l1_mass'],'l2':['OPS_l2_pt','OPS_l2_eta','OPS_l2_phi','OPS_l2_mass']}


        property_name['ElectronMuon']['region']=2
        property_name['ElectronMuon']['weight'] = {'l1':None,'l2':['Electron_RECO_SF']}
        property_name['ElectronMuon']['OPS_p4'] = {'l1':['Muon_corrected_pt','Muon_eta','Muon_phi','Muon_mass'],'l2':['Electron_pt','Electron_eta','Electron_phi','Electron_mass']}


        for channel in channels:
            property_name[channel]['ttc_p4'] = {'l1':['ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass'],'l2':['ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass']}

    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/configuration/name.json','wt') as f:
        json.dump(property_name, f,indent=4)

def GenGoodFlag_File(year:str):
    '''
    Build Json file which contents Flag Name.
    '''
    if year=='2017' or year == '2018':

        Flags = ['Flag_goodVertices','Flag_globalSuperTightHalo2016Filter', 'Flag_HBHENoiseFilter', 'Flag_HBHENoiseIsoFilter', 'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_BadPFMuonFilter', 'Flag_eeBadScFilter', 'Flag_ecalBadCalibFilter']
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/configuration/flag.json','wt') as f :
        json.dump(Flags,f,indent=4)


