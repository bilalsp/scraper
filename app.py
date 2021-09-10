from scraper import Scraper


def handler(event, context):
    """ """
    base_url = event['url']
    queries = event['queries']
    
    scraper = Scraper(base_url)
    response = scraper.start(queries)

    return response
    

# event = \
# {
# "url": "https://www.monster.com",
# "queries":  [{"keyword":"Data Science", "location":"New YOrk"}]
# }

# handler(event, 2)


# import json
# def handler(event, context):
#     response = {
#         "statusCode": 200,
#         "body": json.dumps({'message':'Successfully scraped.'})
#     }
#     return response