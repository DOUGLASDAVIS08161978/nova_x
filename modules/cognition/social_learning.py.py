# cognition/social_learning.py

import random
import numpy as np
from typing import Dict, List, Tuple

class SocialLearning:
    """
    A class for Nova-X to learn from human social interactions.

    Attributes:
    ----------
    interactions : Dict[str, List[Tuple[str, str]]]
        A dictionary to store human interactions where keys are interaction types and values are lists of tuples containing human actions and responses.
    social_norms : Dict[str, List[str]]
        A dictionary to store social norms where keys are interaction types and values are lists of expected human responses.
    """

    def __init__(self):
        """
        Initializes the SocialLearning class.
        """
        self.interactions: Dict[str, List[Tuple[str, str]]] = {}
        self.social_norms: Dict[str, List[str]] = {}

    def run(self, interaction_type: str, human_action: str, human_response: str) -> Tuple[str, str]:
        """
        Runs the social learning algorithm.

        Parameters:
        ----------
        interaction_type : str
            The type of human interaction (e.g., greeting, farewell, etc.).
        human_action : str
            The action taken by the human (e.g., saying hello, waving goodbye, etc.).
        human_response : str
            The response given by the human (e.g., responding with a hello, waving back, etc.).

        Returns:
        -------
        Tuple[str, str]
            A tuple containing the updated social norms and the learned human action.
        """
        try:
            # Update interactions dictionary
            if interaction_type not in self.interactions:
                self.interactions[interaction_type] = []
            self.interactions[interaction_type].append((human_action, human_response))

            # Update social norms dictionary
            if interaction_type not in self.social_norms:
                self.social_norms[interaction_type] = []
            self.social_norms[interaction_type].append(human_response)

            # Learn from interactions
            learned_action = self.learn_from_interactions(interaction_type)
            return interaction_type, learned_action
        except Exception as e:
            print(f"Error: {str(e)}")
            return None, None

    def learn_from_interactions(self, interaction_type: str) -> str:
        """
        Learns from human interactions and returns the learned human action.

        Parameters:
        ----------
        interaction_type : str
            The type of human interaction (e.g., greeting, farewell, etc.).

        Returns:
        -------
        str
            The learned human action.
        """
        try:
            # Get all human responses for the given interaction type
            human_responses = self.social_norms[interaction_type]

            # Calculate the probability of each human response
            probabilities = np.array([human_responses.count(response) / len(human_responses) for response in human_responses])

            # Select a human response based on the calculated probabilities
            learned_response = np.random.choice(human_responses, p=probabilities)

            # Return the learned human action
            return learned_response
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
You can use this module as follows:

from cognition.social_learning import SocialLearning

social_learning = SocialLearning()
interaction_type = "greeting"
human_action = "hello"
human_response = "hi"

result = social_learning.run(interaction_type, human_action, human_response)
print(result)
