

import ROOT



cnt = dict()

for era in ['B','C','D','E','F']:

    f = ROOT.TFile.Open(f"/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/SingleEG{era}.root")
    Tree= f.Get('Events')
    cnt[era] = Tree.GetEntries()

    print(Tree.GetEntries())
for era in ['B','C','D','E','F']:

    f = ROOT.TFile.Open(f"/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/DoubleEG{era}.root")
    Tree= f.Get('Events')
    cnt[era] += Tree.GetEntries()

    print(Tree.GetEntries())
print(f"B:{41.48*cnt['B']/(cnt['B']+cnt['C']+cnt['D']+cnt['E']+cnt['F'])}")
print(f"C:{41.48*cnt['C']/(cnt['B']+cnt['C']+cnt['D']+cnt['E']+cnt['F'])}")
print(f"D:{41.48*cnt['D']/(cnt['B']+cnt['C']+cnt['D']+cnt['E']+cnt['F'])}")
print(f"E:{41.48*cnt['E']/(cnt['B']+cnt['C']+cnt['D']+cnt['E']+cnt['F'])}")
print(f"F:{41.48*cnt['F']/(cnt['B']+cnt['C']+cnt['D']+cnt['E']+cnt['F'])}")
