import http.client
import urllib.parse
import re
import json
import argparse

def getCookie():
    conn = http.client.HTTPSConnection("dltik.com")
    payload = ''  
    conn.request("GET", "/?hl=en", payload)
    res = conn.getresponse()  
    if res.status == 200:
        cookie = res.headers['Set-Cookie']
        html = res.read().decode("utf-8")
        token = ''
        match = re.search(r"<input name=\"__RequestVerificationToken\"[^>]*value=\"([^ ]+)\"", html, re.MULTILINE)
        if match:
            token = match.group(1)
        return [cookie, token]
    return ''
 
def getDownloadUrl(url, cookie):
    conn = http.client.HTTPSConnection("dltik.com")
    cookies = cookie[0].split(';')[0].split('=')
    payload = 'm=getlink&url=' + urllib.parse.quote(url, safe='') + '&__RequestVerificationToken=' + urllib.parse.quote(cookie[1], safe='')  
    headers = {
        'Cookie': cookies[0] + '=' + cookies[1] + ';',
        'content-type': 'application/x-www-form-urlencoded'
    }
    conn.request("POST", "/?hl=en", payload, headers)
    res = conn.getresponse()
    data = res.read()
    out = json.loads(data.decode("utf-8"))
    output = json.dumps(json.loads(data.decode("utf-8")), indent=4, sort_keys=True)
    return out['data']['destinationUrl']
def getDownloadID(url, cookie):
    conn = http.client.HTTPSConnection("dltik.com")
    cookies = cookie[0].split(';')[0].split('=')
    payload = 'm=getlink&url=' + urllib.parse.quote(url, safe='') + '&__RequestVerificationToken=' + urllib.parse.quote(cookie[1], safe='')
    headers = {
        'Cookie': cookies[0] + '=' + cookies[1] + ';',
        'content-type': 'application/x-www-form-urlencoded'
    }
    conn.request("POST", "/?hl=en", payload, headers)
    res = conn.getresponse()
    data = res.read()
    out = json.loads(data.decode("utf-8"))
    output = json.dumps(json.loads(data.decode("utf-8")), indent=4, sort_keys=True)
    return out['data']['videoId']
def getStatus(url, cookie):
    conn = http.client.HTTPSConnection("dltik.com")
    cookies = cookie[0].split(';')[0].split('=')
    payload = 'm=getlink&url=' + urllib.parse.quote(url, safe='') + '&__RequestVerificationToken=' + urllib.parse.quote(cookie[1], safe='')
    headers = {
        'Cookie': cookies[0] + '=' + cookies[1] + ';',
        'content-type': 'application/x-www-form-urlencoded'
    }
    conn.request("POST", "/?hl=en", payload, headers)
    res = conn.getresponse()
    data = res.read()
    out = json.loads(data.decode("utf-8"))
    return out['status']