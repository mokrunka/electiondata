import bs4
import requests
from bs4 import BeautifulSoup as soup
import urllib
import pandas as pd
import matplotlib.pyplot as plt

#we're gonna parse wiki for revenue/employee data
url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue'

#open the connection, grab the page
neweggpage = urllib.request.urlopen(url)
neweggpage_html = neweggpage.read()
neweggpage.close()

#html parsing
page_soup = soup(neweggpage_html, "html.parser")

myTable = page_soup.find('table',{'class':'wikitable sortable'})
companies = []
revenues = []
employees = []

#parse the company name
for row in myTable.findAll('tr'):
    cells = row.findAll('td')
    if len(cells) != 0:
        companies.append(cells[0].text.strip())

#parse the revenue
for row in myTable.findAll('tr'):
    cells = row.findAll('td')
    if len(cells) != 0:
        revenues.append(int(cells[2].text.strip('$').replace(',','')))

#parse the employee count
for row in myTable.findAll('tr'):
    cells = row.findAll('td')
    if len(cells) != 0:
        employees.append(int(cells[4].text.strip().replace(',','')))

#dump the results into a pandas dataframe
df = pd.DataFrame(companies, columns=['Companies'])
df['Revenue']=revenues
df['Employees']=employees
df['Rev/Employee']=df['Revenue'] * 1000000 / df['Employees']

plt.barh(companies, df['Rev/Employee'])
plt.ylabel('Company Name')
plt.xlabel('Revenue per Employee (USD)')
plt.title('Top 50 Companies Revenue per Employee (USD)')

plt.show()