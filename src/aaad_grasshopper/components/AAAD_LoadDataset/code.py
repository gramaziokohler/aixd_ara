import os
import urllib2

if load:
    if not os.path.exists(os.path.join(root, dataset_name)):
        print("Cannot find this dataset!")

    else:
        server_url = "http://127.0.0.1:8000/load_dataset"  # Change this to your server's URL
        data = "root={}&dataset_name={}".format(root, dataset_name)
        request = urllib2.Request(server_url, data=data)
        response = urllib2.urlopen(request)
        response_content = response.read()
        print(response_content)
