import json
import urllib

results = json.load(urllib.urlopen("https://www.kimonolabs.com/api/a36urjfk?apikey=czRXtZDEYS8cpaGl1EhuYQ2sUbsbiMc6"))
print results
