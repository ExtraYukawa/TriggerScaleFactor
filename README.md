# TriggerScaleFactor

The structure of the code is simply derived from [TTC_plots Packages](https://github.com/menglu21/TTC_plots.git).
The main difference is that the previous work is based on python, and this package is based on RDataframe(c++ based).

# Pre-requisite
- CMSSW version >= CMSSW_12_1_0_pre3

## Steps to produce Trigger Scale Factors for three channels.



### step1: 
```
cd $CMSSW_BASE/src

cmsenv

git clone https://github.com/ZhengGang85129/TriggerScaleFactor.git
```

### step2: Initialization

- Build necessary paths to Data and MC directory.
```
python3 WorkFlow/main.py --mode Init  --year 2017 -t TriggerSF
```
### step3: Build Directory

- Build Output Directory
```
python3 WorkFlow/main.py --mode BuildDir --year 2018 --task TriggerSF --DirOut /eos/user/y/yourname/ --channels DoubleElectron DoubleMuon ElectronMuon
```
### step4: Trigger Efficiency Calculation

At the moment, the analysis code haven't include multi-thread calculation, thus you need to calculate channel by channel, type by type(MC/Data).
ex: Channel: DoubleElectron and Type: MC.
```
python3 WorkFlow/main.py --mode TrigEff_Calc --year 2018 --channel DoubleElectron --Type MC --veto
```
After the program is done, you can see your /eos/user/y/yourname/ExtraYukawa/TriggerSF/files/DoubleElectron directory, see what's the change.
By the way, the cost time of this phase is roughly half of a day. Thus for **impatient people**, you could simply add the argument **[-n/--nevents]**
 to limit the number of events. If you want to collect efficiency results for DoubleElectron, take it for example, that means you should type the command twice (MC and Data) at least.
 - [-v/--veto]: To get rid of HEM region issue, if this is speicified, then veto this region. Only valid for UL2018 Data.
 - Running Time: about 1000 sec for Data. about 45000 sec for MC.
### step5: Trigger Efficiency Plot

Before proceed into the further step, to collect DoubleElectron Channel TrigEfficiency Plots, **pleas make sure you have collected the trigger efficiency results for both types (MC/Data)** , otherwise you can't implement this step, and the compilier will throw a error message.
For DoubleElectron:

```
python3 WorkFlow/main.py --mode TrigEff_Plot --year 2018 --channel DoubleElectron
```

### step6: Trigger ScaleFactor 

```
python3 WorkFlow/main.py --mode TrigSF_Calc --year 2018 --channel DoubleElectron
```

After the program is done, you can see trigSF plots and files in your /eos/user/y/yourname/ExtraYukawa/TriggerSF/DoubleElectron/files/ and /eos/user/y/yourname/ExtraYukawa/TriggerSF/DoubleElectron/plots/ .
### Results

Plots for efficiencies and trigger scale factors: [link](https://cernbox.cern.ch/index.php/s/C2DsnT2SjqiApBL)


## Steps to do Drell-Yan Process Reconstruction

### step1: preparation
Firstly you should make some paths to Input Files(Data and MC respectively) and triggerSF files.
Also, make some files to contain the crossection and number of events of MC sample.

e.g.
```
python3 ./WorkFlow/main.py -m Init -t DrellYan --year 2017 
```
### step2: Make Output Directory under EOS space and save this path.

In this step, the directories which will be used to contain the plots of DrellYan-related would be constructed.
Also, the json files which contain the paths to these directories will be also made.

e.g.
```
python3 ./WorkFlow/main.py -m BuildDir -t DrellYan --year 2017 --channels DoubleElectron DoubleMuon ElectronMuon 
```
### step3: Drell_Yan Process Reconstruction

```
python3 ./WorkFlow/main.py -m DrellYanRECO -y 2017 -i DoubleElectron -n -1 --SF_mode 0
```
 arguments: 
 - [-n]: number of events, if specified to be -1, all the events will be loaded.
 - [-a/--trigSF_on]: Apply triggerSF on MC sample or not. If specified, triggerSF will be applied otherwise, the default is no triggerSF.
 - [-a/--SF_mode]: 0: Without any ScaleFactors|1:Only ID Scale Factor|2: Only Trigger Scale Factor | 3: (ID +Trigger) Scale Factor
 - Running Time: 3000 sec ~ 5000 sec
## Steps to do Lepton Fake Rate calculation
### step1 : Initialization and Building Ourput directory

```
python3 ./WorkFlow/main.py -m Init -t FakeRate -y 2017
python3 ./WorkFlow/main.py -m BuildDir -t FakeRate -y 2017 --channels Electron Muon 
```

The similar data output and FilesInput Info. json files structure as previous steps will present.

### step2 : FakeRate Calculation

```
python3 ./WorkFlow/main.py -m FakeRate -y 2017 --channel Electron -t FakeRate -n -1 -a
```
Note:
argument [ -a/--trigSF_on] determine whether the trigSF should be applied or not.

### To-Do List:
- []FakeRate 

