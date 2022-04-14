#include "HEM_veto.h"

bool veto_hemregion(int run,rvec_f Jet_phi,rvec_f Jet_eta){
    if(run >= 319077){
        for(unsigned idx = 0; idx < Jet_phi.size(); idx++){
            if((Jet_eta.at(idx) > -3.2) && (Jet_eta.at(idx) < -1.3)\
                    && (Jet_phi.at(idx) > -1.57) && (Jet_phi.at(idx) < -0.87)){
                    return false;
                    }
        }
    }
    return true;
}


