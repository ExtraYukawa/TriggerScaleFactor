import json


def GEN_METFilters(year:str):
    '''
    Build Json file which contents MET Filters Name.
    '''
    Flags = dict()
    Flags["Data"] = dict()
    Flags["MC"] = dict()
    with open(f'./data/year{year}/PhysProcessRECO/configuration/Phys_process.json') as f:
        Phys_Process = json.load(f)


    if year == '2017' or year =='2018':

        Flags["Data"] = ["Flag_goodVertices",\
                "Flag_globalSuperTightHalo2016Filter",\
                "Flag_HBHENoiseFilter",\
                "Flag_HBHENoiseIsoFilter",\
                "Flag_EcalDeadCellTriggerPrimitiveFilter",\
                "Flag_BadPFMuonFilter",\
                "Flag_BadPFMuonDzFilter",\
                "Flag_eeBadScFilter",\
                "Flag_ecalBadCalibFilter"]
        for process in Phys_Process.keys():
            Flags['MC'][process] = dict()
            for phys_name in Phys_Process[process]:
                Flags["MC"][process][phys_name] = \
                ["Flag_goodVertices",\
                "Flag_globalSuperTightHalo2016Filter",\
                "Flag_HBHENoiseFilter",\
                "Flag_HBHENoiseIsoFilter",\
                "Flag_EcalDeadCellTriggerPrimitiveFilter",\
                "Flag_eeBadScFilter",\
                "Flag_ecalBadCalibFilter",\
                "Flag_BadPFMuonDzFilter",\
                "Flag_BadPFMuonFilter"]

        if year =='2017':
            Flags["MC"]["VV"]["osWW"] =\
                ["Flag_goodVertices",\
                "Flag_globalSuperTightHalo2016Filter",\
                "Flag_eeBadScFilter",\
                "Flag_HBHENoiseFilter",\
                "Flag_HBHENoiseIsoFilter",\
                "Flag_ecalBadCalibFilter",\
                "Flag_EcalDeadCellTriggerPrimitiveFilter",\
                "Flag_BadPFMuonFilter"]
            Flags["MC"]["VV"]["ssWW"]= Flags["MC"]["VV"]["osWW"]
            Flags["MC"]["VV"]["ZG_ew"]= Flags["MC"]["VV"]["osWW"]
            Flags["MC"]["VV"]["WWdps"]= Flags["MC"]["VV"]["osWW"]
            Flags["MC"]["VV"]["WZ_ew"]= Flags["MC"]["VV"]["osWW"]
            Flags["MC"]["SingleTop"]["tsch"]= Flags["MC"]["VV"]["osWW"]
            Flags["MC"]["SingleTop"]["tW"]= Flags["MC"]["VV"]["osWW"]
            Flags["MC"]["SingleTop"]["tbarW"]= Flags["MC"]["VV"]["osWW"]
            Flags["MC"]["SingleTop"]["t_tch"]= Flags["MC"]["VV"]["osWW"]
            Flags["MC"]["SingleTop"]["tbar_tch"]= Flags["MC"]["VV"]["osWW"]
        else:
            Flags["MC"]["VV"]["ZZ"] =["Flag_goodVertices",\
                "Flag_globalSuperTightHalo2016Filter",\
                "Flag_eeBadScFilter",\
                "Flag_HBHENoiseFilter",\
                "Flag_HBHENoiseIsoFilter",\
                "Flag_ecalBadCalibFilter",\
                "Flag_EcalDeadCellTriggerPrimitiveFilter",\
                "Flag_BadPFMuonFilter"]
            Flags["MC"]["VV"]["ssWW"] = Flags["MC"]["VV"]["ZZ"]
            Flags["MC"]["SingleTop"]["t_tch"] = Flags["MC"]["VV"]["ZZ"]
            Flags["MC"]["SingleTop"]["tbar_tch"] = Flags["MC"]["VV"]["ZZ"]
            Flags["MC"]["VV"]["ZG_ew"] = Flags["MC"]["VV"]["ZZ"]
            Flags["MC"]["VV"]["WWdps"] = Flags["MC"]["VV"]["ZZ"]

    elif year =='2016apv' or year =='2016postapv':
        Flags["Data"] = ["Flag_goodVertices",\
                "Flag_globalSuperTightHalo2016Filter",\
                "Flag_HBHENoiseFilter",\
                "Flag_HBHENoiseIsoFilter",\
                "Flag_EcalDeadCellTriggerPrimitiveFilter",\
                "Flag_BadPFMuonFilter",\
                "Flag_BadPFMuonDzFilter",\
                "Flag_eeBadScFilter"]

        for process in Phys_Process.keys():
            Flags['MC'][process] = dict()
            for phys_name in Phys_Process[process]:
                Flags["MC"][process][phys_name] = \
                ["Flag_goodVertices",\
                "Flag_globalSuperTightHalo2016Filter",\
                "Flag_HBHENoiseFilter",\
                "Flag_HBHENoiseIsoFilter",\
                "Flag_EcalDeadCellTriggerPrimitiveFilter",\
                "Flag_BadPFMuonFilter",\
                "Flag_BadPFMuonDzFilter",\
                "Flag_eeBadScFilter"]
    else:
        raise ValueError("year{year} HLT Path has not been specified yet!")
    with open(f'./data/year{year}/PhysProcessRECO/configuration/MET_Filters.json','wt') as f :
        json.dump(Flags,f,indent=4)

    
