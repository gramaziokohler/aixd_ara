import urllib2

"""
Parameters:
-----------

plot_type: [str] Possible options: "distrib_attributes", "distrib_attributes2d"
"""

server_url = "http://127.0.0.1:8000/plot"
data = "plot_type={}".format(plot_type)
request = urllib2.Request(server_url, data=data)
response = urllib2.urlopen(request)
response_content = response.read()
result = str(response_content)
img_str = result
