# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Entry script that is invoked by the driver script from automl."""
from typing import Any, Dict, Optional

import importlib
import logging
import numpy as np
import os

from azureml._common._error_definition import AzureMLError
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import ExecutionFailure
from azureml.automl.core.shared.exceptions import ValidationException
from azureml.automl.dnn.nlp.classification.io.read.dataloader import load_and_validate_multilabel_dataset
from azureml.automl.dnn.nlp.classification.io.write.save_utils import save_model_wrapper, save_metrics
from azureml.automl.dnn.nlp.classification.multilabel.model_wrapper import ModelWrapper
from azureml.automl.dnn.nlp.classification.multilabel.trainer import PytorchTrainer
from azureml.automl.dnn.nlp.classification.multilabel.utils import compute_metrics
from azureml.automl.dnn.nlp.common._resource_path_resolver import ResourcePathResolver
from azureml.automl.dnn.nlp.common._utils import (
    _get_language_code,
    create_unique_dir,
    is_data_labeling_run_with_file_dataset,
    is_main_process,
    prepare_post_run_properties,
    prepare_run_properties,
    save_conda_yml,
    save_script,
    save_deploy_script,
    scrub_system_exception,
    _get_input_example_dictionary,
    _get_output_example
)
from azureml.automl.dnn.nlp.common.constants import (
    DataLiterals, ModelNames, OutputLiterals, TaskNames, ScoringLiterals
)
from azureml.automl.runtime import _metrics_logging
from azureml.core.run import Run
from azureml.train.automl.runtime._code_generation.utilities import generate_nlp_code_and_notebook
from azureml.train.automl.runtime._entrypoints.utils.common import initialize_log_server

horovod_spec = importlib.util.find_spec("horovod")
has_horovod = horovod_spec is not None

_logger = logging.getLogger(__name__)


def run(
        automl_settings: Dict[str, Any],
        mltable_data_json: Optional[str] = None,
        **kwargs: Any
):
    """
    Invoke training by passing settings and write the output model.

    :param automl_settings: dictionary with automl settings
    :param mltable_data_json: mltable data json containing location of data
    """
    current_run = Run.get_context()
    try:
        is_labeling_run = is_data_labeling_run_with_file_dataset(current_run)

        workspace = current_run.experiment.workspace
        prepare_run_properties(current_run, ModelNames.BERT_BASE_UNCASED)

        # Parse settings internally initializes logger
        automl_settings_obj = initialize_log_server(current_run, automl_settings)

        # Extract settings needed
        is_gpu = automl_settings_obj.is_gpu if hasattr(automl_settings_obj, "is_gpu") else True
        primary_metric = automl_settings_obj.primary_metric
        label_column_name = automl_settings_obj.label_column_name
        if label_column_name is None:
            if not is_labeling_run:
                raise ValidationException._with_error(
                    AzureMLError.create(
                        ExecutionFailure,
                        operation_name="runner",
                        error_details="Need to pass in label_column_name argument for training"
                    )
                )
            label_column_name = DataLiterals.LABEL_COLUMN
        dataset_language = _get_language_code(automl_settings_obj.featurization)

        data_dir = create_unique_dir(DataLiterals.DATA_DIR)

        # Get enable distributed dnn training
        distributed = hasattr(automl_settings_obj, "enable_distributed_dnn_training") and \
            automl_settings_obj.enable_distributed_dnn_training is True and has_horovod

        resource_path_resolver = ResourcePathResolver(dataset_language, True)
        tokenizer = resource_path_resolver.tokenizer

        # Load Dataset
        training_set, validation_set, num_label_cols, train_label_list, label_list, y_val, y_transformer =\
            load_and_validate_multilabel_dataset(
                workspace, data_dir, label_column_name, automl_settings, tokenizer,
                mltable_data_json, is_labeling_run
            )

        # Get trainer
        trainer = PytorchTrainer(resource_path_resolver=resource_path_resolver,
                                 num_label_cols=num_label_cols,
                                 train_label_list=train_label_list,
                                 is_gpu=is_gpu,
                                 enable_distributed=distributed)

        # Train
        trainer.train(training_set)

        primary_metric_score = np.nan
        if is_main_process():
            # Validate and Log Metrics if validation set is provided
            if validation_set is not None:
                val_predictions, label_ids = trainer.validate(validation_set)
                metrics_dict, metrics_dict_with_thresholds = compute_metrics(val_predictions, label_ids, y_transformer)
                # Log metrics
                _metrics_logging.log_metrics(current_run, metrics_dict)
                primary_metric_score = metrics_dict[primary_metric]
                save_metrics(metrics_dict_with_thresholds)

            # Get input and output str
            input_sample_str = _get_input_example_dictionary(training_set.data,
                                                             label_column_name),
            output_sample_str = _get_output_example(training_set.data, label_column_name)

            # Save for inference
            model_wrapper = ModelWrapper(
                trainer.trainer.model, training_set.tokenizer, dataset_language, y_transformer
            )
            multilabel_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                "io", "write", TaskNames.MULTILABEL)
            model_path = save_model_wrapper(run=current_run, model=model_wrapper,
                                            save_mlflow=automl_settings_obj.save_mlflow,
                                            input_sample_str=input_sample_str[0],
                                            output_sample_str=output_sample_str)

            save_script(OutputLiterals.SCORE_SCRIPT, multilabel_directory)

            deploy_script_path = save_deploy_script(ScoringLiterals.MULTILABEL_SCORE_FILE,
                                                    input_sample_str[0],
                                                    output_sample_str)

            conda_file_path = save_conda_yml(current_run.get_environment())

            # Update run
            # 2147483648 bytes is 2GB
            # TODO: set the model size based on real model, tokenizer, etc size
            prepare_post_run_properties(
                current_run,
                model_path,
                2147483648,
                conda_file_path,
                deploy_script_path,
                primary_metric,
                primary_metric_score
            )
            _logger.info("Code generation enabled: {}".format(automl_settings_obj.enable_code_generation))
            if automl_settings_obj.enable_code_generation:
                generate_nlp_code_and_notebook(current_run)
    except Exception as e:
        _logger.error("Multi-label runner script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(current_run, scrub_system_exception(e), update_run_properties=True)
        raise
