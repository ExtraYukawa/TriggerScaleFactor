import os,json


def Gen_HLT_MET_File(year:str):
    '''
    
    Build JSON file to record trigger conditions for Each particular channels.
    
    '''
    trigger = dict()

    trigger['Data'] = dict()
    if year=='2016apv':
        eras = ['B2','C','D','E','F']
        for era in eras:
            trigger['Data'][era] = \
                    ["HLT_MET200",
                    "HLT_PFMET120_PFMHT120_IDTight",
                    "HLT_PFMET300",
                    "HLT_PFHT300_PFMET110",
                    "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight"]
                    


        trigger['MC']  =\
                ["HLT_PFMET300",\
                "HLT_MET200",\
                "HLT_PFHT300_PFMET110",\
                "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",\
                "HLT_PFMET120_PFMHT120_IDTight"] \


    elif year =='2016postapv':
        eras = ['F','G','H']
        for era in eras:
            trigger['Data'][era] =\
                    ["HLT_PFMET300",\
                    "HLT_MET200",\
                    "HLT_PFHT300_PFMET110",\
                    "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",\
                    "HLT_PFMET120_PFMHT120_IDTight"]

        
        
        trigger['MC']  = \
                ["HLT_PFMET300",\
                "HLT_MET200",\
                "HLT_PFHT300_PFMET110",\
                "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",\
                "HLT_PFMET120_PFMHT120_IDTight"]


    elif year=='2017':
        eras = ['B','C','D','E','F']
        for era in eras:
            trigger['Data'][era] = \
                    ["HLT_PFMET120_PFMHT120_IDTight",\
                    "HLT_PFHT700_PFMET85_PFMHT85_IDTight",\
                    "HLT_PFMET250_HBHECleaned",\
                    "HLT_PFHT800_PFMET75_PFMHT75_IDTight",\
                    "HLT_PFHT500_PFMET100_PFMHT100_IDTight"]
            if era == 'B':
                trigger['Data'][era] =\
                    ["HLT_PFMET120_PFMHT120_IDTight",\
                    "HLT_PFHT700_PFMET85_PFMHT85_IDTight",\
                    "HLT_PFHT800_PFMET75_PFMHT75_IDTight",\
                    "HLT_PFHT500_PFMET100_PFMHT100_IDTight"]

        trigger['MC'] = \
                ["HLT_PFMET120_PFMHT120_IDTight",\
                "HLT_PFHT700_PFMET85_PFMHT85_IDTight",\
                "HLT_PFMET250_HBHECleaned",\
                "HLT_PFHT800_PFMET75_PFMHT75_IDTight",\
                "HLT_PFHT500_PFMET100_PFMHT100_IDTight"]


    elif year =='2018':

        eras = ['A','B','C','D_0','D_1']
        
        for era in eras:
            trigger['Data'][era]  =\
                    ["HLT_PFMET200_HBHE_BeamHaloCleaned"\
                    ,"HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned",\
                    "HLT_PFMET120_PFMHT120_IDTight",\
                    "HLT_PFMET120_PFMHT120_IDTight_PFHT60",\
                    "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",\
                    "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60",\
                    "HLT_PFHT500_PFMET100_PFMHT100_IDTight",\
                    "HLT_PFHT700_PFMET85_PFMHT85_IDTight",\
                    "HLT_PFHT800_PFMET75_PFMHT75_IDTight"]

            
        
        trigger['MC'] =\
                    ["HLT_PFMET200_HBHE_BeamHaloCleaned"\
                    ,"HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned",\
                    "HLT_PFMET120_PFMHT120_IDTight",\
                    "HLT_PFMET120_PFMHT120_IDTight_PFHT60",\
                    "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",\
                    "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60",\
                    "HLT_PFHT500_PFMET100_PFMHT100_IDTight",\
                    "HLT_PFHT700_PFMET85_PFMHT85_IDTight",\
                    "HLT_PFHT800_PFMET75_PFMHT75_IDTight"]

    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/TriggerSF/configuration/HLT_MET.json','w')  as f:
        json.dump(trigger,f,indent=4)

    
    print(f'Data:\n')
    for era in trigger['Data'].keys():
        print(f"Era:{era}")
        for path in trigger['Data'][era]:
            print(path)

    print(f'MC:\n')
    for path in trigger['MC']:
        print(path)


def GenTotalLuminosity(year:str):
    '''
    Generate the total luminosity.
    '''
    lumi =dict()
    lumi['2016apv'] = 19500 
    lumi['2016postapv'] = 16800
    lumi['2017'] = 41480
    lumi['2018'] = 59700
    with open(f'./data/year{year}/TriggerSF/configuration/lumi.json','w') as f :
        json.dump(lumi,f,indent=4)

def GenTrigEffInput_File(year:str):
    '''
    
    Build JSON file to record Input path for TriggerEfficiency Calculation Stage.
    
    '''
    path = dict()
    path['Data'] = dict()
    if year=='2017' :
        eras = ['B','C','D','E','F']
        path['MC'] = ['/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/TTTo2L.root']
        for era in eras:
            path['Data'][era] = [f'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/MET{era}.root']
    elif year=='2018':
        eras = ['A','B','C','D_0','D_1']
        for era in eras:
            path['Data'][era]= [f'/eos/cms/store/group/phys_top/ExtraYukawa/2018/MET{era}.root']
        path['MC']=['/eos/cms/store/group/phys_top/ExtraYukawa/2018/TTTo2L.root']
        
    elif year == '2016apv':
        eras = ['B2','C','D','E','F']
        path['MC'] = ['/eos/cms/store/group/phys_top/ExtraYukawa/2016apvMerged/TTTo2L2Nu.root']
        for era in eras:
            path['Data'][era] = [f'/eos/cms/store/group/phys_top/ExtraYukawa/2016apvMerged/MET_{era}.root']
        
    elif year == '2016postapv': 
        eras = ['F','G','H']
        path['MC'] = ['/eos/cms/store/group/phys_top/ExtraYukawa/2016postapvMerged/TTTo2L2Nu.root']
        for era in eras:
            path['Data'][era] =[f'/eos/cms/store/group/phys_top/ExtraYukawa/2016postapvMerged/MET_{era}.root']
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/TriggerSF/path/filein.json','w') as f:
        json.dump(path,f,indent=4)

def GenMCWeightsName_File(year:str):
    if year == '2017' or year == '2016apv' or year =='2016postapv':
        weights={
                'Data':'1',
                'MC':['puWeight','PrefireWeight']
                }
    elif year =='2018':
        weights={
                'Data':'1',
                'MC':['puWeight']
                }
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/TriggerSF/configuration/weights.json','w') as f:
        json.dump(weights,f,indent=4)


def GenLeptonIDSF_File(year:str):
    if year=='2017' or year == '2018' or year =='2016apv' or year=='2016postapv':
        year_tmp = year
        if year=='2016postapv':
            year='2016'
            year_tmp = '2016postapv'
        else:
            pass
        path = {
                'DoubleElectron':{ 
                    'path':f'/afs/cern.ch/user/m/melu/public/EG_SF/{year}/{year}.root',
                        'name':'EleIDSF'},
                'DoubleMuon':{
                    'path':f'/eos/user/t/tihsu/share/muonID_SF/{year_tmp}UL/muonIdSF_{year_tmp}UL.root',
                    'name':'muIdSF'
                    },
                'ElectronMuon':{
                    'path':{
                        'Muon':f'/eos/user/t/tihsu/share/muonID_SF/{year_tmp}UL/muonIdSF_{year_tmp}UL.root',
                        'Electron':f'/afs/cern.ch/user/m/melu/public/EG_SF/{year}/{year}.root'
                    },
                    'name':{
                        'Muon':'muIdSF',
                        'Electron':'EleIDSF'
                        }

                    }
        }
        if year =='2016apv':
            path['DoubleMuon']['name']= 'muIdSF_apv2016'
            path['ElectronMuon']['name']['Muon']= 'muIdSF_apv2016'
        if year_tmp =='2016postapv':
            path['DoubleMuon']['name']= 'muIdSF_2016'
            path['ElectronMuon']['name']['Muon']= 'muIdSF_2016'

        if year =='2016':
            year = year_tmp
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/TriggerSF/path/LeptonsID_SF.json','w') as f:
        json.dump(path,f,indent=4)


def GenVariableNames_File(year:str):
    '''
    
    Build JSON file to record Variable names.
    
    '''
    channels = ['DoubleElectron','DoubleMuon','ElectronMuon']

    property_name = dict()
    if year=='2017' or year =='2018' or year=='2016apv' or year =='2016postapv':

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
        property_name['ElectronMuon']['OPS_p4'] = {'l1':['Muon_corrected_pt[OPS_l1_id]','Muon_eta[OPS_l1_id]','Muon_phi[OPS_l1_id]','Muon_mass[OPS_l1_id]'],'l2':['Electron_pt[OPS_l2_id]','Electron_eta[OPS_l2_id]','Electron_phi[OPS_l2_id]','Electron_mass[OPS_l2_id]']}


        for channel in channels:
            property_name[channel]['ttc_p4'] = {'l1':['ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass'],'l2':['ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass']}

    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/TriggerSF/configuration/name.json','wt') as f:
        json.dump(property_name, f,indent=4)

def Gen_MET_Filters_File(year:str):
    '''
    Build Json file which contents MET Filters Name.
    '''
    Flags = dict()

    if year=='2017' or year == '2018':

        Flags["Data"] = ["Flag_goodVertices",\
                "Flag_globalSuperTightHalo2016Filter",\
                "Flag_HBHENoiseFilter",\
                "Flag_HBHENoiseIsoFilter",\
                "Flag_EcalDeadCellTriggerPrimitiveFilter",\
                "Flag_BadPFMuonDzFilter",\
                "Flag_BadPFMuonFilter",\
                "Flag_eeBadScFilter",\
                "Flag_ecalBadCalibFilter"]
        Flags["MC"] = ["Flag_goodVertices",\
                "Flag_globalSuperTightHalo2016Filter",\
                "Flag_HBHENoiseFilter",\
                "Flag_HBHENoiseIsoFilter",\
                "Flag_EcalDeadCellTriggerPrimitiveFilter",\
                "Flag_BadPFMuonDzFilter",\
                "Flag_eeBadScFilter",\
                "Flag_BadPFMuonFilter",\
                "Flag_ecalBadCalibFilter"]
    elif year=='2016apv' or year=='2016postapv':

        Flags["Data"] = ["Flag_goodVertices",\
                "Flag_globalSuperTightHalo2016Filter",\
                "Flag_HBHENoiseFilter",\
                "Flag_HBHENoiseIsoFilter",\
                "Flag_EcalDeadCellTriggerPrimitiveFilter",\
                "Flag_BadPFMuonDzFilter",\
                "Flag_BadPFMuonFilter",\
                "Flag_eeBadScFilter"]
        
        Flags["MC"] = ["Flag_goodVertices",\
                "Flag_globalSuperTightHalo2016Filter",\
                "Flag_HBHENoiseFilter",\
                "Flag_HBHENoiseIsoFilter",\
                "Flag_EcalDeadCellTriggerPrimitiveFilter",\
                "Flag_BadPFMuonFilter",\
                "Flag_BadPFMuonDzFilter",\
                "Flag_eeBadScFilter"]



    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/TriggerSF/configuration/MET_Filters.json','wt') as f :
        json.dump(Flags,f,indent=4)

    print('Data:')
    for flag in Flags["Data"]:
        print(flag)
    print('MC:')
    for flag in Flags["MC"]:
        print(flag)






