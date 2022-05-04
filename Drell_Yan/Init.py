import json
import os,sys
import ROOT
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
from Utils.General_Tool import get_NumberOfEvent



def GenTriggerSF_Path(year:str):
    with open(f'./data/year{year}/TriggerSF/User.json','r') as f:
        UserName = json.load(f)['UserName']

    path = dict()
    path['file'] =dict()
    
    path['branchname'] = dict()
    
    if year != '2018':
        path['file']['DoubleElectron']  =dict()
        path['file']['DoubleMuon'] = dict()
        path['file']['ElectronMuon'] = dict()
    
        path['file']['DoubleElectron']['l1pteta'] = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/DoubleElectron/files/SF_l1pteta.root'
        path['file']['DoubleElectron']['l2pteta'] = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/DoubleElectron/files/SF_l2pteta.root'
        path['file']['DoubleElectron']['l1l2pt'] = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/DoubleElectron/files/SF_l1l2pt.root'
        path['file']['DoubleElectron']['l1l2eta'] = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/DoubleElectron/files/SF_l1l2eta.root'

        path['file']['DoubleMuon']['l1pteta'] = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/DoubleMuon/files/SF_l1pteta.root'
        path['file']['DoubleMuon']['l2pteta'] = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/DoubleMuon/files/SF_l2pteta.root'
        path['file']['DoubleMuon']['l1l2pt'] = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/DoubleMuon/files/SF_l1l2pt.root'
        path['file']['DoubleMuon']['l1l2eta'] = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/DoubleMuon/files/SF_l1l2eta.root'
        
        path['file']['ElectronMuon']['l1pteta'] = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/ElectronMuon/files/SF_l1pteta.root'
        path['file']['ElectronMuon']['l2pteta'] = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/ElectronMuon/files/SF_l2pteta.root'
        path['file']['ElectronMuon']['l1l2pt'] = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/ElectronMuon/files/SF_l1l2pt.root'
        path['file']['ElectronMuon']['l1l2eta'] = f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/ElectronMuon/files/SF_l1l2eta.root'
    else:
        path['file']['all'] = dict()
        path['file']['veto'] = dict()
        channels = ['DoubleElectron','DoubleMuon','ElectronMuon']

        for c in ['all','veto']:
            for channel in channels :
                path['file'][c][channel] = dict()
                for l in ['l1pteta','l2pteta','l1l2pt','l1l2eta']:
                    if c =='all':
                        path['file'][c][channel][l] =  f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/{channel}/files/SF_{l}.root'
                    else:
                        path['file'][c][channel][l] =  f'/eos/user/{UserName[0]}/{UserName}/ExtraYukawa/TriggerSF/year{year}/{channel}/files/SF_{l}_vetohemregion.root'

    path['branchname']['l1pteta'] = 'l1pteta'
    path['branchname']['l2pteta'] = 'l2pteta'
    path['branchname']['l1l2pt'] = 'l1l2pt'
    path['branchname']['l1l2eta'] = 'l1l2eta'


    with open(f'./data/year{year}/DrellYan/path/triggerSF.json','wt') as f:
        json.dump(path,f,indent=4)

def GenDataPath_File(year:str):
    '''
    
    Build JSON file to record MC/Data paths.
    
    '''
    
    data_path = dict()
    data_path['Data'] = dict()
    data_path['MC'] = dict()
    
    data_path['Data']['DoubleElectron'] = dict()
    data_path['Data']['DoubleMuon'] = dict()
    data_path['Data']['ElectronMuon'] = dict()
    Dileptons_types = ['DoubleMuon','SingleMuon','DoubleElectron','SingleElectron','ElectronMuon']
    
    if year=='2017':
        data_dir = '/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/'
        post_fixs = ['B','C','D','E','F']
    elif year=='2018':
        data_dir ='/eos/cms/store/group/phys_top/ExtraYukawa/2018/'
        post_fixs = ['A','B','C','D_0','D_1'] 
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
        
    if year == '2017':
        data_path['Data']['DoubleElectron']['SingleEG'] = [os.path.join(data_dir,'SingleEG'+ postfix + '.root') for postfix in post_fixs]
        data_path['Data']['DoubleElectron']['DoubleEG'] = [os.path.join(data_dir,'DoubleEG'+ postfix + '.root') for postfix in post_fixs]
        data_path['Data']['DoubleMuon']['DoubleMuon'] = [os.path.join(data_dir,'DoubleMuon'+ postfix + '.root') for postfix in post_fixs]
        data_path['Data']['DoubleMuon']['SingleMuon'] = [os.path.join(data_dir, 'SingleMuon' + postfix + '.root') for postfix in post_fixs]
        data_path['Data']['ElectronMuon']['SingleMuon'] = [os.path.join(data_dir, 'SingleMuon'+ postfix + '.root') for postfix in post_fixs]
        data_path['Data']['ElectronMuon']['SingleEG'] = [os.path.join(data_dir,'SingleEG'+ postfix + '.root') for postfix in post_fixs]
        data_path['Data']['ElectronMuon']['MuonEG'] = [os.path.join(data_dir,'MuonEG'+ postfix + '.root') for postfix in post_fixs]
    
    elif year == '2018':

        data_path['Data']['DoubleElectron']['EGamma'] = [os.path.join(data_dir,'EGamma'+ postfix + '.root') for postfix in post_fixs]
        data_path['Data']['DoubleMuon']['DoubleMuon'] = [os.path.join(data_dir,'DoubleMuon'+ postfix + '.root') for postfix in post_fixs]
        data_path['Data']['DoubleMuon']['SingleMuon'] = [os.path.join(data_dir, 'SingleMuon' + postfix + '.root') for postfix in post_fixs]
        data_path['Data']['ElectronMuon']['SingleMuon'] = [os.path.join(data_dir, 'SingleMuon'+ postfix + '.root') for postfix in post_fixs]
        data_path['Data']['ElectronMuon']['EGamma'] = [os.path.join(data_dir,'EGamma'+ postfix + '.root') for postfix in post_fixs]
        data_path['Data']['ElectronMuon']['MuonEG'] = [os.path.join(data_dir,'MuonEG'+ postfix + '.root') for postfix in post_fixs]
    

    data_path['Process'] = ['DY','WJets','VV','VVV','SingleTop','ttXorXX','tzq','TT']
    for p in data_path['Process']:
        data_path['MC'][p] = dict()
    
    data_path['MC']['DY']['DYnlo'] = os.path.join(data_dir,'DYnlo.root')
    
    data_path['MC']['WJets']['WJets'] = os.path.join(data_dir,'WJets.root')
    
    data_path['MC']['VV']['osWW'] = os.path.join(data_dir,'osWW.root')
    data_path['MC']['VV']['ssWW'] = os.path.join(data_dir,'ssWW.root')
    data_path['MC']['VV']['WWdps'] = os.path.join(data_dir,'WWdps.root')
    data_path['MC']['VV']['ZZ'] = os.path.join(data_dir,'ZZ.root')
    data_path['MC']['VV']['ZG_ew'] = os.path.join(data_dir,'ZG_ew.root')
    
    if year == '2017':
        data_path['MC']['VV']['WZ_ew'] = os.path.join(data_dir,'WZ_ew.root')
        data_path['MC']['VV']['WZ_qcd'] = os.path.join(data_dir,'WZ_qcd.root')
    elif year == '2018':
        data_path['MC']['VV']['WZ'] = os.path.join(data_dir,'WZ.root')
    
    data_path['MC']['VVV']['WWW'] = os.path.join(data_dir,'WWW.root')
    data_path['MC']['VVV']['WWZ'] = os.path.join(data_dir,'WWZ.root')
    data_path['MC']['VVV']['WZZ'] = os.path.join(data_dir,'WZZ.root')
    data_path['MC']['VVV']['ZZZ'] = os.path.join(data_dir,'ZZZ.root')
    
    data_path['MC']['SingleTop']['tsch'] = os.path.join(data_dir,'tsch.root')
    data_path['MC']['SingleTop']['t_tch'] = os.path.join(data_dir,'t_tch.root')
    data_path['MC']['SingleTop']['tbar_tch'] = os.path.join(data_dir,'tbar_tch.root')
    data_path['MC']['SingleTop']['tW'] = os.path.join(data_dir,'tW.root')
    data_path['MC']['SingleTop']['tbarW'] = os.path.join(data_dir,'tbarW.root')
    
    data_path['MC']['ttXorXX']['ttWtoLNu'] = os.path.join(data_dir,'ttWtoLNu.root')
    data_path['MC']['ttXorXX']['ttWtoQQ'] = os.path.join(data_dir,'ttWtoQQ.root')
    data_path['MC']['ttXorXX']['ttZ'] = os.path.join(data_dir,'ttZ.root')
    data_path['MC']['ttXorXX']['ttZtoQQ'] = os.path.join(data_dir,'ttZtoQQ.root')
    data_path['MC']['ttXorXX']['ttH'] = os.path.join(data_dir,'ttH.root')
    data_path['MC']['ttXorXX']['ttWW'] = os.path.join(data_dir,'ttWW.root')
    data_path['MC']['ttXorXX']['ttWZ'] = os.path.join(data_dir,'ttWZ.root')
    data_path['MC']['ttXorXX']['ttZZ'] = os.path.join(data_dir,'ttZZ.root')
    data_path['MC']['ttXorXX']['ttWH'] = os.path.join(data_dir,'ttWH.root')
    data_path['MC']['ttXorXX']['ttZH'] = os.path.join(data_dir,'ttZH.root')
    data_path['MC']['ttXorXX']['tttJ'] = os.path.join(data_dir,'tttJ.root')
    data_path['MC']['ttXorXX']['tttW'] = os.path.join(data_dir,'tttW.root')
    data_path['MC']['ttXorXX']['tttt'] = os.path.join(data_dir,'tttt.root')
    
    data_path['MC']['tzq']['tzq'] = os.path.join(data_dir,'tzq.root')
    
    data_path['MC']['TT']['TTTo1L'] = os.path.join(data_dir,'TTTo1L.root')
    data_path['MC']['TT']['TTTo2L'] = os.path.join(data_dir,'TTTo2L.root')

        
    with open(f'./data/year{year}/DrellYan/path/datapath.json','wt') as f:
        json.dump(data_path,f,indent=4)


def GenXsValue_File(year:str):
    '''
    
    Build JSON file to record xs values for associated physics process.
    
    '''
    Event =dict()
    Event['Process'] = ['DY','WJets','VV','VVV','SingleTop','ttXorXX','tzq','TT']
    Event['xs'] = dict()
    Event['NumberOfEvents'] = dict()
    
    for p in Event['Process']:
        Event['xs'][p] = dict()
        Event['NumberOfEvents'][p] = dict()
    


    if year =='2017':
        Event['xs']['lumi'] = 41480.
        Event['xs']['VV']['WZ_ew'] = 0.0163
        Event['xs']['VV']['WZ_qcd'] = 5.213
    elif year =='2018':
        Event['xs']['lumi'] = 59740.
        Event['xs']['VV']['WZ'] =  5.2293
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    
    Event['xs']['DY']['DYnlo'] = 6077.22
    Event['xs']['WJets']['WJets'] = 61526.7
    Event['xs']['VV']['osWW'] = 11.09
    Event['xs']['VV']['ssWW'] = 0.04932
    Event['xs']['VV']['WWdps'] = 1.62

    Event['xs']['VV']['ZZ'] = 0.0086
    Event['xs']['VV']['ZG_ew'] = 0.1097
    
    Event['xs']['VVV']['WWW'] = 0.2086
    Event['xs']['VVV']['WWZ'] = 0.1707
    Event['xs']['VVV']['WZZ'] = 0.05709
    Event['xs']['VVV']['ZZZ'] = 0.01476
    
    Event['xs']['TT']['TTTo2L'] = 88.3419
    Event['xs']['TT']['TTTo1L'] = 365.4574
    
    
    Event['xs']['tzq']['tzq'] = 0.07561
    
    Event['xs']['SingleTop']['tW'] = 35.85
    Event['xs']['SingleTop']['tbarW'] = 35.85
    Event['xs']['SingleTop']['tsch'] = 3.36
    Event['xs']['SingleTop']['t_tch'] = 136.02
    Event['xs']['SingleTop']['tbar_tch'] = 80.95
    
    Event['xs']['ttXorXX']['ttWtoLNu']  = 0.1792
    Event['xs']['ttXorXX']['ttWtoQQ'] = 0.3708
    Event['xs']['ttXorXX']['ttZ'] = 0.2589
    Event['xs']['ttXorXX']['ttZtoQQ'] = 0.6012
    Event['xs']['ttXorXX']['ttH'] = 0.5269
    Event['xs']['ttXorXX']['ttWW'] = 0.007003
    Event['xs']['ttXorXX']['ttWZ'] = 0.002453
    Event['xs']['ttXorXX']['ttZZ'] = 0.001386
    Event['xs']['ttXorXX']['ttWH'] = 0.00114
    Event['xs']['ttXorXX']['ttZH'] = 0.00113
    Event['xs']['ttXorXX']['tttJ'] = 0.0004
    Event['xs']['ttXorXX']['tttW'] = 0.00073
    Event['xs']['ttXorXX']['tttt'] = 0.0082
    
        
    with open(f'./data/year{year}/DrellYan/path/datapath.json' , 'rb') as f:
        MC_Paths = json.load(f)['MC']

    
    for p in Event['Process']:
        for name in MC_Paths[p].keys():
            Event['NumberOfEvents'][p][name] = get_NumberOfEvent(MC_Paths[p][name])

    with open(f'./data/year{year}/DrellYan/configuration/data_xs.json','wt') as f:
        json.dump(Event,f,indent=4)
def GenPaths_HLTTriggerCondition_ForAnalyzer_File(year:str):
    '''
    
    Build JSON file to record trigger conditions for Each particular channels used in Analyzer condition.
    
    '''

    trigger =dict()

    if year=='2017':
        trigger['All'] = 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf'

        trigger['DoubleElectron'] =dict()
        trigger['DoubleElectron']['DoubleEG'] = 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'
        trigger['DoubleElectron']['SingleEG'] = '!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)'
        trigger['DoubleMuon'] = dict()
        trigger['DoubleMuon']['DoubleMuon'] = '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8)'
        trigger['DoubleMuon']['SingleMuon'] = '!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8) && HLT_IsoMu27'

        trigger['ElectronMuon'] = dict()
        trigger['ElectronMuon']['SingleEG'] = '!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)'
        trigger['ElectronMuon']['SingleMuon'] = '!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && HLT_IsoMu27'
        trigger['ElectronMuon']['MuonEG'] = '(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)'
    
    elif year =='2018':

        trigger['All'] = 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf'

        trigger['DoubleElectron'] =dict()

        trigger['DoubleElectron']['EGamma'] = '(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)||(!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)) '

        trigger['DoubleMuon'] = dict()
        trigger['DoubleMuon']['DoubleMuon'] = '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8)'
        trigger['DoubleMuon']['SingleMuon'] = '!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8) && HLT_IsoMu27'

        trigger['ElectronMuon'] = dict()
        trigger['ElectronMuon']['EGamma'] = '!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)'
        trigger['ElectronMuon']['SingleMuon'] = '!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && HLT_IsoMu27'
        trigger['ElectronMuon']['MuonEG'] = '(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)'

    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/DrellYan/configuration/HLTTriggerCondition.json','wt')  as f:
        json.dump(trigger,f,indent=4)



