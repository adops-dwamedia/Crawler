#!/usr/bin/env python

import subprocess
import re
import fileinput


def list_linked_urls(url, htmlSearchText, urlSearchText, depthLimit = float("inf"), ans = [], rejected = []):
# recursively makes a list of URL's that are linked from resource. If searchText is invoked,
# results are limited to pages that contain searchText string.
	if depthLimit < 0:
		return ans, rejected		
		

	
	if urlSearchText not in url:
		print "\t\turlSearchText not in url: ", url
		rejected.append(url)
		return ans, rejected
	elif url in ans or url in rejected:
		print "\t\tpage already checked: ", url
		rejected.append(url)
		return ans, rejected
	elif re.match(".*\\.pdf$", url):
		print "\t\tpage is pdf:", url
		rejected.append(url)
		
		
			
	html = subprocess.check_output(('curl', "-s", url))


	if htmlSearchText not in html:
		print "\t\tsearch text not in html: ", url
		rejected.append(url)
		return ans, rejected
	else:
		print "match: ", url
		ans.append(url)

	lynxOutput = subprocess.check_output(('lynx', '-dump', '-listonly', url)).split("\n")
	
	
	childURLs = [u.strip().split(" ")[1] for u in lynxOutput if re.match("[0-9]*\. .*", u.strip())]
	
	for c in childURLs:
		ans, rejected = list_linked_urls(c, htmlSearchText, urlSearchText, depthLimit-1, ans, rejected)
	return ans, rejected


def main():
	output, rejected =  list_linked_urls(
		"http://www.partnerinfo.lenovo.com/partners/us/index.shtml", 
		"GTM-MKN4HF",
		"www.partnerinfo.lenovo.com/",
		1
	)
	
	f = open('linkedUrls.txt', 'w')
	for l in output:
		f.write("%s\n"%l)
	
	
main()	
