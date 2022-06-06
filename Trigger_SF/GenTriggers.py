import json




def gen_triggers(year:str):
    
    print('Generate Triggers for Dilepton Channel.')
    A = dict()
    A['Data'] = dict()
    A['MC']  = dict()

    for Sample in ['Data','MC']:
        for channel in ['DoubleElectron','DoubleMuon','ElectronMuon']:
            A[Sample][channel] = dict() 

    if year == '2016apv':
        eras = ['B2','C','D','E','F']  
    elif year == '2016postapv':
        eras = ['F','G','H']  
    elif year== '2017':
        eras = ['B','C','D','E','F']
    elif year== '2018':
        eras = ['A','B','C','D_0','D_1']
    
    for channel in ['DoubleElectron','DoubleMuon','ElectronMuon']:
        A['Data'][channel] = dict()
        A['MC'][channel] = dict()
        for era in eras:
            A['Data'][channel][era] = dict()

    if year =='2016postapv':

        A['MC']['DoubleElectron'] = ['HLT_Ele27_WPTight_Gsf','HLT_passEle32WPTight','HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ']
        A['MC']['DoubleMuon']=['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ ','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ','HLT_IsoMu27']
        A['MC']['ElectronMuon'] = ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ','HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ','HLT_Ele27_WPTight_Gsf','HLT_IsoTkMu24','HLT_IsoMu27','HLT_passEle32WPTight']
        
        for era in eras:

            A['Data']['DoubleElectron'][era]['HLT_Ele27_WPTight_Gsf'] = []
            A['Data']['DoubleElectron'][era]['HLT_passEle32WPTight'] = [-1]
            A['Data']['DoubleElectron'][era]['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] = []
            
            A['Data']['DoubleMuon'][era]['HLT_IsoMu27'] = [-1]
            
            A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] = []
            A['Data']['ElectronMuon'][era]['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ']  = [] 
            A['Data']['ElectronMuon'][era]['HLT_Ele27_WPTight_Gsf'] = []
            A['Data']['ElectronMuon'][era]['HLT_IsoTkMu24'] = []
            A['Data']['ElectronMuon'][era]['HLT_IsoMu27'] = [-1]
            A['Data']['ElectronMuon'][era]['HLT_passEle32WPTight'] = [-1]


            if era == 'H':
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'] = []
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'] =[]
            
            else:
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'] = []
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'] = []
                
                for i in range(273158,281640):
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(i)
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(i)
                    
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(281975)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(281975)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(282708)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(282708)

                for i in range(283059,283271):
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(i)
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(i)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(283478)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(283478)

                for i in range(283059,283835):
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(i)
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(i)

                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(283884)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(283884)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(283946)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(283946)

                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(284029)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(284029)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(284036)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(284036)
                for i in range(284038,284040):
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(i)
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(i)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(284042)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(284042)



            for i in range(273158,284045):
                A['Data']['DoubleElectron'][era]['HLT_Ele27_WPTight_Gsf'].append(i)
                A['Data']['DoubleElectron'][era]['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_Ele27_WPTight_Gsf'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_IsoTkMu24'].append(i)
                if era =='H':
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'].append(i)
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'].append(i)
                



    elif year == '2016apv':
        A['MC']['DoubleElectron'] = ['HLT_Ele27_WPTight_Gsf','HLT_passEle32WPTight','HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ']
        A['MC']['DoubleMuon'] = ['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL','HLT_IsoMu27']
        A['MC']['ElectronMuon'] = ['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL','HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ','HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL','HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL','HLT_Ele27_WPTight_Gsf','HLT_IsoMu24','HLT_IsoTkMu24','HLT_IsoMu27','HLT_passEle32WPTight']
        for era in eras:
            
            A['Data']['DoubleElectron'][era]['HLT_Ele27_WPTight_Gsf'] = []
            A['Data']['DoubleElectron'][era]['HLT_passEle32WPTight'] = [-1]
            A['Data']['DoubleElectron'][era]['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] = []
            

            for i in range(273158,284045):
                A['Data']['DoubleElectron'][era]['HLT_Ele27_WPTight_Gsf'].append(i)
                A['Data']['DoubleElectron'][era]['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'].append(i)
            
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'] = []
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL']= []
            A['Data']['DoubleMuon'][era]['HLT_IsoMu27'] = [-1]


            for i in range(273158,281640):
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(i)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(i)

            for i in range(283059,283270):
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(i)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(i)
            
            for i in range(283682,283835):
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(i)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(i)

            
            for i in range(284038,284040):
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(i)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(i)



            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(281975)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(282708)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(283478)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(283884)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(283946)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(284029)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(284036)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'].append(284042)

            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(281975)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(282708)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(283478)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(283884)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(283946)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(284029)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(284036)
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'].append(284042)


            
            if era=='F':
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] = [i for i in range(278273,284045)]
                A['Data']['ElectronMuon'][era]['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'] = [i for i in range(278273,284045)]

            else:
                A['Data']['ElectronMuon'][era]['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL'] = []

                for i in range(273158,280386):
                    A['Data']['ElectronMuon'][era]['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL'].append(i)
                
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'] = [ i for i in range(273158,281640)]
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(281975)
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(282708)
            
                for i in range(283059,283271):
                    A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(i)

                for i in range(283682,283835):
                    A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(i)

                for i in range(284038,284040):
                    A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(i)

                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(283478)
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(283884)
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(283946)
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(284029)
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(284036)
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(284042)

            A['Data']['ElectronMuon'][era]['HLT_Ele27_WPTight_Gsf'] = []
            A['Data']['ElectronMuon'][era]['HLT_IsoTkMu24'] = []
            A['Data']['ElectronMuon'][era]['HLT_IsoMu27'] = [-1]
            A['Data']['ElectronMuon'][era]['HLT_passEle32WPTight'] = [-1]
            for i in range(273158,284045):
                A['Data']['ElectronMuon'][era]['HLT_Ele27_WPTight_Gsf'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_IsoTkMu24'].append(i)

    
    with open(f'./data/year{year}/TriggerSF/configuration/DiLeptonTriggers.json','w') as f:
        json.dump(A,f,indent=1)

