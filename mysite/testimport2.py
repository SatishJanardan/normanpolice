import os, time, nltk, re, pprint, PyPDF4, requests

from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

from django.db import models

found = []
hreflead = 'https://www.normanok.gov/sites/default/files/documents/2020-06/2020-06-'
hrefmid = '_daily_'
hreftail = '_summary.pdf'


for filetype in ['arrest']:  #skip  'arrest' files for now
	for daynum in ['02']:
		href = hreflead + daynum + hrefmid + filetype + hreftail
		found.append(href)


incidents=[]
# Process all the pdf file found
for download_url in found:
	r = requests.get(download_url, allow_redirects=True)
	filename = download_url[download_url.rfind("/")+1:]  # Trim URL to get file name
	open(filename, 'wb').write(r.content)  # Copy the file from web site to local disk
	#(prefix, sep, suffix) = filename.rpartition('.')

for download_url in found:
	r = requests.get(download_url, allow_redirects=True)
	filename = download_url[download_url.rfind("/")+1:]  # Trim URL to get file name
	open(filename, 'wb').write(r.content)  # Copy the file from web site to local disk
	#(prefix, sep, suffix) = filename.rpartition('.')

	fp = open(filename, 'rb')
	rsrcmgr = PDFResourceManager()
	laparams = LAParams()
	device = PDFPageAggregator(rsrcmgr, laparams=laparams)
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	pages = PDFPage.get_pages(fp)

	px = 0
	py = 0

	for page in pages:
	    
	    interpreter.process_page(page)
	    layout = device.get_result()
	    for lobj in layout:
	        if isinstance(lobj, LTTextBox):
	            x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
	            px = round(x-px)
	            py = round(y-py)


	            print('At %r is text: %s' % ((x, y, px, py), text))
	            px=round(x)
	            py=round(y)

	fp.close()
	os.remove(filename)