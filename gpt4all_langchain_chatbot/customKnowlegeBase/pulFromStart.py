import re, requests
from bs4 import BeautifulSoup as bs

siteMap = requests.get("https://start.arcada.fi/en/sitemap.xml")
links = bs(siteMap.text, "html.parser").findAll("loc")

for protoLink in links:
  link = link.getText()
  res = requests.get(link)

  if (res.status_code == 200):
      text = re.sub(r'\n+', '\n', bs(res.text, "html.parser").find("article").getText())
      name = link.replace("https://start.arcada.fi/", "").replace("/", "_") + ".txt"
      with open("docs/" + name , "w") as f:
          f.write(text)
      print("Created file: "+name)