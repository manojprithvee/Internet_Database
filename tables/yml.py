import validators
from benedict import benedict

from tables import tables


class Yml:
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
                self.urls = []
                for expression in parsed_sql["where"]:
                    if "in" in expression:
                        print(expression)
                        inexpression = parsed_sql["where"]["in"]
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
                        selectorexpression = parsed_sql["where"]["eq"]
                        if selectorexpression[0] == "url":
                            self.urls.append(selectorexpression[1])
                if not self.urls:
                    raise Exception("NoUrlCondition")
                for url in self.urls:
                    if type(url) != str:
                        raise Exception("MalformedUrl")
                    if not validators.url(url):
                        raise Exception("MalformedUrl")
            else:
                raise Exception("NotAndStatement")
        else:
            raise Exception("NotSelectStatement")

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
    def download(url, keys):
        d = benedict(url, format='yaml')
        outputs = []
        for key in keys:
            raw_keys = d[key]
            outputs.append(raw_keys)
        return outputs
