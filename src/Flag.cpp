#include "Flag.h"

bool Region_FLAG(int region, int event_region){
    if(region == event_region)
        return true;
    return false;
}
