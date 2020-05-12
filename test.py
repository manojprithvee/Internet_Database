import urllib.parse

import lxml
import lxml.html as lh
from selenium import webdriver


def download(urls, xpaths):
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(executable_path="/Users/divakarmanoj/dev/Final Project/Python/geckodriver",
                               firefox_options=options)
    final = []
    for url in urls:
        driver.get(url)
        dom = lh.fromstring(driver.page_source)
        outputs = []
        for xpath in xpaths:
            raw_xpaths = dom.xpath(xpath)
            temp = []
            for raw_xpath in raw_xpaths:
                if type(raw_xpath) == lxml.etree._ElementUnicodeResult:
                    if xpath.split("@")[-1] == xpath:
                        temp.append({'text': str(raw_xpath)})
                    else:
                        if xpath.split("@")[-1] == "href":
                            temp.append({xpath.split("@")[-1]: urllib.parse.urljoin(url, str(raw_xpath))})
                        else:
                            temp.append({xpath.split("@")[-1]: str(raw_xpath)})
                else:
                    output = {'text': str(raw_xpath.text)}
                    for i in raw_xpath.attrib.keys():
                        output[i] = raw_xpath.attrib.get(i)
                    temp.append(output)
            outputs.append(temp)
        final.append(outputs)
    driver.close()
    return final


abc = download(["https:google.com"], ["/html/body/div[1]/div[3]/form/div[2]/div[1]/div[3]/center/input[2]"])
print(abc)
