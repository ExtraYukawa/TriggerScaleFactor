from multiprocessing import Manager

manager = Manager()

HistSettings =manager.dict()
HistSettings['DY_l1_pt'] = manager.dict()
HistSettings['DY_l1_pt']['name'] = 'OPS_l1_pt'
HistSettings['DY_l1_pt']['nbins'] = 40
HistSettings['DY_l1_pt']['lowedge'] = 0
HistSettings['DY_l1_pt']['highedge'] = 200


HistSettings['DY_l1_eta'] = manager.dict()
HistSettings['DY_l1_eta']['name'] = 'OPS_l1_eta'
HistSettings['DY_l1_eta']['nbins'] = 30
HistSettings['DY_l1_eta']['lowedge'] = -3
HistSettings['DY_l1_eta']['highedge'] = 3

HistSettings['DY_l1_phi'] = manager.dict()
HistSettings['DY_l1_phi']['name'] = 'OPS_l1_phi'
HistSettings['DY_l1_phi']['nbins'] = 20
HistSettings['DY_l1_phi']['lowedge'] = -4
HistSettings['DY_l1_phi']['highedge'] = 4

HistSettings['DY_l2_pt'] = manager.dict()
HistSettings['DY_l2_pt']['name'] = 'OPS_l2_pt'
HistSettings['DY_l2_pt']['nbins'] = 40
HistSettings['DY_l2_pt']['lowedge'] = 0
HistSettings['DY_l2_pt']['highedge'] = 100

HistSettings['DY_l2_eta'] = manager.dict()
HistSettings['DY_l2_eta']['name'] = 'OPS_l2_eta'
HistSettings['DY_l2_eta']['nbins'] = 30
HistSettings['DY_l2_eta']['lowedge'] = -3
HistSettings['DY_l2_eta']['highedge'] = 3

HistSettings['DY_l2_phi'] = manager.dict()
HistSettings['DY_l2_phi']['name'] = 'OPS_l2_phi'
HistSettings['DY_l2_phi']['nbins'] = 20
HistSettings['DY_l2_phi']['lowedge'] = -4
HistSettings['DY_l2_phi']['highedge'] = 4

HistSettings['DY_z_pt'] = manager.dict()
HistSettings['DY_z_pt']['name'] = 'OPS_z_pt'
HistSettings['DY_z_pt']['nbins'] = 50
HistSettings['DY_z_pt']['lowedge'] = 0
HistSettings['DY_z_pt']['highedge'] = 200

HistSettings['DY_z_eta'] = manager.dict()
HistSettings['DY_z_eta']['name'] = 'OPS_z_eta'
HistSettings['DY_z_eta']['nbins'] = 20
HistSettings['DY_z_eta']['lowedge'] = -3
HistSettings['DY_z_eta']['highedge'] = 3

HistSettings['DY_z_phi'] = manager.dict()
HistSettings['DY_z_phi']['name'] = 'OPS_z_phi'
HistSettings['DY_z_phi']['nbins'] = 20
HistSettings['DY_z_phi']['lowedge'] = -4
HistSettings['DY_z_phi']['highedge'] = 4

HistSettings['DY_z_mass'] = manager.dict()
HistSettings['DY_z_mass']['name'] = 'OPS_z_mass'
HistSettings['DY_z_mass']['nbins'] = 60
HistSettings['DY_z_mass']['lowedge'] = 60
HistSettings['DY_z_mass']['highedge'] = 120

HistSettings['ttc_l1_pt'] = manager.dict()
HistSettings['ttc_l1_pt']['name'] = 'OPS_l1_pt'
HistSettings['ttc_l1_pt']['nbins'] = 40
HistSettings['ttc_l1_pt']['lowedge'] = 0
HistSettings['ttc_l1_pt']['highedge'] = 200


HistSettings['ttc_l1_eta'] = manager.dict()
HistSettings['ttc_l1_eta']['name'] = 'OPS_l1_eta'
HistSettings['ttc_l1_eta']['nbins'] = 30
HistSettings['ttc_l1_eta']['lowedge'] = -3
HistSettings['ttc_l1_eta']['highedge'] = 3

HistSettings['ttc_l1_phi'] = manager.dict()
HistSettings['ttc_l1_phi']['name'] = 'ttc_l1_phi'
HistSettings['ttc_l1_phi']['nbins'] = 20
HistSettings['ttc_l1_phi']['lowedge'] = -4
HistSettings['ttc_l1_phi']['highedge'] = 4

HistSettings['ttc_l2_pt'] = manager.dict()
HistSettings['ttc_l2_pt']['name'] = 'ttc_l2_pt'
HistSettings['ttc_l2_pt']['nbins'] = 40
HistSettings['ttc_l2_pt']['lowedge'] = 0
HistSettings['ttc_l2_pt']['highedge'] = 100

HistSettings['ttc_l2_eta'] = manager.dict()
HistSettings['ttc_l2_eta']['name'] = 'ttc_l2_eta'
HistSettings['ttc_l2_eta']['nbins'] = 30
HistSettings['ttc_l2_eta']['lowedge'] = -3
HistSettings['ttc_l2_eta']['highedge'] = 3

HistSettings['ttc_l2_phi'] = manager.dict()
HistSettings['ttc_l2_phi']['name'] = 'ttc_l2_phi'
HistSettings['ttc_l2_phi']['nbins'] = 20
HistSettings['ttc_l2_phi']['lowedge'] = -4
HistSettings['ttc_l2_phi']['highedge'] = 4


HistSettings['ttc_mll'] = manager.dict()
HistSettings['ttc_mll']['name'] = 'ttc_mll'
HistSettings['ttc_mll']['nbins'] = 60
HistSettings['ttc_mll']['lowedge'] = 60
HistSettings['ttc_mll']['highedge'] = 120

