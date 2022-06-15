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

        A['MC']['DoubleElectron'] = ['HLT_Ele27_WPTight_Gsf','HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ']
        A['MC']['DoubleMuon']=['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ ','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ','HLT_IsoMu27']
        A['MC']['ElectronMuon'] = ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ','HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ','HLT_Ele27_WPTight_Gsf','HLT_IsoTkMu24','HLT_IsoMu27']
        
        for era in eras:

            A['Data']['DoubleElectron'][era]['HLT_Ele27_WPTight_Gsf'] = []
            A['Data']['DoubleElectron'][era]['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] = []
            
            A['Data']['DoubleMuon'][era]['HLT_IsoMu27'] = [-1]
            
            A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] = []
            A['Data']['ElectronMuon'][era]['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ']  = [] 
            A['Data']['ElectronMuon'][era]['HLT_Ele27_WPTight_Gsf'] = []
            A['Data']['ElectronMuon'][era]['HLT_IsoTkMu24'] = []
            A['Data']['ElectronMuon'][era]['HLT_IsoMu27'] = []


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
                A['Data']['ElectronMuon'][era]['HLT_IsoMu27'].append(i)
                if era =='H':
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'].append(i)
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'].append(i)

    elif year == '2016apv':
        A['MC']['DoubleElectron'] = ['HLT_Ele27_WPTight_Gsf','HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ']#'HLT_passEle32WPTight','HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ']
        A['MC']['DoubleMuon'] = ['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL','HLT_IsoMu27']
        A['MC']['ElectronMuon'] = ['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ','HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL','HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL','HLT_Ele27_WPTight_Gsf','HLT_IsoTkMu24','HLT_IsoMu27']#,'HLT_passEle32WPTight']
        for era in eras:
            
            A['Data']['DoubleElectron'][era]['HLT_Ele27_WPTight_Gsf'] = []
            #A['Data']['DoubleElectron'][era]['HLT_passEle32WPTight'] = [-1]
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
            A['Data']['ElectronMuon'][era]['HLT_IsoMu27'] = []
            for i in range(273158,284045):
                A['Data']['ElectronMuon'][era]['HLT_Ele27_WPTight_Gsf'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_IsoTkMu24'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_IsoMu27'].append(i)
    elif year == '2018':
        A['MC']['DoubleElectron'] = ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL','HLT_Ele32_WPTight_Gsf']
        A['MC']['DoubleMuon'] = ['HLT_IsoMu27','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8']
        A['MC']['ElectronMuon'] = ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ','HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL','HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ','HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ','HLT_Ele32_WPTight_Gsf','HLT_IsoMu27']

        for era in eras:
            A['Data']['DoubleElectron'][era]['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL']=[]
            A['Data']['DoubleElectron'][era]['HLT_Ele32_WPTight_Gsf']=[]

            A['Data']['DoubleMuon'][era]['HLT_IsoMu27']=[]
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8']=[]
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8']=[]

            A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ']=[]
            A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL']=[]
            A['Data']['ElectronMuon'][era]['HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ']=[]
            A['Data']['ElectronMuon'][era]['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ']=[]
            A['Data']['ElectronMuon'][era]['HLT_Ele32_WPTight_Gsf']=[]
            A['Data']['ElectronMuon'][era]['HLT_IsoMu27']=[]
            
            for i in range(315257,325173):

                A['Data']['DoubleElectron'][era]['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'].append(i)
                A['Data']['DoubleElectron'][era]['HLT_Ele32_WPTight_Gsf'].append(i)

                A['Data']['DoubleMuon'][era]['HLT_IsoMu27'].append(i)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8'].append(i)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'].append(i)

                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_Ele32_WPTight_Gsf'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_IsoMu27'].append(i)

    elif year == '2017':

        A['MC']['DoubleElectron'] = ['HLT_passEle32WPTight','HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL']#,'HLT_Ele35_WPTight_Gsf']
        A['MC']['DoubleMuon'] = ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8','HLT_IsoMu27','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8']
        A['MC']['ElectronMuon'] = ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL','HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ','HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ','HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ','HLT_IsoMu27','HLT_passEle32WPTight']
            
        for era in eras:

            A['Data']['DoubleElectron'][era]['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'] = []
            #A['Data']['DoubleElectron'][era]['HLT_Ele35_WPTight_Gsf'] = []
            A['Data']['DoubleElectron'][era]['HLT_passEle32WPTight'] = [-1]
            
            A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8'] = []
            A['Data']['DoubleMuon'][era]['HLT_IsoMu27'] = []
            
            A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] = []
            A['Data']['ElectronMuon'][era]['HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'] = []
            A['Data']['ElectronMuon'][era]['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'] = []

            A['Data']['ElectronMuon'][era]['HLT_IsoMu27'] = []
            A['Data']['ElectronMuon'][era]['HLT_passEle32WPTight'] = [-1]
            #A['Data']['ElectronMuon'][era]['HLT_Ele35_WPTight_Gsf'] = []

            #for i in range(302026,306461):
            #    A['Data']['DoubleElectron'][era]['HLT_Ele35_WPTight_Gsf'].append(i)

            for i in range(297050,306461):
                A['Data']['DoubleElectron'][era]['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'].append(i)
                A['Data']['DoubleMuon'][era]['HLT_IsoMu27'].append(i)
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'].append(i)
                A['Data']['ElectronMuon'][era]['HLT_IsoMu27'].append(i)
                #A['Data']['ElectronMuon'][era]['HLT_Ele35_WPTight_Gsf'].append(i)


            if era != 'B':
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'] = []
                A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'] = []
            
                for i in range(299368,306461):
                    A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'].append(i)
                    A['Data']['ElectronMuon'][era]['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'].append(i)

            else:
                T = []

                for i in range(297050,299370):
                    T.append(i)
                T.append(299380)
                for i in range(299394,299396):
                    T.append(i)
                for i in range(299477,299481):
                    T.append(i)
                for i in range(299593,299596):
                    T.append(i)
                for i in range(300087,300107):
                    T.append(i)
                for i in range(300122,300156):
                    T.append(i)
                for i in range(300233,300284):
                    T.append(i)
                for i in range(300364,300375):
                    T.append(i)
                for i in range(300389,300401):
                    T.append(i)

                for i in range(300459,300467):
                    T.append(i)

                for i in range(300497,300517):
                    T.append(i)
                T.append(300558)
                for i in range(300574,300576):
                    T.append(i)

                for i in range(300631,300633):
                    T.append(i)

                T.append(300635)
                for i in range(300674,300676):
                    T.append(i)

                for i in range(300777,300781):
                    T.append(i)

                for i in range(300806,300817):
                    T.append(i)
                    
                T.append(301161)
                for i in range(301179,301181):
                    T.append(i)

                T.append(301281)

                for i in range(301391,301393):
                    T.append(i)
                for i in range(301396,301398):
                    T.append(i)
                for i in range(301447,301450):
                    T.append(i)

                T.append(301475)
                T.append(301519)
                for i in range(301529,301532):
                    T.append(i)
                T.append(301664)
                T.append(301912)
                T.append(301913)
                T.append(301959)
                for i in range(301984,301987):
                    T.append(i)
                T.append(301997)

                for i in range(302026,302043):
                    T.append(i)

                for i in range(302163,302166):
                    T.append(i)
                
                T.append(302262)

                T.append(302279)
                for i in range(302337,302344):
                    T.append(i)


                T.append(302392)

                T.append(302472)
                T.append(302473)
                T.append(302475)
                for i in range(302485,302494):
                    T.append(i)

                for i in range(302522,302526):
                    T.append(i)

                for i in range(302548,302555):
                    T.append(i)
                for i in range(302565,302573):
                    T.append(i)
                
                T.append(302596)
                T.append(302634)
                T.append(302651)
                T.append(302661)
                T.append(303998)
                T.append(303999)
                T.append(304119)
                T.append(304120)
                T.append(304169)
                T.append(304199)
                T.append(304291)

                for i in range(304446,304508):
                    T.append(i)
                T.append(304625)
                T.append(304654)
                T.append(304661)
                T.append(304662)
                T.append(304671)

                for i in range(304737,304740):
                    T.append(i)
                T.append(304776)
                T.append(304777)
                T.append(305044)
                T.append(305045)
                for i in range(305059,305064):
                    T.append(i)
                T.append(305112)
                T.append(305113)

                for i in range(305178,305185):
                    T.append(i)

                T.append(305202)
                T.append(305207)

                for i in range(305234,305237):
                    T.append(i)
                T.append(305247)
                T.append(305248)
                for i in range(305310,305314):
                    T.append(i)
                for i in range(305336,305351):
                    T.append(i)
                
                for i in range(305358,305366):
                    T.append(i)

                T.append(305405)
                T.append(305440)
                T.append(305516)
                T.append(305517)
                T.append(305589)
                T.append(305840)
                T.append(306029)
                
                for i in range(306036,306049):
                    T.append(i)
                T.append(306091)
                T.append(306092)
                for i in range(306121,306126):
                    T.append(i)
                T.append(306134)
                T.append(306138)

                for i in range(306153,306171):
                    T.append(i)

                T.append(306418)
                T.append(306419)
                T.append(306422)
                T.append(306423)
                T.append(306454)
                T.append(306460)
            
                A['Data']['DoubleMuon'][era]['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'] = T

    
    with open(f'./data/year{year}/TriggerSF/configuration/DiLeptonTriggers.json','w') as f:
        json.dump(A,f,indent=1)

