from tables.jshtml import JsHtml
from tables.html import Html
from tables.json import Json
from tables.xml import Xml
from tables.yml import Yml


def tableclass(sql):
    # print(sql)
    if sql["from"] == "html":
        return Html(sql)
    elif sql["from"] == "jshtml":
        return JsHtml(sql)
    elif sql["from"] == "json":
        return Json(sql)
    elif sql["from"] == "xml":
        return Xml(sql)
    elif sql["from"] == "yml":
        return Yml(sql)
    else:
        raise Exception("TableNotSupported");

