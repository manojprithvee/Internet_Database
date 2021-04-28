from selenium import webdriver
import lxml.html as lh
import urllib
import json
driver = webdriver.PhantomJS()
init_url="https://www.lttstore.com/collections/all?page=1"
partial_urls=[]
driver.get("https://www.lttstore.com/collections/all?page=1")
dom=lh.fromstring(driver.page_source)
partial_urls=partial_urls+dom.xpath("//*[@id='shopify-section-collection-template']/section/div[2]/div/div/div/div/div/div/div/a[1]/@href")
driver.get("https://www.lttstore.com/collections/all?page=1")
dom=lh.fromstring(driver.page_source)
partial_urls=partial_urls+dom.xpath("//*[@id='shopify-section-collection-template']/section/div[2]/div/div/div/div/div/div/div/a[1]/@href")


output=[]
for partial_url in partial_urls:
    url = urllib.parse.urljoin(init_url, str(partial_url))
    driver.get(url)
    dom=lh.fromstring(driver.page_source)
    output.append({"name":dom.xpath("/html/body/div[6]/main/div[1]/section/div[1]/div[2]/div/div/div/h1/text()")[0],"price":dom.xpath("/html/body/div[6]/main/div[1]/section/div[1]/div[2]/div/div/div/div[1]/span/span/text()")[0]})

print(json.dumps(output))
    
