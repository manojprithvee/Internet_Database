import json

import lxml
import lxml.html as lh
import requests
from cssselect import GenericTranslator



class Html:
    def __init__(self, parsed_sql):
        self.patrsed_sql = parsed_sql;
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
            print(self.selectors)
            if "where" in parsed_sql:
                if "and" in parsed_sql["where"]:
                    self.urls = []
                    for expression in parsed_sql["where"]["and"]:
                        if "in" in expression:
                            inexpression = expression["in"]
                            if inexpression[0] == "url":
                                if type(inexpression[1]) == list:
                                    self.urls += inexpression[1]
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
                    if not self.urls:
                        raise Exception("NoUrlCondition")
                    if self.selector_type is None:
                        raise Exception("NoSelectorTypeCondition")
                else:
                    raise Exception("WhereNotFound")
            else:
                raise Exception("NotAndStatement")
        else:
            raise Exception("NotSelectStatement")
        print(self.selector_type)
        print(self.urls)
        print(self.selectors)
        if self.selector_type == "css":
            self.selectors = map(lambda x: GenericTranslator().css_to_xpath(x), self.selectors)
        arr = [*map(lambda x: self.download(x, self.selectors), self.urls)]
        print(json.dumps(arr))

    def download(self, url, xpaths):
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
