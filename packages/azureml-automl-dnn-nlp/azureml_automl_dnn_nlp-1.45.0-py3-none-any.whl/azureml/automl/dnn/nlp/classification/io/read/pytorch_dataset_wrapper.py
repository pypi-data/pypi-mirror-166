# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
#
# For PyTorchDatasetWrapper:
#
# MIT License
#
# Copyright (c) 2020 Abhishek Kumar Mishra
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""PyTorchDatasetWrapper class for text tasks"""

import logging
import ast
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset as PyTorchDataset
from transformers import PreTrainedTokenizerBase
from typing import Optional

from azureml.automl.dnn.nlp.classification.common.constants import (
    DatasetLiterals,
    MultiClassParameters,
    MultiLabelParameters
)
from azureml.automl.dnn.nlp.common._utils import concat_text_columns
from azureml.automl.dnn.nlp.common.constants import DataLiterals

_logger = logging.getLogger(__name__)


class PyTorchDatasetWrapper(PyTorchDataset):
    """Class for obtaining dataset to be passed into model."""

    def __init__(self, dataframe, tokenizer, label_column_name=None, y_transformer=None):
        """ Init function definition

        :param dataframe: pd.DataFrame holding data to be passed
        :param tokenizer: tokenizer to be used to tokenize the data
        :param label_column_name: name/title of the label column
        :param y_transformer: Optional fitted MultiLabelBinarizer to transform the
                              Multilabel labels column to one-hot encoding
        """
        self.tokenizer = tokenizer
        self.data = dataframe
        self.targets = None
        if label_column_name is not None:
            self.targets = self.data[label_column_name]
        self.max_len = MultiLabelParameters.MAX_LEN
        self.label_column_name = label_column_name
        self.y_transformer = y_transformer

    def __len__(self):
        """Len function definition."""
        return len(self.data)

    def __getitem__(self, index):
        """Getitem function definition."""
        comment_text = concat_text_columns(self.data.iloc[index], self.data.columns, self.label_column_name)
        inputs = self.tokenizer(comment_text,
                                max_length=self.max_len,
                                padding='max_length',
                                truncation=True)

        for tokenizer_key in inputs:
            inputs[tokenizer_key] = torch.tensor(inputs[tokenizer_key], dtype=torch.long)

        if self.targets is not None:
            label_col = np.array([ast.literal_eval(self.targets.iloc[index])])
            label_col = np.array([[str(x) for x in item] for item in label_col])
            sparse_one_hot = self.y_transformer.transform(label_col)
            labels = sparse_one_hot.toarray().astype(int)[0]
            inputs['labels'] = torch.tensor(labels, dtype=torch.float)

        return inputs


class PyTorchMulticlassDatasetWrapper(PyTorchDataset):
    """
    Class for obtaining dataset to be passed into model for multi-class classification.
    This is based on the datasets.Dataset package from HuggingFace.
    """

    def __init__(self, dataframe: pd.DataFrame, train_label_list: np.ndarray,
                 tokenizer: PreTrainedTokenizerBase,
                 max_seq_length: int,
                 label_column_name: Optional[str] = None):
        """ Init function definition

        :param dataframe: pd.DataFrame holding data to be passed
        :param train_label_list: list of labels from training data
        :param tokenizer: tokenizer to be used to tokenize the data
        :param max_seq_length: dynamically computed max sequence length
        :param label_column_name: name/title of the label column
        """
        self.label_to_id = {v: i for i, v in enumerate(train_label_list)}
        self.tokenizer = tokenizer
        self.data = dataframe
        self.label_column_name = label_column_name

        # Padding strategy
        self.padding = False
        if MultiClassParameters.PAD_TO_MAX_LENGTH:
            self.padding = MultiClassParameters.MAX_LEN_PADDING

        self.max_seq_length = min(max_seq_length, self.tokenizer.model_max_length)

    def __len__(self):
        """Len function definition."""
        return len(self.data)

    def __getitem__(self, index):
        """Getitem function definition."""
        sample = concat_text_columns(self.data.iloc[index], self.data.columns, self.label_column_name)
        tokenized = self.tokenizer(sample, padding=self.padding, max_length=self.max_seq_length,
                                   truncation=True)
        tokenized[DatasetLiterals.INPUT_IDS] = torch.tensor(tokenized[DatasetLiterals.INPUT_IDS],
                                                            dtype=torch.long)
        tokenized[DatasetLiterals.TOKEN_TYPE_IDS] = torch.tensor(tokenized[DatasetLiterals.TOKEN_TYPE_IDS],
                                                                 dtype=torch.long)
        tokenized[DatasetLiterals.ATTENTION_MASK] = torch.tensor(tokenized[DatasetLiterals.ATTENTION_MASK],
                                                                 dtype=torch.long)

        if self.label_column_name is not None and self.label_to_id is not None and \
           self.label_column_name in self.data.columns:
            label = self.data[self.label_column_name].iloc[index]
            tokenized[DataLiterals.LABEL_COLUMN] = torch.tensor(self.label_to_id[label], dtype=torch.long)

        return tokenized
