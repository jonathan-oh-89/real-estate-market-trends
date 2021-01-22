import pandas as pd
import requests as r
import import_esri


def unemployment():
    nationalunemployment = pd.DataFrame()
    metrounemployment = pd.DataFrame()

    urls = {
        'national': 'https://download.bls.gov/pub/time.series/ln/ln.data.1.AllData',
        'metro': 'https://download.bls.gov/pub/time.series/la/la.data.60.Metro'
    }

    delimeter = '\t'
    startyear = 2012

    # Parse Data
    for k,v in urls.items():
        data = r.get(v)
        row_list = []
        skip = 0
        for line in data.text.splitlines():
            if skip is 0:
                headers = [x.strip() for x in line.split(delimeter)]
                skip = 1
            else:
                row = [x.strip() for x in line.split(delimeter, maxsplit=len(headers) - 1)]

                if k == 'national':
                    #Get unemployment series and years 2000 and up
                    if row[0] != 'LNS14000000' or int(row[1]) < startyear:
                        continue
                else:
                    if row[2] == 'M13' or row[0][-2:] != '03' or int(row[1]) < startyear or row[0][2] != 'U':
                        continue

                row_list.append(row)

        if k == 'national':
            nationalunemployment = pd.DataFrame(row_list, columns=headers)
            nationalunemployment['series_id'] = '1400'
        else:
            metrounemployment = pd.DataFrame(row_list, columns=headers)
            metrounemployment['series_id'] = metrounemployment['series_id'].str[7:12]

    unemployment = pd.concat([nationalunemployment, metrounemployment], ignore_index=True)
    unemployment['date'] = unemployment['period'].str.replace('M','') + '/01/' + unemployment['year']
    unemployment['date'] = pd.to_datetime(unemployment['date'].str.strip(), format='%m/%d/%Y')
    unemployment = unemployment.drop(columns=['year','period','footnote_codes'])\
        .rename(columns={'series_id':'geographyid','value':'unemploymentrate'})

    NECTAID_to_MSAID_conversion = {
        '70750': '12620', '70900': '12700', '71050': '12740', '71350': '13540', '71500': '13620', '71650': '14460',
        '71950': '14860', '72400': '15540', '72700': '18180',
        '19380': '19430', '73450': '25540', '73750': '28300', '73900': '29060', '74350': '30100', '74650': '30340',
        '74950': '31700', '75700': '35300', '76450': '35980',
        '36860': '36837', '76600': '38340', '76750': '38860', '39140': '39150', '77200': '39300', '77650': '40860',
        '78100': '44140', '78400': '45860', '78500': '47240',
        '11680': '49060', '79600': '49340'}

    unemployment["geographyid"] = unemployment["geographyid"].replace(NECTAID_to_MSAID_conversion)

    top50cbsa = import_esri.get_top50_cbsa()

    unemployment = unemployment[unemployment['geographyid'].isin(list(top50cbsa['StdGeographyID']))]

    unemployment.to_csv('files/unemployment.csv',index=False)

if __name__ == "__main__":
    unemployment()

