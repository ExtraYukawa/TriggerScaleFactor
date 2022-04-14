#ifndef _HEM_VETO_H
#define _HEM_VETO_H
#include "ROOT/RDataFrame.hxx"
#include "TString.h"
#include "TMath.h"
#include "ROOT/RVec.hxx"
using namespace ROOT::VecOps;
using rvec_f = const RVec<float> &;
bool veto_hemregion(int,rvec_f,rvec_f);
#endif
