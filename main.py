import moz_sql_parser
from moz_sql_parser import parse
from pyspark import SparkContext

from tables.tables import *


class Main:
    def __init__(self):
        sc = SparkContext()
        sql = input("Enter your Query: ")
        # sql = 'select "//section/div[1]/div[2]/div/div/div/div[1]/span/span","//section/div[1]/div[' \
        #       '2]/div/div/div/h1/text()" from html where url in (' \
        #       '"https://www.lttstore.com/products/ltt-stealth-hoodie",' \
        #       '"https://www.lttstore.com/products/cpu-deconstructed-t-shirt") and selector=xpath '
        # sql = 'select ".ProductMeta__Price > span:nth-child(1)",".ProductMeta__Title" from html where url in (' \
        #       '"https://www.lttstore.com/products/ltt-stealth-hoodie") and selector=css '
        # sql='select "/html/body/div[6]/main/div[3]/section/div[1]/div/div/div/div/div/a/@href" from html where url' \
        #     ' in ("https://www.lttstore.com") and selector=xpath '
        # sql = 'select "//section/div[1]/div[2]/div/div/div/div[1]/span/span","//section/div[1]/div[' \
        #       '2]/div/div/div/h1/text()" from html where url in (select "/html/body/div[6]/main/div[3]/section/div[' \
        #       '1]/div/div/div/div/div/a/@href" from html where url in ("https://www.lttstore.com") and ' \
        #       'selector=xpath) and selector=xpath '
        while sql != "":
            try:
                parsed_sql = parse(sql)
                table = tableclass(parsed_sql, sc)
                print(table.run(sc))
                sql = input("Enter your Query: ")
            except moz_sql_parser.ParseException:
                print(moz_sql_parser.ParseException)


Main()
