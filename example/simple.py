from mposapi import MPOSApi

api = MPOSApi("https://localhost", "myapikey")
print(api.getdashboarddata({"id":1000}))
print(api.public())