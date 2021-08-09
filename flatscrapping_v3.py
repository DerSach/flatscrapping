import requests
import bs4
import sys
import os
import pandas as pd
from email.mime.text import MIMEText
import pyinputplus as pyip
import datetime
import time
import smtplib
#from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)

''' Scrapping of PAP '''

def get_webpage_html(district_list):
    
    ''' Look at the latest advertisements on pap.fr for the Paris zipcodes provided and get the html of this page '''
    pap_zipcodes = ''
    for district in district_list:
        pap_zipcode = str(37767 + district)
        pap_zipcodes += 'g'+ pap_zipcode
    url = f'https://www.pap.fr/annonce/vente-appartements-{pap_zipcodes}'
    headers = {'Host': 'www.pap.fr',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'}
    
    response = requests.get(url, headers=headers)
    
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    return soup
    
def get_flats_df(soup):
    
    ''' Based on the html content, give a dataframe with the main caracteristics for each flat advertisement of the page '''
    
    encarts = soup.find_all(class_='col-1-3')

    encarts_clean = []
    for encart in encarts:
        if encart.find(class_='item-thumb-link'):
            if encart.find(class_='item-price'):
                if encart.find(class_='item-tags'):
                    if encart.find(class_='item-description'):
                        encarts_clean.append(encart)
    
    
    ''' Store in various lists all the details for all the flat advertisements of the page '''
    prices_list = []
    surfaces_list = []
    pieces_list = []
    rooms_list = []
    images_list = []
    description_list = []
    urls_list = []

    for encart in encarts_clean:
        
        price = int(encart.find(class_='item-price').contents[0].replace(u'\xa0€', '').replace('.',''))
        
        pieces = ''
        rooms = ''
        surface = 0
        for tag in encart.find(class_='item-tags').contents:
            if type(tag) == bs4.element.Tag:
                if 'pièce' in tag.contents[0]:
                    pieces = int(tag.contents[0].replace('pièces','').replace('pièce',''))
                if 'chambre' in tag.contents[0]:
                    rooms = int(tag.contents[0].replace('chambres','').replace('chambre',''))
                if len(tag.contents) > 1:
                    surface = int(tag.contents[0])
                    
        descr = encart.find(class_='item-description').contents[0].replace('\n','').replace('\t','')
        url = 'https://www.pap.fr' + encart.find(class_='item-thumb-link').attrs['href']
        prices_list.append(price)
        surfaces_list.append(surface)
        pieces_list.append(pieces)
        rooms_list.append(rooms)
        description_list.append(descr)
        urls_list.append(url)
        
        image_list = []
        images = encart.find_all(class_='img-liquid')
        for image in images:
            image_list.append(image.contents[1].attrs['src'])
        images_list.append(image_list)
    
    ''' Compute the price per square meter for each flat (also given in another tag of the html page) '''  
    ppm2_list = []
    for price, surface in zip(prices_list,surfaces_list):
        if type(price) == int and type(surface) == int:
            ppm2_list.append(round(price/surface))
        else:
            ppm2_list.append('')
    
    ''' Stores everything inside a single dataframe '''
    flats_df = pd.DataFrame(data = {'url' : urls_list, 
                                'ppm2' : ppm2_list, 
                                'price' : prices_list, 
                                'surface' : surfaces_list,
                                'pieces' : pieces_list, 
                                'rooms' : rooms_list, 
                                'images' : images_list,
                                'description' : description_list})
    
    return flats_df
    
def get_interesting_flat_advertisements(flats_df, max_price, min_surface):
        
    ''' Select most interesting flat advertisements based on max price per m² given '''
    filtered_df = flats_df[(flats_df['price'] <= max_price)&(flats_df['surface'] >= min_surface)].reset_index(drop = True)
    
    ''' Remove flats advertisements already sent '''
    if os.path.isfile('already_sent_flats.csv'):
        sent_flats_df = pd.read_csv('already_sent_flats.csv',index_col=[0])
        for url in sent_flats_df['url']:
            filtered_df = filtered_df[filtered_df['url'] != url]
        filtered_df.reset_index(drop = True, inplace = True)
    
    return filtered_df

def write_html_mail_content(filtered_df, district_list):
    
    ''' For each flat advertisement selected, write the content of the mail that will be sent with their main details and images '''
    
    if len(district_list) == 1:
        if district_list[0] != 1:
            content = f"""
        <p><span style="font-family: Georgia, serif;"><strong>Les annonces int&eacute;ressantes vers le {district_list[0]}&egrave;me arrondissement</strong></span></p>

        """
        else:
            content = f"""
        <p><span style="font-family: Georgia, serif;"><strong>Les annonces int&eacute;ressantes vers le 1er arrondissement</strong></span></p>

        """
    
    else:
        districts = ''
        for district in district_list[:-1]:
            if district != 1:
                districts += f'{district}&egrave;me, '
            else:
                districts += '1er, '
        
        districts += f'et {district_list[-1]}&egrave;me'
        content = f"""
        <p><span style="font-family: Georgia, serif;"><strong>Les annonces int&eacute;ressantes vers les {districts} arrondissements</strong></span></p>

        """
    for i in range(len(filtered_df)):
        details = f"""
    <pre style="line-height: 1;"><span style="font-family: Georgia, serif;">{filtered_df.loc[i,'description']}</span>
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
            <pre style="line-height: 1;"><span style="font-family: Georgia, serif;">Number of pi&egrave;ces: {filtered_df.loc[i,'pieces']}</span></pre>
        </li>
    </ul>
        
    """
        images = ''
        
        for j in filtered_df.loc[i,'images']:

            if j != ' ':
                images += f'''
                <img src="{j}" alt="lcb" width="200" height="140">
            
            '''
        
        content += details + images
        content += '''
        
        <pre style="line-height: 1;"><span style="font-family: Georgia, serif;">---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</span> </pre> 
        
        '''
        
    return content
    
''' Light version of sending mail module '''    
def send_mail(content, filtered_df):
    
    print('Number of advertisements corresponding to your request not already sent: ',len(filtered_df))
    
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
    if os.path.isfile('already_sent_flats.csv'):
        sent_flats_df = pd.read_csv('already_sent_flats.csv',index_col=[0])
        new_sent_flats_df = pd.concat([sent_flats_df, filtered_df], ignore_index=True)
        new_sent_flats_df.to_csv('already_sent_flats.csv')
    else:
        filtered_df.to_csv('already_sent_flats.csv')
    
''' More complex version of sending mail module '''    
# def send_mail(content, filtered_df, server, sender, password, destination):
    
#     ''' Send the content to the desired mail address '''

#     # Create message container - the correct MIME type is multipart/alternative.
#     try:
#         msg = MIMEText(content, 'html')
#         msg['Subject']= "Leboncoin alerts"
#         msg['From']   = sender # some SMTP servers will do this automatically, not all

#         conn = SMTP(server)
#         conn.set_debuglevel(False)
#         conn.login(sender, password)
#         try:
#             conn.sendmail(sender, destination, msg.as_string())

#         finally:
#             conn.quit()
#             print(f'Mail sent at {datetime.datetime.now()}')
#             filtered_df.to_csv('already_sent_flats.csv')

#     except:
#         sys.exit( "mail failed; %s" % "CUSTOM_ERROR" )
    

def main(district_list = None, 
         max_price = None, 
         min_surface = None,
        #  server = None, 
        #  sender = None, 
        #  password = None, 
        #  destination = None
        ):
    if not district_list:
        district_list = []
        district_list.append(pyip.inputInt('Please enter the Paris district number of the area where you want to look for flat advertisements (between 1 and 20): ', min = 1, max = 20))
        other_district = pyip.inputYesNo('Would you like to add another district? ')
        while other_district == 'yes':
            district_list.append(pyip.inputInt('Please enter the Paris district number of the area where you want to look for flat advertisements (between 1 and 20): ', min = 1, max = 20))
            other_district = pyip.inputYesNo('Would you like to add another district? ')
    
    ''' Remove if duplicates '''
    district_list = list(set(district_list))
    
    soup = get_webpage_html(district_list)
    flats_df = get_flats_df(soup)
    if not max_price:
        max_price = pyip.inputNum('What is the maximum price of the flat advertisements you would like to select? ')
    if not min_surface:
        min_surface = pyip.inputNum('What is the minimum m² surface of the flat advertisements you would like to select? ')
    filtered_df = get_interesting_flat_advertisements(flats_df, max_price, min_surface)
    
    ''' If filtered_df is not empty, send the mail, else keep calling the main function till new advertisements appear '''
    if len(filtered_df) > 0:
        content = write_html_mail_content(filtered_df, district_list)
        # if not server:
        #     server = pyip.inputStr('Please enter your SMTP server: ')
        # if not sender:
        #     sender = pyip.inputEmail('Please the email from which you would like the email to be sent: ')
        # if not password:
        #     password = pyip.inputStr('Please the password of that email address: ')
        # if not destination:
        #     destination = pyip.inputEmail('Please the email to which you would like the email to be sent: ')
        
        send_mail(content, 
                filtered_df, 
                #   server, 
                #   sender, 
                #   password, 
                #   destination
                )
    else:
        print('No advertisement corresponding to your request not already sent for the time being...')
        
    time.sleep(30)
    main(district_list, 
         max_price,
         min_surface, 
        #  server, 
        #  sender, 
        #  password, 
        #  destination
         )
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python flatscrapping_v3.py destimation_mail_address@domain.com")
        sys.exit(1)
    else:
        try:
            while True:
                main()
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit(0)