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
