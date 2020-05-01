from tables.html import Html
from tables.jshtml import JsHtml
from tables.json import Json
from tables.xml import Xml
from tables.yml import Yml


def tableclass(sql, sc):
    # print(sql)
    if sql["from"] == "html":
        return Html(sql, sc)
    elif sql["from"] == "jshtml":
        return JsHtml()
    elif sql["from"] == "json":
        return Json()
    elif sql["from"] == "xml":
        return Xml()
    elif sql["from"] == "yml":
        return Yml()
    else:
        raise Exception("TableNotSupported")
