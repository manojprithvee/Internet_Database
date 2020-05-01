from tables.jshtml import JsHtml
from tables.html import Html
from tables.json import Json
from tables.xml import Xml
from tables.yml import Yml


def tableclass(sql,sc):
    # print(sql)
    if sql["from"] == "html":
        return Html(sql,sc)
    elif sql["from"] == "jshtml":
        return JsHtml(sql,sc)
    elif sql["from"] == "json":
        return Json(sql,sc)
    elif sql["from"] == "xml":
        return Xml(sql,sc)
    elif sql["from"] == "yml":
        return Yml(sql,sc)
    else:
        raise Exception("TableNotSupported");

