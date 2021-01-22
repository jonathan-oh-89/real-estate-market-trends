import os
import pandas as pd
from arcgis.gis import GIS
from arcgis.geoenrichment import enrich
import redfin

def get_top50_cbsa():
    path = os.getcwd()
    with open(os.path.join(path + '/files/population_by_cbsa.csv')) as f:
        df = pd.read_csv(f,converters={'StdGeographyID':str})
        df = df.sort_values(by=['2020 Total Population'], ascending=False)[:51]
        return df

def dump_csv():
    redfin_names = redfin.use_redfin_msa_names()
    cbsa_top50 = get_top50_cbsa()
    df = cbsa_top50
    data_variables = get_data_variables()
    final_df = pd.DataFrame()

    gis = GIS('https://www.arcgis.com', 'arcgis_python', 'P@ssword123')

    for k,v in data_variables.items():
        data = enrich(study_areas=[{"sourceCountry": "US", "layer": "US.CBSA", "ids": list(df['StdGeographyID'])}],
                      analysis_variables=list(v),
                      return_geometry=False)
        data = data.drop(columns=['StdGeographyLevel' ,'ID', 'apportionmentConfidence', 'OBJECTID', 'aggregationMethod', 'populationToPolygonSizeRating', 'HasData', 'sourceCountry'])

        if k == 'population':
            data = data.rename(columns=data_variables['population'])
            data = pd.melt(data, id_vars=['StdGeographyName','StdGeographyID'], var_name='year')
            data['variable'] = data['year']
            data['year'] = data['year'].apply(lambda x: x.replace(' Total Population',''))
        else:
            data = data.rename(columns=data_variables[k])
            data = pd.melt(data, id_vars=['StdGeographyName','StdGeographyID'], var_name='variable')
            data['year'] = 2020
            data['value'] = data['value'] * .01

        data['datatype'] = k

        if final_df.empty:
            final_df = data
        else:
            final_df = final_df.append(data)

    final_df[['StdGeographyID']] = final_df[['StdGeographyID']].astype(int)
    final_df = pd.merge(final_df,redfin_names,left_on=['StdGeographyID'], right_on=['geographyid'],how='left')[['geographyid','datatype','variable','region','year','value']]
    final_df.to_csv('files/metrostats.csv',index=False)



def get_data_variables():
    data_variables = {
        'population':{
            'TSPOP10_CY': '2010 Total Population',
            'TSPOP11_CY': '2011 Total Population',
            'TSPOP12_CY': '2012 Total Population',
            'TSPOP13_CY': '2013 Total Population',
            'TSPOP14_CY': '2014 Total Population',
            'TSPOP15_CY': '2015 Total Population',
            'TSPOP16_CY': '2016 Total Population',
            'TSPOP17_CY': '2017 Total Population',
            'TSPOP18_CY': '2018 Total Population',
            'TSPOP19_CY': '2019 Total Population',
            'TOTPOP_CY': '2020 Total Population',
        },
        'propertytypes':{
            'ACSUNT1DET_P': 'Single Family (detached)',
            'ACSUNT1ATT_P': 'Single Family (attached)',
            'ACSUNT2_P': 'Duplex',
            'ACSUNT3_P': 'Triplex and Quadplex',
            'ACSUNT5_P': '5-9 Unit Multifamily',
            'ACSUNT10_P': '10-19 Unit Multifamily',
            'ACSUNT20_P': '20-49 Unit Multifamily',
            'ACSUNT50UP_P': '50 or More Unit Multifamily',
            'ACSUNTMOB_P': 'Mobile Homes',
        },
        'employmentindustries':{
            'INDAGRI_CY_P':'Agriculture/Forestry/Fishing/Hunting',
            'INDMIN_CY_P':'Mining/Quarrying/Oil & Gas Extraction',
            'INDCONS_CY_P':'Construction',
            'INDMANU_CY_P':'Manufacturing',
            'INDWHTR_CY_P':'Wholesale Trade',
            'INDRTTR_CY_P':'Retail Trade',
            'INDTRAN_CY_P':'Transportation/Warehousing',
            'INDUTIL_CY_P':'Utilities',
            'INDINFO_CY_P':'Information (non-tech)',
            'INDFIN_CY_P':'Finance/Insurance',
            'INDRE_CY_P':'Real Estate/Rental/Leasing',
            'INDTECH_CY_P':'Professional/Scientific/Technology',
            'INDMGMT_CY_P':'Management of Companies/Enterprises',
            'INDADMN_CY_P':'Admin/Support/Waste Management Services',
            'INDEDUC_CY_P':'Educational Services',
            'INDHLTH_CY_P':'Health Care/Social Assistance',
            'INDARTS_CY_P':'Arts/Entertainment/Recreation',
            'INDFOOD_CY_P':'Accommodation/Food Services',
            'INDOTSV_CY_P':'Other Services',
            'INDPUBL_CY_P':'Public Administration'
        }
    }

    return data_variables




if __name__ == "__main__":
    dump_csv()