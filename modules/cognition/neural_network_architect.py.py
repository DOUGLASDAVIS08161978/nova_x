# cognition/neural_network_architect.py

"""
Module for designing and optimizing neural network architectures.
"""

import numpy as np
from typing import Dict, List, Tuple
from tensorflow.keras.layers import Layer
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

class NeuralNetworkArchitect:
    """
    Class for designing and optimizing neural network architectures.

    Attributes:
        input_shape (Tuple[int, int]): Input shape of the neural network.
        output_shape (Tuple[int, int]): Output shape of the neural network.
        hidden_layers (List[Dict[str, int]]): List of dictionaries containing information about each hidden layer.
        optimizer (str): Optimizer used for training the neural network.
        loss_function (str): Loss function used for training the neural network.
    """

    def __init__(self,
                 input_shape: Tuple[int, int],
                 output_shape: Tuple[int, int],
                 hidden_layers: List[Dict[str, int]],
                 optimizer: str = 'adam',
                 loss_function: str = 'mean_squared_error'):
        """
        Initializes the NeuralNetworkArchitect class.

        Args:
            input_shape (Tuple[int, int]): Input shape of the neural network.
            output_shape (Tuple[int, int]): Output shape of the neural network.
            hidden_layers (List[Dict[str, int]]): List of dictionaries containing information about each hidden layer.
            optimizer (str, optional): Optimizer used for training the neural network. Defaults to 'adam'.
            loss_function (str, optional): Loss function used for training the neural network. Defaults to 'mean_squared_error'.

        Raises:
            ValueError: If the input shape or output shape is not a tuple of two integers.
            ValueError: If the hidden layers is not a list of dictionaries.
            ValueError: If the optimizer or loss function is not a string.
        """
        if not isinstance(input_shape, tuple) or len(input_shape) != 2 or not all(isinstance(x, int) for x in input_shape):
            raise ValueError("Input shape must be a tuple of two integers.")
        if not isinstance(output_shape, tuple) or len(output_shape) != 2 or not all(isinstance(x, int) for x in output_shape):
            raise ValueError("Output shape must be a tuple of two integers.")
        if not isinstance(hidden_layers, list) or not all(isinstance(layer, dict) for layer in hidden_layers):
            raise ValueError("Hidden layers must be a list of dictionaries.")
        if not isinstance(optimizer, str):
            raise ValueError("Optimizer must be a string.")
        if not isinstance(loss_function, str):
            raise ValueError("Loss function must be a string.")

        self.input_shape = input_shape
        self.output_shape = output_shape
        self.hidden_layers = hidden_layers
        self.optimizer = optimizer
        self.loss_function = loss_function

        self.model = self._create_model()

    def _create_model(self) -> Model:
        """
        Creates a neural network model based on the provided architecture.

        Returns:
            Model: The created neural network model.
        """
        inputs = Layer(input_shape=self.input_shape)
        x = inputs.output

        for layer in self.hidden_layers:
            x = Layer(layer['units'], activation=layer['activation'])(x)

        outputs = Layer(self.output_shape)(x)
        model = Model(inputs=inputs, outputs=outputs)

        optimizer = Adam() if self.optimizer == 'adam' else self.optimizer
        model.compile(optimizer=optimizer, loss=self.loss_function)

        return model

    def run(self,
            x_train: np.ndarray,
            y_train: np.ndarray,
            x_val: np.ndarray,
            y_val: np.ndarray,
            epochs: int = 10,
            batch_size: int = 32,
            patience: int = 5) -> Tuple[float, float]:
        """
        Trains the neural network model on the provided training data and evaluates its performance on the validation data.

        Args:
            x_train (np.ndarray): Training input data.
            y_train (np.ndarray): Training output data.
            x_val (np.ndarray): Validation input data.
            y_val (np.ndarray): Validation output data.
            epochs (int, optional): Number of epochs to train the model. Defaults to 10.
            batch_size (int, optional): Batch size for training the model. Defaults to 32.
            patience (int, optional): Patience for early stopping. Defaults to 5.

        Returns:
            Tuple[float, float]: The training loss and validation loss after training the model.
        """
        early_stopping = EarlyStopping(monitor='val_loss', patience=patience)
        history = self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_val, y_val), callbacks=[early_stopping])

        return history.history['loss'][-1], history.history['val_loss'][-1]
This module provides a `NeuralNetworkArchitect` class that can be used to design and optimize neural network architectures. The class has an `__init__` method that initializes the architecture and a `run` method that trains the model on the provided training data and evaluates its performance on the validation data.

The `__init__` method takes the input shape, output shape, hidden layers, optimizer, and loss function as arguments. It checks the types of these arguments and raises a `ValueError` if any of them are invalid.

The `_create_model` method creates a neural network model based on the provided architecture. It defines the input layer, hidden layers, and output layer, and compiles the model with the specified optimizer and loss function.

The `run` method trains the model on the provided training data and evaluates its performance on the validation data. It uses early stopping to prevent overfitting. The method returns the training loss and validation loss after training the model.
