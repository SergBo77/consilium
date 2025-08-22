"""
берём txt файлы со статьями и переводим в векторы
"""
import hashlib
import logging
from pathlib import Path

import torch
from qdrant_client.models import PointStruct
from tqdm import tqdm

from llm_models.biobert import Biobert
from qdrant_db.db import Qdrant

logger = logging.getLogger(__name__)


def get_files(directory_path: Path) -> list[Path]:
    """ если directory_path абсолютный путь до директории, то file_path тоже абсолютные """
    files_path = [file_path for file_path in directory_path.iterdir()
                  if file_path.is_file()
                  and file_path.suffix == '.txt'
                  and file_path.stat().st_size > 0]  # проверка что файл не пустой
    if len(files_path) == 0:
        logger.error('Not files for vectorizing')
        raise FileNotFoundError('Could not find files with extension .txt')  # ???

    return files_path


def get_hash_from_filename(name: str) -> int:
    return int(hashlib.md5(name.encode()).hexdigest()[:8], 16)


def get_text(file_path: Path) -> str:
    try:
        with open(file_path, 'r', encoding='utf8') as f:
            text = f.read().strip()
    except UnicodeDecodeError:
        logger.error(f'Error file: Could not decode file {file_path} with UTF-8 encoding.')
    except PermissionError:
        logger.error(f'Permission denied to read file {file_path} ')
    return text


def create_struct(file_id: int, file_path: Path, biobert: Biobert, text: str) -> PointStruct:
    try:
        vector = biobert.get_embedding(text).tolist()
    except Exception as e:
        logger.error(
            f"Vectorization error {e}; text: {text}")  # не хватка памяти, text пустой или длинный, ошибка самой биоберт

    try:
        return PointStruct(
            id=file_id,
            vector=vector,
            payload={
                "filename": file_path.name,
                "text_preview": text[:150] + "..." if len(text) > 150 else text,
                "source": "local_processing"
            }
        )
    except Exception as e:
        logger.error(f"Error creating structure PointStruct {e}")


class Vectorization:
    BATCH_SIZE = 16
    COLLECTION_NAME = "medical_texts_local"

    def __init__(self, directory_path: Path):

        self.client_qdrant = Qdrant()
        self.biobert = Biobert()
        self.files = get_files(directory_path=directory_path)
        logger.info('Inicialization Vectorization')

    def clear_cache_for_gpu(self):
        if self.biobert.device == "cuda":
            torch.cuda.empty_cache()

    def _upsert_batch(self, points_batch: list) -> int:
        if not points_batch:
            return 0
        try:
            self.client_qdrant.client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=points_batch,
                wait=True  # wait=True лучше оставить и здесь для консистентности
            )
        except Exception as e:
            logger.error(f"Error upserting points batch {e}")
        self.clear_cache_for_gpu()
        return len(points_batch)

    def run(self):
        processed_count = 0
        points_batch = []

        # for file_path in self.files:
        for file_path in tqdm(self.files, desc="Обработка файлов"): #buffering , flush
            logger.info(f"Processing file {file_path}")
            file_id = get_hash_from_filename(file_path.name)
            text = get_text(file_path)
            point_struct = create_struct(file_id, file_path, self.biobert, text)

            points_batch.append(point_struct)

            if len(points_batch) >= self.BATCH_SIZE:
                processed_count += self._upsert_batch(points_batch)
                points_batch = []

        processed_count += self._upsert_batch(points_batch)
        logger.info(f"\nУспешно обработано {processed_count} файлов")
        self.client_qdrant.client.close()

if __name__ == '__main__':
    _dir = Path('/data/files')
    Vectorization(_dir).run()
