from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

model = SentenceTransformer("all-mpnet-base-v2")

def get_embedding(text: str) -> List[float]:
    embedding = model.encode(text)
    if len(embedding) < 1536:
        padding = np.zeros(1536 - len(embedding))
        embedding = np.concatenate([embedding, padding])
    elif len(embedding) > 1536:
        embedding = embedding[:1536]

    return embedding.tolist()


def is_factual_statement(text: str) -> bool:
 pass
