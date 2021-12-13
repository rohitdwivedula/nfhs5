from bs4 import BeautifulSoup
import pandas as pd
import requests

state_links = pd.read_csv("statewise_links.csv")
districtwise_links = pd.DataFrame(columns=['state', 'district', 'link'])

for index, row in state_links.iterrows():
    print(f"Processing state #{index} {row['state']} at link {row['link']}")
    webpage = requests.get(url = row['link']).text
    soup = BeautifulSoup(webpage, 'html.parser')
    try:
        s = soup.find_all('select')[0].find_all('option')
        for i in range(0, len(s)):
            link_to_report = s[i].get('value')
            district_name = s[i].text
            if link_to_report is not None:
                districtwise_links = districtwise_links.append(
                    {
                        'state': row['state'],
                        'district': district_name,
                        'link': link_to_report
                    },
                    ignore_index=True
                )
    except:
        print("[ERROR] Could not process:", row)

districtwise_links.to_csv('districtwise_links.csv')

'''
	Output for this program:

		Processing state #0 Andhra Pradesh at link http://rchiips.org/nfhs/NFHS-5_AP.shtml
		Processing state #1 Arunachal Pradesh at link http://rchiips.org/nfhs/NFHS-5_AR.shtml
		Processing state #2 Assam at link http://rchiips.org/nfhs/NFHS-5_AS.shtml
		Processing state #3 Bihar at link http://rchiips.org/nfhs/NFHS-5_BR.shtml
		Processing state #4 Chhattisgarh at link http://rchiips.org/nfhs/NFHS-5_CT.shtml
		Processing state #5 Goa at link http://rchiips.org/nfhs/NFHS-5_GA.shtml
		Processing state #6 Gujarat at link http://rchiips.org/nfhs/NFHS-5_GJ.shtml
		Processing state #7 Haryana at link http://rchiips.org/nfhs/NFHS-5_HR.shtml
		Processing state #8 Himachal Pradesh at link http://rchiips.org/nfhs/NFHS-5_HP.shtml
		Processing state #9 Jharkhand at link http://rchiips.org/nfhs/NFHS-5_JH.shtml
		Processing state #10 Karnataka at link http://rchiips.org/nfhs/NFHS-5_KA.shtml
		Processing state #11 Kerala at link http://rchiips.org/nfhs/NFHS-5_KL.shtml
		Processing state #12 Madhya Pradesh at link http://rchiips.org/nfhs/NFHS-5_MP.shtml
		Processing state #13 Maharashtra at link http://rchiips.org/nfhs/NFHS-5_MH.shtml
		Processing state #14 Manipur at link http://rchiips.org/nfhs/NFHS-5_MN.shtml
		Processing state #15 Meghalaya at link http://rchiips.org/nfhs/NFHS-5_ML.shtml
		Processing state #16 Mizoram at link http://rchiips.org/nfhs/NFHS-5_MZ.shtml
		Processing state #17 Nagaland at link http://rchiips.org/nfhs/NFHS-5_NL.shtml
		Processing state #18 Odisha at link http://rchiips.org/nfhs/NFHS-5_OR.shtml
		Processing state #19 Punjab at link http://rchiips.org/nfhs/NFHS-5_PB.shtml
		Processing state #20 Rajasthan at link http://rchiips.org/nfhs/NFHS-5_RJ.shtml
		Processing state #21 Sikkim at link http://rchiips.org/nfhs/NFHS-5_SK.shtml
		Processing state #22 Tamil Nadu at link http://rchiips.org/nfhs/NFHS-5_TN.shtml
		Processing state #23 Telangana at link http://rchiips.org/nfhs/NFHS-5_TL.shtml
		[ERROR] Could not process: state                                  Telangana
		link     http://rchiips.org/nfhs/NFHS-5_TL.shtml
		Name: 23, dtype: object
		Processing state #24 Tripura at link http://rchiips.org/nfhs/NFHS-5_TR.shtml
		Processing state #25 Uttar Pradesh at link http://rchiips.org/nfhs/NFHS-5_UP.shtml
		Processing state #26 Uttarakhand at link http://rchiips.org/nfhs/NFHS-5_UT.shtml
		Processing state #27 West Bengal at link http://rchiips.org/nfhs/NFHS-5_WB.shtml
		Processing state #28 Andaman & Nicobar Island (UT) at link http://rchiips.org/nfhs/NFHS-5_AN.shtml
		Processing state #29 Chandigarh (UT) at link http://rchiips.org/nfhs/NFHS-5_CH.shtml
		[ERROR] Could not process: state                            Chandigarh (UT)
		link     http://rchiips.org/nfhs/NFHS-5_CH.shtml
		Name: 29, dtype: object
		Processing state #30 Dadra Nagar Haveli & Daman & Diu (UT) at link http://rchiips.org/nfhs/NFHS-5_DD.shtml
		Processing state #31 NCT of Delhi (UT) at link http://rchiips.org/nfhs/NFHS-5_DL.shtml
		Processing state #32 Jammu & Kashmir (UT) at link http://rchiips.org/nfhs/NFHS-5_JK.shtml
		Processing state #33 Ladakh (UT) at link http://rchiips.org/nfhs/NFHS-5_LH.shtml
		Processing state #34 Puducherry (UT) at link http://rchiips.org/nfhs/NFHS-5_PY.shtml
'''