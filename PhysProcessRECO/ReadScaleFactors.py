
Claim = dict()

Claim['TrigSF'] =''
Claim['IDSF'] = dict()


Claim['TrigSF']='''
#include "TFile.h"
#include "TH2D.h"
TFile *f_TrigSF = TFile::Open("{0}");
TH2D *h_TrigSF= (TH2D*)f_TrigSF->Get("{1}");
'''

Claim['IDSF']['DoubleElectron']='''
#include "TFile.h"
#include "TH2D.h"
TFile *f_IDSF = TFile::Open("{0}");
TH2D *h_IDSF= (TH2D*)f_IDSF->Get("{1}");
'''

Claim['IDSF']['DoubleMuon'] = '''
#include "TFile.h"
#include "TH2D.h"
TFile *f_IDSF = TFile::Open("{0}");
TH2D *h_IDSF= (TH2D*)f_IDSF->Get("{1}");
TH2F *h_RECOSF= (TH2F*)f_IDSF->Get("{2}");

'''

Claim['IDSF']['ElectronMuon'] ='''

#include "TFile.h"
#include "TH2D.h"
#include "TH2F.h"
TFile *f1_IDSF = TFile::Open("{0}");
TFile *f2_IDSF = TFile::Open("{1}");
TH2D *h1_IDSF= (TH2D*)f1_IDSF->Get("{2}");
TH2D *h2_IDSF = (TH2D*)f2_IDSF->Get("{3}");
TH2F *h_RECOSF= (TH2F*)f1_IDSF->Get("{4}");

'''


Claim['ChargeFlipSF'] ='''

#include "TFile.h"
#include "TH2D.h"
TFile*f_cf=TFile::Open("{0}");
TH2D*h_OS=(TH2D*)f_cf->Get("OS_ChargeFlip_SF");
TH2D*h_SS = (TH2D*)f_cf->Get("SS_ChargeFlip_SF_AllUnc"); 

TFile*f_cfregion=TFile::Open("{1}");
TH2D*h_data = (TH2D*) f_cfregion->Get("data_CFRate");

'''
Claim['FakeRate']=dict()


Claim['FakeRate']['DoubleElectron'] = '''
#include "TFile.h"
#include "TH2D.h"
TFile *f1_fr = TFile::Open("{0}");
TH2D *h_fr_1 = (TH2D*)f1_fr->Get("fakerate");
TH2D *h_fr_2 = h_fr_1
'''

Claim['FakeRate']['DoubleMuon'] = '''
#include "TFile.h"
#include "TH2D.h"
TFile *f1_fr = TFile::Open("{0}");
TH2D *h_fr_1 = (TH2D*)f1_fr->Get("fakerate");
TH2D *h_fr_2 = h_fr_1
'''
Claim['FakeRate']['ElectronMuon'] = '''
#include "TFile.h"
#include "TH2D.h"
TFile *f1_fr = TFile::Open("{0}");
TH2D *h_fr_1 = (TH2D*)f1_fr->Get("fakerate");
TFile *f2_fr = TFile::Open("{1}");
TH2D *h_fr_2 = (TH2D*)f2_fr->Get("fakerate");
'''
Claim['CtagSF'] ='''

#include "TFile.h"
#include "TH2D.h"
TFile*fctag=TFile::Open("{0}");
TH2D*h_flavc=(TH2D*)fctag->Get("SFc_hist");
TH2D*h_flavb=(TH2D*)fctag->Get("SFb_hist");
TH2D*h_flavl=(TH2D*)fctag->Get("SFl_hist");

'''

