# TriggerScaleFactor

The structure of the code is simply derived from [TTC_plots Packages](https://github.com/menglu21/TTC_plots.git)

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
python3 WorkFlow/main.py --mode Init --channels DoubleElectron DoubleMuon ElectronMuon --year 2017
sh ./script/script.sh
```
### step3: Build Directory

- Build Output Directory
```
python3 WorkFlow/main.py --mode BuildDir --year2017 --task TriggerSF --DirOut /eos/user/y/yourname/
```
### step4: Trigger Efficiency Calculation

At the moment, the analysis code haven't include multi-thread calculation, thus you need to calculate channel by channel, type by type(MC/Data).
ex: Channel: DoubleElectron and Type: MC.
```
python3 WorkFlow/main.py --mode TrigEff_Calc --year2017 --channel DoubleElectron --Type MC
```
After the program is done, you can see your /eos/user/y/yourname/ExtraYukawa/TriggerSF/files/DoubleElectron directory, see what's the change.
By the way, the cost time of this phase is roughly half of a day. Thus for **impatient people**, you could simply add the argument **[-n/--nevents]**
 to limit the number of events. If you want to collect efficiency results for DoubleElectron, take it for example, that means you should type the command twice (MC and Data) at least.

### step5: Trigger Efficiency Plot

Before proceed into the further step, to collect DoubleElectron Channel TrigEfficiency Plots, **pleas make sure you have collected the trigger efficiency results for both types (MC/Data)** , otherwise you can't implement this step, and the compilier will throw a error message.
For DoubleElectron:

```
python3 WorkFlow/main.py --mode TrigEff_Plot --year2017 --channel DoubleElectron
```

### step6: Trigger ScaleFactor 

```
python3 WorkFlow/main.py --mode TrigSF_Calc --year2017 --channel DoubleElectron
```

After the program is done, you can see trigSF plots and files in your /eos/user/y/yourname/ExtraYukawa/TriggerSF/DoubleElectron/files/ and /eos/user/y/yourname/ExtraYukawa/TriggerSF/DoubleElectron/plots/ .
### Results

Plots for efficiencies and trigger scale factors: [link](https://cernbox.cern.ch/index.php/s/C2DsnT2SjqiApBL)

### To-Do List:
- [ ] Rewrite the script in MakeFile.
- [ ] Multi-Thread Implementation in Trigger Efficiency Calculation.
- [ ] Further divide Efficiency Calculation into two sub-programs. 
   - Saving Cut-Flow dataframe into root files. 
   - Read corresponding root files, and plot them.

