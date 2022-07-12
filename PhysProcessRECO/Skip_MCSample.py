


def Skip_MC(phys_name:str,year:str,IsFake=True,Skip_Sample=True)->bool:

    if IsFake:
        MC_Sample_Skipped = ['TTTo1L','WJets']
    else:MC_Sample_Skipped=['']
    if year=='2017':
        if Skip_Sample:
            MC_Sample_Skipped.append('ssWW')
            MC_Sample_Skipped.append('ZG_ew')
            MC_Sample_Skipped.append('WZ_ew')

    if phys_name in MC_Sample_Skipped:
        return True
    else:return False
