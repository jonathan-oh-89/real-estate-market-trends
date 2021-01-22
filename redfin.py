import os
import pandas as pd


def use_redfin_msa_names():
    path = os.getcwd()
    with open(os.path.join(path + '/files/med_sale_price_Full_Data_data.csv')) as f:
        df = pd.read_csv(f)
        df = df[['Table Id','Region']].drop_duplicates()

        df = convert_redfinid_to_cbsaid(df)

        return df

def convert_redfinid_to_cbsaid(df):
    redfinid_to_cbsaid = {
        16984: 16980,
        19124: 19100,
        31084: 31080,
        41884: 41860,
        37964: 37980,
        14454: 14460,
        35614: 35620,
        47894: 47900,
        33124: 33100,
        19804: 19820,
        42644: 42660,
    }

    df = df.rename(columns={'Table Id': 'geographyid','Region':'region'})
    df['region'] = df['region'].apply(lambda x: x.replace(' metro area',''))
    df['geographyid'] = df['geographyid'].replace(redfinid_to_cbsaid)

    return df

def redfin():
    path = os.getcwd()
    with open(os.path.join(path + '/files/med_sale_price_Full_Data_data.csv')) as f:
        df = pd.read_csv(f)
        df['date'] = pd.to_datetime(df['Period Begin'].str.strip(), format='%m/%d/%y')
        df['Median Sale Price'] = df['Median Sale Price'].apply(lambda x: str(x).replace('$','').replace(',','').replace('K','000'))

        df = df[['Table Id','Region','date','months_of_supply','Median Sale Price']].rename(columns={'months_of_supply':'monthsofsupply','Median Sale Price':'mediansaleprice'})

        df = convert_redfinid_to_cbsaid(df)

        df.to_csv('files/redfin.csv', index=False)


if __name__ == "__main__":
    redfin()