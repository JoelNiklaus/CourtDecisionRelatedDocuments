import requests
from bs4 import BeautifulSoup
import tika
tika.initVM()
from tika import parser
import json
import re

ROOT = 'https://www.bger.ch'
URL = 'https://www.bger.ch/index/press/press-inherit-template/press-mitteilungen.htm?histo=true'
response = requests.get(URL)
content = BeautifulSoup(response.text, 'lxml')
urls = content.find_all('a')

# JSON data
data = []

# filter for 'href' attribute and '.pdf' in html and scrape pdf files
i = 0
for url in urls:
    try:
        if '.pdf' in url['href']:
            pdf_url = ROOT + url['href']
            pdf_res = requests.get(pdf_url)
            filename = pdf_url.split('/')[-1]
            
            # save pdf files
            with open('./pdf/' + filename, 'wb') as f:
                f.write(pdf_res.content)
            
            # parse metadata and content from pdf files
            parsed = parser.from_file('./pdf/' + filename)
            pdf_metadata = parsed["metadata"]
            pdf_content = parsed["content"]

            # extract data to json format and add to data array
            pdf_subject = ""
            if pdf_subject:
                pdf_subject = pdf_metadata["subject"]

            pdf_references = list(dict.fromkeys(re.findall(r'[\d+]+[\w]+[\d{0,9}]+[\W+]+[\d+]+[\d+]+[\d+]+[\d+]', pdf_content)))
            data.append({
                "id" : i, 
                "subject" : pdf_subject, 
                "date" : pdf_metadata["Creation-Date"], 
                "url" : pdf_url, 
                "references" : pdf_references, 
                "content" : pdf_content})
            print(filename + ' scraped successfully')

            i += 1

    except Exception as e:
        print('Error', e)

# create json file
with open('./data/bger.json', 'w') as f:
    f.write(json.dumps(data))

    



        