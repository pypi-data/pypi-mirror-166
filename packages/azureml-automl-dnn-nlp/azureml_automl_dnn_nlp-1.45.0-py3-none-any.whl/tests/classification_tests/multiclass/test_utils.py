import numpy as np
import pytest

from azureml.automl.core.shared import constants
from azureml.automl.dnn.nlp.classification.common.constants import MultiClassParameters
from azureml.automl.dnn.nlp.classification.multiclass.utils import compute_metrics, get_max_seq_length
from azureml.automl.dnn.nlp.common._utils import concat_text_columns, is_data_labeling_run_with_file_dataset
from ...mocks import MockRun


class TestTextClassificationUtils:
    """Tests for utility functions for multi-class text classification."""
    @pytest.mark.parametrize('class_labels, train_labels',
                             [pytest.param(np.array(['ABC', 'DEF', 'XYZ']), np.array(['ABC', 'DEF'])),
                              pytest.param(np.array(['ABC', 'DEF', 'XYZ']), np.array(['ABC', 'DEF', 'XYZ']))])
    def test_compute_metrics(self, class_labels, train_labels):
        predictions = np.random.rand(5, len(train_labels))
        y_val = np.random.choice(class_labels, size=5)
        results = compute_metrics(y_val, predictions, class_labels, train_labels)
        metrics_names = list(constants.Metric.CLASSIFICATION_SET)
        assert all(key in metrics_names for key in results)

    @pytest.mark.usefixtures('MulticlassDatasetTester')
    @pytest.mark.parametrize('multiple_text_column', [True, False])
    @pytest.mark.parametrize('include_label_col', [True, False])
    def test_concat_text_columns(self, MulticlassDatasetTester, include_label_col):
        input_df = MulticlassDatasetTester.get_data().copy()
        label_column_name = "labels_col" if include_label_col else None
        all_text_cols = [column for column in input_df.columns
                         if label_column_name is None or label_column_name != column]
        expected_concatenated_text = input_df[all_text_cols].apply(lambda x: ". ".join(x.values.astype(str)), axis=1)
        for index in range(len(input_df)):
            concatenated_text = concat_text_columns(input_df.iloc[index], input_df.columns, label_column_name)
            assert concatenated_text == expected_concatenated_text[index]

    @pytest.mark.usefixtures('MulticlassDatasetTester')
    @pytest.mark.usefixtures('MulticlassTokenizer')
    @pytest.mark.parametrize('multiple_text_column', [True, False])
    @pytest.mark.parametrize('include_label_col', [True])
    @pytest.mark.parametrize('is_long_range_text', [True, False])
    @pytest.mark.parametrize('enable_long_range_text', [True, False])
    def test_get_max_seq_length(self, MulticlassDatasetTester, is_long_range_text,
                                MulticlassTokenizer, enable_long_range_text):
        input_df = MulticlassDatasetTester.get_data(is_long_range_text).copy()
        label_column_name = "labels_col"
        max_seq_length = get_max_seq_length(input_df, MulticlassTokenizer, label_column_name,
                                            enable_long_range_text=enable_long_range_text)
        if enable_long_range_text and is_long_range_text:
            assert max_seq_length == MultiClassParameters.MAX_SEQ_LENGTH_256
        else:
            assert max_seq_length == MultiClassParameters.MAX_SEQ_LENGTH_128

        # Test cases below assert that the long range feature is turned ON by default
        max_seq_length = get_max_seq_length(input_df, MulticlassTokenizer, label_column_name)
        if is_long_range_text:
            assert max_seq_length == MultiClassParameters.MAX_SEQ_LENGTH_256
        else:
            assert max_seq_length == MultiClassParameters.MAX_SEQ_LENGTH_128

    def test_is_data_lebeling_negative_with_parent(self):
        current_run = MockRun()
        assert not is_data_labeling_run_with_file_dataset(current_run)

    def test_is_data_lebeling_negative_none_parent(self):
        assert not is_data_labeling_run_with_file_dataset(None)

    def test_is_data_lebeling_positive_with_parent(self):
        current_run = MockRun('Labeling', 'y', "auto", 'FileDataset')
        assert is_data_labeling_run_with_file_dataset(current_run)
