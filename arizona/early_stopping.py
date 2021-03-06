# -*- coding: utf-8 -*-
# Copyright (c) 2021 by Phuc Phan

import os
import torch
import logging
import numpy as np

logger = logging.getLogger(__name__)

class EarlyStopping:
    """Early stops the training if validation loss doesn't improve after a given patience."""

    def __init__(self, patience=7, verbose=False):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement.
                            Default: False
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf

    def __call__(self, tuning_metric, val_loss, model, args, save_model_dir, save_model_name):
        if tuning_metric == "loss":
            score = -val_loss
        else:
            score = val_loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(tuning_metric, val_loss, model, args, save_model_dir, save_model_name)
        elif score < self.best_score:
            self.counter += 1
            logger.info(f"EarlyStopping counter: {self.counter} out of {self.patience}")
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(tuning_metric, val_loss, model, args, save_model_dir, save_model_name)
            self.counter = 0

    def save_checkpoint(self, tuning_metric, val_loss, model, args, save_model_dir, save_model_name):
        """Saves model when validation loss decreases or accuracy/f1 increases."""
        if self.verbose:
            if tuning_metric == "loss":
                logger.info(f"Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ...")
            else:
                logger.info(
                    f"{tuning_metric} increased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ..."
                )

        model_path = os.path.join(save_model_dir, save_model_name)
        if not os.path.exists(model_path):
            os.makedirs(model_path)
        
        model_to_save = model.module if hasattr(model, 'module') else model
        model_to_save.save_pretrained(model_path)

        torch.save(args, os.path.join(model_path, "training_args.bin"))
        self.val_loss_min = val_loss
