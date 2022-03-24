import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-m','--mode',help='Program Modes',choices=['Init','BuildDir','TrigEff_Calc','TrigEff_Plot','TrigSF_Calc','DrellYanRECO','Fake_Rate'],type=str)

parser.add_argument('-y','--year',help='year',choices=['2017','2018'],type=str)

parser.add_argument('-c','--channels',help='Channels, ex: DoubleElectron DoubleMuon',nargs='+')
parser.add_argument('-i','--channel',choices=['DoubleElectron','DoubleMuon','ElectronMuon'],default=None)
parser.add_argument('-o','--DirOut',help="Output Directory's Parent,ex: /eos/user/z/zhenggan",type=str)
parser.add_argument('-t','--task',help="Task",type=str,choices=["TriggerSF","DrellYan","FakeRate"])
parser.add_argument('-f','--Type',help="MC/Data",type=str,choices=["MC","Data"])
parser.add_argument('-n','--nevents',help="Number of Events. Only used in mode[TrigEff_Calc] at this moment. Default is set to -1.",type=int,default=-1)
parser.add_argument('-a','--trigSF_on',action = "store_true",help="This option is to determine whether to apply TriggerSF on MC Sample")
args = parser.parse_args()


if args.mode == 'Init':
    if args.year is None:
        raise ValueError('You need to specify ex:[-y/--year 2017]')
    from Utils.General_Tool import MakeDir

    RootDIR = './'
    MakeDir('./','data') 
    RootDIR = os.path.join(RootDIR,'data')
    MakeDir(RootDIR,'year{}'.format(args.year))
    RootDIR = os.path.join(RootDIR,'year{}'.format(args.year))
    
    MakeDir(RootDIR,args.task)
    RootDIR = os.path.join(RootDIR,args.task)
    MakeDir(RootDIR,'configuration')
    MakeDir(RootDIR,'path')
    if args.task == 'TriggerSF':
        from Trigger_SF.Trigger_Utils import *
        GenPaths_HLTTrigger_File(args.year)
        GenTrigEffInput_File(args.year) 
        GenLeptonIDSF_File(args.year)
        GenMCWeightsName_File(args.year)
        GenVariableNames_File(args.year)
        GenGoodFlag_File(args.year) 
    
    elif args.task == 'DrellYan':
        from Drell_Yan.DY_utils import *
        GenDataPath_File(args.year) ##Need to be checked.
        GenPaths_HLTTriggerCondition_ForAnalyzer_File(args.year)
        GenXsValue_File(args.year) ##Need to be checked.
        GenTriggerSF_Path(args.year)
    elif args.task == 'FakeRate':
        from Fake_Rate.FR_Utils import *
        FakeRateConfiguration(args.year)
        FakeRageFilesIn(args.year)
    else:
        pass
elif args.mode == 'BuildDir':
    from Utils.Build_Dir import Build_Dir
    Build_Dir(args) 
elif args.mode == 'TrigEff_Calc':
    from Trigger_SF.Program_Step import * 
    if args.channel == None:
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")
    if args.Type == None:
        raise ValueError("Should Specify the type of input file(s) ex:[-f/--Type MC]")

    Trig_Calc(year = args.year , channel = args.channel, Type = args.Type,nevents=args.nevents)
elif args.mode == 'TrigEff_Plot':
    from Trigger_SF.Program_Step import * 
    if args.channel == 'None':
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")
    if args.year == 'None':
        raise ValueError('You need to specify ex:[-y/--year 2017]')
    
    Plot_efficiency(channel=args.channel,year=args.year)


elif args.mode == 'TrigSF_Calc':
    if args.channel == 'None':
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")
    if args.year == 'None':
        raise ValueError('You need to specify ex:[-y/--year 2017]')
    from Trigger_SF.Program_Step import * 
    SF_Calc(channel=args.channel,year=args.year)

elif args.mode =='DrellYanRECO':
    if args.channel == 'None':
        raise ValueError("Channel should be specified or The Specified Channel is Not in the list. ex:[-i/--channel DoubleElectron]")
    if args.year == 'None':
        raise ValueError('You need to specify ex:[-y/--year 2017]')
    from Drell_Yan.Program_Step import *
    Drell_Yan_Reconstruction(year = args.year, channel = args.channel, nevents = args.nevents,trig_SF_on = args.trigSF_on)

else:
    raise ValueError("Mode should be specified or The Specified Mode is Not in the list.")

