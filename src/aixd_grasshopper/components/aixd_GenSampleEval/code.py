summarytxt = {}  # key =obj name, values= [req, pred, real]

request_dict = {}
for rv in request:
    k, v = rv.split(":")
    v = float(v)
    request_dict[k] = v
# print request_dict


real = [list(b) for b in real.Branches]
real_dict = {k: v for k, v in real}

predicted_dict = predicted.dict["performance_attributes"]
keys = predicted_dict.keys()


txt = "{:>12} |".format("name")
for k in keys:
    txt += "{:>12} |".format(k)
txt += "\n"

txt += "\n{:>12} |".format("request")
for k in keys:
    if k in request_dict:
        txt += "{:>12.2f} |".format(request_dict[k])
    else:
        txt += "{:>12} |".format("*")

txt += "\n{:>12} |".format("pred")
for k in keys:
    txt += "{:>12.2f} |".format(predicted_dict[k])

txt += "\n{:>12} |".format("real")
for k in keys:
    txt += "{:>12.2f} |".format(real_dict[k])


comparison = txt
