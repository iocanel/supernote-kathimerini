from requests_html import HTMLSession
from pathlib import Path
import logging
import pdfkit
import datetime
from PyPDF2 import PdfMerger

import http.client
http.client.HTTPConnection.debuglevel = 0

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.WARN)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.WARN)
requests_log.propagate = True

def scrap():
  print('Scrapping kathimerini')
  session = HTMLSession()
  url = "https://www.kathimerini.gr/epikairothta"
  r = session.get(url)
  
  print('rendering ...')
  r.html.render()
  #r.html.render(sleep = 1, scrolldown = 5)
  
  print('finding articles ...')
  articles = r.html.find("a.mainlink")
  article_pages = []
  article_urls = []
  for article in articles:
      print(article.attrs['href'])
      article_url = article.attrs['href']
      article_page = session.get(article_url)
      article_page.html.render()
      article_pages.append(article_page)
      article_urls.append(article_url)
  
  print('Saving articles ...')
  # Convert to PDF
  pdfs = []
  
  pdf_options = {
      'page-width': '120mm',  # Adjust the width as needed
      'page-height': '700mm'  # Adjust the height as needed
  }
  for index, url in enumerate(article_urls):
      pdf_filename = f'output{index}.pdf'
      pdfkit.from_url(url, pdf_filename, options=pdf_options)
      pdfs.append(pdf_filename)
  
  # Merge PDFs
  merger = PdfMerger()
  for pdf in pdfs:
      merger.append(pdf)
  
  today = datetime.datetime.now().strftime('%Y-%m-%d')
  file_name = f'news.pdf'
  merger.write(file_name)
  merger.close()
  
  # Delete PDFs
  for pdf in pdfs:
      Path(pdf).unlink()

if __name__ == '__main__':
    scrap()
