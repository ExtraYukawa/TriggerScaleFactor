#include "HEM_veto.h"
int not_hem_event(int run,rvec_f Jet_phi,rvec_f Jet_eta){

    if(run < 319077){
        return 1;
    }
    
    else{
        for(unsigned idx = 0; idx < Jet_phi.size(); idx++){
            if((Jet_eta.at(idx) > -3.2) && (Jet_eta.at(idx) < -1.3)\
                    && (Jet_phi.at(idx) > -1.57) && (Jet_phi.at(idx) < -0.87)){
                        return 0;
            }
        }
        return 1;
    }





}


bool veto_hemregion(int run,rvec_f Jet_phi,rvec_f Jet_eta){
    if(run < 319077){
        return true;
    }
    
    else{
        for(unsigned idx = 0; idx < Jet_phi.size(); idx++){
            if((Jet_eta.at(idx) > -3.2) && (Jet_eta.at(idx) < -1.3)\
                    && (Jet_phi.at(idx) > -1.57) && (Jet_phi.at(idx) < -0.87)){
                        return false;
            }
        }
        return true;
    }
}

bool valid_region_hem(int run){
    if(run >= 319077){
        return true;
    }
    else 
        return false;
}
bool veto_hemregion_sim(float prob, rvec_f Jet_phi,rvec_f Jet_eta,float veto_ratio){
    if(prob > veto_ratio)
        return true;
    
    else{
        for(unsigned idx = 0; idx < Jet_phi.size(); idx++){
            if((Jet_eta.at(idx) > -3.2) && (Jet_eta.at(idx) < -1.3)\
                && (Jet_phi.at(idx) > -1.57) && (Jet_phi.at(idx) < -0.87)){
                return false;
            }
    
        }
        return true;
    }
}  
float prob(){
    return (float) rand()/ RAND_MAX;
}

int test_prob(float prob){
    if (prob < 0.6){
        return 1.;
    }
    else
        return 0.;
}
