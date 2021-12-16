For now, we attempt to download only district-wise data, which has 104 indicators. NFHS also provides state-wise data too, which contain statistics for a few more indicators.

## Downloading district-wise data

1. District wise data is available at [this link](http://rchiips.org/nfhs/districtfactsheet_NFHS-5.shtml) ([web archive link](http://web.archive.org/web/20211213200517/http://rchiips.org/nfhs/districtfactsheet_NFHS-5.shtml)). 

2. From this webpage, we get the links to each of the statewise pages, which is saved in the `statewise_district_links.csv` file. 

3. Then, the `get_districtwise_links.py` script is used to compile the list of all district wise file URLs into `districtwise_links.csv`. 

4. `download_all_districts.py` is used to download PDFs and save them to `districtwise_data/pdfs`. During this process, it appears that the webpages for one state ([Telangana](http://rchiips.org/nfhs/NFHS-5_TL.shtml)) and one Union Territory ([Chandigarh](http://rchiips.org/nfhs/NFHS-5_CH.shtml)), currently point to a `404` page. So data for these. 

5. It looks like district wise data for `Telangana` is available in the [Telangana State Compendium](http://rchiips.org/nfhs/NFHS-5_FCTS/COMPENDIUM/Telangana.pdf) - we slice this file up, district wise and save the PDFs in the `districtwise_data/telangana` folder. `Chandigarh` has only one district, which covers the entire union territory, so it probably won't have any separate "district-wise" data, as such.

6. There are `704` district-wise PDF files, totalling to approximately `450MB` of data.  

7. With all this done, we use `parse_pdf.py` to parse the PDF and dump district wise data to JSON (in the directory `districtwise_data/json/`. This script uses [Tabula](https://github.com/chezou/tabula-py) and [pdfminer.six](https://github.com/pdfminer/pdfminer.six) for parsing PDFs.