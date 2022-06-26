Histogram_Definition=dict()
Histogram_Definition['Same_Type']='''
#include "TFile.h"
#include "TH2D.h"
TFile *f1 = TFile::Open("{0}");
TH2D *h1= (TH2D*)f1->Get("{1}");
TH2D *h2 = h1;
'''
Histogram_Definition['Diff_Type']='''
#include "TFile.h"
#include "TH2D.h"
TFile *f1 = TFile::Open("{0}");
TFile *f2 = TFile::Open("{1}");
TH2D *h1= (TH2D*)f1->Get("{2}");
TH2D *h2 = (TH2D*)f2->Get("{3}");
'''
Histogram_Definition['Single']='''
#include "TFile.h"
#include "TH2D.h"
TFile *f1 = TFile::Open("{0}");
TH2D *h1= (TH2D*)f1->Get("{1}");
'''
Histogram_Definition['DoubleElectron']='''
#include "TFile.h"
#include "TH2D.h"
TFile *f_IDSF = TFile::Open("{0}");
TH2D *h1_IDSF= (TH2D*)f_IDSF->Get("{1}");
TH2D *h2_IDSF = h1_IDSF;
'''
Histogram_Definition['DoubleMuon']='''
#include "TFile.h"
#include "TH2D.h"
#include "TH2F.h"
TFile *f_IDSF = TFile::Open("{0}");
TH2D *h1_IDSF= (TH2D*)f_IDSF->Get("{1}");
TH2D *h2_IDSF = h1_IDSF;
TH2F *h_RECOSF= (TH2F*)f_IDSF->Get("{2}");
'''

Histogram_Definition['ElectronMuon']='''
#include "TFile.h"
#include "TH2D.h"
#include "TH2F.h"
TFile *f1_IDSF = TFile::Open("{0}");
TFile *f2_IDSF = TFile::Open("{1}");
TH2D *h1_IDSF= (TH2D*)f1_IDSF->Get("{2}");
TH2D *h2_IDSF = (TH2D*)f2_IDSF->Get("{3}");
TH2F *h_RECOSF = (TH2F*)f1_IDSF->Get("{4}");
'''

Histogram_Definition['TrigSF']='''
#include "TFile.h"
#include "TH2D.h"
TFile *TrigSF = TFile::Open("{0}");
TH2D *h_TrigSF= (TH2D*)TrigSF->Get("{1}");
'''

