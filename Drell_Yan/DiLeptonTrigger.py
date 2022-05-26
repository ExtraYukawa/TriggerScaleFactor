import json




def GenPaths_HLTTriggerCondition_ForAnalyzer_File(year:str):
    '''
    
    Build JSON file to record trigger conditions for Each particular channels used in Analyzer condition.
    
    '''

    trigger =dict()
    trigger['MC'] = dict()
    trigger['MC']['DoubleElectron'] = dict()
    trigger['MC']['DoubleMuon'] = dict()
    trigger['MC']['ElectronMuon'] = dict()

    trigger['Data'] = dict()
    trigger['Data']['DoubleElectron'] = dict()
    trigger['Data']['DoubleMuon'] = dict()
    trigger['Data']['ElectronMuon'] = dict()
    
    with open(f'./data/year{year}/DrellYan/configuration/Phys_process.json') as f:
        Phys_Process = json.load(f)
    
    
    for dataset in ["SingleEG","DoubleEG"]:
        trigger['Data']["DoubleElectron"][dataset] = dict()
    trigger['Data']['ElectronMuon']['SingleEG'] = dict()
    
    for dataset in  ['SingleMuon','DoubleMuon']:

        trigger['Data']['DoubleMuon'][dataset]  = dict()        

    trigger['Data']['ElectronMuon']['SingleMuon'] = dict()
    trigger['Data']['ElectronMuon']['MuonEG'] = dict()
    
    for process in Phys_Process.keys():
        for channel in ['DoubleElectron','DoubleMuon','ElectronMuon']:
            trigger['MC'][channel][process] = dict()


    if year=='2017':
        #DoubleElectron

        for era in ["B","C","D","E","F"]:
            trigger['Data']['DoubleElectron']['SingleEG'][era]  = "!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL ) &&(HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf )"
            if era in ["D","E","F"]:
                trigger['Data']['DoubleElectron']['SingleEG'][era]  = "!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL ) &&(HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf || HLT_Ele32_WPTight_Gsf)"
                
            trigger['Data']['DoubleElectron']['DoubleEG'][era] = "(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL )"
        
        for process in Phys_Process.keys():
            for phys_name in Phys_Process[process]:
                trigger['MC']['DoubleElectron'][process][phys_name] = "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf || HLT_Ele32_WPTight_Gsf"
        

        #DoubleMuon
        trigger['Data']['DoubleMuon']['DoubleMuon']['B'] = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ"
        for era in ["C","D","E","F"]:
            trigger['Data']['DoubleMuon']['DoubleMuon'][era] = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"

        trigger['Data']['DoubleMuon']['SingleMuon']['B'] = "HLT_IsoMu27 && !(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ)"
        for era in ["C","D","E","F"]:
            trigger['Data']['DoubleMuon']['SingleMuon'][era] = "HLT_IsoMu27 && !(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)"

        for process in Phys_Process.keys():
            for phys_name in Phys_Process[process]:
                trigger['MC']['DoubleMuon'][process][phys_name] = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 || HLT_IsoMu27 "

        
        #ElectronMuon

        for era in ["B","C","D","E","F"] :
            if era in ["B"] :
                trigger['Data']['ElectronMuon']['SingleEG'][era] = "!(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ ||HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ)&&(HLT_Ele35_WPTight_Gsf || HLT_passEle32WPTight)"
                trigger['Data']['ElectronMuon']['MuonEG'][era] = "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ ||  HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"
                trigger['Data']['ElectronMuon']['SingleMuon'][era] = "!(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && HLT_IsoMu27"
            else:
                trigger['Data']['ElectronMuon']['SingleEG'][era] = "!(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ ||HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ)&&(HLT_Ele35_WPTight_Gsf || HLT_passEle32WPTight ||HLT_Ele32_WPTight_Gsf)"
                trigger['Data']['ElectronMuon']['MuonEG'][era] = "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ ||  HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"
                trigger['Data']['ElectronMuon']['SingleMuon'][era] = "!(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && HLT_IsoMu27"


        for process in Phys_Process.keys():
            for phys_name in Phys_Process[process]:
                trigger['MC']['ElectronMuon'][process][phys_name] = "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ ||  HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele35_WPTight_Gsf || HLT_passEle32WPTight || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele32_WPTight_Gsf"
        
    elif year =='2016apv':
        for era in ["B2","C","D","E","F"]:
            #DoubleElectron
            trigger["Data"]["DoubleElectron"]["SingleEG"][era] = "!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) &&(HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf)"

            trigger["Data"]["DoubleElectron"]["DoubleEG"][era] = "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"
            #DoubleMuon
            trigger["Data"]["DoubleMuon"]["SingleMuon"][era] = "!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL) && HLT_IsoMu27"
            trigger["Data"]["DoubleMuon"]["DoubleMuon"][era] = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL"
            
            #ElectronMuon
            
            if era == "F":
                trigger["Data"]["ElectronMuon"]["SingleEG"][era] = "!(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ  || HLT_IsoTkMu24) && (HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf)"
                trigger["Data"]["ElectronMuon"]["SingleMuon"][era] = "!(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoTkMu24 ) && (HLT_IsoMu27)"

                trigger["Data"]["ElectronMuon"]["MuonEG"][era] = "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_IsoTkMu24"
            else:
                trigger["Data"]["ElectronMuon"]["SingleEG"][era] = "!(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL|| HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL  || HLT_IsoTkMu24) && (HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf)"
                trigger["Data"]["ElectronMuon"]["SingleMuon"][era] = "!(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL || HLT_IsoTkMu24 ) && (HLT_IsoMu27)"

                trigger["Data"]["ElectronMuon"]["MuonEG"][era] = "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL|| HLT_IsoTkMu24"

        for process in Phys_Process.keys():
            for phys_name in Phys_Process[process]:
                trigger["MC"]["DoubleElectron"][process][phys_name] = " HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf"
                trigger["MC"]["DoubleMuon"][process][phys_name] = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL || HLT_IsoMu27"
                trigger["MC"]["ElectronMuon"][process][phys_name]= "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ||HLT_IsoMu27||HLT_IsoTkMu24||HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL ||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL"

    elif year =='2016postapv':
        for era in ["F","G","H"]:
            #DoubleElectron
            trigger["Data"]["DoubleElectron"]["SingleEG"][era] = "!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) &&(HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf)"
            trigger["Data"]["DoubleElectron"]["DoubleEG"][era] = " HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"
            trigger["Data"]["ElectronMuon"]["SingleEG"][era] = "!(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ ) && (HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf)"
            trigger["Data"]["ElectronMuon"]["SingleMuon"][era] = "!(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ ) && (HLT_IsoMu27)"
            trigger["Data"]["ElectronMuon"]["MuonEG"][era] = "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoTkMu24"
            if era != "H":
                trigger["Data"]["DoubleMuon"]["SingleMuon"][era] = "!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL) && HLT_IsoMu27"
                trigger["Data"]["DoubleMuon"]["DoubleMuon"][era] = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL"
            else:
                trigger["Data"]["DoubleMuon"]["SingleMuon"][era] = "!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ) && HLT_IsoMu27"
                trigger["Data"]["DoubleMuon"]["DoubleMuon"][era] = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ"
        for process in Phys_Process.keys():
            for phys_name in Phys_Process[process]:
                trigger["MC"]["DoubleElectron"][process][phys_name] = "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf"
                trigger["MC"]["DoubleMuon"][process][phys_name] = "HLT_IsoMu27|| HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL|| HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ"
                trigger["MC"]["ElectronMuon"][process][phys_name] = " HLT_IsoTkMu24 || HLT_IsoMu27 || HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"
    elif year == '2018':
        for era in ["A","B","C","D_0","D_1"]:
            trigger["Data"]["DoubleElectron"]["SingleEG"][era] = "!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && (HLT_Ele32_WPTight_Gsf || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf )"
            trigger["Data"]["DoubleElectron"]["DoubleEG"][era] = "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL"
            trigger["Data"]["DoubleMuon"]["SingleMuon"][era] = "!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)&& HLT_IsoMu27"
            trigger["Data"]["DoubleMuon"]["DoubleMuon"][era] = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"

            trigger["Data"]["ElectronMuon"]["SingleEG"][era]  = "!(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_Ele32_WPTight_Gsf || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf )"
            trigger["Data"]["ElectronMuon"]["SingleMuon"][era] = "!(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && HLT_IsoMu27"
            trigger["Data"]["ElectronMuon"]["MuonEG"][era] = "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"


            for process in Phys_Process.keys():
                for phys_name in Phys_Process[process]:
                    trigger["MC"]["DoubleElectron"][process][phys_name] = "HLT_Ele32_WPTight_Gsf || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL"
                    trigger["MC"]["DoubleMuon"][process][phys_name] = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_IsoMu27 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"
                    trigger["MC"]["ElectronMuon"][process][phys_name] = "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ|| HLT_Ele32_WPTight_Gsf|| HLT_IsoMu27|| HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf"




    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/DrellYan/configuration/HLTTriggerCondition.json','wt')  as f:
        json.dump(trigger,f,indent=4)
    

    print("Dilepton HLT Triggers for Data:")
    
    for channel in trigger["Data"].keys():
        print(f"Channel: {channel}")

        for dataset in trigger["Data"][channel].keys():
            print(f"Dataset:{dataset}")
            for era in trigger["Data"][channel][dataset].keys():
                print(f'{era} : {trigger["Data"][channel][dataset][era]}')
            
    print("Dilepton HLT Triggers for MC:")
        
    for channel in trigger["MC"].keys():
        print(f'{channel} : {trigger["MC"][channel]["DY"]["DYnlo"]}')





