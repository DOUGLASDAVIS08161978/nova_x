
# Uncertainty Quantification Module
class UncertaintyQuantifier:
    def __init__(self):
        self.uncertainty_models = {}

    def quantify_uncertainty(self, model_name, input_data):
        # Quantify the uncertainty of a model's prediction
        if model_name in self.uncertainty_models:
            return self.uncertainty_models[model_name].quantify_uncertainty(input_data)
        else:
            raise ValueError('Model not found')

    def add_uncertainty_model(self, model_name, uncertainty_model):
        # Add an uncertainty model for a given model
        self.uncertainty_models[model_name] = uncertainty_model
