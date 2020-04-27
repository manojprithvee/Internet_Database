import moz_sql_parser
from tables.tables import *
from moz_sql_parser import parse
class main:
    def __init__(self):
        sql = input("Enter your Query: ")
        while(sql!=""):
            try:
                parsed_sql=parse(sql);
            except moz_sql_parser.ParseException:
                print(moz_sql_parser.ParseException)
            table = tableclass(parsed_sql)
            sql = input("Enter your Query: ")

main()





