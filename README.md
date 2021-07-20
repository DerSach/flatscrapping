# flatscrapping
Get latest flat advertisements on leboncoin website by mail based on specified conditions

## **Prerequisite**

`pip install pandas`

`pip install requests`

`pip install pyinputplus`

`pip install bs4`

## **Usage**

Execute from terminal this way:

`python flatscrapping_v1.py destination_email_address@domain.com`

You will have the possibility to enter a French zipcode when asked (e.g. '75017' for Paris 17th district)
The program will then get the latest metadata from leboncoin website parsing its html.

UPDATE NOTE: easier to execute from a jupyter notebook as CAPTCHA protection can't be bypassed from terminal

Here the 'Cookies' key in the 'headers' dictionnary needs to be updated to bypass the CAPTCHA (to do so, see: https://medium.com/@rifaislamet1509/bypass-recaptcha-to-scraping-australian-yellowpages-using-python-9330101e99a3)

Then you will be asked a maximum price per m². The program selects the corresponding flat advertisements, compares them to a csv storing all the flat advertisements already sent, and sends only the flat advertisements not already sent.

In the end, you should receive an email (as below) on the specified email address with the main characteristics of each flat advertisement corresponding to your request and that have not been already sent.
