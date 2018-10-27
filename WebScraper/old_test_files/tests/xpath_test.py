from lxml import html 

# Load sample file for parsing
with open('/home/jay/projects/python_projects/campaign_finance_scraper/samples/candidate_a.html') as f:
    page = f.read()
    # Treeify the plaintext html
    tree = html.fromstring(page)
    # Xpath parses the DOM and creates a list of objects matching the designated criteria
    # In the below example the leading './/' signifies to search amongst all elements that are descendants of the root node
    res = tree.xpath(".//a[@class='lblentrylink']")
    for item in res:
        # .get(attribute) methods are used to extract data from HTMLElements
        print(item.get('id'))
    f.close()
