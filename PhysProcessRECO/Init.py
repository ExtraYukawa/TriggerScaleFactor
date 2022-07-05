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
    '''
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
    '''
    path['branchname']['l1pteta'] = 'l1pteta'
    path['branchname']['l2pteta'] = 'l2pteta'
    path['branchname']['l1l2pt'] = 'l1l2pt'
    path['branchname']['l1l2eta'] = 'l1l2eta'


    with open(f'./data/year{year}/PhysProcessRECO/path/triggerSF.json','wt') as f:
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
    
    elif year=='2016apv':
        data_dir ='/eos/cms/store/group/phys_top/ExtraYukawa/2016apvMerged'
        post_fixs = ['B2','C','D','E','F'] 

    elif year =='2016postapv':
        data_dir = '/eos/cms/store/group/phys_top/ExtraYukawa/2016postapvMerged/'
        post_fixs = ['F','G','H']

    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
        
    if year == '2017':
        data_path['Data']['DoubleElectron']['SingleEG'] = dict()
        data_path['Data']['DoubleElectron']['DoubleEG'] = dict()
        data_path['Data']['DoubleMuon']['DoubleMuon'] = dict()
        data_path['Data']['DoubleMuon']['SingleMuon'] = dict()
        data_path['Data']['ElectronMuon']['SingleMuon'] = dict()
        data_path['Data']['ElectronMuon']['SingleEG'] = dict() 
        data_path['Data']['ElectronMuon']['MuonEG'] = dict()
    
    
        for era in post_fixs:
            data_path['Data']['DoubleElectron']['SingleEG'][era] = os.path.join(data_dir,'SingleEG'+ era + '.root') 
            data_path['Data']['DoubleElectron']['DoubleEG'][era] = os.path.join(data_dir,'DoubleEG'+ era + '.root') 
            data_path['Data']['DoubleMuon']['DoubleMuon'][era] = os.path.join(data_dir,'DoubleMuon'+ era + '.root') 
            data_path['Data']['DoubleMuon']['SingleMuon'][era] = os.path.join(data_dir, 'SingleMuon' + era + '.root') 
            data_path['Data']['ElectronMuon']['SingleMuon'][era] = os.path.join(data_dir, 'SingleMuon'+ era + '.root') 
            data_path['Data']['ElectronMuon']['SingleEG'][era] = os.path.join(data_dir,'SingleEG'+ era + '.root')
            data_path['Data']['ElectronMuon']['MuonEG'][era] = os.path.join(data_dir,'MuonEG'+ era + '.root')
    
    elif year == '2018':

        data_path['Data']['DoubleElectron']['SingleEG'] = dict()
        data_path['Data']['DoubleElectron']['DoubleEG'] = dict()
        data_path['Data']['DoubleMuon']['DoubleMuon'] = dict()
        data_path['Data']['DoubleMuon']['SingleMuon'] = dict()
        data_path['Data']['ElectronMuon']['SingleMuon'] = dict()
        data_path['Data']['ElectronMuon']['SingleEG'] = dict() 
        data_path['Data']['ElectronMuon']['MuonEG'] = dict()
        
        for postfix in post_fixs:
            data_path['Data']['DoubleElectron']['SingleEG'][postfix] = os.path.join(data_dir,'EGamma'+ postfix + '.root') 
            data_path['Data']['DoubleElectron']['DoubleEG'][postfix] = os.path.join(data_dir,'EGamma'+ postfix + '.root')
            data_path['Data']['DoubleMuon']['DoubleMuon'][postfix] = os.path.join(data_dir,'DoubleMuon'+ postfix + '.root') 
            data_path['Data']['DoubleMuon']['SingleMuon'][postfix] = os.path.join(data_dir, 'SingleMuon' + postfix + '.root') 
            data_path['Data']['ElectronMuon']['SingleMuon'][postfix] = os.path.join(data_dir, 'SingleMuon'+ postfix + '.root') 
            data_path['Data']['ElectronMuon']['SingleEG'][postfix] = os.path.join(data_dir,'EGamma'+ postfix + '.root') 
            data_path['Data']['ElectronMuon']['MuonEG'][postfix] = os.path.join(data_dir,'MuonEG'+ postfix + '.root') 
   

    elif year =='2016apv' or year =='2016postapv':
        
        data_path['Data']['DoubleElectron']['SingleEG'] = dict()
        data_path['Data']['DoubleElectron']['DoubleEG'] = dict()
        data_path['Data']['DoubleMuon']['DoubleMuon'] = dict()
        data_path['Data']['DoubleMuon']['SingleMuon'] = dict()
        data_path['Data']['ElectronMuon']['SingleMuon'] = dict()
        data_path['Data']['ElectronMuon']['SingleEG'] = dict() 
        data_path['Data']['ElectronMuon']['MuonEG'] = dict()

        for era in post_fixs:
            
            data_path['Data']['DoubleElectron']['SingleEG'][era] = os.path.join(data_dir,'SingleEG_'+ era + '.root') 
            data_path['Data']['DoubleElectron']['DoubleEG'][era] = os.path.join(data_dir,'DoubleEG_'+ era + '.root') 
            data_path['Data']['DoubleMuon']['DoubleMuon'][era] = os.path.join(data_dir,'DoubleMuon_'+ era + '.root') 
            data_path['Data']['DoubleMuon']['SingleMuon'][era] = os.path.join(data_dir, 'SingleMuon_' + era + '.root') 
            data_path['Data']['ElectronMuon']['SingleMuon'][era] = os.path.join(data_dir, 'SingleMuon_'+ era + '.root') 
            data_path['Data']['ElectronMuon']['SingleEG'][era] = os.path.join(data_dir,'SingleEG_'+ era + '.root')
            data_path['Data']['ElectronMuon']['MuonEG'][era] = os.path.join(data_dir,'MuonEG_'+ era + '.root')
    else:
        raise ValueError("Wrong Year!")
    
    data_path['Process'] = ['DY','WJets','VV','VVV','SingleTop','ttXorXX','tzq','TT']
    for p in data_path['Process']:
        data_path['MC'][p] = dict()
    
    if year =='2016apv' or year == '2016postapv':
        data_path['MC']['DY']['DYnlo'] = os.path.join(data_dir,'DYnlo.root')
        data_path['MC']['WJets']['WJets'] = os.path.join(data_dir,'WJets.root')
        data_path['MC']['VV']['ww'] = os.path.join(data_dir,'ww.root')
        data_path['MC']['VV']['wz_qcd'] = os.path.join(data_dir,'wz_qcd.root')
        data_path['MC']['VV']['zz2l'] = os.path.join(data_dir,'zz2l.root')
        data_path['MC']['VVV']['www1'] = os.path.join(data_dir,'www1.root')
        data_path['MC']['VVV']['wwz1'] = os.path.join(data_dir,'wwz1.root')
        data_path['MC']['VVV']['wzz1'] = os.path.join(data_dir,'wzz1.root')
        data_path['MC']['VVV']['zzz1'] = os.path.join(data_dir,'zzz1.root')
        data_path['MC']['SingleTop']['t_sch'] = os.path.join(data_dir,'t_sch.root')
        data_path['MC']['SingleTop']['t_tch'] = os.path.join(data_dir,'t_tch.root')
        data_path['MC']['SingleTop']['tbar_tch'] = os.path.join(data_dir,'tbar_tch.root')
        data_path['MC']['SingleTop']['tW'] = os.path.join(data_dir,'tW.root')
        data_path['MC']['SingleTop']['tbarW'] = os.path.join(data_dir,'tbarW.root')
        data_path['MC']['ttXorXX']['ttW'] = os.path.join(data_dir,'ttW.root')
        data_path['MC']['ttXorXX']['ttWToQQ'] = os.path.join(data_dir,'ttWToQQ.root')
        data_path['MC']['ttXorXX']['ttZ'] = os.path.join(data_dir,'ttZ.root')
        data_path['MC']['ttXorXX']['ttZToQQ'] = os.path.join(data_dir,'ttZToQQ.root')
        data_path['MC']['ttXorXX']['ttH'] = os.path.join(data_dir,'ttH.root')
        data_path['MC']['ttXorXX']['ttWW'] = os.path.join(data_dir,'ttWW.root')
        data_path['MC']['ttXorXX']['ttWZ'] = os.path.join(data_dir,'ttWZ.root')
        data_path['MC']['ttXorXX']['ttZZ'] = os.path.join(data_dir,'ttZZ.root')
        data_path['MC']['tzq']['tZq'] = os.path.join(data_dir,'tZq.root')
        data_path['MC']['TT']['TTTo2L2Nu'] = os.path.join(data_dir,'TTTo2L2Nu.root')
        data_path['MC']['TT']['TTTo1L'] = os.path.join(data_dir,'TTTo1L.root')
    elif year =='2017' or year =='2018':
        data_path['MC']['DY']['DYnlo'] = os.path.join(data_dir,'DYnlo.root')
        
        data_path['MC']['WJets']['WJets'] = os.path.join(data_dir,'WJets.root')
        
        data_path['MC']['SingleTop']['tsch'] = os.path.join(data_dir,'tsch.root')
        data_path['MC']['VV']['osWW'] = os.path.join(data_dir,'osWW.root')
        data_path['MC']['SingleTop']['tW'] = os.path.join(data_dir,'tW.root')
        data_path['MC']['SingleTop']['tbarW'] = os.path.join(data_dir,'tbarW.root')
        data_path['MC']['VV']['ZZ'] = os.path.join(data_dir,'ZZ.root')
        data_path['MC']['VV']['ssWW'] = os.path.join(data_dir,'ssWW.root')
        data_path['MC']['VV']['ZG_ew'] = os.path.join(data_dir,'ZG_ew.root')
        data_path['MC']['SingleTop']['t_tch'] = os.path.join(data_dir,'t_tch.root')
        data_path['MC']['SingleTop']['tbar_tch'] = os.path.join(data_dir,'tbar_tch.root')
        data_path['MC']['VV']['WWdps'] = os.path.join(data_dir,'WWdps.root')
        
        if year == '2017':
            data_path['MC']['VV']['WZ_ew'] = os.path.join(data_dir,'WZ_ew.root')
            data_path['MC']['VV']['WZ_qcd'] = os.path.join(data_dir,'WZ_qcd.root')
        elif year == '2018':
            data_path['MC']['VV']['WZ'] = os.path.join(data_dir,'WZ.root')
        
        data_path['MC']['VVV']['WWW'] = os.path.join(data_dir,'WWW.root')
        data_path['MC']['VVV']['WWZ'] = os.path.join(data_dir,'WWZ.root')
        data_path['MC']['VVV']['WZZ'] = os.path.join(data_dir,'WZZ.root')
        data_path['MC']['VVV']['ZZZ'] = os.path.join(data_dir,'ZZZ.root')
        
        
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

        
    with open(f'./data/year{year}/PhysProcessRECO/path/datapath.json','wt') as f:
        json.dump(data_path,f,indent=4)
def GenProcessName(year:str):

    Event =[]
        
    Event =dict()


    for p in ['DY','WJets','VV','VVV','SingleTop','ttXorXX','tzq','TT']:
        Event[p]  = list()
    
    Event['DY'].append('DYnlo')
    Event['WJets'].append('WJets')
    
    if year == '2017' or year == '2018':

        if year =='2017':
            Event['VV'].append('WZ_ew')
            Event['VV'].append('WZ_qcd')
        elif year =='2018':
            Event['VV'].append('WZ')
        
        else:
            raise ValueError("year{year} HLT Path has not been specified yet!")

        Event['VV'].append('ssWW')
        Event['VV'].append('WWdps')
        Event['VV'].append('ZG_ew')
        Event['VV'].append('osWW')
        Event['VV'].append('ZZ')
        
        
        Event['SingleTop'].append('t_tch')
        Event['SingleTop'].append('tbar_tch')
        
        Event['SingleTop'].append('tsch')
        Event['SingleTop'].append('tW')
        Event['SingleTop'].append('tbarW')



        
        Event['VVV'].append('WWW')
        Event['VVV'].append('WWZ')
        Event['VVV'].append('WZZ')
        Event['VVV'].append('ZZZ')
        
        Event['TT'].append('TTTo2L')
        Event['TT'].append('TTTo1L')
        
        
        Event['tzq'].append('tzq')
        
        
        Event['ttXorXX'].append('ttWtoLNu')
        Event['ttXorXX'].append('ttWtoQQ')
        Event['ttXorXX'].append('ttZ')
        Event['ttXorXX'].append('ttZtoQQ')
        Event['ttXorXX'].append('ttH')
        Event['ttXorXX'].append('ttWW')
        Event['ttXorXX'].append('ttWZ') 
        Event['ttXorXX'].append('ttZZ') 
        Event['ttXorXX'].append('ttWH') 
        Event['ttXorXX'].append('ttZH') 
        Event['ttXorXX'].append('tttJ') 
        Event['ttXorXX'].append('tttW') 
        Event['ttXorXX'].append('tttt') 
    elif year == '2016apv' or year =='2016postapv':

        Event['VV'].append('ww')
        Event['VV'].append('wz_qcd')
        Event['VV'].append('zz2l')
        Event['VVV'].append('www1')
        Event['VVV'].append('wwz1')
        Event['VVV'].append('wzz1')
        Event['VVV'].append('zzz1')
        Event['TT'].append('TTTo2L2Nu')
        Event['TT'].append('TTTo1L')

        Event['ttXorXX'].append('ttH')
        Event['ttXorXX'].append('ttW')
        Event['ttXorXX'].append('ttWToQQ')
        Event['ttXorXX'].append('ttZ')
        Event['ttXorXX'].append('ttZToQQ')
        Event['ttXorXX'].append('ttWW')
        Event['ttXorXX'].append('ttWZ')
        Event['ttXorXX'].append('ttZZ')

        Event['tzq'].append('tZq')
        
        Event['SingleTop'].append('tW')
        Event['SingleTop'].append('tbarW')
        Event['SingleTop'].append('t_sch')
        Event['SingleTop'].append('t_tch')
        Event['SingleTop'].append('tbar_tch')
    with open(f'./data/year{year}/PhysProcessRECO/configuration/Phys_process.json','wt') as f:
        json.dump(Event,f,indent=4)


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
    

    if year =='2017' or year == '2018':
        if year =='2017':
            Event['xs']['lumi'] = 41480.
            Event['xs']['VV']['WZ_ew'] = 0.0163
            Event['xs']['VV']['WZ_qcd'] = 5.213
        elif year =='2018':
            Event['xs']['lumi'] = 59830.
            Event['xs']['VV']['WZ'] =  5.2293
        else:
            raise ValueError("year{year} HLT Path has not been specified yet!")
        

        Event['xs']['VV']['ssWW'] = 0.04932
        Event['xs']['VV']['WWdps'] = 1.62
        Event['xs']['VV']['ZG_ew'] = 0.1097
        Event['xs']['SingleTop']['t_tch'] = 136.02
        Event['xs']['SingleTop']['tbar_tch'] = 80.95
        
        Event['xs']['VV']['osWW'] = 11.09
        Event['xs']['SingleTop']['tsch'] = 3.36
        Event['xs']['SingleTop']['tW'] = 35.85
        Event['xs']['SingleTop']['tbarW'] = 35.85

        Event['xs']['VV']['ZZ'] = 0.0086

        Event['xs']['DY']['DYnlo'] = 6077.22
        Event['xs']['WJets']['WJets'] = 61526.7

        
        Event['xs']['VVV']['WWW'] = 0.2086
        Event['xs']['VVV']['WWZ'] = 0.1707
        Event['xs']['VVV']['WZZ'] = 0.05709
        Event['xs']['VVV']['ZZZ'] = 0.01476
        
        Event['xs']['TT']['TTTo2L'] = 88.29
        Event['xs']['TT']['TTTo1L'] = 365.34
        
        
        Event['xs']['tzq']['tzq'] = 0.07561
        
        
        Event['xs']['ttXorXX']['ttWtoLNu']  = 0.1792
        Event['xs']['ttXorXX']['ttWtoQQ'] = 0.3708
        Event['xs']['ttXorXX']['ttZ'] = 0.2589
        Event['xs']['ttXorXX']['ttZtoQQ'] = 0.6012
        Event['xs']['ttXorXX']['ttH'] = 0.5638
        Event['xs']['ttXorXX']['ttWW'] = 0.007003
        Event['xs']['ttXorXX']['ttWZ'] = 0.002453
        Event['xs']['ttXorXX']['ttZZ'] = 0.001386
        Event['xs']['ttXorXX']['ttWH'] = 0.00114
        Event['xs']['ttXorXX']['ttZH'] = 0.00113
        Event['xs']['ttXorXX']['tttJ'] = 0.0004
        Event['xs']['ttXorXX']['tttW'] = 0.00073
        Event['xs']['ttXorXX']['tttt'] = 0.0082
   
    elif year =='2016apv' or year =='2016postapv' :
        
        if year =='2016apv':
            Event['xs']['lumi'] = 19520
        else:
            Event['xs']['lumi'] = 16810
        Event['xs']['DY']['DYnlo'] = 6077.22
        Event['xs']['WJets']['WJets'] = 61526.7
        Event['xs']['VV']['ww'] = 11.09
        Event['xs']['VV']['wz_qcd'] =  5.213
        Event['xs']['VV']['zz2l'] = 0.0086
        Event['xs']['VVV']['www1'] = 0.2086
        Event['xs']['VVV']['wwz1'] = 0.1707
        Event['xs']['VVV']['wzz1'] = 0.05709
        Event['xs']['VVV']['zzz1'] = 0.01476
        Event['xs']['TT']['TTTo2L2Nu'] = 88.29
        Event['xs']['TT']['TTTo1L'] = 365.34

        Event['xs']['ttXorXX']['ttH'] =  0.5638
        Event['xs']['ttXorXX']['ttW'] = 0.1792
        Event['xs']['ttXorXX']['ttWToQQ'] = 0.3708
        Event['xs']['ttXorXX']['ttZ'] =  0.2589
        Event['xs']['ttXorXX']['ttZToQQ'] = 0.6012
        Event['xs']['ttXorXX']['ttWW'] = 0.007003
        Event['xs']['ttXorXX']['ttWZ'] = 0.002453
        Event['xs']['ttXorXX']['ttZZ'] = 0.001386

        Event['xs']['tzq']['tZq'] = 0.07561
        
        Event['xs']['SingleTop']['tW'] = 35.85
        Event['xs']['SingleTop']['tbarW'] = 35.85
        Event['xs']['SingleTop']['t_sch'] = 3.36
        Event['xs']['SingleTop']['t_tch'] = 136.02
        Event['xs']['SingleTop']['tbar_tch'] = 80.95

        
    with open(f'./data/year{year}/PhysProcessRECO/path/datapath.json' , 'rb') as f:
        MC_Paths = json.load(f)['MC']

    
    for p in Event['Process']:
        for name in MC_Paths[p].keys():
            Event['NumberOfEvents'][p][name] = get_NumberOfEvent(MC_Paths[p][name])

    with open(f'./data/year{year}/PhysProcessRECO/configuration/data_xs.json','wt') as f:
        json.dump(Event,f,indent=4)


def GenChargeFlipFiles(year:str):

    PATH = dict()
    PATH['prob_MLE'] = f'/eos/user/z/zhenggan/ExtraYukawa/PhysProcessRECO/year{year}/ChargeFlipProbability_{year}_MLE.root'
    PATH['prob_chi2'] = f'/eos/user/z/zhenggan/ExtraYukawa/PhysProcessRECO/year{year}/ChargeFlipProbability_{year}_chi2.root'
    PATH['SF'] = f'/eos/user/z/zhenggan/ExtraYukawa/PhysProcessRECO/year{year}/ChargeFlipSF_{year}_MLE.root'

    with open(f'./data/year{year}/PhysProcessRECO/path/ChargeFlipFiles.json','wt') as f:
        json.dump(PATH,f,indent =4 )

def GenFakeRateFiles(year:str):
    if year =='2016apv':
        year_ = '2016APV'
    elif year =='2016postapv':
        year_ = '2016postAPV'
    else:
        year_ = year
    PATH =dict()
    PATH['electron'] = f'/eos/user/z/zhenggan/ExtraYukawa/PhysProcessRECO/year{year}/fr_data_mu_{year_}.root'
    PATH['muon'] = f'/eos/user/z/zhenggan/ExtraYukawa/PhysProcessRECO/year{year}/fr_data_ele_{year_}.root'


    with open(f'./data/year{year}/PhysProcessRECO/path/FakeRateFiles.json','wt') as f:
        json.dump(PATH,f,indent=4)





