# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Scoring functions that can load a serialized model and predict."""
from typing import Optional, Union
from sklearn.preprocessing import MultiLabelBinarizer

import json
import logging
import numpy as np
import pandas as pd
import torch

from azureml.automl.dnn.nlp.classification.common.constants import (
    DatasetLiterals
)
from azureml.automl.dnn.nlp.classification.io.read._labeling_data_helper import (
    format_multilabel_predicted_df,
    generate_predictions_output_for_labeling_service,
    load_dataset_for_labeling_service
)
from azureml.automl.dnn.nlp.classification.io.read.pytorch_dataset_wrapper import PyTorchDatasetWrapper
from azureml.automl.dnn.nlp.classification.io.read.read_utils import load_model_wrapper
from azureml.automl.dnn.nlp.classification.io.write.save_utils import save_predicted_results
from azureml.automl.dnn.nlp.classification.multilabel.model_wrapper import ModelWrapper
from azureml.automl.dnn.nlp.classification.multilabel.utils import change_label_col_format
from azureml.automl.dnn.nlp.common._data_utils import get_dataset
from azureml.automl.dnn.nlp.common._utils import is_data_labeling_run_with_file_dataset
from azureml.automl.dnn.nlp.common.constants import DataLiterals, OutputLiterals, Split, Warnings
from azureml.core.run import Run

_logger = logging.getLogger(__name__)


class MultilabelInferencer:
    """Class to perform inferencing using training runId and on an unlabeled dataset"""

    def __init__(
            self,
            run: Run,
            device: Union[str, torch.device]
    ):
        """Function to initialize the inferencing object

        :param: Run object
        :param device: device to be used for inferencing
        """
        self.run_object = run
        self.device = device

        if self.device == "cpu":
            _logger.warning(Warnings.CPU_DEVICE_WARNING)

        self.workspace = self.run_object.experiment.workspace

    def predict(
            self,
            model_wrapper: ModelWrapper,
            y_transformer: MultiLabelBinarizer,
            df: pd.DataFrame,
            inference_data: PyTorchDatasetWrapper,
            label_column_name: str
    ) -> pd.DataFrame:
        """Generate predictions using model
        :param model_wrapper: model wrapper
        :param y_transformer: y_transformer
        :param df: DataFrame to make predictions on
        :param inference_data: data for inference
        :param label_column_name: Name/title of the label column
        """

        fin_outputs = model_wrapper.predict_proba(inference_data)

        # create dataframes with label columns
        label_columns = y_transformer.classes_
        label_columns_str = ",".join(label_columns)
        formatted_outputs = [[label_columns_str, ",".join(map(str, list(xi)))] for xi in fin_outputs]
        predicted_labels_df = pd.DataFrame(np.array(formatted_outputs))
        predicted_labels_df.columns = [label_column_name, DataLiterals.LABEL_CONFIDENCE]
        predicted_df = pd.concat([df, predicted_labels_df], join='outer', axis=1)
        return predicted_df

    def score(
            self,
            input_dataset_id: Optional[str] = None,
            input_mltable_uri: Optional[str] = None,
            enable_datapoint_id_output: Optional[bool] = None
    ) -> pd.DataFrame:
        """Generate predictions from input files.
        :param input_dataset_id: The input dataset id
        :param input_mltable_uri: The input mltable uri.
        :param enable_datapoint_id_output: Whether to include datapoint_id in the output
        :return: Dataframe with predictions
        """
        model_wrapper = load_model_wrapper(self.run_object)
        label_column_name = json.loads(
            self.run_object.parent.parent.properties.get("AMLSettingsJsonString")
        ).get('label_column_name', DataLiterals.LABEL_COLUMN)

        is_file_dataset_labeling_run = is_data_labeling_run_with_file_dataset(self.run_object)
        input_file_paths = []
        test_dataset = get_dataset(
            self.workspace,
            Split.test,
            dataset_id=input_dataset_id,
            mltable_uri=input_mltable_uri
        )

        # Fetch dataframe
        if is_file_dataset_labeling_run:
            df, input_file_paths = load_dataset_for_labeling_service(
                test_dataset, DataLiterals.DATA_DIR, False, Split.test
            )
        else:
            df = test_dataset.to_pandas_dataframe()

        warning_message = "You are using the old format of label column. "
        warning_message += "It may parse wrong labels. "
        warning_message += "Please update your label column format to the new format"
        # TODO: add the link of new format into warning message
        if df.shape[0] > 0 and label_column_name in df.columns and df.iloc[0][label_column_name][0] != "[":
            _logger.warning(warning_message)
            change_label_col_format(df, label_column_name)

        # Drop datapoint_id column as it is not part of the text to be trained for but keep data to add back later
        datapoint_column = pd.Series()
        if enable_datapoint_id_output:
            datapoint_column = df[DatasetLiterals.DATAPOINT_ID]

        columns_to_drop = [label_column_name, DatasetLiterals.DATAPOINT_ID]
        df = df[df.columns.difference(columns_to_drop)]

        # Create final inference data
        inference_data = PyTorchDatasetWrapper(df, model_wrapper.tokenizer)

        predicted_df = self.predict(model_wrapper=model_wrapper,
                                    y_transformer=model_wrapper.y_transformer,
                                    df=df,
                                    inference_data=inference_data,
                                    label_column_name=label_column_name
                                    )

        if is_file_dataset_labeling_run:
            predicted_df = format_multilabel_predicted_df(predicted_df, label_column_name)
            generate_predictions_output_for_labeling_service(
                predicted_df, input_file_paths, OutputLiterals.PREDICTIONS_TXT_FILE_NAME, label_column_name
            )
        else:
            # Don't save the actual text in the inference data to the generated predictions file for privacy reasons
            if enable_datapoint_id_output:
                predicted_df[DatasetLiterals.DATAPOINT_ID] = datapoint_column
                output_cols = [DatasetLiterals.DATAPOINT_ID, label_column_name, DataLiterals.LABEL_CONFIDENCE]
                predicted_df = predicted_df[output_cols]
            else:
                output_cols = [label_column_name, DataLiterals.LABEL_CONFIDENCE]
                predicted_df = predicted_df[output_cols]

            save_predicted_results(predicted_df, OutputLiterals.PREDICTIONS_CSV_FILE_NAME)

        return predicted_df
