import logging
import json

from scraper.components import *


formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
streamhandler = logging.StreamHandler()
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)


class Scraper:
    
    def __init__(self, base_url):
        logger.info('Scraper Object Start.....')
        self.base_url = base_url
        logger.info('gettable method Created.....')
        self.table = get_table('JobTable')
        logger.info('Scraper Object Created.....')
        
    
    def start(self, queries, **kwargs):
        """Start Scraping the website"""
        
        logger.info('Scraper started')
        
        # fetch all jobs using Multithreading and process using Multiprocessing based on queries 
        jobs = Utils.fetch_jobs(self.base_url, queries)
        
        # save into dynamoDB
        db.save(self.table, jobs)
   
        logger.info('scraping done')
        
        response = {
            "statusCode": 200,
            "body": json.dumps({'message':'Successfully scraped.'})
        }
        
        return response