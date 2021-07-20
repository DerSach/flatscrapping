import requests
from bs4 import BeautifulSoup
import sys
import os
import pandas as pd
import json
import smtplib
from email.mime.text import MIMEText
import pyinputplus as pyip
import datetime
import time

# def filter_flat_advertisements(zipcode):
#   ''' ''' TO DO: write a function enabling to custom the flat advertisements search (min sq/m2, max price, etc.)

def get_webpage_html(zipcode):
    
    ''' Look at the latest advertisements on leboncoin.fr for this zipcode provided and get the html of this page, bypassing the captcha anti-scrapping system '''
    
    url = f'https://www.leboncoin.fr/recherche?category=9&text=appartement&locations={zipcode}'
    headers = {'Host': 'www.leboncoin.fr',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
'Accept-Encoding': 'gzip, deflate, br',
'Connection': 'keep-alive',
'Cookie': 'datadome=ZfeIUNkwyM6S0uo50OMzusY6yp3MmcRg~vv9pvpC43CjYB.cg1~ik9LVP65jlUrFqou5N3jTsf~YUzrHjCKv9Mlq1fapD3ML.bTmhYcovG; __Secure-InstanceId=601c660a-8bf0-40a7-bb44-9628e01290fe; didomi_token=eyJ1c2VyX2lkIjoiMTczMjU3ZmQtN2ZjOS02MDI5LTlhYTItZWU5MDAxNDkxMmZiIiwiY3JlYXRlZCI6IjIwMjEtMDctMTRUMTU6NDM6NTUuMzYxWiIsInVwZGF0ZWQiOiIyMDIxLTA3LTE0VDE1OjQzOjU1LjM2MVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiYW1hem9uIiwic2FsZXNmb3JjZSIsImdvb2dsZSIsImM6bmV4dC1wZXJmb3JtYW5jZSIsImM6Y29sbGVjdGl2ZS1oaFNZdFJWbiIsImM6cm9ja3lvdSIsImM6cHVib2NlYW4tYjZCSk10c2UiLCJjOnJ0YXJnZXQtR2VmTVZ5aUMiLCJjOnNjaGlic3RlZC1NUVBYYXF5aCIsImM6Z3JlZW5ob3VzZS1RS2JHQmtzNCIsImM6cmVhbHplaXRnLWI2S0NreHlWIiwiYzp2aWRlby1tZWRpYS1ncm91cCIsImM6c3dpdGNoLWNvbmNlcHRzIiwiYzpsdWNpZGhvbGQteWZ0YldUZjciLCJjOmxlbW9tZWRpYS16YllocDJRYyIsImM6eW9ybWVkaWFzLXFuQldoUXlTIiwiYzpzYW5vbWEiLCJjOnJhZHZlcnRpcy1TSnBhMjVIOCIsImM6cXdlcnRpemUtemRuZ0UyaHgiLCJjOnZkb3BpYSIsImM6cmV2bGlmdGVyLWNScE1ucDV4IiwiYzpyZXNlYXJjaC1ub3ciLCJjOndoZW5ldmVybS04Vllod2IyUCIsImM6YWRtb3Rpb24iLCJjOndvb2JpIiwiYzpzaG9wc3R5bGUtZldKSzJMaVAiLCJjOnRoaXJkcHJlc2UtU3NLd21IVksiLCJjOmIyYm1lZGlhLXBRVEZneVdrIiwiYzpwdXJjaCIsImM6bGlmZXN0cmVldC1tZWRpYSIsImM6c3luYy1uNzRYUXByZyIsImM6aW50b3dvd2luLXFhenQ1dEdpIiwiYzpkaWRvbWkiLCJjOnJhZGl1bW9uZSIsImM6YWRvdG1vYiIsImM6YWItdGFzdHkiLCJjOmdyYXBlc2hvdCIsImM6YWRtb2IiLCJjOmFkYWdpbyIsImM6bGJjZnJhbmNlIl19LCJwdXJwb3NlcyI6eyJlbmFibGVkIjpbInBlcnNvbm5hbGlzYXRpb25jb250ZW51IiwicGVyc29ubmFsaXNhdGlvbm1hcmtldGluZyIsInByaXgiLCJtZXN1cmVhdWRpZW5jZSIsImV4cGVyaWVuY2V1dGlsaXNhdGV1ciJdfSwidmVuZG9yc19saSI6eyJlbmFibGVkIjpbImdvb2dsZSJdfSwidmVyc2lvbiI6MiwiYWMiOiJERTJBd0FFSUFmb0JoUUR4QUhtQVNTQWtzQ0pJSEVBT3JBaURCRktDS2dFbTRKdkFUa0F0ckJiZUM0d0Z5UUxsZ1lEQXdpQmlhQUFBLkRFMkF3QUVJQWZvQmhRRHhBSG1BU1NBa3NDSklIRUFPckFpREJGS0NLZ0VtNEp2QVRrQXRyQmJlQzR3RnlRTGxnWURBd2lCaWFBQUEifQ==; utag_main=v_id:017aa5aeb9ea009768587420a54800052001900f0093c$_sn:14$_ss:1$_st:1626766707531$_pn:1%3Bexp-session$ses_id:1626764904035%3Bexp-session; atauthority=%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22default%22%2C%22visitor_mode%22%3A%22optin%22%7D%2C%22options%22%3A%7B%22end%22%3A%222022-08-19T07%3A08%3A27.490Z%22%2C%22path%22%3A%22%2F%22%7D%7D; ry_ry-l3b0nco_realytics=eyJpZCI6InJ5XzM2QjVBNkE1LTEyOUYtNDQ1Qi05MkJELTVCREMzQkM5ODNGRiIsImNpZCI6bnVsbCwiZXhwIjoxNjU3ODEzMzM0MDU3LCJjcyI6bnVsbH0%3D; euconsent-v2=CPJVj5SPJVj5SAHABBENBiCgAP_AAHLAAAAAG7tf_X_fb2vj-_59d_t0eY1P9_63v6wzjheNs-8NyZ_X_L4Xo2M6vB36pq4KmR4Eu3LBAQdlHOHcTQmQ4IkVqTPsbk2Mr7NKJ7LEmlMbO2dYGH9_n8XTuZKY70_8___z_3-v_v__7rbgCAAAAAAAIAgc6ASYal8AA2JY4Ek0aVQogRhWEhUAoAKKAYWiawgJHBTsrgI9QQoAEJqAjAiBBiCjFgEAAgEASERACAHggEQBEAgABACpAQgAIkAQWAFgYBAAKAaFABFAEIEhBEYFRymBARItFBPIGAAQAAAAAAAAAAAAAAAgBigYwABwAEgANAAeABSADAAMgAigBSAFQALAAYgA1gB8AH8AQgBDACYAFoALkAXgBfgDCAMQAZgA2gB4AD1AH8AggBCwCNAI4ASYAlQBMwCfAKAAUgAqABWgCygFuAXEAygDLgGaAZ0A0wDVAGwANoAcEA4gDkAHMAOyAd4B4QDzAPSAfIB9AD8AH_AQUBBoCEgIUARAAjABHICSgJMASuAloCXAE3gJ4AnwBQQCigFIAKWAVEAq8BXQFfALNAWgBaQC5wF2AXcAvIBfAC_AGBAMIAYqAzgDOgGgANOAa0A2gBvADhQHNAc4A6oB2QDtgHfAPEAesA9sB-gH7AP-AgQBA4CDAEJAIXAQ-AiUBFgCOIEdAR2Aj0BIICQwEigJRASpAl4CX4EwgTEAmaBNgE2gJ3AT-AoUBRACigFGQKOApABTMCmwKcAU-AqIBUkCrQKvAVmAraBYgFiwLHAsmBZYFmALOAWiAtWBa4FsALcAXBAuMC5IFzAXQAuuBdoF3QLzAvWBe4F9gMCAYVAw0DD4GKAYqAxqBjwGQAMiAZKAyuBmAGYgM0gZwBnMDPAM-gaCBoQDRQGnwNaA1uBroGvANgAbIA2oBtoDcAG5QN0A3WBvoG_QOEA4aBxIHFAOOAckA5SBzAHMgOeAdPA60DsAHcAO7Ad7A8IDwwHoQPTA9SB6wHsAPcAe8A-AB8QD5wH0gPsgfeB-ED8gP0AfxA_wD_YH_ggDBAMEBgIEDAYIABwAEgAPAApABgAGQARQApACoAFgAMQAagA_gCEAIYATAAvQBhAGIAMwAbYA_gEFAI0AjwBJgCVAEzAJ8AoABSACoAFaALKAW4BcADHgGUAZYAzoBpgGqANoAcEA4gDkAHMAOyAd4B4QDzAPSAfQB-AD_gISAhQBEACJAEYAI4ASUAlYBLQCbwE8AT4AoIBRQCkAFLAKiAVcArcBXQFfALEAWYAucBdgF3ALyAXwAvwBhADFQGcAZ0A0EBpgGnANaAbQA3gBwoDmgOcAdUA7IB2wDvgHiAPWAe0A-QB-wECAIHAQkAhcBD4CJQEWAI4gR0BHYCPQEggJDASKAk4BKICVIEvAS_AmECYgEzQJsAm0BOICdwE_gKFAUQAooBRkCjgKQAUzApsCnIFPAU-AqIBUkCrQKvAVmArYBYkCxwLJgWWBZgCzgFogLVgWuBbEC2wLcAXAAuOBcwF0ALrgXaBd0C8gL0gXuBfAC-wGBAMKAYaAw-BigGKgMaAY8AyABkQDJQGVgMxAZpAzgDOYGeAZ9A0EDQgGigNPga0BrYDXQGwANkgbUBtgDcIG6AbrA30DfoHCAcMA4kBxwDkgHKQOYA5kBzwDp4HWgdgA7gB3YDvYHhAeGA9CB6YHqQPWA9gB7gD3gHwAPiAfOA-kB9kD7wPwgfmB-gD-IH-Af7A_8EAYICAgMBAggDsAADAAcACQAFgANAAeABQAC0AGQAaAA6ACIAEgAKgAWAAuABiAD-AIIAhwBMAE0AKYAVQArgBcgC8AL8AYQBiADMAGgANoAbwA7gB6gD-AQIAi4BGgEeAJEASYAlYBPgFAAKQAVAAqgBWwCxALKAW4BcgC-AGEAMSAZQBlwDNAM6AaYBqgDYAG1AN8A4ABxADkgHMAc4A7IB3gHhAPMA9AB7QD5APwAf4BBYCEgIUARAAikBGAEZAI4ASUAlIBK4CbgJwATwAnwBQQChgFFgKQApIBSwCngFRAKuAVkArcBXQFfALEAWaAtAC0gFzgLsAu4BeQC-AF-AMAAYQAxQBmYDOAM6AaCA0wDTgGrANaAbQA3gBwgDmwHUAdUA64B2QDtgHfAPEAeiA9QD1gHtgPyA_gCAAECAIHAQnAhcCGAEPgIhgRKBEwCLIEcAR3Aj0CPoEggSKAk4BKICVAErgJagS8BL8CYQJiATMAmmBNgE2gJxATuAn-BQgFCgKIgUYBSECkgKTgUyBTkCngKfAVEAqSBVoFXgKzAVtAr4Cv4FiAWLAscCyYFlgWYAs4BaIC0wFqwLXAtwBbwC4IFxgXJAucC6IF1gXcAvIBekC9gL9gYCBgYDCoGGAYeAxKBigGKgMaAY8AyABkQDJQGTgMrAZaAzEBmkDNwM_gaCBoUDRANFAaPA0kDSwGngNTgaqBq0DWgNbAa7A18DYQGyQNqA2wBtwDcIG6AbrA3kDeoG-gb9A4ADgYHCAcMA4kBxgDjgHJQOYA5mBzwHPgOjgdKB08DqQOqgdYB2ADtQHcAO7gd6B3wDwYHhgeIA8eB5IHlQPOA9GB6YHqQPWA9iB7gHvQPgA-KB84H0gPsAfgA_QB-wD-IH-Af7A_8EAYICAgMBAg.f_gADlgAAAAA; include_in_experiment=true; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22an%22%3A%22NaN%22%2C%22ac%22%3A%22%22%2C%22vrn%22%3A%22-562498-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A34128000%2C%22end%22%3A34128000%7D%7D; _gcl_au=1.1.1693989734.1626277511; cto_bundle=QWEIH19nU1Y0blFMZ2JNbzAlMkZvaGpPV1RPdE1XS0dmblEzT1ElMkI1bmM2Wk5KbUhKSnJJQVROU0F3NU1vYmtVSHZ6JTJCT1Nyb3hDJTJCMlBvYnl3c0poRGJsd2IlMkJoVlIxN1dPbkZBOTIwcHVqNWNyNUhvUmJZR1QybVg5U08wQnlrTUdaQ0xwWFglMkZ3bG9pYTc3MTlZMjhncjBWUDNka2NQUkFPajhjRnkwbkNLT2tXVzdxOUElMkYybExWZVdzWXR3RGJ6cG5SMTExN2hPVWhSR3Q2WURNMDlNd0dNV0FXSldDc3NFVk1RRVI4Nlp0RVFDVGFmbEElM0Q; _fbp=fb.1.1626278369445.5513548; __gads=ID=237e5e3b3f366732:T=1626699368:S=ALNI_MaM-Ry3izvaOF6F3lbaUtFSN6i9jw; adview_clickmeter=search__listing__4__517fd8f1-e55c-11eb-bbe7-52ad51233314; atreman=%7B%22name%22%3A%22atreman%22%2C%22val%22%3A%7B%22camp%22%3A%22ES-3999-%5BMYSRCH%5D--%5Bsee_results_top%5D%22%2C%22date%22%3A451763.7025361111%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A2592000%2C%22end%22%3A2592000%7D%7D; ry_ry-l3b0nco_so_realytics=eyJpZCI6InJ5XzM2QjVBNkE1LTEyOUYtNDQ1Qi05MkJELTVCREMzQkM5ODNGRiIsImNpZCI6bnVsbCwib3JpZ2luIjp0cnVlLCJyZWYiOm51bGwsImNvbnQiOm51bGwsIm5zIjpmYWxzZX0%3D',
'Upgrade-Insecure-Requests': '1',
'TE': 'Trailers'}
    
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
def get_flats_df(soup):
    
    ''' Based on the html content, give a dataframe with the main caracteristics for each flat advertisement of the page '''

    ''' Parse the last 'string' tag of the html where all the data is present '''
    last_script_tag = soup.find_all('script')[-1]
    print(last_script_tag)
    
    ''' Access the metadata inside of this last 'string' tag. metadata_list is a list where each element contains all the details for a given flat advertisement '''
    metadata_list = json.loads(last_script_tag.contents[0])['props']['pageProps']['searchData']['ads']
    
    ''' Store in various lists all the details for all the flat advertisements of the page '''
    publication_date_list = []
    subjects_list = []
    urls_list = []
    prices_list = []
    images_list = []
    surfaces_list = []
    rooms_list = []
    locations_list = []

    for metadata in metadata_list:
        publication_date_list.append(metadata['first_publication_date'])
        subjects_list.append(metadata['subject'])
        urls_list.append(metadata['url'])
        prices_list.append(int(metadata['price'][0]))
        image_list = []
        for image in metadata['images']['urls']:
            image_list.append(image)
        images_list.append(image_list)
        for dic in metadata['attributes']:
            if dic['key'] == 'square':
                surfaces_list.append(int(dic['value']))
            if dic['key'] == 'rooms':
                rooms_list.append(int(dic['value']))
        locations_list.append([metadata['location']['lat'],metadata['location']['lng']])
     
    ''' Compute the price per square meter for each flat (also given in another tag of the html page) '''    
    ppm2_list = []
    for price, surface in zip(prices_list, surfaces_list):
        ppm2 = round(price / surface, 0)
        ppm2_list.append(ppm2)
    
    ''' Storeseverything inside a single dataframe '''
    flats_df = pd.DataFrame(data = {'url' : urls_list, 
                               'subject' : subjects_list, 
                               'ppm2' : ppm2_list, 
                               'price' : prices_list, 
                               'surface' : surfaces_list, 
                               'rooms' : rooms_list, 
                               'location' : locations_list,
                                'publication_date' : publication_date_list,
                               'images' : images_list})
    
    return flats_df
    
def get_interesting_flat_advertisements(flats_df, max_ppm2):
    
    ''' Select most interesting flat advertisements based on max price per m² given '''
    filtered_df = flats_df[flats_df['ppm2'] <= max_ppm2].reset_index(drop = True)
    
    ''' Remove flats advertisements already sent '''
    if os.path.isfile('already_sent_flats.csv'):
        sent_flats_df = pd.read_csv('already_sent_flats.csv',index_col=[0])
        for url in sent_flats_df['url']:
            filtered_df = filtered_df[filtered_df['url'] != url]
        filtered_df.reset_index(drop = True, inplace = True)
            
    return filtered_df

def write_html_mail_content(filtered_df):
    
    ''' For each flat advertisement selected, write the content of the mail that will be sent with their main details and images '''
    
    content = """
<p><span style="font-family: Georgia, serif;"><strong>Les annonces int&eacute;ressantes du XVII&egrave;me</strong></span></p>

"""

    for i in range(len(filtered_df)):
        details = f"""
    <pre style="line-height: 1;"><span style="font-family: Georgia, serif;">{filtered_df.loc[i,'subject']}</span>
    <span style="font-family: Georgia, serif;">
    <a href="{filtered_df.loc[i,'url']}\n\n" target="_blank">{filtered_df.loc[i,'url']}</a>
    </span></pre>
    <ul>
        <li>
            <pre style="line-height: 1;"><span style="font-family: Georgia, serif;">&euro;/m&sup2;: {filtered_df.loc[i,'ppm2']:,.0f}</span></pre>
        </li>
        <li>
            <pre style="line-height: 1;"><span style="font-family: Georgia, serif;">Price (&euro;): {filtered_df.loc[i,'price']:,}</span></pre>
        </li>
        <li>
            <pre style="line-height: 1;"><span style="font-family: Georgia, serif;">Surface (m&sup2;): {filtered_df.loc[i,'surface']}</span></pre>
        </li>
        <li>
            <pre style="line-height: 1;"><span style="font-family: Georgia, serif;">Number of rooms: {filtered_df.loc[i,'rooms']}</span></pre>
        </li>
        <li>
            <pre style="line-height: 1;"><span style="font-family: Georgia, serif;">Publication date: {filtered_df.loc[i,'publication_date']}</span>

    </pre>
        </li>

    </ul>
    """
        images = ''
        
        for j in filtered_df.loc[i,'images']:

            images += f'''
            <img src="{j}" alt="lcb" width="200" height="140">
            
            '''
        
        content += details + images
        
        return content
    
def send_mail(content, filtered_df):
    
    ''' Send the content to the desired mail address '''
    
    SMTPserver = 'smtp.bbox.fr'
    sender = 'leboncoin@alerts.fr'
    destination = sys.argv[1]


    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEText(content, 'html')
    msg['Subject'] = "Alerte leboncoin"
    msg['From'] = sender
    msg['To'] = destination

    # Send the message via local SMTP server.
    s = smtplib.SMTP(SMTPserver)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(sender, destination, msg.as_string())
    s.quit()
    
    print(f'Mail sent at {datetime.datetime.now()}')
    filtered_df.to_csv('already_sent_flats.csv')

def main(zipcode = None, max_ppm2 = None):
    if not zipcode:
        zipcode = pyip.inputNum('Please enter the zipcode of the area where you want to look for flat advertisements: ')
    soup = get_webpage_html(zipcode)
    flats_df = get_flats_df(soup)
    if not max_ppm2:
        max_ppm2 = pyip.inputNum('What is the maximum price per m² of the flat advertisements you would like to select? ')
    filtered_df = get_interesting_flat_advertisements(flats_df, max_ppm2)
    content = write_html_mail_content(filtered_df)
    send_mail(content, filtered_df)
    time.sleep(10)
    main(zipcode, max_ppm2)
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python flatscrapping_v1.py destination_email_address@domain.com")
        sys.exit(1)
    else:
        try:
            while True:
                main()
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit(0)