import json
import time

import lxml
import lxml.html as lh
import requests
from moz_sql_parser import parse
from pyspark import SparkContext

sc = SparkContext()
lists = ['https://www.lttstore.com/products/ltt-stealth-hoodie',
         'https://www.lttstore.com/products/cpu-deconstructed-t-shirt',
         'https://www.lttstore.com/products/hard-drive-shirt', 'https://www.lttstore.com/products/gpu-t-shirt',
         'https://www.lttstore.com/products/usb-c-t-shirt', 'https://www.lttstore.com/products/ram-t-shirt',
         'https://www.lttstore.com/products/constellations', 'https://www.lttstore.com/products/fan-t-shirt',
         'https://www.lttstore.com/products/mystery-t-shirt', 'https://www.lttstore.com/products/ltt-hat',
         'https://www.lttstore.com/products/underwear-3-pack', 'https://www.lttstore.com/products/techlinked-tee',
         'https://www.lttstore.com/products/techlinked-hat']

listing = sc.parallelize(lists)


# print(sc.getConf().getAll())

def download(url, xpaths):
    request = requests.get(url)
    dom = lh.fromstring(request.text)
    outputs = []
    for xpath in xpaths:
        raw_xpath = dom.xpath(xpath)
        if type(raw_xpath[0]) == lxml.etree._ElementUnicodeResult:
            if xpath.split("@")[-1] == xpath:
                outputs.append({'text': str(raw_xpath[0])})
            else:
                outputs.append({xpath.split("@")[-1]: str(raw_xpath[0])})
        else:
            output = {'text': str(raw_xpath[0].text)}
            for i in raw_xpath[0].attrib.keys():
                output[i] = raw_xpath[0].attrib.get(i)
            outputs.append(output)
    return outputs


x_path = ["/html/body/div[6]/main/div[1]/section/div[1]/div[2]/div/div/div/div[1]/span/span",
          "/html/body/div[6]/main/div[1]/section/div[1]/div[2]/div/div/div/h1/text()"]
sql = parse('select "/html/body/div[6]/main/div[1]/section/div[1]/div[2]/div/div/div/div[1]/span/span",'
            '"/html/body/div[6]/main/div[1]/section/div[1]/div[2]/div/div/div/h1/text()" from html where url in ('
            '"https://www.lttstore.com/products/ltt-stealth-hoodie", '
            '"https://www.lttstore.com/products/cpu-deconstructed-t-shirt", '
            '"https://www.lttstore.com/products/hard-drive-shirt", "https://www.lttstore.com/products/gpu-t-shirt", '
            '"https://www.lttstore.com/products/usb-c-t-shirt", "https://www.lttstore.com/products/ram-t-shirt", '
            '"https://www.lttstore.com/products/constellations", "https://www.lttstore.com/products/fan-t-shirt", '
            '"https://www.lttstore.com/products/mystery-t-shirt", "https://www.lttstore.com/products/ltt-hat", '
            '"https://www.lttstore.com/products/underwear-3-pack", '
            '"https://www.lttstore.com/products/techlinked-tee", "https://www.lttstore.com/products/techlinked-hat") '
            'and selector=xpath')
start_time = time.time()
dirdd = listing.distinct()
arr = dirdd.map(lambda x: download(x, x_path)).collect()
print(json.dumps(arr))
print("--- Spark: %s seconds ---" % (time.time() - start_time))
start_time = time.time()
arr = [*map(lambda x: download(x, x_path), lists)]
print(json.dumps(arr))
print("--- Non Spark: %s seconds ---" % (time.time() - start_time))
