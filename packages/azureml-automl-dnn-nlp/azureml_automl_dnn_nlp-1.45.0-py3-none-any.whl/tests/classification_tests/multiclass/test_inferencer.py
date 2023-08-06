from typing import NamedTuple
from pandas.util.testing import assert_frame_equal
from unittest.mock import MagicMock, patch, PropertyMock

import numpy as np
import pandas as pd
import pytest

from azureml.automl.dnn.nlp.classification.common.constants import DatasetLiterals, MultiClassParameters
from azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer import MulticlassInferencer
from azureml.automl.dnn.nlp.classification.io.read.pytorch_dataset_wrapper import PyTorchMulticlassDatasetWrapper
from azureml.automl.dnn.nlp.common.constants import DataLiterals, SystemSettings
from ...mocks import (
    aml_dataset_mock, aml_label_dataset_mock,
    get_multiclass_labeling_df, MockRun, open_classification_file, get_np_load_mock
)

try:
    import torch
    has_torch = True
except ImportError:
    has_torch = False


class OutputName(NamedTuple):
    predictions: np.array


class MockTrainer:
    def __init__(self, nrows=5, ncols=3):
        self.nrows = nrows
        self.ncols = ncols

    def predict(self, test_dataset=None):
        return OutputName(predictions=np.random.rand(self.nrows, self.ncols))

    def is_world_process_zero(self):
        return True


class TestTextClassificationInferenceTests:
    """Tests for Text Classification inference."""
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.PyTorchMulticlassDatasetWrapper")
    @patch("azureml.automl.dnn.nlp.common._data_utils.AmlDataset")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.np.load")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.AutoConfig")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.AutoTokenizer")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.AutoModelForSequenceClassification")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.Trainer")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.MulticlassInferencer.download_file")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer._get_language_code")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.ResourcePathResolver")
    @pytest.mark.usefixtures('MulticlassDatasetTester')
    @pytest.mark.usefixtures('MulticlassTokenizer')
    @pytest.mark.parametrize('multiple_text_column', [True, False])
    @pytest.mark.parametrize('include_label_col', [True, False])
    def test_inference(self, resource_path_resolve_mock, langauge_mock, file_download, trainer_mock, auto_model_mock,
                       auto_token_mock, auto_config_mock, np_load_mock, aml_dataset_mock, pytorch_data_wrapper_mock,
                       MulticlassDatasetTester, MulticlassTokenizer, multiple_text_column, include_label_col):
        test_df = MulticlassDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        mock_run = MockRun(label_column_name=label_column_name)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        inferencer = MulticlassInferencer(mock_run, device)

        mock_aml_dataset = MagicMock()
        mock_aml_dataset.get_by_id.return_value = MagicMock()
        aml_dataset_mock.get_by_id.return_value = mock_aml_dataset

        auto_model = MagicMock()
        auto_model.from_pretrained.return_value = MagicMock()
        auto_model_mock.return_value = auto_model

        pytorch_data_wrapper = MagicMock()
        pytorch_data_wrapper_mock.return_value = pytorch_data_wrapper

        auto_config = MagicMock()
        auto_config.from_pretrained.return_value = MagicMock()
        auto_config_mock.return_value = auto_config

        auto_token_mock.from_pretrained.return_value = MagicMock()

        file_download.return_value = MagicMock()
        langauge_mock.return_value = 'some_language'

        np_load_mock.return_value = MagicMock()

        trainer_mock.return_value = MockTrainer()

        predicted_df = inferencer.score(input_dataset_id="some_dataset_id")
        assert aml_dataset_mock.get_by_id.call_count == 1
        assert file_download.call_count == 5
        assert auto_model_mock.from_pretrained.call_count == 1
        assert auto_config_mock.from_pretrained.call_count == 1
        assert resource_path_resolve_mock.call_args[0][0] == 'some_language'

        if include_label_col:
            label_list = pd.unique(test_df[label_column_name])
        else:
            label_list = ['ABC', 'PQR', 'XYZ']
        mock_trainer_obj = MockTrainer(nrows=len(test_df), ncols=len(label_list))

        if label_column_name in test_df.columns:
            test_df.drop(columns=label_column_name, inplace=True)
        inference_data = PyTorchMulticlassDatasetWrapper(test_df, label_list, MulticlassTokenizer,
                                                         MultiClassParameters.MAX_SEQ_LENGTH_128,
                                                         label_column_name=None)

        predicted_df = inferencer.predict(mock_trainer_obj, inference_data, test_df, label_list, label_column_name)
        if multiple_text_column:
            assert all(column in ['text_first', 'text_second', label_column_name,
                                  DataLiterals.LABEL_CONFIDENCE] for column in predicted_df.columns)
            assert predicted_df.shape == (50, 4)
        else:
            assert all(column in ['text_first', label_column_name,
                                  DataLiterals.LABEL_CONFIDENCE] for column in predicted_df.columns)
            assert predicted_df.shape == (50, 3)
        assert all(item in label_list for item in predicted_df[label_column_name])
        assert all(item >= 0 and item <= 1 for item in predicted_df[DataLiterals.LABEL_CONFIDENCE])

    @patch("azureml.core.Dataset.get_by_id")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.PyTorchMulticlassDatasetWrapper")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.AutoConfig")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.AutoTokenizer")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.AutoModelForSequenceClassification")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.Trainer")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.MulticlassInferencer.download_file")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.ResourcePathResolver.tokenizer",
           new_callable=PropertyMock)
    def test_inference_labeling_service(
            self, tokenizer_mock, file_download, trainer_mock, auto_model_mock, auto_token_mock,
            auto_config_mock, pytorch_data_wrapper_mock, get_by_id_mock
    ):
        label_column_name = "labels_col"
        mock_run = MockRun(
            run_source=SystemSettings.LABELING_RUNSOURCE,
            label_column_name=label_column_name,
            labeling_dataset_type="FileDataset"
        )
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        inferencer = MulticlassInferencer(mock_run, device)

        mock_dataset = aml_label_dataset_mock(
            'TextClassificationMultiClass', data_df=get_multiclass_labeling_df()
        )
        get_by_id_mock.return_value = mock_dataset

        auto_model = MagicMock()
        auto_model.from_pretrained.return_value = MagicMock()
        auto_model_mock.return_value = auto_model

        pytorch_data_wrapper = MagicMock()
        pytorch_data_wrapper_mock.return_value = pytorch_data_wrapper

        auto_config = MagicMock()
        auto_config.from_pretrained.return_value = MagicMock()
        auto_config_mock.return_value = auto_config

        auto_token_mock.from_pretrained.return_value = MagicMock()
        tokenizer_mock.return_value = MagicMock()
        file_download.return_value = MagicMock()

        trainer_mock.return_value = MockTrainer(nrows=60, ncols=3)

        with patch("azureml.automl.dnn.nlp.classification.io.read._labeling_data_helper.open",
                   new=open_classification_file):
            with patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.np.load",
                       new=get_np_load_mock):
                predicted_df = inferencer.score(input_dataset_id="some_dataset_id")
        assert get_by_id_mock.call_count == 1
        assert file_download.call_count == 5
        assert auto_model_mock.from_pretrained.call_count == 1
        assert auto_config_mock.from_pretrained.call_count == 1
        assert tokenizer_mock.call_count == 1

        label_list = ['label_1', 'label_2', 'label_3']

        assert all(column in ['text', label_column_name,
                              DataLiterals.LABEL_CONFIDENCE] for column in predicted_df.columns)
        assert predicted_df.shape == (60, 3)
        assert all(item in label_list for item in predicted_df[label_column_name])
        assert all(0 <= item <= 1 for item in predicted_df[DataLiterals.LABEL_CONFIDENCE])

    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.save_predicted_results")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.MulticlassInferencer.predict")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.PyTorchMulticlassDatasetWrapper")
    @patch("azureml.core.Dataset.get_by_id")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.Trainer")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.MulticlassInferencer."
           "load_training_artifacts")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer."
           "is_data_labeling_run_with_file_dataset")
    @pytest.mark.usefixtures('MulticlassDatasetTester')
    @pytest.mark.parametrize('multiple_text_column', [False])
    @pytest.mark.parametrize('include_label_col', [True, False])
    def test_inference_with_datapoint_id(
            self, is_data_labeling_run_with_file_dataset_mock, load_training_artifacts_mock,
            trainer_mock, get_by_id_mock, pytorch_data_wrapper_mock, predict_mock, save_predicted_results_mock,
            MulticlassDatasetTester
    ):
        test_df = MulticlassDatasetTester.get_data().copy()
        test_df[DatasetLiterals.DATAPOINT_ID] = [f"id_{i}" for i in range(test_df.shape[0])]
        label_column_name = "labels_col"
        mock_run = MockRun(
            run_source=SystemSettings.LABELING_RUNSOURCE,
            label_column_name=label_column_name,
            labeling_dataset_type="TabularDataset"
        )
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        inferencer = MulticlassInferencer(mock_run, device)

        # Labeling run but tabular dataset input
        is_data_labeling_run_with_file_dataset_mock.return_value = False
        load_training_artifacts_mock.return_value = MagicMock(), MagicMock(), MagicMock(), MagicMock()

        mock_aml_dataset = aml_dataset_mock(test_df)
        get_by_id_mock.return_value = mock_aml_dataset

        pytorch_data_wrapper = MagicMock()
        pytorch_data_wrapper_mock.return_value = pytorch_data_wrapper

        trainer_mock.return_value = MockTrainer()

        expected_df = pd.DataFrame(
            [
                ["XYZ", '0.758'],
                ["DEF", '0.831'],
                ["ABC", '0.63'],
                ["ABC", '0.547'],
                ["XYZ", '0.852']
            ] * 10,
            columns=[label_column_name, DataLiterals.LABEL_CONFIDENCE]
        )
        predict_mock.return_value = expected_df

        predicted_df = inferencer.score(input_dataset_id="some_dataset_id", enable_datapoint_id_output=True)
        assert sorted(pytorch_data_wrapper_mock.call_args[0][0].columns) == sorted(['text_first'])
        assert save_predicted_results_mock.call_count == 1
        assert sorted(predicted_df.columns) == sorted([DatasetLiterals.DATAPOINT_ID,
                                                       label_column_name, "label_confidence"])
        assert predicted_df[DatasetLiterals.DATAPOINT_ID].equals(test_df[DatasetLiterals.DATAPOINT_ID])

    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.save_predicted_results")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.MulticlassInferencer.predict")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.PyTorchMulticlassDatasetWrapper")
    @patch("azureml.data.abstract_dataset.AbstractDataset._load")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.Trainer")
    @patch("azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer.MulticlassInferencer."
           "load_training_artifacts")
    @pytest.mark.usefixtures('MulticlassDatasetTester')
    @pytest.mark.parametrize('multiple_text_column', [False])
    @pytest.mark.parametrize('include_label_col', [False])
    def test_score_mltable_uri(
            self, load_training_artifacts_mock, trainer_mock, load_dataset_mock, pytorch_data_wrapper_mock,
            predict_mock, save_predicted_results_mock,
            MulticlassDatasetTester
    ):
        load_training_artifacts_mock.return_value = MagicMock(), MagicMock(), MagicMock(), MagicMock()

        label_column_name = "labels_col"
        mock_run = MockRun(label_column_name=label_column_name)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        inferencer = MulticlassInferencer(mock_run, device)

        test_df = MulticlassDatasetTester.get_data().copy()
        mock_aml_dataset = aml_dataset_mock(test_df)
        load_dataset_mock.return_value = mock_aml_dataset

        pytorch_data_wrapper = MagicMock()
        pytorch_data_wrapper_mock.return_value = pytorch_data_wrapper

        trainer_mock.return_value = MockTrainer()

        expected_df = pd.DataFrame(
            [
                ["XYZ", '0.758'],
                ["DEF", '0.831'],
                ["ABC", '0.63'],
                ["ABC", '0.547'],
                ["XYZ", '0.852']
            ] * 10,
            columns=[label_column_name, DataLiterals.LABEL_CONFIDENCE]
        )
        predict_mock.return_value = expected_df

        predicted_df = inferencer.score(input_mltable_uri="some_mltable_uri")
        assert_frame_equal(predicted_df, expected_df)
        assert predict_mock.call_count == 1
        assert save_predicted_results_mock.call_count == 1
        assert load_dataset_mock.call_count == 1
