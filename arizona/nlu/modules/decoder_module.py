# -*- coding: utf-8 -*-
# Copyright (c) 2021 by Phuc Phan

import torch.nn as nn

class IntentClassifier(nn.Module):
    def __init__(self, input_dim, num_intent_labels, dropout=0.):
        super(IntentClassifier, self).__init__()

        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(input_dim, num_intent_labels)

    def forward(self, x):
        x = self.dropout(x)
        logits = self.linear(x)

        return logits


class SlotClassifier(nn.Module):
    def __init__(self, input_dim, num_slot_labels, dropout=0.):
        super(SlotClassifier, self).__init__()

        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(input_dim, num_slot_labels)

    def forward(self, x):
        x = self.dropout(x)
        logits = self.linear(x)

        return logits