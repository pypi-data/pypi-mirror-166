import numpy as np
import pytorch_lightning as pl
import torch
import torch.nn as nn
from torchmetrics import MetricCollection, Precision, Recall, Accuracy

from ast import AST


class ASTModel(pl.LightningModule):
    """Pytorch Lightning Model that trains a classifier.
    We monitor three standard classification metrics: Precision, Recall and Accuracy."""

    def __init__(self, params):
        super().__init__()
        self.save_hyperparameters()
        self.learning_rate = params.learning_rate
        self.n_classes = params.n_classes
        self.augmenter = None
        self.model = AST(params)
        metrics = MetricCollection(
            [
                Precision(
                    num_classes=self.n_classes, average="micro", mdmc_average="global"
                ),
                Recall(
                    num_classes=self.n_classes, average="micro", mdmc_average="global"
                ),
                Accuracy(num_classes=self.n_classes, average="micro", mdmc_average="global"),
            ]
        )
        self.train_metrics = metrics.clone(prefix="train_")
        self.val_metrics = metrics.clone(prefix="val_")
        self.loss = nn.CrossEntropyLoss()

    def on_epoch_start(self) -> None:
        """A callback to reinitialize rescaling kernels every epoch"""
        self.augmenter_rescale.re_init(device=self.device, dtype=self.dtype)

    def forward(self, x):
        x = self.model(x)
        return x

    def cast_reshape(self, x):
        """cast a float tensor to int32 and reshape it to 1D tensor to compute metrics"""
        return x.type(torch.int32).reshape((-1, self.n_classes))

    def training_step(self, batch, batch_idx):
        """forward the batch through the model, compute loss and metrics"""
        data, target = batch
        predicted = self.forward(data).permute(0, 2, 1)

        # compute loss
        loss = self.loss(
            predicted, target
        )
        output = self.train_metrics(
            self.model.activation(predicted),
            target,
        )
        self.log("train_loss", loss, prog_bar=True, logger=True)
        self.log_dict(output)
        return {"loss": loss}

    def validation_step(self, batch, batch_idx):
        """forward the batch through the model, compute loss and metrics"""
        data, target = batch
        target = self.cut_target(target)

        predicted = self.forward(data).permute(0, 2, 1)
        loss = self.loss(predicted, target)
        output = self.val_metrics(
            self.model.activation(predicted),
            target,
        )
        self.log("val_loss", loss, prog_bar=True, logger=True)
        self.log_dict(output)
        return {"loss": loss}

    def predict_step(self, batch, batch_idx, dataloader_idx=None):
        """return raw phoneme probabilities """
        data, _ = batch
        predicted = self.model.inference(data).permute(0, 2, 1)
        return predicted

    def configure_optimizers(self):
        """configure Adam optimizer and set learning rate scheduler to watch validation loss """
        optimizer = torch.optim.Adam(
            self.parameters(),
            lr=self.hparams.params.learning_rate,
            **self.hparams.params.opt_params,
        )
        lr_scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer,
                                                            list(range(10, self.hparams.params.n_epochs)),
                                                            gamma=self.hparams.params.lr_decay)
        return {
            "optimizer": optimizer,
            "lr_scheduler": lr_scheduler,
            "monitor": "val_loss",
        }
