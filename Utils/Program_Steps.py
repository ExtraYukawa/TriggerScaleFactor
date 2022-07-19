import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import ROOT,json
import time

def RuntimeMeasure(args):
    start = time.time()
    if args.mode == 'TrigEff_Calc':
        func = Trig_Calc
    elif args.mode  == 'TrigEff_Plot':
        func = Plot_efficiency
    elif args.mode == 'TrigSF_Calc':
        func = SF_Calc
    #elif args.mode == 'DrellYanRECO':
    #    func = Drell_Yan_Reconstruction
    elif  args.mode == 'FakeRate':
        func = FakeRateCalculation
    elif args.mode =='PhysProcessRECO':
        func = PhysProcessRECO
    elif args.mode =='NEventsCount':
        func = EventCounter
    else:
        raise ValueError(f'No such mode: {args.mode}')
    
    func(args)
    print(time.time() - start)


def FakeRateCalculation(args):
    ROOT.gInterpreter.ProcessLine('#include "include/FakeRate_Utils.h"') 
    ROOT.gSystem.Load('./myLib/FakeRate_Utils_cpp.so')
    ROOT.gInterpreter.ProcessLine('#include "include/IDScaleFactor.h"') 
    ROOT.gSystem.Load('./myLib/IDScaleFactor_cpp.so')
    print('./myLib/myLib.so is Loaded.')
    
    if args.year is None:
        raise ValueError('Arguments [year] must be speicified.')
    if args.channel == 'None':
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")

    settings = dict()
    settings['year'] = args.year
    settings['channel'] = args.channel
    settings['nevents'] = args.nevents
    
    settings['SF_mode']  = args.SF_mode


    with open(f'./data/year{args.year}/FakeRate/configuration/filters.json', 'rb') as f:
        structure = json.load(f)
        settings['LeptonFilters'] = structure[args.channel]
        settings['QCDFilters'] = structure[args.channel+'QCD']


    with open(f'./data/year{args.year}/FakeRate/path/FilesIn.json','rb') as f:
        FilesIn= json.load(f)
        settings['Data_FilesIn']= FilesIn['Data'][args.channel]
        settings['MC_Lepton'] = FilesIn['MC']['Lepton']
        settings['MC_QCD'] = FilesIn['MC'][args.channel+'QCD']

    with open(f'./data/year{args.year}/DrellYan/path/triggerSF.json','rb') as f:
        structure = json.load(f)
        settings['path'] = structure['file']['Double'+args.channel]
        settings['branchname'] = structure['branchname']
    with open(f'./data/year{args.year}/TriggerSF/configuration/weights.json','rb') as f :
        settings['weight_set'] = '*'.join(json.load(f)['MC'])
    from Fake_Rate.Analyzer import FakeRateAnalyzer
    
    FakeRateAnalyzer(settings)

def EventCounter(args):
    from PhysProcessRECO.NEvents_Counter import NEvents_Counter
    if args.year is None:
        raise ValueError('Arguments [year] must be speicified.')
    if args.channel == 'None':
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")
    if args.ylog == 1:
        print('Setting y scale to be log scale...')

    settings = dict()
    settings['year'] = args.year
    settings['channel'] = args.channel
    settings['nevents'] = args.nevents
    settings['veto'] = args.veto
    settings['debug'] = args.debug
    settings['ylog'] = args.ylog
    settings['TrigSF']= args.TrigSF
    settings['IDSF'] = args.IDSF
    settings['RECOSF'] = args.RECOSF
    settings['CFSF'] = args.CFSF
    settings['Eras'] = args.Eras
    settings['lumi'] = args.lumi
    settings['region'] = args.region
    settings['FakeRate'] = args.FakeRate
    settings['CtagSF']  = args.CtagSF

    if args.CtagSF:
        with open(f'./data/year{args.year}/PhysProcessRECO/path/CtagShape.json','rb') as f:
            settings['CtagSFInfo'] = json.load(f)
            print(settings['CtagSFInfo'])
    with open(f'./data/year{args.year}/PhysProcessRECO/configuration/data_xs.json','rb') as f:
        structure = json.load(f)
        settings['xs'] = structure['xs']
        settings['NumberOfEvents'] = structure['NumberOfEvents'] 
        settings['Process'] = structure['Process']
    with open(f'./data/year{args.year}/PhysProcessRECO/path/datapath.json','rb') as f :
        settings['FilesIn'] = json.load(f)
    
    with open(f'./data/year{args.year}/PhysProcessRECO/path/triggerSF.json','rb') as f:
        settings['trigSFInfo'] = json.load(f)

    with open(f'./data/year{args.year}/TriggerSF/configuration/weights.json','rb') as f:
        settings['Weights'] = json.load(f)
    
    with open(f'./data/year{args.year}/TriggerSF/path/LeptonsID_SF.json','rb') as f:
        settings['LepIDSF_File'] = json.load(f)[args.channel]
    
    with open(f'./data/year{args.year}/PhysProcessRECO/path/FakeRateFiles.json','rb') as f:
        settings['FakeRateFiles'] = json.load(f)

    
    with open(f"./data/year{args.year}/PhysProcessRECO/configuration/MET_Filters.json","r") as f:
        settings['MET_Filters'] = json.load(f)
    

    with open(f'./data/year{args.year}/PhysProcessRECO/configuration/data_xs.json','rb') as f:

        settings['Phys_Process'] = json.load(f)

    with open(f'./data/year{args.year}/PhysProcessRECO/configuration/DiLepton_Trigger.json','rb')  as f:
        settings['DiLep_Conditions'] = json.load(f)[args.channel]
        
    with open(f'./data/year{args.year}/TriggerSF/configuration/DiLeptonTriggers.json','rb')  as f:
        settings['DiLepton_Triggers'] = json.load(f)['Data'][args.channel] # Implemented only in Data
    ROOT.gInterpreter.ProcessLine('#include "./include/Triggers.h"')
    ROOT.gSystem.Load('./myLib/Triggers_cpp.so')
    print('./include/Triggers.h is Loaded.')
    ROOT.gInterpreter.ProcessLine('#include "./include/ScaleFactor.h"')
    print('./include/ScaleFactor.h is Loaded.')
    ROOT.gSystem.Load('./myLib/ScaleFactor_cpp.so')
    print('./myLib/myLib.so is Loaded.')



    Az = NEvents_Counter(settings)
    Az.Run()


def PhysProcessRECO(args):
    from PhysProcessRECO.Analyzer import Analyzer 
    if args.year is None:
        raise ValueError('Arguments [year] must be speicified.')
    if args.channel == 'None':
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")
    if args.ylog == 1:
        print('Setting y scale to be log scale...')

    settings = dict()
    settings['year'] = args.year
    settings['channel'] = args.channel
    settings['nevents'] = args.nevents
    settings['veto'] = args.veto
    settings['debug'] = args.debug
    settings['ylog'] = args.ylog
    settings['TrigSF']= args.TrigSF
    settings['IDSF'] = args.IDSF
    settings['RECOSF'] = args.RECOSF
    settings['CFSF'] = args.CFSF
    settings['Eras'] = args.Eras
    settings['lumi'] = args.lumi
    settings['region'] = args.region
    settings['FakeRate'] = args.FakeRate
    settings['CtagSF']  = args.CtagSF


    with open(f'./data/year{args.year}/PhysProcessRECO/configuration/data_xs.json','rb') as f:
        structure = json.load(f)
        settings['xs'] = structure['xs']
        settings['NumberOfEvents'] = structure['NumberOfEvents'] 
        settings['Process'] = structure['Process']
    with open(f'./data/year{args.year}/PhysProcessRECO/path/datapath.json','rb') as f :
        settings['FilesIn'] = json.load(f)
    
    with open(f'./data/year{args.year}/PhysProcessRECO/path/triggerSF.json','rb') as f:
        settings['trigSFInfo'] = json.load(f)
    if args.CtagSF:
        with open(f'./data/year{args.year}/PhysProcessRECO/path/CtagShape.json','rb') as f:
            settings['CtagSFInfo'] = json.load(f)

    with open(f'./data/year{args.year}/TriggerSF/configuration/weights.json','rb') as f:
        settings['Weights'] = json.load(f)
    
    with open(f'./data/year{args.year}/TriggerSF/path/LeptonsID_SF.json','rb') as f:
        settings['LepIDSF_File'] = json.load(f)[args.channel]
    
    with open(f'./data/year{args.year}/PhysProcessRECO/path/FakeRateFiles.json','rb') as f:
        settings['FakeRateFiles'] = json.load(f)

    
    with open(f"./data/year{args.year}/PhysProcessRECO/configuration/MET_Filters.json","r") as f:
        settings['MET_Filters'] = json.load(f)
    

    with open(f'./data/year{args.year}/PhysProcessRECO/configuration/data_xs.json','rb') as f:

        settings['Phys_Process'] = json.load(f)

    with open(f'./data/year{args.year}/PhysProcessRECO/configuration/DiLepton_Trigger.json','rb')  as f:
        settings['DiLep_Conditions'] = json.load(f)[args.channel]
        
    with open(f'./data/year{args.year}/TriggerSF/configuration/DiLeptonTriggers.json','rb')  as f:
        settings['DiLepton_Triggers'] = json.load(f)['Data'][args.channel] # Implemented only in Data
    ROOT.gInterpreter.ProcessLine('#include "./include/Triggers.h"')
    ROOT.gSystem.Load('./myLib/Triggers_cpp.so')
    print('./include/Triggers.h is Loaded.')
    ROOT.gInterpreter.ProcessLine('#include "./include/ScaleFactor.h"')
    print('./include/ScaleFactor.h is Loaded.')
    ROOT.gSystem.Load('./myLib/ScaleFactor_cpp.so')
    print('./myLib/myLib.so is Loaded.')



    Az = Analyzer(settings)
    Az.Run()



    """
    if args.SF_mode==3 or args.SF_mode==2:
        if args.trigSFType == 0:
            trigSFType = 'l1pteta'
        elif args.trigSFType == 1:
            trigSFType = 'l2pteta'
        elif args.trigSFType == 2:
            trigSFType = 'l1l2pt'
        elif args.trigSFType==3 :
            trigSFType = 'l1l2eta'
        else:
            raise ValueError('please specify trigSFType: [-x/--trigSFType "0,1,2,3"]')
        print(f'Trigger Scale Factor Array: {trigSFType}')
        '''
        if args.year=='2018':
            if args.veto:
                settings['TriggerSF']['FileIn'] = trigSF['file']['veto'][args.channel][trigSFType]
            else:
                settings['TriggerSF']['FileIn'] = trigSF['file']['all'][args.channel][trigSFType]
        else:
        '''
        settings['TriggerSF']['FileIn'] = trigSF['file'][args.channel][trigSFType]
        settings['TriggerSF']['branchname'] = trigSF['branchname'][trigSFType]
    else:
        print("Warning: The control region will not involve the Trigger Scale Factor.")
    """


from Drell_Yan.Analyzer import *


def Drell_Yan_Reconstruction(args):
    if args.year is None:
        raise ValueError('Arguments [year] must be speicified.')
    if args.channel == 'None':
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")
    if args.ylog == 1:
        print('Setting y scale to be log scale...')

    settings = dict()
    settings['year'] = args.year
    settings['channel'] = args.channel
    settings['nevents'] = args.nevents
    settings['SF_mode']  = args.SF_mode
    settings['veto'] = args.veto
    settings['debug'] = args.debug
    settings['ylog'] = args.ylog
    
    settings['TriggerSF']=dict()

    with open(f'./data/year{args.year}/DrellYan/configuration/data_xs.json','rb') as f:
        structure = json.load(f)
        settings['xs'] = structure['xs']
        settings['NumberOfEvents'] = structure['NumberOfEvents'] 
        settings['Process'] = structure['Process']
    with open(f'./data/year{args.year}/DrellYan/path/datapath.json','rb') as f :
        settings['FilesIn'] = json.load(f)
    
    with open(f'./data/year{args.year}/DrellYan/path/triggerSF.json','rb') as f:
        trigSF = json.load(f)

    with open(f'./data/year{args.year}/TriggerSF/configuration/weights.json','rb') as f:
        settings['Weights'] = json.load(f)
    with open(f'./data/year{args.year}/TriggerSF/path/LeptonsID_SF.json','rb') as f:
        settings['LepIDSF_File'] = json.load(f)[args.channel]
    
    
    with open(f"./data/year{args.year}/DrellYan/configuration/MET_Filters.json","r") as f:
        settings['MET_Filters'] = json.load(f)
    

    with open(f'./data/year{args.year}/DrellYan/configuration/data_xs.json','rb') as f:
        settings['Phys_Process'] = json.load(f)

    with open(f'./data/year{args.year}/DrellYan/configuration/DiLepton_Trigger.json','rb')  as f:
        settings['DiLep_Conditions'] = json.load(f)[args.channel]
        
    with open(f'./data/year{args.year}/TriggerSF/configuration/DiLeptonTriggers.json','rb')  as f:
        settings['DiLepton_Triggers'] = json.load(f)['Data'][args.channel] # Implemented only in Data
    ROOT.gInterpreter.ProcessLine('#include "./include/Triggers.h"')
    ROOT.gSystem.Load('./myLib/Triggers_cpp.so')
    print('./include/Triggers.h is Loaded.')
    if args.SF_mode==3 or args.SF_mode==2:
        if args.trigSFType == 0:
            trigSFType = 'l1pteta'
        elif args.trigSFType == 1:
            trigSFType = 'l2pteta'
        elif args.trigSFType == 2:
            trigSFType = 'l1l2pt'
        elif args.trigSFType==3 :
            trigSFType = 'l1l2eta'
        else:
            raise ValueError('please specify trigSFType: [-x/--trigSFType "0,1,2,3"]')
        print(f'Trigger Scale Factor Array: {trigSFType}')
        '''
        if args.year=='2018':
            if args.veto:
                settings['TriggerSF']['FileIn'] = trigSF['file']['veto'][args.channel][trigSFType]
            else:
                settings['TriggerSF']['FileIn'] = trigSF['file']['all'][args.channel][trigSFType]
        else:
        '''
        settings['TriggerSF']['FileIn'] = trigSF['file'][args.channel][trigSFType]
        settings['TriggerSF']['branchname'] = trigSF['branchname'][trigSFType]
    else:
        print("Warning: The control region will not involve the Trigger Scale Factor.")
    Analyzer = DrellYanRDataFrame(settings)
    Analyzer.Run()

from array import array
import Utils.CMSTDRStyle as CMSTDRStyle
import Utils.CMSstyle as CMSstyle
import Utils.mypalette as mypalette
import json
from Trigger_SF.Trig_DataFrame import *
import Trigger_SF.Trigger_Utils as TrigUtils
from Utils.General_Tool import *
import Utils.plot_settings as plt_set

def Trig_Calc(args):
    '''
    *args.year
        - 2016apv/2016postapv/2017/2018   
    *args.channel
        - DoubleElectron/DoubleMuon/ElectronMuon
    *args.veto
        - to veto HEM region or not
        - only valid for UL2018
    *Condition_Weights
        -MC:
            - PrefireWeight(UL2017),puWeight
        -Data:
            - 1.
    *HLT_Path
        - High-Level Trigger 
    *Leptons_Information
        - Leptons_Information
            - region: 1 for mumu, 2 for emu, 3 for ee
            - OPS_p4: p4 names for l1/l2 if in OPS_region
            - ttc_p4: p4 names for l1/l1 if in ttc_region
            - weight: RECO Scale factors name for l1/l2(Currently, this is deprecated)
    *Flag
        - HLT_MET Filters.
    *FileIn
        -Data: MET.root path
        -MC: TTTo2L.root path
    *LepSF_File
        -ID scale factors path and branch name
    *User
        -Path to eos space and your name
    *args.Type
        - Data / MC
    '''
    ROOT.gInterpreter.ProcessLine('#include "./include/IDScaleFactor.h"')
    ROOT.gSystem.Load('./myLib/IDScaleFactor_cpp.so')
    print('./include/IDScaleFactor.h is Loaded.')
    ROOT.gInterpreter.ProcessLine('#include "./include/Flag.h"')
    ROOT.gSystem.Load('./myLib/Flag_cpp.so')
    print('./include/Flag.h is Loaded.')
    ROOT.gInterpreter.ProcessLine('#include "./include/Lepton_Info.h"')
    ROOT.gSystem.Load('./myLib/Lepton_Info_cpp.so')
    print('./include/Lepton_Info.h is Loaded.')
    ROOT.gInterpreter.ProcessLine('#include "./include/Triggers.h"')
    ROOT.gSystem.Load('./myLib/Triggers_cpp.so')
    print('./include/Triggers.h is Loaded.')
    if args.year is None:
        raise ValueError('Arguments [year] must be speicified.')
    if args.channel == None:
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")
    if args.Type == None:
        raise ValueError("Should Specify the type of input file(s) ex:[-f/--Type MC]")
    if args.veto == True:
        print('Veto HEM region.\nRemind: The option[-v/--veto] is only valid for UL2018 Data.')
     
    with open(f'./data/year{args.year}/TriggerSF/configuration/HLT_MET.json','rb') as f:
        HLT_MET = json.load(f)[args.Type]
    with open(f'./data/year{args.year}/TriggerSF/configuration/name.json','rb') as f :
        Leptons_Information = json.load(f)[args.channel]
    with open(f'./data/year{args.year}/TriggerSF/configuration/MET_Filters.json','rb') as f :
        MET_Filters = json.load(f)[args.Type]

    with open(f'./data/year{args.year}/TriggerSF/path/filein.json','rb') as f:
        FileIn = json.load(f)[args.Type]

    with open(f'./data/year{args.year}/TriggerSF/User.json','rb') as f:
        DirOut = json.load(f)['DirOut'][args.channel]['files']
    
    with open(f'./data/year{args.year}/TriggerSF/path/LeptonsID_SF.json','rb') as f:
        LepSF_File = json.load(f)[args.channel]

    with open(f'./data/year{args.year}/TriggerSF/configuration/weights.json','rb') as f:
        Condition_Weights = json.load(f)[args.Type]
    
    with open(f'./data/year{args.year}/TriggerSF/configuration/DiLeptonTriggers.json','rb')  as f:
        DiLepton_Triggers = json.load(f)[args.Type][args.channel]

    
    setting={
        'Leptons_Information' : Leptons_Information,
        'channel' : args.channel,
        'DirOut' : DirOut,
        'FileIn' : FileIn,
        'MET_Filters':MET_Filters,
        'Type':args.Type,
        'LepSF_File':LepSF_File,
        'Year':'year'+args.year,
        'nevents':args.nevents,
        'Condition_Weights':Condition_Weights,
        'veto':args.veto,
        'debug':args.debug,
        'year':args.year
    }
    Trig_DFs = dict() 
    if args.Type=='MC':
        setting['FileIn'] = FileIn
        setting['HLT_MET'] = HLT_MET
        setting['HLT_LEP'] = DiLepton_Triggers#selection run list
        Trig_DFs['MC'] = TrigRDataFrame(setting)
        Trig_DFs['MC'].Run()
    else:
        if args.Era == ['']:
            print('Full Data!')
            eras =FileIn.keys()
        else:
            eras = args.Era
            print(eras)
        for era in eras:
            setting['FileIn'] = FileIn[era]
            setting['HLT_MET'] = HLT_MET[era]
            setting['HLT_LEP'] = DiLepton_Triggers[era]#selection run list
            for filename in setting['FileIn']:
                print('Data name with era: '+filename)
            Trig_DFs[era] = TrigRDataFrame(setting)
            Trig_DFs[era].Run()
    
    Data_Processor(Trig_DFs,DirOut=DirOut,Type=args.Type,veto=args.veto)


def Plot_efficiency(args):
    '''
    plot Trigger histograms to visualize what's in root file respectively.
    '''
    if args.channel == 'None':
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")
    if args.year == 'None':
        raise ValueError('You need to specify ex:[-y/--year 2017]')
    if args.veto == True:
        print('Veto HEM region.\n')
    
    with open(f'./data/year{args.year}/TriggerSF/User.json','rb') as f:
        User = json.load(f)
    user_settings={
            'channel':args.channel,
            'DirIn':User['DirOut'][args.channel]['files'],
            'DirOut':User['DirOut'][args.channel]['plots'],
            'colors' : {'Data':1,'MC':4},
            'year':args.year,
            'veto':args.veto
            }
    tags = {
            'l1':{
                'pt':['l1pt','l1pt_highjet','l1pt_lowjet','l1pt_highpv','l1pt_lowpv','l1pt_highmet','l1pt_lowmet'] ,
                'eta':['l1eta','l1eta_highjet','l1eta_lowjet','l1eta_highpv','l1eta_lowpv','l1eta_highmet','l1eta_lowmet'],
                'pteta':['l1pteta','l1pteta_highjet','l1pteta_lowjet','l1pteta_highpv','l1pteta_lowpv','l1pteta_highmet','l1pteta_lowmet']
            },
            'l2':{
                'pt':['l2pt','l2pt_highjet','l2pt_lowjet','l2pt_highpv','l2pt_lowpv','l2pt_highmet','l2pt_lowmet'] ,
                'eta':['l2eta','l2eta_highjet','l2eta_lowjet','l2eta_highpv','l2eta_lowpv','l2eta_highmet','l2eta_lowmet'],
                'pteta':['l2pteta','l2pteta_highjet','l2pteta_lowjet','l2pteta_highpv','l2pteta_lowpv','l2pteta_highmet','l2pteta_lowmet']
            },
            'l1l2':{
                'pt':['l1l2pt','l1l2pt_highjet','l1l2pt_lowjet','l1l2pt_highpv','l1l2pt_lowpv','l1l2pt_highmet','l1l2pt_lowmet'] ,
                'eta':['l1l2eta','l1l2eta_highjet','l1l2eta_lowjet','l1l2eta_highpv','l1l2eta_lowpv','l1l2eta_highmet','l1l2eta_lowmet'],
                }
        }

    print(f'Plotting 1D histograms for channel :{args.channel}')
    
    user_settings['Type'] = 'Trigger Efficiency 1D Histogram'
    for tag in  tags['l1']['pt']:
        TrigUtils.Plot(TrigUtils.plot_eff1d,**user_settings)(tag=tag)
    for tag in  tags['l1']['eta']:
        TrigUtils.Plot(TrigUtils.plot_eff1d,**user_settings)(tag=tag)
    for tag in  tags['l2']['pt']:
        TrigUtils.Plot(TrigUtils.plot_eff1d,**user_settings)(tag=tag)
    for tag in  tags['l2']['eta']:
        TrigUtils.Plot(TrigUtils.plot_eff1d,**user_settings)(tag=tag)
    
    print(f'Plotting 2D histograms for channel :{args.channel}')
    user_settings['Type'] = 'Trigger Efficiency 2D Histogram'
    for tag in  tags['l1']['pteta']:
        user_settings['axis'] = 'pteta'#used to classify axis title of histogram
        TrigUtils.Plot(TrigUtils.plot_eff2d,**user_settings)(tag=tag)
    for tag in  tags['l2']['pteta']:
        user_settings['axis'] = 'pteta'
        TrigUtils.Plot(TrigUtils.plot_eff2d,**user_settings)(tag=tag)
    for tag in  tags['l1l2']['pt']:
        user_settings['axis'] = 'ptpt'
        TrigUtils.Plot(TrigUtils.plot_eff2d,**user_settings)(tag=tag)
    for tag in  tags['l1l2']['eta']:
        user_settings['axis'] = 'etaeta'
        TrigUtils.Plot(TrigUtils.plot_eff2d,**user_settings)(tag=tag)
    TrigUtils.Calculate_Eff(**user_settings)

def SF_Calc(args):
    '''
    MC -> TTTo2L
    data -> MET
    '''
    if args.channel == 'None':
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")
    if args.year == 'None':
        raise ValueError('You need to specify ex:[-y/--year 2017]')
    if args.veto == True:
        print('Veto HEM region.\n')
    
    with open(f'./data/year{args.year}/TriggerSF/User.json','rb') as f:
        User = json.load(f)
    settings={
            'channel':args.channel,
            'DirIn':User['DirOut'][args.channel]['files'],
            'DirOut':User['DirOut'][args.channel]['plots'],
            'year':args.year,
            'veto':args.veto
            }
    
    nominal_names =['l1pteta','l2pteta','l1l2pt','l1l2eta']
    
    print('Producing TriggerSF...')
    for nominal_name in nominal_names:
        TrigUtils.ScaleFactors(nominal_name,**settings)
    


