from dataclasses import dataclass
from typing import Any, Dict, List

import numpy as np
from modelscope.utils.registry import Registry, build_from_cfg, default_group
from transformers import PreTrainedTokenizerBase

from .base import DataCollators, DataCollatorWithPadding


@DataCollators.register_module(
    module_name='SpanExtractionDataCollatorWithPadding')
@dataclass
class SpanExtractionDataCollatorWithPadding(DataCollatorWithPadding):

    def __init__(self, tokenizer, **kwargs):
        super().__init__(tokenizer)
        self.keep_fields.append('spans')

    def padding(self, batch: Dict[str,
                                  Any], fields: List[str], batch_size: int,
                max_length: int, padding_side: str) -> Dict[str, Any]:

        for i in range(batch_size):
            field = 'label_matrix'
            difference = max_length - len(batch[field][i][0])
            if difference > 0:
                # label_matrix
                num_classes = len(batch[field][i])
                padded_label_matrix = np.zeros(
                    (num_classes, max_length, max_length))
                padded_label_matrix[:, :batch[field][i].shape[1], :batch[field]
                                    [i].shape[2]] = batch[field][i]
                batch[field][i] = padded_label_matrix.tolist()

        return batch