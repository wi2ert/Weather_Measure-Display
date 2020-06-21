"""
Database object
"""

import urequests


class Dbo:
    def __init__(self, host, port, database, series, tag, field):
        self.host = host
        self.port = port
        self.database = database
        self.series = str(series).replace(" ", "_")
        self.tag = str(tag).replace(" ", "_")
        self.field = str(field).replace(" ", "_")
        self.data = ""
        print("Creating series: " + self.series)

    def make_datapoint(self, tag, field, type="*"):
        try:
            tag = str(tag).replace(" ", "_")
            if type == "s":  # convert the field to a literal string
                self.data += self.series + "," + self.tag + "=" + tag + " " + self.field + "=\"" + str(field) + "\"\n"
            else:  # assumed wildcard type, just paste it in in the format it came
                self.data += self.series + "," + self.tag + "=" + tag + " " + self.field + "=" + str(field) + "\n"
        except Exception as e:
            print(e)

    def write_cache(self):  # write all accumulated cache to the database
        if len(self.data) > 0:
            res = None
            try:
                url = "http://" + self.host + ":" + str(self.port) + "/write?db=" + self.database
                print(url)
                res = urequests.request("POST", url, self.data.rstrip())  # strip the trailing \n
                print(res.status_code)
                if str(res.status_code)[0] == "4" or str(res.status_code)[0] == "5":
                    print(res.reason)
            except Exception as e:
                print(e)
            finally:
                self.data = ""  # reset the data
                if res is not None:  # if there has been a connection, close it
                    res.close()

    def write_s(self, tag, field):  # method to immediately write a string to the database
        self.make_datapoint("s", tag, field)
        self.write_cache()
