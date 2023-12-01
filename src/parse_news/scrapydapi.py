from scrapyd_api import ScrapydAPI
scrapyd = ScrapydAPI('http://localhost:6800')
res = scrapyd.list_projects()
print(res)
