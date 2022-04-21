#ifndef _HEM_VETO_H
#define _HEM_VETO_H
#include "ROOT/RDataFrame.hxx"
#include "TString.h"
#include "TMath.h"
#include "ROOT/RVec.hxx"
#include <iostream>
#include <time.h>
#include <stdlib.h>
using namespace ROOT::VecOps;
using namespace std;
using rvec_f = const RVec<float> &;
bool veto_hemregion(int,rvec_f,rvec_f);
bool valid_region_hem(int);
bool veto_hemregion_sim(float, rvec_f,rvec_f,float);
int not_hem_event(int,rvec_f,rvec_f);

float prob();
int test_prob(float);
#endif
