from multiprocessing import Manager

manager = Manager()

HistSettings =manager.dict()
HistSettings['SignalRegion'] = manager.dict()
HistSettings['ChargeFlipRegion'] = manager.dict()
HistSettings['DrellYan'] = manager.dict()



HistSettings['DrellYan']['DY_l1_pt'] = manager.dict()
HistSettings['DrellYan']['DY_l1_pt']['name'] = 'OPS_l1_pt'
HistSettings['DrellYan']['DY_l1_pt']['nbins'] = 40
HistSettings['DrellYan']['DY_l1_pt']['lowedge'] = 0
HistSettings['DrellYan']['DY_l1_pt']['highedge'] = 200


HistSettings['DrellYan']['DY_l1_eta'] = manager.dict()
HistSettings['DrellYan']['DY_l1_eta']['name'] = 'OPS_l1_eta'
HistSettings['DrellYan']['DY_l1_eta']['nbins'] = 30
HistSettings['DrellYan']['DY_l1_eta']['lowedge'] = -3
HistSettings['DrellYan']['DY_l1_eta']['highedge'] = 3

HistSettings['DrellYan']['DY_l1_phi'] = manager.dict()
HistSettings['DrellYan']['DY_l1_phi']['name'] = 'OPS_l1_phi'
HistSettings['DrellYan']['DY_l1_phi']['nbins'] = 20
HistSettings['DrellYan']['DY_l1_phi']['lowedge'] = -4
HistSettings['DrellYan']['DY_l1_phi']['highedge'] = 4

HistSettings['DrellYan']['DY_l2_pt'] = manager.dict()
HistSettings['DrellYan']['DY_l2_pt']['name'] = 'OPS_l2_pt'
HistSettings['DrellYan']['DY_l2_pt']['nbins'] = 40
HistSettings['DrellYan']['DY_l2_pt']['lowedge'] = 0
HistSettings['DrellYan']['DY_l2_pt']['highedge'] = 100

HistSettings['DrellYan']['DY_l2_eta'] = manager.dict()
HistSettings['DrellYan']['DY_l2_eta']['name'] = 'OPS_l2_eta'
HistSettings['DrellYan']['DY_l2_eta']['nbins'] = 30
HistSettings['DrellYan']['DY_l2_eta']['lowedge'] = -3
HistSettings['DrellYan']['DY_l2_eta']['highedge'] = 3

HistSettings['DrellYan']['DY_l2_phi'] = manager.dict()
HistSettings['DrellYan']['DY_l2_phi']['name'] = 'OPS_l2_phi'
HistSettings['DrellYan']['DY_l2_phi']['nbins'] = 20
HistSettings['DrellYan']['DY_l2_phi']['lowedge'] = -4
HistSettings['DrellYan']['DY_l2_phi']['highedge'] = 4

HistSettings['DrellYan']['DY_z_pt'] = manager.dict()
HistSettings['DrellYan']['DY_z_pt']['name'] = 'OPS_z_pt'
HistSettings['DrellYan']['DY_z_pt']['nbins'] = 50
HistSettings['DrellYan']['DY_z_pt']['lowedge'] = 0
HistSettings['DrellYan']['DY_z_pt']['highedge'] = 200

HistSettings['DrellYan']['DY_z_eta'] = manager.dict()
HistSettings['DrellYan']['DY_z_eta']['name'] = 'OPS_z_eta'
HistSettings['DrellYan']['DY_z_eta']['nbins'] = 20
HistSettings['DrellYan']['DY_z_eta']['lowedge'] = -3
HistSettings['DrellYan']['DY_z_eta']['highedge'] = 3

HistSettings['DrellYan']['DY_z_phi'] = manager.dict()
HistSettings['DrellYan']['DY_z_phi']['name'] = 'OPS_z_phi'
HistSettings['DrellYan']['DY_z_phi']['nbins'] = 20
HistSettings['DrellYan']['DY_z_phi']['lowedge'] = -4
HistSettings['DrellYan']['DY_z_phi']['highedge'] = 4

HistSettings['DrellYan']['DY_z_mass'] = manager.dict()
HistSettings['DrellYan']['DY_z_mass']['name'] = 'OPS_z_mass'
HistSettings['DrellYan']['DY_z_mass']['nbins'] = 60
HistSettings['DrellYan']['DY_z_mass']['lowedge'] = 60
HistSettings['DrellYan']['DY_z_mass']['highedge'] = 120

HistSettings['SignalRegion']['ttc_l1_pt'] = manager.dict()
HistSettings['SignalRegion']['ttc_l1_pt']['name'] = 'ttc_l1_pt'
HistSettings['SignalRegion']['ttc_l1_pt']['nbins'] = 40
HistSettings['SignalRegion']['ttc_l1_pt']['lowedge'] = 0
HistSettings['SignalRegion']['ttc_l1_pt']['highedge'] = 200


HistSettings['SignalRegion']['ttc_l1_eta'] = manager.dict()
HistSettings['SignalRegion']['ttc_l1_eta']['name'] = 'ttc_l1_eta'
HistSettings['SignalRegion']['ttc_l1_eta']['nbins'] = 30
HistSettings['SignalRegion']['ttc_l1_eta']['lowedge'] = -3
HistSettings['SignalRegion']['ttc_l1_eta']['highedge'] = 3

HistSettings['SignalRegion']['ttc_l1_phi'] = manager.dict()
HistSettings['SignalRegion']['ttc_l1_phi']['name'] = 'ttc_l1_phi'
HistSettings['SignalRegion']['ttc_l1_phi']['nbins'] = 20
HistSettings['SignalRegion']['ttc_l1_phi']['lowedge'] = -4
HistSettings['SignalRegion']['ttc_l1_phi']['highedge'] = 4

HistSettings['SignalRegion']['ttc_l2_pt'] = manager.dict()
HistSettings['SignalRegion']['ttc_l2_pt']['name'] = 'ttc_l2_pt'
HistSettings['SignalRegion']['ttc_l2_pt']['nbins'] = 40
HistSettings['SignalRegion']['ttc_l2_pt']['lowedge'] = 0
HistSettings['SignalRegion']['ttc_l2_pt']['highedge'] = 100

HistSettings['SignalRegion']['ttc_l2_eta'] = manager.dict()
HistSettings['SignalRegion']['ttc_l2_eta']['name'] = 'ttc_l2_eta'
HistSettings['SignalRegion']['ttc_l2_eta']['nbins'] = 30
HistSettings['SignalRegion']['ttc_l2_eta']['lowedge'] = -3
HistSettings['SignalRegion']['ttc_l2_eta']['highedge'] = 3

HistSettings['SignalRegion']['ttc_l2_phi'] = manager.dict()
HistSettings['SignalRegion']['ttc_l2_phi']['name'] = 'ttc_l2_phi'
HistSettings['SignalRegion']['ttc_l2_phi']['nbins'] = 20
HistSettings['SignalRegion']['ttc_l2_phi']['lowedge'] = -4
HistSettings['SignalRegion']['ttc_l2_phi']['highedge'] = 4


HistSettings['SignalRegion']['ttc_mll'] = manager.dict()
HistSettings['SignalRegion']['ttc_mll']['name'] = 'ttc_mll'
HistSettings['SignalRegion']['ttc_mll']['nbins'] = 60
HistSettings['SignalRegion']['ttc_mll']['lowedge'] = 60
HistSettings['SignalRegion']['ttc_mll']['highedge'] = 120


HistSettings['SignalRegion']['ttc_mllj1'] = manager.dict()
HistSettings['SignalRegion']['ttc_mllj1']['name'] = 'ttc_mllj1'
HistSettings['SignalRegion']['ttc_mllj1']['nbins'] = 20
HistSettings['SignalRegion']['ttc_mllj1']['lowedge'] = 0
HistSettings['SignalRegion']['ttc_mllj1']['highedge'] = 1000

HistSettings['SignalRegion']['ttc_mllj2'] = manager.dict()
HistSettings['SignalRegion']['ttc_mllj2']['name'] = 'ttc_mllj2'
HistSettings['SignalRegion']['ttc_mllj2']['nbins'] = 22
HistSettings['SignalRegion']['ttc_mllj2']['lowedge'] = 0
HistSettings['SignalRegion']['ttc_mllj2']['highedge'] = 1100


HistSettings['SignalRegion']['ttc_mllj3'] = manager.dict()
HistSettings['SignalRegion']['ttc_mllj3']['name'] = 'ttc_mllj3'
HistSettings['SignalRegion']['ttc_mllj3']['nbins'] = 20
HistSettings['SignalRegion']['ttc_mllj3']['lowedge'] = 0
HistSettings['SignalRegion']['ttc_mllj3']['highedge'] = 1000

HistSettings['SignalRegion']['ttc_met_phi'] = manager.dict()
HistSettings['SignalRegion']['ttc_met_phi']['name'] = 'ttc_met_phi'
HistSettings['SignalRegion']['ttc_met_phi']['nbins'] = 20
HistSettings['SignalRegion']['ttc_met_phi']['lowedge'] = -4
HistSettings['SignalRegion']['ttc_met_phi']['highedge'] = 4

HistSettings['SignalRegion']['ttc_met'] = manager.dict()
HistSettings['SignalRegion']['ttc_met']['name'] = 'ttc_met'
HistSettings['SignalRegion']['ttc_met']['nbins'] = 20
HistSettings['SignalRegion']['ttc_met']['lowedge'] = 0
HistSettings['SignalRegion']['ttc_met']['highedge'] = 200

HistSettings['SignalRegion']['HT'] = manager.dict()
HistSettings['SignalRegion']['HT']['name'] = 'HT'
HistSettings['SignalRegion']['HT']['nbins'] =25
HistSettings['SignalRegion']['HT']['lowedge'] = 0
HistSettings['SignalRegion']['HT']['highedge'] = 250

'''
HistSettings['SignalRegion']['j1_FlavCvL'] = manager.dict()
HistSettings['SignalRegion']['j1_FlavCvL']['name'] = 'j1_FlavCvL'
HistSettings['SignalRegion']['j1_FlavCvL']['nbins'] = 50
HistSettings['SignalRegion']['j1_FlavCvL']['lowedge'] = 0
HistSettings['SignalRegion']['j1_FlavCvL']['highedge'] = 1

HistSettings['SignalRegion']['j2_FlavCvL'] = manager.dict()
HistSettings['SignalRegion']['j2_FlavCvL']['name'] = 'j2_FlavCvL'
HistSettings['SignalRegion']['j2_FlavCvL']['nbins'] = 50
HistSettings['SignalRegion']['j2_FlavCvL']['lowedge'] = 0
HistSettings['SignalRegion']['j2_FlavCvL']['highedge'] = 1


HistSettings['SignalRegion']['j3_FlavCvL'] = manager.dict()
HistSettings['SignalRegion']['j3_FlavCvL']['name'] = 'j3_FlavCvL'
HistSettings['SignalRegion']['j3_FlavCvL']['nbins'] = 50
HistSettings['SignalRegion']['j3_FlavCvL']['lowedge'] = 0
HistSettings['SignalRegion']['j3_FlavCvL']['highedge'] = 1

HistSettings['SignalRegion']['j1_FlavB'] = manager.dict()
HistSettings['SignalRegion']['j1_FlavB']['name'] = 'j1_FlavB'
HistSettings['SignalRegion']['j1_FlavB']['nbins'] = 50
HistSettings['SignalRegion']['j1_FlavB']['lowedge'] = 0
HistSettings['SignalRegion']['j1_FlavB']['highedge'] = 1

HistSettings['SignalRegion']['j2_FlavB'] = manager.dict()
HistSettings['SignalRegion']['j2_FlavB']['name'] = 'j2_FlavB'
HistSettings['SignalRegion']['j2_FlavB']['nbins'] = 50
HistSettings['SignalRegion']['j2_FlavB']['lowedge'] = 0
HistSettings['SignalRegion']['j2_FlavB']['highedge'] = 1


HistSettings['SignalRegion']['j3_FlavB'] = manager.dict()
HistSettings['SignalRegion']['j3_FlavB']['name'] = 'j3_FlavB'
HistSettings['SignalRegion']['j3_FlavB']['nbins'] = 50
HistSettings['SignalRegion']['j3_FlavB']['lowedge'] = 0
HistSettings['SignalRegion']['j3_FlavB']['highedge'] = 1

HistSettings['SignalRegion']['j1_FlavCvB'] = manager.dict()
HistSettings['SignalRegion']['j1_FlavCvB']['name'] = 'j1_FlavCvB'
HistSettings['SignalRegion']['j1_FlavCvB']['nbins'] = 50
HistSettings['SignalRegion']['j1_FlavCvB']['lowedge'] = 0
HistSettings['SignalRegion']['j1_FlavCvB']['highedge'] = 1

HistSettings['SignalRegion']['j2_FlavCvB'] = manager.dict()
HistSettings['SignalRegion']['j2_FlavCvB']['name'] = 'j2_FlavCvB'
HistSettings['SignalRegion']['j2_FlavCvB']['nbins'] = 50
HistSettings['SignalRegion']['j2_FlavCvB']['lowedge'] = 0
HistSettings['SignalRegion']['j2_FlavCvB']['highedge'] = 1


HistSettings['SignalRegion']['j3_FlavCvB'] = manager.dict()
HistSettings['SignalRegion']['j3_FlavCvB']['name'] = 'j3_FlavCvB'
HistSettings['SignalRegion']['j3_FlavCvB']['nbins'] = 50
HistSettings['SignalRegion']['j3_FlavCvB']['lowedge'] = 0
HistSettings['SignalRegion']['j3_FlavCvB']['highedge'] = 1
'''
HistSettings['ChargeFlipRegion']['ttc_l1_pt'] = manager.dict()
HistSettings['ChargeFlipRegion']['ttc_l1_pt']['name'] = 'ttc_l1_pt'
HistSettings['ChargeFlipRegion']['ttc_l1_pt']['nbins'] = 40
HistSettings['ChargeFlipRegion']['ttc_l1_pt']['lowedge'] = 0
HistSettings['ChargeFlipRegion']['ttc_l1_pt']['highedge'] = 200


HistSettings['ChargeFlipRegion']['ttc_l1_eta'] = manager.dict()
HistSettings['ChargeFlipRegion']['ttc_l1_eta']['name'] = 'ttc_l1_eta'
HistSettings['ChargeFlipRegion']['ttc_l1_eta']['nbins'] = 30
HistSettings['ChargeFlipRegion']['ttc_l1_eta']['lowedge'] = -3
HistSettings['ChargeFlipRegion']['ttc_l1_eta']['highedge'] = 3

HistSettings['ChargeFlipRegion']['ttc_l1_phi'] = manager.dict()
HistSettings['ChargeFlipRegion']['ttc_l1_phi']['name'] = 'ttc_l1_phi'
HistSettings['ChargeFlipRegion']['ttc_l1_phi']['nbins'] = 20
HistSettings['ChargeFlipRegion']['ttc_l1_phi']['lowedge'] = -4
HistSettings['ChargeFlipRegion']['ttc_l1_phi']['highedge'] = 4

HistSettings['ChargeFlipRegion']['ttc_l2_pt'] = manager.dict()
HistSettings['ChargeFlipRegion']['ttc_l2_pt']['name'] = 'ttc_l2_pt'
HistSettings['ChargeFlipRegion']['ttc_l2_pt']['nbins'] = 40
HistSettings['ChargeFlipRegion']['ttc_l2_pt']['lowedge'] = 0
HistSettings['ChargeFlipRegion']['ttc_l2_pt']['highedge'] = 100

HistSettings['ChargeFlipRegion']['ttc_l2_eta'] = manager.dict()
HistSettings['ChargeFlipRegion']['ttc_l2_eta']['name'] = 'ttc_l2_eta'
HistSettings['ChargeFlipRegion']['ttc_l2_eta']['nbins'] = 30
HistSettings['ChargeFlipRegion']['ttc_l2_eta']['lowedge'] = -3
HistSettings['ChargeFlipRegion']['ttc_l2_eta']['highedge'] = 3

HistSettings['ChargeFlipRegion']['ttc_l2_phi'] = manager.dict()
HistSettings['ChargeFlipRegion']['ttc_l2_phi']['name'] = 'ttc_l2_phi'
HistSettings['ChargeFlipRegion']['ttc_l2_phi']['nbins'] = 20
HistSettings['ChargeFlipRegion']['ttc_l2_phi']['lowedge'] = -4
HistSettings['ChargeFlipRegion']['ttc_l2_phi']['highedge'] = 4


HistSettings['ChargeFlipRegion']['ttc_mll'] = manager.dict()
HistSettings['ChargeFlipRegion']['ttc_mll']['name'] = 'ttc_mll'
HistSettings['ChargeFlipRegion']['ttc_mll']['nbins'] = 60
HistSettings['ChargeFlipRegion']['ttc_mll']['lowedge'] = 60
HistSettings['ChargeFlipRegion']['ttc_mll']['highedge'] = 120


