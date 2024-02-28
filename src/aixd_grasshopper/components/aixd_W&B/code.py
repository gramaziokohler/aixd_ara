import webbrowser

if launch:
    url = "https://wandb.ai/{}".format(user)
    webbrowser.open(url)
    trigger = False
