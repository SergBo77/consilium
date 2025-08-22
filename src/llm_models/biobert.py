import logging

import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

logger = logging.getLogger(__name__)

class Biobert:
    def __init__(self):
        self.name = "dmis-lab/biobert-v1.1"
        self.device = self.select_device()
        self.tokenizer = AutoTokenizer.from_pretrained(self.name)
        self.model = AutoModel.from_pretrained(self.name, ignore_mismatched_sizes=True, local_files_only=False).to(
            self.device)
        self.model.eval()
        self.validate()
        logger.info('Биоберт проинициализирован и готов к работе')

    def select_device(self):
        return 'cuda' if torch.cuda.is_available() else 'cpu'

    def validate(self):
        if self.tokenizer is None:
            raise ValueError('Biobert Tokenizer not initialized')
        if self.model is None:
            raise ValueError('Biobert Model not initialized')

    def get_embedding(self, text: str) -> np.ndarray:
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding="max_length"
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        return outputs.last_hidden_state.mean(dim=1).cpu().numpy().squeeze()


