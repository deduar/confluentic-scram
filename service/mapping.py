import pandas as pd

class MAPPING:
    
    def __init__(self) -> None:
        pass

    def load_mapping(self):
        mapp = pd.read_csv('/app/data/CatMyvalueAba.csv')
        mapp[['cat','subcat']] = mapp.PFM_V6.str.split("_", expand = True)
        mapp['cat'] = mapp['cat'].str.lower()
        mapp['subcat'] = mapp['subcat'].str.lower()
        return mapp
    
    def get_cat_subcat(self,mapp:pd,cat_id:int):
        return mapp[(mapp['N1_ID_padre'] == cat_id) | (mapp['N2_ID_padre'] == cat_id) | (mapp['N3_ID_padre'] == cat_id)]