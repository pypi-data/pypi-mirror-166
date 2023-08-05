# BMKG-Latest
This package will guide us to receive the latest Eartquake Information from BMKG Indonesia

## How it works?
This package is getting the latest data of Indonesia Earthquake by scrapping from [BMKG](https://www.bmkg.go.id/) 

BeautifulSoup4 and Requests pacakge are used to produce JSON-form output which is ready to use in web or mobile apps

# How to use?

import gempaterkini

if __name__ == '__main__':
    print('Aplikasi utama')
    result = gempaterkini.ekstraksi_data()
    gempaterkini.tampilkan_data(result)

# Author
Firdaus Wahyu Nugroho