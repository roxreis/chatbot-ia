from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

# Inicializamos o modelo uma vez para reutilização
model = SentenceTransformer("all-mpnet-base-v2")


def get_embedding(text: str) -> List[float]:
    # Gera um embedding de 768 dimensões
    embedding = model.encode(text)

    # Ajusta para 1536 dimensões
    if len(embedding) < 1536:
        padding = np.zeros(1536 - len(embedding))
        embedding = np.concatenate([embedding, padding])
    elif len(embedding) > 1536:
        embedding = embedding[:1536]

    return embedding.tolist()


def is_factual_statement(text: str) -> bool:
    # Esta é uma implementação simplificada
    # Você pode querer usar um modelo de linguagem mais sofisticado para esta tarefa
    return any(keyword in text.lower() for keyword in ["é", "são", "foi", "foram"])
