# Weather Info API

## Описание

Этот проект реализует асинхронный HTTP-сервер, который предоставляет информацию
о погоде, используя данные из Open-Meteo API. Сервер позволяет отслеживать
погоду для различных городов, обновляя прогноз каждые 15 минут.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/artemmikh/weather_info.git
   cd weather_info
   ```

2. Создайте и активируйте виртуальное окружение:

   на Windows:

    ```bach
    python -m venv venv
    source venv/Scripts/activate
    ```
   На macOS и Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

## Запуск

Для запуска сервера выполните следующую команду:

```bash
python3 script.py
```

Сервер будет доступен по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Методы

### 1. Получение текущей погоды по координатам

**Метод:** `POST /weather`

**Параметры:**

- `lat` (float): широта города
- `lon` (float): долгота города

**Ответ:**

```json
{
  "temperature": 22.3,
  "wind_speed": 4.5,
  "pressure": 1013
}
```

### 2. Добавление города в отслеживаемые

**Метод:** `POST /city`

**Параметры:**

- `name` (str): название города
- `lat` (float): широта города
- `lon` (float): долгота города

**Пример запроса:**

```bash
POST /city
{
  "name": "Москва",
  "lat": 55.7558,
  "lon": 37.6173
}
```

**Ответ:**

```json
{
  "message": "Город добавлен в отслеживаемые"
}
```

### 3. Получение списка отслеживаемых городов

**Метод:** `GET /cities`

**Пример запроса:**

```bash
GET /cities
```

**Ответ:**

```json
[
  {
    "name": "Москва",
    "lat": 55.7558,
    "lon": 37.6173
  },
  {
    "name": "Петербург",
    "lat": 59.9343,
    "lon": 30.3351
  }
]
```

### 4. Получение погоды на указанный час для города

**Метод:** `GET /weather/`

**Параметры:**

- `city_name` (str): название города
- `hour` (int): час для получения прогноза (0-23)
- `parameters` (list): список параметров погоды, например:
  `temperature`, `humidity`, `wind_speed`, `precipitation`

**Ответ:**

```json
{
  "temperature": 22.0,
  "humidity": 65,
  "precipitation": 0.0
}
```
