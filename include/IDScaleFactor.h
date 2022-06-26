#ifndef __IDSCALEFACTOR_H__
#define __IDSCALEFACTOR_H__
#include "TH2D.h"
#include "TH2F.h"
#include "TFile.h"
#include <stdexcept>
#include "TMath.h"

float IDScaleFact(const char *, TH2D*,TH2D*,float ,float , float , float );

//float ID_sf_singlelepton(TH2D*,float,float);
float Lepton_IDSF(TH2D*,float,float);
float RECO_Muon_SF(TH2F*,float,float);


float Trigger_sf_pteta(TH2D *, float, float);
float Trigger_sf_l1l2pt(TH2D *, float, float);
float Trigger_sf_l1l2eta(TH2D *, float, float);


#endif
