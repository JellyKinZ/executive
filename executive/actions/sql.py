from sys import argv
from django.db import connection, transaction
import traceback

class RawSQL(object):
    def run(self, query):
        with transaction.commit_manually():
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                if query.startswith("select"):
                    self.printout(cursor)
                else:
                    if query.startswith("delete"):
                        if not "where" in query:
                            confirm = input("Really delete everything?\nIf so, please write 'yes sir, delete everything.'\n>")
                            if confirm != "yes sir, delete everything.":
                                raise Exception("aborted")
                            
                print("query affected {} rows".format(cursor.rowcount))
                connection.commit()
            except Exception as e:
                traceback.print_exc()

    def printout(self, cursor):
        #truncated to 100
        rows = []
        for x in range(100):
            row = cursor.fetchone()
            if row:
                rows.append(row)
        else:
            for row in rows:
                print(row)

if __name__ == "__main__":
    sql = argv[1]
    r = RawSQL()
    r.run(sql)
