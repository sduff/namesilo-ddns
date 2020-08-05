#!/usr/local/bin/python3

# Programatically update DNS records in NameSilo
# Simon Duff 2020
#
# Based on http://www.forkrobotics.com/2014/10/dynamic-dns-with-namesilo-and-powershell/

import requests, xml.etree.ElementTree as et

# Customise me
api_key     = ""                # API Key from NameSilo
domain      = "simonduff.net"   # Main Domain
hostname    = "myhome"          # Sub-Domain

# List Domains URL
list_domains = "https://www.namesilo.com/api/dnsListRecords?version=1&type=xml&key={0}&domain={1}".format(api_key, domain)
r = requests.get(list_domains)
assert (r.status_code==200), "Response Code was not 200"

root = et.fromstring(r.text)
my_ip = root.findall("./request/ip")[0].text

res_rec = (root.find("./reply/resource_record/host[.='{0}.{1}']/..".format(hostname, domain)))
assert (res_rec!=None), "Couldn't find record"

rec_ip = res_rec.find("./value").text
rec_id = res_rec.find("./record_id").text
assert (rec_ip != my_ip), "Stored IP is the same as current IP, no update required"

# Update URL
update_domain = "https://www.namesilo.com/api/dnsUpdateRecord?version=1&type=xml&key={0}&domain={1}&rrid={2}&rrhost={3}&rrvalue={4}&rrttl=3600".format(api_key, domain, rec_id, hostname, my_ip)
r = requests.get(update_domain)
assert (r.status_code==200), "Update Response Code was not 200"
