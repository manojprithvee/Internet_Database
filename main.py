import findspark
import moz_sql_parser
from moz_sql_parser import parse

findspark.init()
from pyspark import SparkContext

from tables.tables import *


class Main:
    def __init__(self):
        sc = SparkContext()
        while sql != "":
            try:
                parsed_sql = parse(sql)
                table = tableclass(parsed_sql, sc)
                print(table.run(sc))
                sql = input("Enter your Query: ")
            except moz_sql_parser.ParseException:
                print(moz_sql_parser.ParseException)


Main()
