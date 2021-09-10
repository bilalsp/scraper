from __future__ import annotations

import re
import uuid
import itertools
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Utils:
    
    @staticmethod
    def fetch_jobs(base_url, filter_list):
        """ 
        Args:
            base_url: base url of website to start scrapping
            filter_list: list of filter 
        Returns:
            iterable of job
        """
        
        # IO bound
        with ThreadPoolExecutor() as executor:
            
            construct_url = lambda filter_: f"{base_url}/jobs/search/?page=10&perPage=100\
                                                &q={'-'.join(filter_.get('keyword','').split())}\
                                                &where={'-'.join(filter_.get('location','').split())}\
                                                &tm={filter_.get('posted_on',0)}".replace(" ","")
            
            urls = map(construct_url, filter_list)
            contents = executor.map(Utils.fetch_content, urls)
        
        logger.info('Fetched all the jobs from web')
        
        
        list_jobs = map(Utils.process_content, contents)
        jobs = itertools.chain(*list_jobs)
        
        # # CPU bound
        # with ProcessPoolExecutor() as executor:
        #     list_jobs = executor.map(Utils.process_content, contents)
        #     jobs = itertools.chain(*list_jobs)
        
        logger.info('Processed all the fetched jobs')
        
        return jobs
    
    
    @staticmethod
    def fetch_content(url):
        """ """ 
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.content


    @staticmethod
    def process_content(content):
        """ """
        jobs = []
        try:
            soup = BeautifulSoup(content, features="html.parser")
            results = soup.find('div', id='SearchResults')
            job_cards = results.find_all('section', class_='card-content')

            #process all the job cards
            for job_card in job_cards:
                title_elm = job_card.find('h2', class_='title')
                comp_elem = job_card.find('div', class_='company')
                loc_elem = job_card.find('div', class_='location')
                time_elm = job_card.find('time')
                
    
                job = {}
                job['id'] = str(uuid.uuid1())
                
                if title_elm:
                    title = title_elm.get_text()
                    title = re.sub(r'[\t\r\n]', '', title)
                    job['title'] = title
                    
                if comp_elem:
                    company = comp_elem.get_text()
                    company = re.sub(r'[\t\r\n]', '', company)
                    job['company'] = company
                    
                if loc_elem:
                    location = loc_elem.get_text()
                    location = re.sub(r'[\t\r\n]', '', location)
                    job['location'] = location
                    
                if time_elm:
                    posted_on = time_elm.get_text()
                    posted_on = re.sub(r'[\t\r\n]', '', posted_on)
                    job['posted_on'] = posted_on
            
                jobs.append(job)
                
        except Exception:
            pass
        
        return jobs    