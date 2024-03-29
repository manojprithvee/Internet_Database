import urllib.parse

import lxml
import lxml.html as lh
import requests
import validators
from cssselect import GenericTranslator

from tables import tables


class Html:
    def __init__(self, parsed_sql, sc):
        self.patrsed_sql = parsed_sql
        if "select" in parsed_sql:
            if type(parsed_sql["select"]) == dict:
                if "value" in parsed_sql["select"]:
                    self.selectors = [parsed_sql["select"]["value"]]
                else:
                    raise Exception("SelectorNotPresent")
            else:
                if "value" in parsed_sql["select"][0]:
                    self.selectors = list(map(lambda x: x["value"], parsed_sql["select"]))
                else:
                    raise Exception("SelectorNotPresent")

            if "where" in parsed_sql:
                if "and" in parsed_sql["where"]:
                    self.urls = []
                    for expression in parsed_sql["where"]["and"]:
                        if "in" in expression:
                            inexpression = expression["in"]
                            if inexpression[0] == "url":
                                if type(inexpression[1]) == list:
                                    self.urls += inexpression[1]
                                elif type(inexpression[1]) == dict:
                                    table = tables.tableclass(inexpression[1], sc)
                                    self.urls += map(lambda x: x["href"], table.run(sc)[0])
                                else:
                                    self.urls += [inexpression[1]]
                            if inexpression[0] != "url":
                                raise Exception("FoundUnknownExpression")
                        if 'eq' in expression:
                            selectorexpression = expression["eq"]
                            if selectorexpression[0] == "selector":
                                if selectorexpression[1] in ["xpath", "css"]:
                                    self.selector_type = selectorexpression[1]
                                else:
                                    raise Exception("FoundUnknownSelectorType")
                            elif selectorexpression[0] == "url":
                                self.selector_type = "xpath"
                                # self.urls.append(inexpression[1])
                    if not self.urls:
                        raise Exception("NoUrlCondition")
                    if self.selector_type is None:
                        raise Exception("NoSelectorTypeCondition")
                    for url in self.urls:
                        if type(url) != str:
                            raise Exception("MalformedUrl")
                        if not validators.url(url):
                            raise Exception("MalformedUrl")
                else:
                    raise Exception("WhereNotFound")
            else:
                raise Exception("NotAndStatement")
        else:
            raise Exception("NotSelectStatement")
        if self.selector_type == "css":
            self.selectors = map(lambda x: GenericTranslator().css_to_xpath(x), self.selectors)

    def run(self, sc):
        listing = sc.parallelize(self.urls)
        dirdd = listing.distinct()
        outputs = dirdd.map(lambda x: self.download(x, self.selectors)).collect()
        arr = [[] for j in self.selectors]
        for output in outputs:
            for i in range(len(self.selectors)):
                if type(output[i]) == list:
                    arr[i] += output[i]
                else:
                    arr[i].append(output[i])

        return arr

    @staticmethod
    def download(url, xpaths):
        request = requests.get(url)
        dom = lh.fromstring(request.text)
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
        return outputs
