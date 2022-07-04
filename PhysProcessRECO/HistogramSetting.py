from multiprocessing import Manager

manager = Manager()

HistSettings =manager.dict()
HistSettings['SignalRegion'] = manager.dict()
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
HistSettings['SignalRegion']['ttc_l1_pt']['name'] = 'OPS_l1_pt'
HistSettings['SignalRegion']['ttc_l1_pt']['nbins'] = 40
HistSettings['SignalRegion']['ttc_l1_pt']['lowedge'] = 0
HistSettings['SignalRegion']['ttc_l1_pt']['highedge'] = 200


HistSettings['SignalRegion']['ttc_l1_eta'] = manager.dict()
HistSettings['SignalRegion']['ttc_l1_eta']['name'] = 'OPS_l1_eta'
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

