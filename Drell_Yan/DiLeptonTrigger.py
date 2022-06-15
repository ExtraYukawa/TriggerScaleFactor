import json




def GenPaths_HLTTriggerCondition_ForAnalyzer_File(year:str):
    '''
    
    Build JSON file to record trigger conditions for Each particular channels used in Analyzer condition.
    
    '''

    trigger =dict()
    #trigger['MC'] = dict()
    



    if year =='2016apv':
        eras = ['B2','C','D','E','F']
    elif year =='2016postapv':
        eras = ['F','G','H']
    elif year =='2017':
        eras = ['B','C','D','E','F']
    elif year =='2018':
        eras = ['A','B','C','D_0','D_1']
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    
    for channel in ['DoubleElectron','DoubleMuon','ElectronMuon']:
        trigger[channel] = dict()
        trigger[channel]['Data'] = dict()
        trigger[channel]['MC'] = dict()
    for channel in ['DoubleElectron','DoubleMuon','ElectronMuon']:
        for era in eras:
            trigger[channel]['Data'][era] = dict()
    
    if year == '2016apv':
        trigger['DoubleElectron']['MC'] = "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Ele27_WPTight_Gsf"#HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf"
        trigger['DoubleMuon']['MC'] = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL|| HLT_IsoMu27"

        trigger['ElectronMuon']['MC'] = "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_IsoMu27||HLT_IsoTkMu24 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL|| HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL || HLT_Ele27_WPTight_Gsf"#|| HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL|| HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL"
        
        for era in eras:
            trigger['DoubleElectron']['Data'][era]['SingleEG'] = '!Triggers(run,HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) &&Triggers(run,HLT_Ele27_WPTight_Gsf,{DiLepton_slc_run["HLT_Ele27_WPTight_Gsf"]})'#( Triggers(run , HLT_passEle32WPTight,{DiLepton_slc_run["HLT_passEle32WPTight"]}) || Triggers(run,HLT_Ele27_WPTight_Gsf,{DiLepton_slc_run["HLT_Ele27_WPTight_Gsf"]}))'
            trigger['DoubleElectron']['Data'][era]['DoubleEG'] = 'Triggers(run,HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]})'
            
            trigger['DoubleMuon']['Data'][era]['SingleMuon'] = '!( Triggers(run,HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL"]}) || Triggers(run,HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL"]}) ) && Triggers(run,HLT_IsoMu27,{DiLepton_slc_run["HLT_IsoMu27"]})' 

            trigger['DoubleMuon']['Data'][era]['DoubleMuon'] = 'Triggers(run,HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL"]}) || Triggers(run,HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL"]})'


            if era != 'F':
                trigger['ElectronMuon']['Data'][era]['SingleEG'] = '!( Triggers(run,HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]}) || Triggers(run,HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL, {DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL"]})) && Triggers( run , HLT_Ele27_WPTight_Gsf,{DiLepton_slc_run["HLT_Ele27_WPTight_Gsf"]})'#( Triggers( run , HLT_passEle32WPTight,{DiLepton_slc_run["HLT_passEle32WPTight"]}) || Triggers( run , HLT_Ele27_WPTight_Gsf,{DiLepton_slc_run["HLT_Ele27_WPTight_Gsf"]}))'
                trigger['ElectronMuon']['Data'][era]['SingleMuon'] = '!( Triggers(run,HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]}) || Triggers(run,HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL, {DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL"]}))'
                trigger['ElectronMuon']['Data'][era]['MuonEG'] = 'Triggers(run , HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL , {DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]}) || Triggers(run,HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL,{DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL"]}) || Triggers(run , HLT_IsoTkMu24,{DiLepton_slc_run["HLT_IsoTkMu24"]})' 
            
            else:
                trigger['ElectronMuon']['Data'][era]['SingleEG'] = '!( Triggers(run,HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run,HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]})) && Triggers( run , HLT_Ele27_WPTight_Gsf,{DiLepton_slc_run["HLT_Ele27_WPTight_Gsf"]})'#( Triggers( run , HLT_passEle32WPTight,{DiLepton_slc_run["HLT_passEle32WPTight"]}) || Triggers( run , HLT_Ele27_WPTight_Gsf,{DiLepton_slc_run["HLT_Ele27_WPTight_Gsf"]}))'
                trigger['ElectronMuon']['Data'][era]['SingleMuon'] = '!( Triggers(run,HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run,HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]})) && ( Triggers( run , HLT_IsoMu27,{DiLepton_slc_run["HLT_IsoMu27"]}))'
                trigger['ElectronMuon']['Data'][era]['MuonEG'] = 'Triggers(run , HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ , {DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run,HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run , HLT_IsoTkMu24,{DiLepton_slc_run["HLT_IsoTkMu24"]})' 

    
    elif year == '2016postapv':

        trigger['DoubleElectron']['MC'] = 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Ele27_WPTight_Gsf'#HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf'
        trigger['DoubleMuon']['MC'] = 'HLT_IsoMu27|| HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL|| HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'
        trigger['ElectronMuon']['MC'] = 'HLT_IsoMu27||HLT_IsoTkMu24 || HLT_Ele27_WPTight_Gsf || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'
        for era in eras: 

            trigger['DoubleElectron']['Data'][era]['SingleEG'] = '!Triggers(run,HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) &&( Triggers(run,HLT_Ele27_WPTight_Gsf,{DiLepton_slc_run["HLT_Ele27_WPTight_Gsf"]}))'
            trigger['DoubleElectron']['Data'][era]['DoubleEG'] = 'Triggers(run,HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]})'
            
            trigger['ElectronMuon']['Data'][era]['SingleEG'] = '! (Triggers(run,HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run , HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) ) &&(Triggers(run , HLT_Ele27_WPTight_Gsf, {DiLepton_slc_run["HLT_Ele27_WPTight_Gsf"]}))'

            trigger['ElectronMuon']['Data'][era]['SingleMuon'] = '! (Triggers(run,HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run , HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) ) &&(Triggers(run,HLT_IsoMu27,{DiLepton_slc_run["HLT_IsoMu27"]}) || Triggers(run , HLT_IsoTkMu24, {DiLepton_slc_run["HLT_IsoTkMu24"]}))'
            
            trigger['ElectronMuon']['Data'][era]['MuonEG'] = 'Triggers(run,HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run , HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]})'

            
            if era != 'H':
                trigger['DoubleMuon']['Data'][era]['SingleMuon'] = '!( Triggers(run,HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL"]}) || Triggers(run,HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL"]}) ) && Triggers(run,HLT_IsoMu27,{DiLepton_slc_run["HLT_IsoMu27"]})' 

                trigger['DoubleMuon']['Data'][era]['DoubleMuon'] = 'Triggers(run,HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL"]}) || Triggers(run,HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL"]})'
            else:

                trigger['DoubleMuon']['Data'][era]['SingleMuon'] = '!( Triggers(run,HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ"]}) || Triggers(run,HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ"]}) ) && Triggers(run,HLT_IsoMu27,{DiLepton_slc_run["HLT_IsoMu27"]})' 

                trigger['DoubleMuon']['Data'][era]['DoubleMuon'] = 'Triggers(run,HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ"]}) || Triggers(run,HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ"]})'

    
    elif year =='2017':
        trigger['DoubleElectron']['MC'] = "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_passEle32WPTight"
        trigger['DoubleMuon']['MC'] = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 || HLT_IsoMu27"
        trigger['ElectronMuon']['MC'] = "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 ||HLT_passEle32WPTight|| HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"
    
        
        for era in eras:
            trigger['DoubleElectron']['Data'][era]['DoubleEG'] = 'Triggers(run , HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL,{DiLepton_slc_run["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL"]})'
            
            if era == 'B':
                trigger['DoubleElectron']['Data'][era]['SingleEG'] = '!Triggers(run , HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL,{DiLepton_slc_run["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL"]}) && (Triggers( run ,HLT_passEle32WPTight , {DiLepton_slc_run["HLT_passEle32WPTight"]}))'
                
                trigger['DoubleMuon']['Data'][era]['SingleMuon'] = 'Triggers( run , HLT_IsoMu27,{DiLepton_slc_run["HLT_IsoMu27"]}) &&!(Triggers( run , HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"]}) || Triggers( run , HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ"]}))'
                trigger['DoubleMuon']['Data'][era]['DoubleMuon'] = 'Triggers(run , HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 ,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"]})  || Triggers(run , HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ"]})'
                
                trigger['ElectronMuon']['Data'][era]['SingleEG'] = '!(Triggers(run, HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]})|| Triggers(run , HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]})|| Triggers(run,HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]})) && (Triggers(run , HLT_passEle32WPTight, {DiLepton_slc_run["HLT_passEle32WPTight"]}))'
                trigger['ElectronMuon']['Data'][era]['SingleMuon'] = '!(Triggers( run , HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers( run , HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run , HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]})) && Triggers(run , HLT_IsoMu27 , {DiLepton_slc_run["HLT_IsoMu27"]})'
                trigger['ElectronMuon']['Data'][era]['MuonEG'] = 'Triggers( run , HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ ,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]})|| Triggers(run, HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers( run , HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]})'

            
            else:
                trigger['DoubleElectron']['Data'][era]['SingleEG'] = '!Triggers(run , HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL,{DiLepton_slc_run["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL"]}) && ( Triggers( run ,HLT_passEle32WPTight , {DiLepton_slc_run["HLT_passEle32WPTight"]} ) )'
                trigger['DoubleMuon']['Data'][era]['SingleMuon'] = 'Triggers( run , HLT_IsoMu27,{DiLepton_slc_run["HLT_IsoMu27"]}) &&!(Triggers( run , HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"]}) || Triggers( run , HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"]}))'
                trigger['DoubleMuon']['Data'][era]['DoubleMuon'] = 'Triggers(run , HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 ,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"]})  || Triggers(run , HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"]})'
                
                trigger['ElectronMuon']['Data'][era]['SingleEG'] = '!(Triggers(run, HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]})|| Triggers(run , HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]})|| Triggers(run,HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run,HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]})) && ( Triggers(run , HLT_passEle32WPTight, {DiLepton_slc_run["HLT_passEle32WPTight"]}))'
                trigger['ElectronMuon']['Data'][era]['SingleMuon'] = '!(Triggers( run , HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers( run , HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run , HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run,HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]})) && Triggers(run , HLT_IsoMu27 , {DiLepton_slc_run["HLT_IsoMu27"]})'
                trigger['ElectronMuon']['Data'][era]['MuonEG'] = 'Triggers( run , HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ ,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]})|| Triggers(run, HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers( run , HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run,HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]})'

    

    elif year =='2018':
        trigger['DoubleElectron']['MC'] = 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_Ele32_WPTight_Gsf '     
        trigger['DoubleMuon']['MC'] = 'HLT_IsoMu27||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'
        trigger['ElectronMuon']['MC'] = 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Ele32_WPTight_Gsf || HLT_IsoMu27 '
        
        for era in eras:
            trigger['DoubleElectron']['Data'][era]['SingleEG'] = '!Triggers(run , HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL, {DiLepton_slc_run["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL"]}) && Triggers(run , HLT_Ele32_WPTight_Gsf , {DiLepton_slc_run["HLT_Ele32_WPTight_Gsf"]})'
            trigger['DoubleElectron']['Data'][era]['DoubleEG'] = 'Triggers(run , HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL, {DiLepton_slc_run["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL"]})'
            trigger['DoubleMuon']['Data'][era]['SingleMuon'] = '!(Triggers(run , HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 , {DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"]}) || Triggers(run , HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"]})) && Triggers(run, HLT_IsoMu27,{DiLepton_slc_run["HLT_IsoMu27"]})'
            trigger['DoubleMuon']['Data'][era]['DoubleMuon'] = '(Triggers(run , HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 , {DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"]}) || Triggers(run , HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8,{DiLepton_slc_run["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"]}))'

            trigger['ElectronMuon']['Data'][era]['SingleEG'] = '!(Triggers(run, HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run , HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]}) ||Triggers(run , HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]} ) || Triggers(run , HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) ) && (Triggers(run , HLT_Ele32_WPTight_Gsf,{DiLepton_slc_run["HLT_Ele32_WPTight_Gsf"]}))'
            trigger['ElectronMuon']['Data'][era]['SingleMuon'] = '!(Triggers(run, HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run , HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]}) ||Triggers(run , HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]} ) || Triggers(run , HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) ) && (Triggers(run , HLT_IsoMu27, {DiLepton_slc_run["HLT_IsoMu27"]}))'
            trigger['ElectronMuon']['Data'][era]['MuonEG'] = '(Triggers(run, HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]}) || Triggers(run , HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL,{DiLepton_slc_run["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]}) ||Triggers(run , HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,{DiLepton_slc_run["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]} ) || Triggers(run , HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ, {DiLepton_slc_run["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]}) )'



    with open(f'./data/year{year}/DrellYan/configuration/DiLepton_Trigger.json','wt')  as f:
        json.dump(trigger,f,indent=4)
    

    print("Dilepton HLT Triggers for Data:")
    
    for channel in trigger.keys():
        print(f"Channel: {channel}")

        for era in trigger[channel]['Data'].keys():
            print(f"Era :{era}")
            for dataset in trigger[channel]['Data'][era].keys():
                print(f"{dataset} : {trigger[channel]['Data'][era][dataset]}")
            
        print("Dilepton HLT Triggers for MC:")
        
        print(f'Monte Carlo : {trigger[channel]["MC"]}')





