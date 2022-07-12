#ifndef __IDSCALEFACTOR_H__
#define __IDSCALEFACTOR_H__
#include "TH2D.h"
#include "TH2F.h"
#include "TFile.h"
#include <stdexcept>
#include "TMath.h"
#include <iostream>


double IDScaleFact(const char *, TH2D*,TH2D*,float ,float , float , float );

//float ID_sf_singlelepton(TH2D*,float,float);
double Lepton_IDSF(TH2D*,float,float);
double RECO_Muon_SF(TH2F*,float,float);


double Trigger_sf_pteta(TH2D *, float, float);
double Trigger_sf_l1l2pt(TH2D *, float, float);
double Trigger_sf_l1l2eta(TH2D *, float, float);

int kinematic(bool activate, float l1_pt,float l2_pt ,float l1_eta , float l2_eta);
double chargeflip_sf(TH2D *h , int kinematic_region , bool same_sign,float sigma);
double fr_weight(TH2D* h_fr_l1, TH2D * h_fr_l2, bool Flag_1P1F, bool Flag_0P2F, bool l1_faketag, float l1_pt , float l1_eta, float l2_pt, float l2_eta, bool IsData);

#endif
