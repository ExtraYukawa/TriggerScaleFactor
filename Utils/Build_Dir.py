import sys
import os,json 
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
#import utils.listoutdata2txt as d2t
from Utils.General_Tool import MakeDir


def Build_Dir(setting):
    '''
    Build Necessary Directories For Saving Trigger Efficiency/Scale Factors Calculation, e.t.c
    
    '''
    YEAR = setting.year
    DirParName = setting.DirOut
    Channels = setting.channels
    Task = setting.task
    
    if YEAR is None:
        raise ValueError('Argument: [-y/--year] must be specified.')
    if DirParName is None:
        raise ValueError('Argument: [-o/--DirOut] must be specified.')
    if Channels is None:
        raise ValueError('Argument: [-c/--channels] must be specified.')
    if Task is None:
        raise ValueError('Argument: [-t/--task] must be specified.')
    
    MakeDir(Root = DirParName,ChildName = 'ExtraYukawa')
    DirParName = os.path.join(DirParName,'ExtraYukawa')
    MakeDir(Root = DirParName,ChildName = Task)
    DirParName = os.path.join(DirParName,Task)
    MakeDir(Root = DirParName,ChildName = 'year'+YEAR)
    DirParName = os.path.join(DirParName,'year'+YEAR)
    User = dict()
    User['DirOut'] = dict()
    for channel in Channels:
        User['DirOut'][channel] = dict()
        MakeDir(Root = DirParName, ChildName = channel)
        DirParName_tmp = os.path.join(DirParName,channel)
        MakeDir(Root = DirParName_tmp, ChildName = 'plots')
        User['DirOut'][channel]['plots'] = os.path.join(DirParName_tmp,'plots')
        
        if Task =='TriggerSF':
            MakeDir(Root = DirParName_tmp, ChildName = 'files')
            User['DirOut'][channel]['files'] = os.path.join(DirParName_tmp,'files')
        else:
            pass
    User['UserName'] = DirParName.split("/")[4]
    PrivateFile = f'data/year{setting.year}/{setting.task}/User.json'
    print(f'Your Out put file will store here: {PrivateFile}')
    with open(PrivateFile,'w') as f:
        json.dump(User,f,indent=4)
