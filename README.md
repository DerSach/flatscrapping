# flatscrapping
Sometimes real estate websites offering alerts are not quick enough and you might be aware of a flat advertisement only few minutes or few hours after it has been published. This delay can sometimes be big enough for you not to be able to bid or even visit the flat as too many people already contacted the landlord or real estate agency.

**The main purpose of this program is thus to know immediatly when a flat advertisement corresponding to your criteria is published by letting the program run in your terminal window. As soon as a new flat advertisement corresponding to your search is published on PAP.fr website, you will get an email alert on the specified email address with the main details of the advertisement.**

This is a recursive function, hence infinite unless you volontarily interrupt it (by closing the terminal window for instance). When closed, you will not be able to get emails anymore. You will have to restart to program and let it run again.

## **Prerequisite**

In your terminal enter the following:

`pip install pandas`

`pip install requests`

`pip install pyinputplus`

`pip install bs4`

## **Usage**

Execute from terminal this way:

`python flatscrapping_v3.py destination_email_address@domain.com`

You will have the possibility to enter Paris district numbers when asked (e.g. '1' for Paris 1st district, '17' for Paris 17th district, etc.)
The program will then get the latest metadata from PAP website parsing its html.

Then you will be asked a maximum price and a minimum m² surface for the flat advertisements you want to select. The program compares the corresponding flat advertisements to a csv storing all the flat advertisements already sent, and sends only the flat advertisements not already sent.

In the end, you should receive an email (as below) on the specified email address with the main characteristics of each flat advertisement corresponding to your request and that have not already been sent.

![Capture d’écran 2021-07-20 à 16 30 51](https://user-images.githubusercontent.com/78410163/126343066-c1a1bd10-39a6-4d45-9fc9-36b4f52d58eb.png)

Hope it helps ! :)

DerSach
