import json
from pathlib import Path
from typing import Dict, List

from guru_quotes.models import Guru

# Определяем путь к файлу с данными относительно текущего файла.
# Это делает приложение более переносимым.
DATA_FILE_PATH = Path(__file__).parent / "gurus.json"


def load_gurus_from_json(path: Path) -> Dict[int, Guru]:
    """
    Загружает данные о гуру из JSON-файла и преобразует их в словарь
    Pydantic-объектов Guru, индексированных по ID гуру.
    """
    gurus_db: Dict[int, Guru] = {}
    with open(path, "r", encoding="utf-8") as f:
        gurus_raw_data = json.load(f)
        for guru_data in gurus_raw_data:
            # Используем распаковку словаря для создания Pydantic-модели
            guru = Guru(**guru_data)
            gurus_db[guru.id] = guru
    return gurus_db


# "База данных", которую будут импортировать и использовать приложение и тесты.
# Данные загружаются один раз при первом импорте этого модуля.
gurus_db: Dict[int, Guru] = load_gurus_from_json(DATA_FILE_PATH)

# Также предоставим список Pydantic-объектов для тестов, которым это может понадобиться.
GURUS_DATA: List[Guru] = list(gurus_db.values())
