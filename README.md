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
 - Running Time: about 1000 sec for Data. about 45000 sec for MC of full events. about O(1000) ~ O(10000) sec for ten million events.
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


## Steps to do physics process reconstruction

### step1: preparation
Firstly you have to utilize the already existed json files production function to produce the necessary information files.
Since each year data will face different scenerio, likes PrefireWeight or different lepton IDSFs etc. You need to do this sperately. 

e.g. to produce needed files for 2016apv
```
python3 ./WorkFlow/main.py -m Init -t PhysProcessRECO --year 2016 
```
### step2: Make Output Directory under EOS space and save this path.

In this step, you would make the output directories to store the plots.
Also, the json files which contain the paths to these directories will be also made.

e.g.
```
python3 ./WorkFlow/main.py -m BuildDir -t PhysProcessRECO --year 2016 --channels DoubleElectron DoubleMuon ElectronMuon 
```
Note: It's up to you to feed number of channels to the channels options, but there are only these three channels for sure.  

### step3: Physics Process Reconstruction
Region Option: Signal Region, Drell-Yan process enriched region, Charge Flip derivation region.
A typical command to produce the signal region associated plots are like:
```
python3 ./WorkFlow/main.py -m PhysProcessRECO -y 2017 -i DoubleElectron -r SignalRegion --TrigSF 3 --IDSF --RECOSF --CFSF --FakeRate 
```
 arguments: 
 - [--TrigSF]: Activate trigger scale factor if specify 1/2/3/4. [1->l1pteta,2->l2pteta,3->l1l2pt,4->l1l2eta]. Deactivate if specify 0. 
 - [--IDSF]: Activate identification scale factor if specified.
 - [--RECOSF]: Activate Reconstruction scale factor if specified.
 - [--FakeRate]: Activate nonprompt background estimation if specified.
 - [--CFSF]: Activate charge flip scale factor if specified.
 - [--Era]: Only consider certain eras of data. Generally, this option accompanies with \[lumi\]
 - [--lumi]: Luminosity.
 - [-i/--channel]: Channel, choices: [DoubleElectron/DoubleMuon/ElectronMuon]. Note: You should make sure whether you make the corresponding output folders for your favour channel!
 Running Time: 3000 sec ~ 5000 sec for 2017/2018, 1000 sec for 2016apv/2016postapv
 
 ##Steps to calculate the number of events(Data) or yields(MC) under cutflow
 Currently, the SignalRegion is the only provided option for [--region].
 The command to do the computation,for example, ElectronMuon in year2017 is:
 ```
 python3 ./WorkFlow/main.py -m NEventsCount -y 2017 -i ElectronMuon -r SignalRegion --IDSF --RECOSF --TrigSF 3 --FakeRate --CFSF > NEvent_result.log
 ```
 - [--TrigSF]: Activate trigger scale factor if specify 1/2/3/4. [1->l1pteta,2->l2pteta,3->l1l2pt,4->l1l2eta]. Deactivate if specify 0.
 - [--IDSF]: Activate identification scale factor if specified.
 - [--RECOSF]: Activate Reconstruction scale factor if specified.
 - [--FakeRate]: Activate nonprompt background estimation if specified.
 - [--CFSF]: Activate charge flip scale factor if specified.
 - [--Era]: Only consider certain eras of data. Generally, this option accompanies with \[lumi\]
 - [--lumi]: Luminosity.
 - [-i/--channel]: Channel, choices: [DoubleElectron/DoubleMuon/ElectronMuon]. Note: You should make sure whether you make the corresponding output folders for your favour channel!
- Running time: ~7200 sec for 2017 Data.
