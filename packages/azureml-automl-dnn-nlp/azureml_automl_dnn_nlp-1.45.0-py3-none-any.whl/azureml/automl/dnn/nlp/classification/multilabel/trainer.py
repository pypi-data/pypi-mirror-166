# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Class for training Pytorch Models"""
from transformers import (
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)

import logging

from azureml.automl.core.shared import constants, logging_utilities as log_utils
from azureml.automl.dnn.nlp.classification.common.constants import MultiLabelParameters
from azureml.automl.dnn.nlp.classification.io.read.pytorch_dataset_wrapper import PyTorchDatasetWrapper
from azureml.automl.dnn.nlp.common._resource_path_resolver import ResourcePathResolver
from azureml.automl.dnn.nlp.common._utils import _convert_memory_exceptions, is_main_process
from azureml.automl.dnn.nlp.common.constants import OutputLiterals, SystemSettings
from azureml.automl.dnn.nlp.common.distributed_trainer import DistributedTrainer


_logger = logging.getLogger(__name__)


class PytorchTrainer:
    """Class to perform training on a model given a dataset"""

    def __init__(self,
                 resource_path_resolver: ResourcePathResolver,
                 num_label_cols,
                 train_label_list,
                 is_gpu=True,
                 enable_distributed=False):
        """
        Function to initialize pytorch trainer

        :param num_label_cols: Number of unique classes in label column
        :param resource_path_resolver: ResourcePathResolver to get model based on language.
        :param train_label_list: List of labels coming from the training data
        :param is_gpu: Setting to allow for gpu training
        :param enable_distributed: Enable distributed training on multiple gpus and machines
        """
        self.model_name = resource_path_resolver.model_name
        self.tokenizer = resource_path_resolver.tokenizer
        download_dir = resource_path_resolver.model_path

        # load model
        model_name_or_path = download_dir if download_dir else self.model_name
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name_or_path,
                                                                        problem_type='multi_label_classification',
                                                                        num_labels=num_label_cols,
                                                                        return_dict=False)
        self.enable_distributed = enable_distributed
        self.train_label_list = train_label_list
        self.trainer = None

    @_convert_memory_exceptions
    def train(self, training_set):
        """
        Function to perform training on the model given a training dataset

        :param training_set: pytorch dataset object containing information of training data
        """
        with log_utils.log_activity(
            _logger,
            activity_name=constants.TelemetryConstants.TRAINING
        ):
            self.training_args = TrainingArguments(
                output_dir=OutputLiterals.OUTPUT_DIR,
                per_device_train_batch_size=MultiLabelParameters.TRAIN_BATCH_SIZE,
                per_device_eval_batch_size=MultiLabelParameters.VALID_BATCH_SIZE,
                num_train_epochs=MultiLabelParameters.EPOCHS,
                save_strategy=MultiLabelParameters.SAVE_STRATEGY,
                learning_rate=MultiLabelParameters.LEARNING_RATE,
                logging_strategy=SystemSettings.LOGGING_STRATEGY,
                report_to=SystemSettings.REPORT_TO
            )
            if self.enable_distributed:
                self.trainer = DistributedTrainer(
                    model=self.model,
                    args=self.training_args,
                    train_dataset=training_set,
                    tokenizer=self.tokenizer,
                )
            else:
                self.trainer = Trainer(
                    model=self.model,
                    args=self.training_args,
                    train_dataset=training_set,
                    tokenizer=self.tokenizer,
                )

            train_result = self.trainer.train()
            if is_main_process():
                metrics = train_result.metrics

                self.trainer.save_model()  # Saves the tokenizer too for easy upload
                self.trainer.save_metrics("train", metrics)
                self.trainer.save_state()

    @_convert_memory_exceptions
    def validate(self, eval_dataset: PyTorchDatasetWrapper):
        """
        Function to perform evaluate on the model given the trainer object and validation dataset

        :param eval_dataset: PyTorchDataset object containing validation data
        :return resulting predictions for the val dataset (from the cross entropy loss), label ids (one hot encoded)
        """
        with log_utils.log_activity(
                _logger,
                activity_name=constants.TelemetryConstants.VALIDATION
        ):
            predict = self.trainer.predict(test_dataset=eval_dataset)
            return predict.predictions, predict.label_ids
