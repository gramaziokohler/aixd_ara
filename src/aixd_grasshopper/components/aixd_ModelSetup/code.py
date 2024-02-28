settings = {
    "inputML": inputML,
    "outputML": outputML,
    "model_type": "CAE",
    "latent_dim": latent_dim,
    "hidden_layers": hidden_layers,
    "batch_size": batch_size,
}


class wrapper:
    def __init__(self, dict):
        self.dict = dict

    def __repr__(self):
        return "Settings Object"


settings = wrapper(settings)
