# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Model Wrapper class to encapsulate automl model functionality"""
import numpy as np
import pandas as pd
import torch

from scipy.special import expit
from sklearn.preprocessing import MultiLabelBinarizer
from torch.utils.data import Dataset
from transformers import Trainer
from transformers.models.bert.tokenization_bert import BertTokenizer

from azureml.automl.dnn.nlp.classification.io.read.pytorch_dataset_wrapper import PyTorchDatasetWrapper


class ModelWrapper:
    """Class to wrap AutoML NLP models in the AutoMLTransformer interface"""

    def __init__(self,
                 model: torch.nn.Module,
                 tokenizer: BertTokenizer,
                 dataset_language: str,
                 y_transformer: MultiLabelBinarizer):
        """
        Transform the input data into outputs tensors from model

        :param model: Trained model
        :param tokenizer: Tokenizer used to tokenize text data during training
        :param dataset_language: Language code of dataset
        :param y_transformer: Fitted MultiLabelBinarizer
        """
        super().__init__()
        self.model = model.to(torch.device("cpu"))
        self.tokenizer = tokenizer
        self.dataset_language = dataset_language
        self.y_transformer = y_transformer
        self.classes_ = y_transformer.classes_

    def predict_proba(self,
                      dataset: Dataset) -> np.ndarray:
        """
        Helper function for transforming the input data into outputs tensors using model

        :param dataset: Pytorch dataset object which returns items in the format {'input_ids', 'attention_mask',
            'token_type_ids'}
        :return: List of arrays representing outputs
        """

        trainer = Trainer(model=self.model)
        predictions = trainer.predict(test_dataset=dataset).predictions
        return expit(predictions)

    def predict(self,
                X: pd.DataFrame,
                threshold: int = 0.5):
        """
        Predict output labels for text datasets

        :param context: The PythonModelContext, automatically loaded and used by MLFlow
        :param X: pandas dataframe in the same format as training data, without label columns
        :param threshold: model output threshold at which labels are selected
        :return: returns a list of tuples representing the predicted labels
        """
        dataset = PyTorchDatasetWrapper(X, self.tokenizer, y_transformer=self.y_transformer)

        # predict_probas shape is num examples by num labels
        predict_probas = self.predict_proba(dataset)
        return self.y_transformer.inverse_transform(predict_probas > threshold)
