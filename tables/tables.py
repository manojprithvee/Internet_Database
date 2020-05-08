from tables.html import *
from tables.jshtml import *
from tables.json import *
from tables.xml import *
from tables.yml import *


def tableclass(sql, sc):
    # print(sql)
    if sql["from"] == "html":
        return Html(sql, sc)
    elif sql["from"] == "jshtml":
        return JsHtml(sql, sc)
    elif sql["from"] == "json":
        return Json()
    elif sql["from"] == "xml":
        return Xml()
    elif sql["from"] == "yml":
        return Yml()
    else:
        raise Exception("TableNotSupported")
