import ROOT
import sys
import os 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('-m','--mode',help='Program Modes',choices=['Init','BuildDir','TrigEff_Calc','TrigEff_Plot','TrigSF_Calc','DrellYanRECO','FakeRate'],type=str)

parser.add_argument('-y','--year',help='year',choices=['2017','2018','2016apv','2016postapv'],type=str)

parser.add_argument('-c','--channels',help='Channels, ex: DoubleElectron DoubleMuon',nargs='+')
parser.add_argument('-i','--channel',choices=['DoubleElectron','DoubleMuon','ElectronMuon','Electron','Muon'],default=None)
parser.add_argument('-o','--DirOut',help="Output Directory's Parent,ex: /eos/user/z/zhenggan",type=str)
parser.add_argument('-t','--task',help="Task",type=str,choices=["TriggerSF","DrellYan","FakeRate"])
parser.add_argument('-f','--Type',help="MC/Data",type=str,choices=["MC","Data"])
parser.add_argument('-n','--nevents',help="Number of Events. Only used in mode[TrigEff_Calc] at this moment. Default is set to -1.",type=int,default=-1)
parser.add_argument('-a','--SF_mode',choices=[0,1,2,3],help="This option is to determine whether to apply TriggerSF on MC Sample",type=int,default=3)
parser.add_argument('-v','--veto',action = "store_true",help="In 2018 Issue, veto the HEM region if specified.")
parser.add_argument('-d','--debug',action="store_true",help="Debug mode")
parser.add_argument('-s','--ylog',choices=[0,1],help="Set y scale to be log scale, only works for Control Region validation at this moment.",type=int,default = 0)
parser.add_argument('-x','--trigSFType',choices=[0,1,2,3],help="Trigger Scale Factors Type. 0: l1pteta,1: l2pteta,2:l1l2pt,3:l1l2eta",type=int,default=-1)
parser.add_argument('-e','--Era',type=str,help='Data Era',default=[''],nargs='+')

args = parser.parse_args()



if args.mode == 'Init':
    if args.year is None:
        raise ValueError('You need to specify ex:[-y/--year 2017]')
    if args.task is None:
        raise ValueError('You need to specify ex:[-t/--task TriggerSF]')
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
        from Trigger_SF.Init import *
        Gen_HLT_MET_File(args.year)
        GenTrigEffInput_File(args.year) 
        GenLeptonIDSF_File(args.year)
        GenMCWeightsName_File(args.year)
        GenVariableNames_File(args.year)
        Gen_MET_Filters_File(args.year)
        GenTotalLuminosity(args.year)
        from Trigger_SF.GenTriggers import gen_triggers    
        
        gen_triggers(args.year)
    elif args.task == 'DrellYan':
        from Drell_Yan.Init import *
        from Drell_Yan.DiLeptonTrigger import *
        from Drell_Yan.MET_Filters import *
        GenDataPath_File(args.year) ##
        GenXsValue_File(args.year) ##
        GenProcessName(args.year)
        GenTriggerSF_Path(args.year)
        GEN_METFilters(args.year)
        GenPaths_HLTTriggerCondition_ForAnalyzer_File(args.year)
    elif args.task == 'FakeRate':
        from Fake_Rate.Init import *
        FakeRateConfiguration(args.year)
        FakeRateFilesIn(args.year)
    else:
        pass
elif args.mode == 'BuildDir':
    from Utils.Build_Dir import Build_Dir
    if args.year is None:
        raise ValueError('Argument: [-y/--year] must be specified.')
    if args.channels is None:
        raise ValueError('Argument: [-c/--channels] must be specified.')
    if args.task is None:
        raise ValueError('Argument: [-t/--task] must be specified.')
    Build_Dir(args) 


else:
    from Utils.Program_Steps import RuntimeMeasure
    RuntimeMeasure(args)

#elif args.mode == 'TrigEff_Calc':
#    from Utils.Program_Steps import * 
    
#    RuntimeMeasure(args,Trig_Calc)
    #Trig_Calc(year = args.year , channel = args.channel, Type = args.Type,nevents=args.nevents)

#elif args.mode == 'TrigEff_Plot':
#    from Utils.Program_Steps import * 
#    RuntimeMeasure(args,Plot_efficiency)
    #Plot_efficiency(channel=args.channel,year=args.year)


#elif args.mode == 'TrigSF_Calc':
#    from Utils.Program_Steps import * 
#    RuntimeMeasure(args,SF_Calc)
    #SF_Calc(channel=args.channel,year=args.year)

#elif args.mode =='DrellYanRECO':
#    from Utils.Program_Steps import *
#    Drell_Yan_Reconstruction(year = args.year, channel = args.channel, nevents = args.nevents,trig_SF_on = args.trigSF_on)

#elif args.mode == 'FakeRate':

 #   from Utils.Program_Steps import *
 #   
 #   FakeRateCalculation(year=args.year,channel=args.channel,nevents=args.nevents,trig_SF_on=args.trigSF_on)



#else:
#    raise ValueError("Mode should be specified or The Specified Mode is Not in the list.")

