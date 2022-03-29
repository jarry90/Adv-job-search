import requests
from bs4 import BeautifulSoup
import pprint

keywords = ["python junior", "python Graduate"]
# strongkeywords = ["junior"]
locations = ["brisbane", "gold coast"]
min_salary = 80000
# wfh_decision = "yes" ***need to add this

def get_seek_jobs(keywords, locations, strongkeywords):
	seekjobs = []
	seek_url_list = build_seek_links(keywords, locations)
	for url in seek_url_list:
		for job in get_seek_jobs_for_url(url):
			if job not in seekjobs:
				# if job["title"].find(strongkeywords[0]):
				seekjobs.append(job)
	return seekjobs

def build_seek_links(keywords, locations):
	seek_url_list = []
	for location in locations:
		seek_url = "https://www.seek.com.au/jobs/in-" + location.replace(" ", "-") + "?keywords="
		for kw_set in keywords:
			seek_url_list.append(seek_url + "\"" + kw_set.replace(" ", '"%20"') + "\"" + "&salaryrange=" + str(min_salary) + "-999999&salarytype=annual&sortmode=ListedDate")
	print(seek_url_list)
	return seek_url_list

def get_seek_jobs_for_url(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text, 'html.parser')
	jobs = soup.select('article[data-automation="normalJob"]')
	return seek_jobs_to_dict(jobs)

def seek_jobs_to_dict(jobs):
	jobsdata = []
	for job in jobs:
		title = job.select('a[data-automation="jobTitle"]')[0].getText()
		href = "https://www.seek.com.au" + job.select('a[data-automation="jobTitle"]')[0].get('href', None)
		date = job.select('span[data-automation="jobListingDate"]')[0].getText()
		# need to add better date functionallity
		location = job.select('a[data-automation="jobLocation"]')[0].getText()
		# description = ***might add later
		jobsdata.append({"title": title, "href": href, "date": date,"location": location})
	return jobsdata
 
print(get_seek_jobs(keywords, locations, strongkeywords))