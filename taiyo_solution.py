from bs4 import BeautifulSoup
import requests
import pandas as pd
# 1
def worold_bank():
    # World Bank Evaluation and Ratings: https://ieg.worldbankgroup.org/data

    link_request = requests.get('https://ieg.worldbankgroup.org/data')
    website_code = BeautifulSoup(link_request.text,'html.parser')
    table_info = website_code.find('table')
    title = []
    description = []
    for tr in table_info.find_all('tr'):
        title_data = [x.text.strip() for x in tr.find_all('h3')]
        title.append(title_data)
        desc_data = [x.text.strip() for x in tr.find_all('p')]
        description.append(desc_data)

    # data cleaning
    clean_titles = [i for j in title for i in j]
    clean_description = [i for j in description for i in j]
    clean_description_1 = [x for x in clean_description if x !='']

    # dataframes
    '''notes
    when i tried adding both title and description lists, title list was coming as rows
    so i made two data frames and merged into into one final data frame
    '''
    des_df = pd.DataFrame(clean_description_1,columns=['description'])
    title_df = pd.DataFrame(clean_titles,columns=['title'])
    final_df = pd.concat([title_df,des_df],axis=1)
    return final_df

worod_bank_df = worold_bank()

# China Procurement Sources
def chaina_procurement_1():
    link_request = requests.get('http://en.chinabidding.mofcom.gov.cn/')
    website_code = BeautifulSoup(link_request.text,'html.parser')
    ul_info = website_code.find_all('ul',{'class':'txt-02'})
    titles = []
    links = []
    for data in ul_info:
        titles.append([x.text.strip() for x in data.find_all('a')])
        links.append([x['href'] for x in data.find_all('a')])
    # cleaning
    urls_1 = [i for j in links for i in j]
    final_links = []
    for i in urls_1:
        final_links.append(f"http://en.chinabidding.mofcom.gov.cn/{i}")
    clean_titles = [i for j in titles for i in j]

    # dataframes
    '''notes
        1) when i tried adding both url and description lists, url list was coming as rows
        so i made two data frames and merged into into one final data frame
        2) date here were all same so i have added by assiging it
    '''
    url_df = pd.DataFrame(final_links,columns=['ulrs'])
    title_df = pd.DataFrame(clean_titles,columns=['title'])
    final_df = pd.concat([title_df,url_df],axis=1)
    final_df['dates'] = '04-28-2023'
    return final_df

chaina_procurement_df = chaina_procurement_1()

# 3
def scrap_e_tenders():
    link = requests.get('https://etenders.gov.in/eprocure/app').text
    code = BeautifulSoup(link, 'html.parser')

    # print(src_code.prettify())
    table = code.find('table', {'class': "list_table"})
    table_row = table.find('tr', {'class': 'list_header'})
    table_col = [x.text.strip() for x in table_row.find_all('td')]
    td_data = []
    for i in table.find_all('tr', {'class': ['even', 'odd']}):
        td_data.append([x.text.strip() for x in i.find_all('td')])
    df = pd.DataFrame(td_data,columns=table_col)
    return df
e_tenders = scrap_e_tenders()