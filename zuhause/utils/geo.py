# -*- coding: utf-8 -*-
import urllib, urllib2, json

def coord(address):
    params = {
        'address' : address,
        'sensor' : 'false',
    }

    url = 'https://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode(params)

    response = urllib2.urlopen(url)
    result = json.load(response)

    try:
        coords = result['results'][0]['geometry']['location']
        return ",".join(str(i) for i in coords.values())
    except:
        return None

def address(latitude_and_logitude):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=%s' % latitude_and_logitude

    response = urllib2.urlopen(url)
    result = json.load(response)

    try:
        return str(result['results'][0]['formatted_address'].encode('utf-8'))
    except:
        return None
