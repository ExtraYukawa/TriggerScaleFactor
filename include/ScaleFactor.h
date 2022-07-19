#ifndef __IDSCALEFACTOR_H__
#define __IDSCALEFACTOR_H__
#include "TH2D.h"
#include "TH2F.h"
#include "TFile.h"
#include "ROOT/RDataFrame.hxx"
#include <stdexcept>
#include "TMath.h"
#include <iostream>
#include "DataFormats/Math/interface/deltaR.h"
#include "ROOT/RVec.hxx"

double IDScaleFact(const char *, TH2D*,TH2D*,float ,float , float , float );

//float ID_sf_singlelepton(TH2D*,float,float);
double Lepton_IDSF(TH2D*,float,float);
double RECO_Muon_SF(TH2F*,float,float);


double Trigger_sf_pteta(TH2D *, float, float);
double Trigger_sf_l1l2pt(TH2D *, float, float);
double Trigger_sf_l1l2eta(TH2D *, float, float);

int kinematic(bool activate, float l1_pt,float l2_pt ,float l1_eta , float l2_eta);
double chargeflip_sf(TH2D *h , int kinematic_region , int reco_isOS, int gen_isOS,float sigma);
double fr_weight(TH2D* h_fr_l1, TH2D * h_fr_l2, bool Flag_1P1F, bool Flag_0P2F, bool l1_faketag, float l1_pt , float l1_eta, float l2_pt, float l2_eta, bool IsData);

double CtagSF(TH2D *h_flavc,TH2D *h_flavb,TH2D *h_flavl,int n_tight_jet , ROOT::VecOps::RVec<Int_t> tightJets_id_in24,ROOT::VecOps::RVec<Int_t> JetpuId,ROOT::VecOps::RVec<Float_t> Jet_pt, ROOT::VecOps::RVec<Int_t> Jet_hadflav, ROOT::VecOps::RVec<Float_t> CvsL, ROOT::VecOps::RVec<Float_t> CvsB);

int gen_isOS(float l1_pt, float l1_eta, float l1_phi, int l1_pdgid, float l2_pt, float l2_eta, float l2_phi, int l2_pdgid, int ngenlepton, ROOT::VecOps::RVec<Float_t> gen_pt, ROOT::VecOps::RVec<Float_t> gen_eta, ROOT::VecOps::RVec<Float_t> gen_phi, ROOT::VecOps::RVec<Int_t> gen_pdgid);
#endif
