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
Histogram_Definition['Same_Type_IDSF']='''
#include "TFile.h"
#include "TH2D.h"
TFile *f1_IDSF = TFile::Open("{0}");
TH2D *h1_IDSF= (TH2D*)f1_IDSF->Get("{1}");
TH2D *h2_IDSF = h1_IDSF;
'''

Histogram_Definition['Diff_Type_IDSF']='''
#include "TFile.h"
#include "TH2D.h"
TFile *f1_IDSF = TFile::Open("{0}");
TFile *f2_IDSF = TFile::Open("{1}");
TH2D *h1_IDSF= (TH2D*)f1_IDSF->Get("{2}");
TH2D *h2_IDSF = (TH2D*)f2_IDSF->Get("{3}");
'''
Histogram_Definition['TrigSF']='''
#include "TFile.h"
#include "TH2D.h"
TFile *f1_TrigSF = TFile::Open("{0}");
TFile *f2_TrigSF = TFile::Open("{1}");
TH2D *h1_TrigSF= (TH2D*)f1_TrigSF->Get("{2}");
TH2D *h2_TrigSF = (TH2D*)f2_TrigSF->Get("{3}");
'''

