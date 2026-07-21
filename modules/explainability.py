
# Explainability Module
class Explainer:
    def __init__(self):
        self.explanations = {}

    def explain(self, model_name, input_data):
        # Generate an explanation for a model's prediction
        if model_name in self.explanations:
            return self.explanations[model_name].explain(input_data)
        else:
            raise ValueError('Model not found')

    def add_explanation(self, model_name, explanation):
        # Add an explanation for a model's prediction
        self.explanations[model_name] = explanation
