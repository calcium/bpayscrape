# app.py

import os
import json

from datetime import datetime
import requests

def getDialogue(theBillerCode):
    print('getDialogue')
    # from botocore.vendored import requests  # this is needed for lambda
    from requests.utils import quote
    from lxml import html

    from bs4 import BeautifulSoup

    # wpURL = "https://bpay.com.au/BillerLookupResults?query={billerCode}"
    wpURL = "https://bpay.com.au/BillerLookupResults?query={billerCode}"
    agent = {"User-Agent": "Mozilla/5.0"}

    url = wpURL.format(billerCode=theBillerCode)
    print('bpay URL={}'.format(url))

    response = requests.get(url, headers=agent)
    print('done')

    root = html.fromstring(response.content)

    xpath = '//*[@id="tab1"]/div/div/div/div[1]/h3/text()'
    numResults = root.xpath(xpath)

    # these are the fields of interest
    billerCodeXP = root.xpath('//*[@id="tab1"]/div/div/div/div[2]/div/div[1]/p[1]')
    billerShortXP = root.xpath('//*[@id="tab1"]/div/div/div/div[2]/div/div[1]/p[2]')
    billerLongNameXP = root.xpath('//*[@id="tab1"]/div/div/div/div[2]/div/div[1]/p[3]')
    locationOfReferenceNumberXP = root.xpath('//*[@id="tab1"]/div/div/div/div[2]/div/div[1]/p[4]')
    billerAcceptsXP = root.xpath('//*[@id="tab1"]/div/div/div/div[2]/div/div[1]/p[5]')

    if len(numResults) == 0:
        print("No results")
        response = {"Dialogue": "No results found"}

        return json.dumps(response)

    results = "Results {} {} {} {} {} {}".format(
                        numResults[0].strip(),
                        billerCodeXP[0].text,
                        billerShortXP[0].text,
                        billerLongNameXP[0].text,
                        locationOfReferenceNumberXP[0].text,
                        billerAcceptsXP[0].text)


    results = { "numResults": numResults[0].strip(),
                "billerCodeXP" : billerCodeXP[0].text,
                "billerShortXP" : billerShortXP[0].text,
                "billerLongNameXP" : billerLongNameXP[0].text,
                "locationOfReferenceNumberXP" : locationOfReferenceNumberXP[0].text,
                "billerAcceptsXP" : billerAcceptsXP[0].text
    }

    response = {
        "statusCode": 200,
        "results": results  # json.dumps(body)
    }

    return response


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("eg. python app.py billerCode")
        sys.exit(1)
        
    billerCode = sys.argv[1]

    res = getDialogue(billerCode)

    print(res)
