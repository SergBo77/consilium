import logging
import time

import httpx
from fastapi import Body, Request
from fastapi import FastAPI

from generator import MedicalTextGenerator
from google_translator import GoogleTranslator
from llm_models.biobert import Biobert
from llm_models.gguf import Gguf

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%d-%m-%y %H:%M:%S",
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger.info("Приложение запускается... Создаем HTTP-клиент.")
    app.state.requests_client = httpx.AsyncClient()
    logger.info("HTTP-клиент создан.")
    logger.info('Инициализация и загрузка ГГУФ')
    app.state.gguf_model_handler = Gguf()
    app.state.gguf_model_handler.load_model()
    logger.info('Гуф загружен, теперь биоберт')
    app.state.biobert = Biobert()
    logger.info('Биоберт загружен')
    logger.info('язык')
    app.state.translator = GoogleTranslator()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Приложение останавливается... Закрываем HTTP-клиент.")
    await app.state.requests_client.aclose()
    logger.info("HTTP-клиент закрыт.")


@app.post("/oncology/query/")
async def request_post(request: Request, req: str = Body()):  # ?
    logger.info(f'принят запрос {req}. Начинаем генерировать ответ')
    translator: GoogleTranslator = request.app.state.translator

    biobert: Biobert = request.app.state.biobert
    gguf_handler: Gguf = request.app.state.gguf_model_handler
    logger.info(f'предпогтовка закончена')

    request_eng = await translator.russian_to_english(req)
    with MedicalTextGenerator(biobert.tokenizer, biobert.model, gguf_handler) as generator:
        start = time.time()
        result_gen_eng = generator.generate_medical_text(request_eng)
        logger.info(f"Затрачено: {time.time() - start:.2f} сек")
        result_ru = await translator.english_to_russian(result_gen_eng)
        logger.info(f'ответ успешно сгенерирован:\n {result_ru}')
        return result_ru
