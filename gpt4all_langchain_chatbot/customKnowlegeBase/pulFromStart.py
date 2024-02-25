import re
import requests
from bs4 import BeautifulSoup as bs

siteMap = requests.get("https://start.arcada.fi/en/sitemap.xml")
soupMap = bs(siteMap.text,"html.parser")
links = soupMap.findAll("loc")

for protoLink in links:
  protoLink2 = re.split("<loc>", str(protoLink))[1]
  link = re.split("</loc>", protoLink2)[0]
  res = requests.get(link)

  if (res.status_code == 200):
    soup = bs(res.text,"html.parser")

    for toolBar in soup.findAll("div", {"class":"toolbar"}):
        toolBar.decompose()

    for navigation in soup.findAll("nav"):
        navigation.decompose()

    name = link.replace("/", "_")
    name = name.replace(".", "")
    name = name + ".txt"

    file = open("./docs/" + name , "w")
    file.write(soup.get_text())
    file.close()
    print("Created file: "+name)