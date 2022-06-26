python3 ./WorkFlow/main.py -m TrigEff_Calc -y 2016apv -i DoubleMuon --Type MC -n 2000000;
python3 ./WorkFlow/main.py -m TrigEff_Plot -y 2016apv -i DoubleMuon ;
python3 ./WorkFlow/main.py -m TrigSF_Calc -y 2016apv -i DoubleMuon ;
python3 ./WorkFlow/main.py -m TrigEff_Calc -y 2016apv -i ElectronMuon --Type MC -n 2000000;
python3 ./WorkFlow/main.py -m TrigEff_Plot -y 2016apv -i ElectronMuon ;
python3 ./WorkFlow/main.py -m TrigSF_Calc -y 2016apv -i ElectronMuon ;

python3 ./WorkFlow/main.py -m TrigEff_Calc -y 2016postapv -i DoubleMuon --Type MC -n 2000000;
python3 ./WorkFlow/main.py -m TrigEff_Plot -y 2016postapv -i DoubleMuon ;
python3 ./WorkFlow/main.py -m TrigSF_Calc -y 2016postapv -i DoubleMuon ;
python3 ./WorkFlow/main.py -m TrigEff_Calc -y 2016postapv -i ElectronMuon --Type MC -n 2000000;
python3 ./WorkFlow/main.py -m TrigEff_Plot -y 2016postapv -i ElectronMuon ;
python3 ./WorkFlow/main.py -m TrigSF_Calc -y 2016postapv -i DoubleMuon ;
python3 ./WorkFlow/main.py -m TrigEff_Calc -y 2017 -i DoubleMuon --Type MC -n 2000000;
python3 ./WorkFlow/main.py -m TrigEff_Plot -y 2017 -i DoubleMuon ;
python3 ./WorkFlow/main.py -m TrigSF_Calc -y 2017 -i DoubleMuon ;
python3 ./WorkFlow/main.py -m TrigEff_Calc -y 2017 -i ElectronMuon --Type MC -n 2000000;
python3 ./WorkFlow/main.py -m TrigEff_Plot -y 2017 -i ElectronMuon ;
python3 ./WorkFlow/main.py -m TrigSF_Calc -y 2017 -i ElectronMuon ;
python3 ./WorkFlow/main.py -m TrigEff_Calc -y 2018 -i DoubleMuon --Type MC -n 2000000;
python3 ./WorkFlow/main.py -m TrigEff_Plot -y 2018 -i DoubleMuon ;
python3 ./WorkFlow/main.py -m TrigSF_Calc -y 2018 -i DoubleMuon ;
python3 ./WorkFlow/main.py -m TrigEff_Calc -y 2018 -i ElectronMuon --Type MC -n 2000000;
python3 ./WorkFlow/main.py -m TrigEff_Plot -y 2018 -i DoubleMuon ;
python3 ./WorkFlow/main.py -m TrigSF_Calc -y 2018 -i ElectronMuon ;

