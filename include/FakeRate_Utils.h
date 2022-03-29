#ifndef FakeRate_Utils_H
#define FakeRate_Utils_H

#include "ROOT/RDataFrame.hxx"
#include "TString.h"
#include "TMath.h"
#include "ROOT/RVec.hxx"

using namespace ROOT::VecOps;
using rvec_f = const RVec<float> &;
float MC_eff_lumi(float ,const char *);
#endif
