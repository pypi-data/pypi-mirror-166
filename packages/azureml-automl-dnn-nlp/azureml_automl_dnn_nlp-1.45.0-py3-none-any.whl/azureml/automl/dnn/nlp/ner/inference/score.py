# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Scoring functions that can load a serialized model and predict."""

import logging
import os
import json
from typing import Optional, Tuple

from transformers import (
    AutoConfig,
    AutoModelForTokenClassification,
    AutoTokenizer,
    Trainer,
)

from azureml.automl.core.shared import constants, logging_utilities as log_utils
from azureml.automl.dnn.nlp.common.constants import DataLiterals, OutputLiterals, Split
from azureml.automl.dnn.nlp.common._resource_path_resolver import ResourcePathResolver
from azureml.automl.dnn.nlp.common._data_utils import download_file_dataset, get_dataset
from azureml.automl.dnn.nlp.common._utils import _get_language_code, get_run_by_id, is_data_labeling_run
from azureml.automl.dnn.nlp.ner.io.read.dataset_wrapper import DatasetWrapper
from azureml.automl.dnn.nlp.ner.io.read._labeling_data_helper import (
    load_dataset_for_labeling_service, generate_results_for_labeling_service
)
from azureml.automl.dnn.nlp.ner.token_classification_metrics import TokenClassificationMetrics
from azureml.automl.dnn.nlp.ner._utils import (
    get_labels, log_metrics, remove_metric_prefix, write_predictions_to_file
)
from azureml.core.run import Run

_logger = logging.getLogger(__name__)


def _download_file(
        run: Run,
        artifact_type,
        path,
        file_name
) -> None:
    """Downloads artifact files associated with the run.

    :param run: run context of the run that produced the model
    :param artifact_type: artifact file type
    :param path: artifacts directory path
    :file_name: file name for artifact
    """
    _logger.info("Start downloading {} artifact".format(artifact_type))
    run.download_file(os.path.join(path, file_name), output_file_path=file_name)
    _logger.info("Finished downloading {} artifact".format(artifact_type))


def _load_training_artifacts(
        run: Run,
        artifacts_dir: str,
        dataset_language: str
) -> Tuple[AutoModelForTokenClassification, AutoTokenizer]:
    """Load the training artifacts.

    :param run: run context of the run that produced the model
    :param artifacts_dir: artifacts directory
    :return: returns the model, tokenizer and config from the model's training
    """
    _logger.info("Start fetching model from artifacts")

    _download_file(run, OutputLiterals.ARTIFACT_TYPE_CONFIG, artifacts_dir, OutputLiterals.CONFIG_FILE_NAME)
    _download_file(run, OutputLiterals.ARTIFACT_TYPE_MODEL, artifacts_dir, OutputLiterals.NER_MODEL_FILE_NAME)
    _download_file(run, OutputLiterals.ARTIFACT_TYPE_TRAINING_ARGS, artifacts_dir, OutputLiterals.TRAINING_ARGS)
    _download_file(run, OutputLiterals.ARTIFACT_TYPE_LABELS, artifacts_dir, OutputLiterals.LABELS_FILE)

    config = AutoConfig.from_pretrained(OutputLiterals.CONFIG_FILE_NAME)
    resource_path_resolver = ResourcePathResolver(dataset_language, False)
    tokenizer = resource_path_resolver.tokenizer
    model = AutoModelForTokenClassification.from_pretrained(OutputLiterals.NER_MODEL_FILE_NAME, config=config)

    _logger.info("Training artifacts restored successfully")
    return model, tokenizer


def score(
        run_id: str,
        data_dir: str,
        output_dir: str,
        input_dataset_id: Optional[str] = None,
        input_mltable_uri: Optional[str] = None,
        batch_size: int = 8
) -> None:
    """
    Generate predictions from input files.

    :param run_id: azureml run id
    :param data_dir: path to data file
    :param output_dir: path to output file
    :param input_dataset_id: The input dataset id.
    :param input_mltable_uri: The input mltable uri.
    :param batch_size: batch size for prediction
    """
    _logger.info("Starting inference for run {} batch_size: {}".format(run_id, batch_size))

    _logger.info("Get run context")
    current_run = Run.get_context()
    train_run = get_run_by_id(run_id)
    featurization = json.loads(
        train_run.parent.parent.properties.get("AMLSettingsJsonString"))['featurization']
    dataset_language = _get_language_code(featurization)

    is_labeling_run = is_data_labeling_run(train_run)

    # Load training artifacts
    model, tokenizer = _load_training_artifacts(train_run, output_dir, dataset_language)

    # Get Test Dataset object
    _logger.info("Load test dataset")
    test_dataset = get_dataset(
        train_run.experiment.workspace,
        Split.test,
        dataset_id=input_dataset_id,
        mltable_uri=input_mltable_uri
    )
    if is_labeling_run:
        test_file, labeling_input_file_paths = load_dataset_for_labeling_service(
            test_dataset,
            data_dir,
            DataLiterals.TEST_TEXT_FILENAME,
            Split.test
        )
    else:
        test_file = download_file_dataset(test_dataset, Split.test, data_dir)

    # Init for NER task class, labels and metrics
    _logger.info("Initialize Trainer")
    labels = get_labels(OutputLiterals.LABELS_FILE)
    token_classification_metrics = TokenClassificationMetrics(labels)
    # from HF code - modified
    trainer = Trainer(
        model=model,
        # TODO: unable to use training_args on 'cpu' device
        # args=training_args,
        compute_metrics=token_classification_metrics.compute_metrics
    )

    test_file_path = os.path.join(data_dir, test_file)
    with open(test_file_path, encoding=DataLiterals.ENCODING, errors=DataLiterals.ERRORS) as f:
        test_data = f.read()
    test_dataset = DatasetWrapper(
        data=test_data,
        tokenizer=tokenizer,
        labels=labels,
        max_seq_length=128,
        mode=Split.test
    )

    with log_utils.log_activity(
            _logger,
            activity_name=constants.TelemetryConstants.PREDICT_NAME
    ):
        predictions, label_ids, metrics = trainer.predict(test_dataset)
        if metrics and test_dataset.include_label:
            metrics = remove_metric_prefix(metrics, "test_")
            log_metrics(current_run, metrics)
        preds_list, _, preds_proba_list = token_classification_metrics.align_predictions_with_proba(predictions,
                                                                                                    label_ids)
        # Save predictions
        _logger.info("Save predictions")
        os.makedirs(output_dir, exist_ok=True)
        predictions_file_path = os.path.join(output_dir, OutputLiterals.PREDICTIONS_TXT_FILE_NAME)
        write_predictions_to_file(predictions_file_path, test_file_path, preds_list, preds_proba_list)
        if is_labeling_run:
            # For labeling service, extra conversion is needed to output
            generate_results_for_labeling_service(
                predictions_file_path, labeling_input_file_paths, data_dir
            )

    return
