import os,json



def FakeRateConfiguration(year:str):

    filters = dict()
    filters['Electron'] = dict()
    filters['Muon'] = dict()
    filters['ElectronQCD']  = dict()
    filters['MuonQCD']  = dict()
    if year == '2017':
        
        filters['Electron']['All'] = '(HLT_Ele17_CaloIdM_TrackIdM_PFJet30 && l1_pt<35) || (HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 && l1_pt>35)'
        filters['Electron']['numerator'] ='n_tight_ele==1 &&met<30 &&mt<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30_dr07'
        filters['Electron']['denominator'] = '(n_tight_ele==1 ||n_fakeable_ele==1)&&met<30 && mt<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30_dr07'
        
        
        filters['ElectronQCD']['All'] = '(HLT_Ele17_CaloIdM_TrackIdM_PFJet30 && l1_pt<35) || (HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 && l1_pt>35)'
        filters['ElectronQCD']['numerator'] = 'n_tight_ele==1 &&mt<30 && met<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30'
        filters['ElectronQCD']['denominator'] = '(n_tight_ele==1 ||n_fakeable_ele==1)&&mt<30 && met<30&& Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30'
        

        
        filters['Muon']['All'] = '(HLT_Mu8 && l1_pt<30) || (HLT_Mu17 && l1_pt>30)'
        filters['Muon']['numerator'] = 'n_tight_muon==1 && mt<30 &&met<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30_dr07'
        filters['Muon']['denominator'] ='(n_tight_muon==1 ||n_fakeable_muon==1)&& mt<30 && met<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30_dr07'
        
        filters['MuonQCD']['All'] = '(HLT_Mu8 && l1_pt<30) || (HLT_Mu17 && l1_pt>30)'
        filters['MuonQCD']['numerator'] = 'n_tight_muon==1 &&met<30&&mt<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30'

        filters['MuonQCD']['denominator'] ='(n_tight_muon==1 ||n_fakeable_muon==1)&&met<30&&mt<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30'

        with open(f'./data/year{year}/FakeRate/configuration/filters.json','wt') as f:
            json.dump(filters,f,indent=4)
import os
from Utils.General_Tool import get_NumberOfEvent
def FakeRateFilesIn(year:str):
    FilesIn = dict()
    FilesIn['Data'] = dict()
    FilesIn['Data']['Electron'] = list()
    FilesIn['Data']['Muon'] = list()

    FilesIn['MC'] = dict()
    FilesIn['MC']['Lepton'] = dict()
    FilesIn['MC']['Lepton']['DY'] = dict()
    FilesIn['MC']['Lepton']['WJets'] = dict()
    FilesIn['MC']['Lepton']['TTTo1L'] = dict()
    FilesIn['MC']['Lepton']['TTTo2L'] = dict()

    FilesIn['MC']['ElectronQCD'] = dict()
    FilesIn['MC']['MuonQCD'] = dict()
    if year == '2017':
        path='/eos/user/m/melu/TTC_fakerate_newLepID_1129/'
        FilesIn['Data']['Electron'] = [os.path.join(path,'SingleEG'+postfix+'.root') for postfix in ['C','D','E','F']]
        FilesIn['Data']['Muon'] = [os.path.join(path,'DoubleMuon'+postfix+'.root') for postfix in ['B','C','D','E','F']]
        FilesIn['MC']['Lepton']['DY']['path'] = os.path.join(path,'DY.root')
        FilesIn['MC']['Lepton']['WJets']['path'] = os.path.join(path,'WJets.root')
        FilesIn['MC']['Lepton']['TTTo1L']['path'] = os.path.join(path,'TTTo1L.root')
        FilesIn['MC']['Lepton']['TTTo2L']['path'] = os.path.join(path,'TTTo2L.root')
        
        FilesIn['MC']['Lepton']['DY']['xs'] = 6077.22 
        FilesIn['MC']['Lepton']['DY']['nevents'] =get_NumberOfEvent(FilesIn['MC']['Lepton']['DY']['path'])
        FilesIn['MC']['Lepton']['WJets']['xs'] = 61526.7
        FilesIn['MC']['Lepton']['WJets']['nevents'] =get_NumberOfEvent(FilesIn['MC']['Lepton']['WJets']['path'])
        FilesIn['MC']['Lepton']['TTTo1L']['xs'] = 365.4574
        FilesIn['MC']['Lepton']['TTTo1L']['nevents'] =get_NumberOfEvent(FilesIn['MC']['Lepton']['TTTo1L']['path'])
        FilesIn['MC']['Lepton']['TTTo2L']['xs'] = 88.3419
        FilesIn['MC']['Lepton']['TTTo2L']['nevents'] =get_NumberOfEvent(FilesIn['MC']['Lepton']['TTTo2L']['path'])

        FilesIn['MC']['ElectronQCD']['QCDEM15to20'] = dict()
        FilesIn['MC']['ElectronQCD']['QCDEM15to20']['path'] = os.path.join(path,'QCDEM15to20'+'.root')
        FilesIn['MC']['ElectronQCD']['QCDEM15to20']['xs'] =  1327000. 
        FilesIn['MC']['ElectronQCD']['QCDEM15to20']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCDEM15to20']['path'])

        FilesIn['MC']['ElectronQCD']['QCDEM20to30'] = dict()
        FilesIn['MC']['ElectronQCD']['QCDEM20to30']['path'] = os.path.join(path,'QCDEM20to30'+'.root')
        FilesIn['MC']['ElectronQCD']['QCDEM20to30']['xs'] = 4908000.
        FilesIn['MC']['ElectronQCD']['QCDEM20to30']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCDEM20to30']['path'])


        FilesIn['MC']['ElectronQCD']['QCDEM30to50'] = dict()
        FilesIn['MC']['ElectronQCD']['QCDEM30to50']['path'] = os.path.join(path,'QCDEM30to50'+'.root')
        FilesIn['MC']['ElectronQCD']['QCDEM30to50']['xs'] = 6396000.
        FilesIn['MC']['ElectronQCD']['QCDEM30to50']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCDEM30to50']['path'])


        FilesIn['MC']['ElectronQCD']['QCDEM50to80'] = dict()
        FilesIn['MC']['ElectronQCD']['QCDEM50to80']['path'] = os.path.join(path,'QCDEM50to80'+'.root')
        FilesIn['MC']['ElectronQCD']['QCDEM50to80']['xs'] = 1989000.
        FilesIn['MC']['ElectronQCD']['QCDEM50to80']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCDEM50to80']['path'])


        FilesIn['MC']['ElectronQCD']['QCDEM80to120'] = dict()
        FilesIn['MC']['ElectronQCD']['QCDEM80to120']['path'] = os.path.join(path,'QCDEM80to120'+'.root')
        FilesIn['MC']['ElectronQCD']['QCDEM80to120']['xs'] = 366500.
        FilesIn['MC']['ElectronQCD']['QCDEM80to120']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCDEM80to120']['path'])


        FilesIn['MC']['ElectronQCD']['QCDEM120to170'] = dict()
        FilesIn['MC']['ElectronQCD']['QCDEM120to170']['path'] = os.path.join(path,'QCDEM120to170'+'.root')
        FilesIn['MC']['ElectronQCD']['QCDEM120to170']['xs'] = 66490.
        FilesIn['MC']['ElectronQCD']['QCDEM120to170']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCDEM120to170']['path'])

        FilesIn['MC']['ElectronQCD']['QCDEM170to300'] = dict()
        FilesIn['MC']['ElectronQCD']['QCDEM170to300']['path'] = os.path.join(path,'QCDEM170to300'+'.root')
        FilesIn['MC']['ElectronQCD']['QCDEM170to300']['xs'] = 16480.
        FilesIn['MC']['ElectronQCD']['QCDEM170to300']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCDEM170to300']['path'])

        FilesIn['MC']['ElectronQCD']['QCDEM300toInf'] = dict()
        FilesIn['MC']['ElectronQCD']['QCDEM300toInf']['path'] = os.path.join(path,'QCDEM300toInf'+'.root')
        FilesIn['MC']['ElectronQCD']['QCDEM300toInf']['xs'] = 1099.
        FilesIn['MC']['ElectronQCD']['QCDEM300toInf']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCDEM300toInf']['path'])


        FilesIn['MC']['ElectronQCD']['QCD_bctoE_15to20'] = dict()
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_15to20']['path'] = os.path.join(path,'QCD_bctoE_15to20'+'.root')
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_15to20']['xs'] = 186200.0
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_15to20']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCD_bctoE_15to20']['path'])


        FilesIn['MC']['ElectronQCD']['QCD_bctoE_20to30'] = dict()
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_20to30']['path'] = os.path.join(path,'QCD_bctoE_20to30'+'.root')
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_20to30']['xs'] = 303800.
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_20to30']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCD_bctoE_20to30']['path'])


        FilesIn['MC']['ElectronQCD']['QCD_bctoE_30to80'] = dict()
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_30to80']['path'] = os.path.join(path,'QCD_bctoE_30to80'+'.root')
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_30to80']['xs'] = 362300.
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_30to80']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCD_bctoE_30to80']['path'])


        FilesIn['MC']['ElectronQCD']['QCD_bctoE_80to170'] = dict()
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_80to170']['path'] = os.path.join(path,'QCD_bctoE_80to170'+'.root')
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_80to170']['xs'] = 33700.
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_80to170']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCD_bctoE_80to170']['path'])


        FilesIn['MC']['ElectronQCD']['QCD_bctoE_170to250'] = dict()
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_170to250']['path'] = os.path.join(path,'QCD_bctoE_170to250'+'.root')
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_170to250']['xs'] = 2125.
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_170to250']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCD_bctoE_170to250']['path'])


        FilesIn['MC']['ElectronQCD']['QCD_bctoE_250toInf'] = dict()
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_250toInf']['path'] = os.path.join(path,'QCD_bctoE_250toInf'+'.root')
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_250toInf']['xs'] = 562.5
        FilesIn['MC']['ElectronQCD']['QCD_bctoE_250toInf']['nevents'] = get_NumberOfEvent(FilesIn['MC']['ElectronQCD']['QCD_bctoE_250toInf']['path'])

        
        FilesIn['MC']['MuonQCD']['QCD15to20'] = dict()
        FilesIn['MC']['MuonQCD']['QCD15to20']['path'] = os.path.join(path,'QCD15to20'+'.root')
        FilesIn['MC']['MuonQCD']['QCD15to20']['xs'] = 2799000.
        FilesIn['MC']['MuonQCD']['QCD15to20']['nevents'] = get_NumberOfEvent(FilesIn['MC']['MuonQCD']['QCD15to20']['path'])

        FilesIn['MC']['MuonQCD']['QCD20to30'] = dict()
        FilesIn['MC']['MuonQCD']['QCD20to30']['path'] = os.path.join(path,'QCD20to30'+'.root')
        FilesIn['MC']['MuonQCD']['QCD20to30']['xs'] =  2526000.
        FilesIn['MC']['MuonQCD']['QCD20to30']['nevents'] = get_NumberOfEvent(FilesIn['MC']['MuonQCD']['QCD20to30']['path'])


        FilesIn['MC']['MuonQCD']['QCD30to50'] = dict()
        FilesIn['MC']['MuonQCD']['QCD30to50']['path'] = os.path.join(path,'QCD30to50'+'.root')
        FilesIn['MC']['MuonQCD']['QCD30to50']['xs'] = 1362000.
        FilesIn['MC']['MuonQCD']['QCD30to50']['nevents'] = get_NumberOfEvent(FilesIn['MC']['MuonQCD']['QCD30to50']['path'])


        FilesIn['MC']['MuonQCD']['QCD50to80']=dict()
        FilesIn['MC']['MuonQCD']['QCD50to80']['path'] = os.path.join(path,'QCD50to80'+'.root')
        FilesIn['MC']['MuonQCD']['QCD50to80']['xs'] = 376600.
        FilesIn['MC']['MuonQCD']['QCD50to80']['nevents'] = get_NumberOfEvent(FilesIn['MC']['MuonQCD']['QCD50to80']['path'])


        FilesIn['MC']['MuonQCD']['QCD80to120']=dict()
        FilesIn['MC']['MuonQCD']['QCD80to120']['path'] = os.path.join(path,'QCD80to120'+'.root')
        FilesIn['MC']['MuonQCD']['QCD80to120']['xs'] = 88930.
        FilesIn['MC']['MuonQCD']['QCD80to120']['nevents'] = get_NumberOfEvent(FilesIn['MC']['MuonQCD']['QCD80to120']['path'])


        FilesIn['MC']['MuonQCD']['QCD120to170'] = dict()
        FilesIn['MC']['MuonQCD']['QCD120to170']['path'] = os.path.join(path,'QCD120to170'+'.root')
        FilesIn['MC']['MuonQCD']['QCD120to170']['xs'] = 21230.
        FilesIn['MC']['MuonQCD']['QCD120to170']['nevents'] = get_NumberOfEvent(FilesIn['MC']['MuonQCD']['QCD120to170']['path'])


        FilesIn['MC']['MuonQCD']['QCD170to300']=dict()
        FilesIn['MC']['MuonQCD']['QCD170to300']['path'] = os.path.join(path,'QCD170to300'+'.root')
        FilesIn['MC']['MuonQCD']['QCD170to300']['xs'] = 7055.
        FilesIn['MC']['MuonQCD']['QCD170to300']['nevents'] = get_NumberOfEvent(FilesIn['MC']['MuonQCD']['QCD170to300']['path'])


        FilesIn['MC']['MuonQCD']['QCD300to470']=dict()
        FilesIn['MC']['MuonQCD']['QCD300to470']['path'] = os.path.join(path,'QCD300to470'+'.root')
        FilesIn['MC']['MuonQCD']['QCD300to470']['xs'] = 619.3
        FilesIn['MC']['MuonQCD']['QCD300to470']['nevents'] = get_NumberOfEvent(FilesIn['MC']['MuonQCD']['QCD300to470']['path'])
        
        FilesIn['MC']['MuonQCD']['QCD470to600']=dict()
        FilesIn['MC']['MuonQCD']['QCD470to600']['path'] = os.path.join(path,'QCD470to600'+'.root')
        FilesIn['MC']['MuonQCD']['QCD470to600']['xs'] = 59.24
        FilesIn['MC']['MuonQCD']['QCD470to600']['nevents'] = get_NumberOfEvent(FilesIn['MC']['MuonQCD']['QCD470to600']['path'])


        FilesIn['MC']['MuonQCD']['QCD600to800']=dict()
        FilesIn['MC']['MuonQCD']['QCD600to800']['path'] = os.path.join(path,'QCD600to800'+'.root')
        FilesIn['MC']['MuonQCD']['QCD600to800']['xs'] = 18.21
        FilesIn['MC']['MuonQCD']['QCD600to800']['nevents'] = get_NumberOfEvent(FilesIn['MC']['MuonQCD']['QCD600to800']['path'])


        FilesIn['MC']['MuonQCD']['QCD800to1000']=dict()
        FilesIn['MC']['MuonQCD']['QCD800to1000']['path'] = os.path.join(path,'QCD800to1000'+'.root')
        FilesIn['MC']['MuonQCD']['QCD800to1000']['xs'] = 3.275
        FilesIn['MC']['MuonQCD']['QCD800to1000']['nevents'] = get_NumberOfEvent(FilesIn['MC']['MuonQCD']['QCD800to1000']['path'])


        FilesIn['MC']['MuonQCD']['QCD1000toInf'] =dict()
        FilesIn['MC']['MuonQCD']['QCD1000toInf']['path'] = os.path.join(path,'QCD1000toInf'+'.root')
        FilesIn['MC']['MuonQCD']['QCD1000toInf']['xs'] = 1.078
        FilesIn['MC']['MuonQCD']['QCD1000toInf']['nevents'] = get_NumberOfEvent(FilesIn['MC']['MuonQCD']['QCD1000toInf']['path'])
        with open(f'./data/year{year}/FakeRate/path/FilesIn.json','wt') as f:
            json.dump(FilesIn,f,indent=4)

