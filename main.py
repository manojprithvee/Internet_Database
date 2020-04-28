import moz_sql_parser
from tables.tables import *
from moz_sql_parser import parse
class main:
    def __init__(self):
        sql = input("Enter your Query: ")
        # sql = 'select "//section/div[1]/div[2]/div/div/div/div[1]/span/span","//section/div[1]/div[2]/div/div/div/h1/text()" from html where url in ("https://www.lttstore.com/products/ltt-stealth-hoodie") and selector=xpath'
        # sql = 'select ".ProductMeta__Price > span:nth-child(1)",".ProductMeta__Title" from html where url in (' \
        #       '"https://www.lttstore.com/products/ltt-stealth-hoodie") and selector=css '
        sql= 'select "//div[1]/div[2]/div/div/div/div[1]","//section/div[1]/div[2]/div/div/div/h1/text()" from html where url in (select "/html/body/div[6]/main/div[3]/section/div[1]/div/div/div/div/div/a/@href" from html where url in ("https://www.lttstore.com") and selector=xpath) and selector=xpath'
        while(sql!=""):
            try:
                parsed_sql=parse(sql);
            except moz_sql_parser.ParseException:
                print(moz_sql_parser.ParseException)
            table = tableclass(parsed_sql)
            print(table.run())
            sql = input("Enter your Query: ")

main()






