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
    elif args.mode == 'DrellYanRECO':
        func = Drell_Yan_Reconstruction
    elif  args.mode == 'FakeRate':
        func = FakeRateCalculation
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

from Drell_Yan.DY_Analyzer import *



def Drell_Yan_Reconstruction(args):
    if args.year is None:
        raise ValueError('Arguments [year] must be speicified.')
    if args.channel == 'None':
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")
    
    settings = dict()
    settings['year'] = args.year
    settings['channel'] = args.channel
    settings['nevents'] = args.nevents
    settings['SF_mode']  = args.SF_mode
    settings['veto'] = args.veto
    
    with open(f'./data/year{args.year}/DrellYan/configuration/HLTTriggerCondition.json','rb') as f:
        settings['HLT_Path'] = json.load(f)
    with open(f'./data/year{args.year}/DrellYan/configuration/data_xs.json','rb') as f:
        structure = json.load(f)
        settings['xs'] = structure['xs']
        settings['NumberOfEvents'] = structure['NumberOfEvents'] 
        settings['Process'] = structure['Process']
    with open(f'./data/year{args.year}/DrellYan/path/datapath.json','rb') as f :
        settings['FilesIn'] = json.load(f)
    
    with open(f'./data/year{args.year}/DrellYan/path/triggerSF.json','rb') as f:
        settings['TriggerSF'] = json.load(f)

    with open(f'./data/year{args.year}/TriggerSF/configuration/weights.json','rb') as f:
        settings['Weights'] = json.load(f)
    with open(f'./data/year{args.year}/TriggerSF/path/LeptonsID_SF.json','rb') as f:
        settings['LepIDSF_File'] = json.load(f)[args.channel]


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
    if args.year is None:
        raise ValueError('Arguments [year] must be speicified.')
    if args.channel == None:
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")
    if args.Type == None:
        raise ValueError("Should Specify the type of input file(s) ex:[-f/--Type MC]")
    if args.veto == True:
        print('Veto HEM region.\nRemind: The option[-v/--veto] is only valid for UL2018 Data.')
    
    with open(f'./data/year{args.year}/TriggerSF/configuration/HLTTrigger.json','rb') as f:
        HLT_Path = json.load(f)
    with open(f'./data/year{args.year}/TriggerSF/configuration/name.json','rb') as f :
        Var_Name = json.load(f)
    with open(f'./data/year{args.year}/TriggerSF/configuration/flag.json','rb') as f :
        Flag = json.load(f)

    with open(f'./data/year{args.year}/TriggerSF/path/filein.json','rb') as f:
        FileIn = json.load(f)

    with open(f'./data/year{args.year}/TriggerSF/User.json','rb') as f:
        User = json.load(f)
    
    with open(f'./data/year{args.year}/TriggerSF/path/LeptonsID_SF.json','rb') as f:
        LepSF_File = json.load(f)[args.channel]

    with open(f'./data/year{args.year}/TriggerSF/configuration/weights.json','rb') as f:
        Weights = json.load(f)[args.Type]

    
    setting={
        'HLT_MET': HLT_Path['MET'],
        'HLT_LEP': HLT_Path[args.channel],
        'Var_Name' : Var_Name[args.channel],
        'channel' : args.channel,
        'DirOut' : User['DirOut'][args.channel]['files'],
        'FileIn' : FileIn[args.Type],
        'Flag':Flag,
        'Type':args.Type,
        'LepSF_File':LepSF_File,
        'Year':'year'+args.year,
        'nevents':args.nevents,
        'Weights':Weights,
        'veto':args.veto
    }
    A = TrigRDataFrame(setting)
    A.Run()


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
        TrigUtils.Plot(TrigUtils.plot_eff2d,**user_settings)(tag=tag)
    for tag in  tags['l2']['pteta']:
        TrigUtils.Plot(TrigUtils.plot_eff2d,**user_settings)(tag=tag)
    #for tag in  tags['l1l2']['pt']:
    #    Plot(plot_eff2d,**user_settings)(tag=tag)
    #for tag in  tags['l1l2']['eta']:
    #    Plot(plot_eff2d,**user_settings)(tag=tag)


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
    
    nominal_names =['l1pteta','l2pteta']

    
    print('Producing TriggerSF...')
    for nominal_name in nominal_names:
        TrigUtils.ScaleFactors(nominal_name,**settings)
    


