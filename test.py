from Utils.Header import Histogram_Definition
import json

import ROOT


ROOT.gInterpreter.ProcessLine('#include "./include/IDScaleFactor.h"')
ROOT.gSystem.Load('./myLib/IDScaleFactor_cpp.so')


l1_trigSF_File = "/eos/user/z/zhenggan/ExtraYukawa/TriggerSF/year2017/DoubleElectron/files/SF_l1pteta.root"
l2_trigSF_File = "/eos/user/z/zhenggan/ExtraYukawa/TriggerSF/year2017/DoubleElectron/files/SF_l2pteta.root"
l1_trigSF_branchname = "l1pteta"
l2_trigSF_branchname = "l2pteta"

ROOT.gInterpreter.ProcessLine(Histogram_Definition['TrigSF'].format(l1_trigSF_File,l2_trigSF_File,l1_trigSF_branchname,l2_trigSF_branchname))

ROOT.gInterpreter.ProcessLine("std::cout<<Trigger_sf(h1_TrigSF,50,1.5)*Trigger_sf(h2_TrigSF,20,0.5)")



