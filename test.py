import json


path = {
        "MET":['/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METB.root'
            ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METC.root'
            ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METD.root'
            ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METE.root'
            ,'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/METF.root'],
        "TTTo2L":'/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/TTTo2L.root'
        }



#with open('./data/year2018/ForEfficiency/filein.json','w') as f:

#    json.dump(path,f)
#print(data['DoubleElectron'])


#with open('./others/property_name/name.json','rb') as f:
#    data = json.load(f)
#print(type(data))
#print(data['DoubleElectron'])


#df = {a: a for a in [1,2,3,]}

#print(df)

import os 
if not os.path.isfile('./123.json'):
    data = dict()
else:
    with open('./123.json','r') as f :
        data = json.load(f)

#data['MC'] = '123'
data['Data'] = '789'

with open('./123.json',mode='w') as f :
    json.dump(data,f,indent=4)
