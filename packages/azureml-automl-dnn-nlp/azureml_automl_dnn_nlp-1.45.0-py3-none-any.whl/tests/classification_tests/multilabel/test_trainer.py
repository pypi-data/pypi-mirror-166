from tests.mocks import aml_dataset_mock, multilabel_trainer_mock
from unittest.mock import MagicMock, patch, Mock

import numpy as np
import pandas as pd
import pytest

from azureml.automl.dnn.nlp.classification.common.constants import MultiLabelParameters
from azureml.automl.dnn.nlp.classification.io.read.dataloader import load_and_validate_multilabel_dataset
from azureml.automl.dnn.nlp.classification.multilabel.trainer import PytorchTrainer


@pytest.mark.usefixtures('MultilabelTokenizer')
@patch("azureml.automl.dnn.nlp.classification.multilabel.trainer.AutoModelForSequenceClassification")
def test_initialization_variables(MultilabelTokenizer):
    tokenizer_mock = Mock(name_or_path="some path")
    rpr = Mock(model_name="some model", model_path="some path", tokenizer=tokenizer_mock)
    PytorchTrainer(rpr, 2, np.array(['A', 'a', '1', '2', 'label5', 'label6']))


@pytest.mark.usefixtures('MultilabelDatasetTester')
@pytest.mark.usefixtures('MultilabelValDatasetTester')
@pytest.mark.parametrize('multiple_text_column', [True, False])
@pytest.mark.parametrize('enable_distributed', [True, False])
@patch("azureml.automl.dnn.nlp.classification.multilabel.trainer.AutoModelForSequenceClassification")
@patch("azureml.automl.dnn.nlp.classification.multilabel.trainer.Trainer")
@patch("azureml.automl.dnn.nlp.classification.multilabel.trainer.DistributedTrainer")
@patch("azureml.core.Dataset.get_by_id")
def test_train(get_by_id_mock, distributed_trainer_mock, trainer_mock, auto_model_mock, MultilabelDatasetTester,
               MultilabelValDatasetTester, enable_distributed):
    num_labels = 2
    train_df = MultilabelDatasetTester.get_data().copy()
    validation_df = MultilabelValDatasetTester.get_data().copy()
    label_column_name = "labels_col"
    concat_df = pd.concat([train_df, validation_df], ignore_index=True)
    mock_aml_dataset = aml_dataset_mock(concat_df)
    get_by_id_mock.return_value = mock_aml_dataset
    aml_workspace_mock = MagicMock()
    automl_settings = dict()
    automl_settings['dataset_id'] = 'mock_id'
    automl_settings['validation_dataset_id'] = 'mock_validation_id'

    tokenizer_mock = Mock(name_or_path="some path")
    rpr = Mock(model_name="some model", model_path="some path", tokenizer=tokenizer_mock)

    training_set, validation_set, _, train_label_list, label_list, _, _ = load_and_validate_multilabel_dataset(
        aml_workspace_mock, "data_dir", label_column_name, automl_settings, tokenizer_mock
    )

    trainer = PytorchTrainer(rpr, num_labels, train_label_list, enable_distributed=enable_distributed)

    # trainer mock
    mock_trainer = multilabel_trainer_mock(len(concat_df))
    distributed_mock_trainer = multilabel_trainer_mock(len(concat_df))
    trainer_mock.return_value = mock_trainer
    distributed_trainer_mock.return_value = distributed_mock_trainer

    trainer.train(training_set)

    assert trainer.training_args.per_device_train_batch_size == MultiLabelParameters.TRAIN_BATCH_SIZE
    assert trainer.training_args.num_train_epochs == MultiLabelParameters.EPOCHS

    # train function
    trainer.trainer.train.assert_called_once()
    trainer.trainer.save_model.assert_called_once()
    trainer.trainer.save_state.assert_called_once()

    if enable_distributed is True:
        assert trainer.trainer is distributed_mock_trainer


@pytest.mark.usefixtures('MultilabelDatasetTester')
@pytest.mark.usefixtures('MultilabelValDatasetTester')
@pytest.mark.parametrize('multiple_text_column', [True, False])
@pytest.mark.parametrize('enable_distributed', [True, False])
@patch("azureml.automl.dnn.nlp.classification.multilabel.trainer.AutoModelForSequenceClassification")
@patch("azureml.automl.dnn.nlp.classification.multilabel.trainer.Trainer")
@patch("azureml.automl.dnn.nlp.classification.multilabel.trainer.DistributedTrainer")
@patch("azureml.core.Dataset.get_by_id")
def test_validate(get_by_id_mock, distributed_trainer_mock, trainer_mock, auto_model_mock, MultilabelDatasetTester,
                  MultilabelValDatasetTester, enable_distributed):
    # validate function
    train_df = MultilabelDatasetTester.get_data().copy()
    validation_df = MultilabelValDatasetTester.get_data().copy()
    concat_df = pd.concat([train_df, validation_df], ignore_index=True)
    mock_aml_dataset = aml_dataset_mock(concat_df)
    get_by_id_mock.return_value = mock_aml_dataset

    label_column_name = "labels_col"

    aml_workspace_mock = MagicMock()
    automl_settings = dict()
    automl_settings['dataset_id'] = 'mock_id'
    automl_settings['validation_dataset_id'] = 'mock_validation_id'

    tokenizer_mock = Mock(name_or_path="some path")
    rpr = Mock(model_name="some model", model_path="some path", tokenizer=tokenizer_mock)

    training_set, validation_set, _, train_label_list, label_list, _, _ = load_and_validate_multilabel_dataset(
        aml_workspace_mock, "data_dir", label_column_name, automl_settings, tokenizer_mock
    )

    num_labels = 2
    trainer = PytorchTrainer(rpr, num_labels, train_label_list,
                             enable_distributed=enable_distributed)

    mock_trainer = multilabel_trainer_mock(len(concat_df))
    distributed_mock_trainer = multilabel_trainer_mock(len(concat_df))
    trainer_mock.return_value = mock_trainer
    distributed_trainer_mock.return_value = distributed_mock_trainer

    trainer.train(training_set)

    predictions, label_ids = trainer.validate(validation_set)
    trainer.trainer.predict.assert_called_once()
    assert predictions.shape[0] == (len(concat_df))
    assert label_ids.shape[0] == (len(concat_df))
    trainer.trainer.save_metrics.assert_called_once()
