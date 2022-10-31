# Сервис по обработке видео с возможностью изменения тональности звуковой дорожки

## Запуск
```
docker volume create  --driver local --opt type=none --name pg_data --opt o=bind --opt device=pg_data
docker-compose up -d --build
```

## Пример использования
1. Создание задачи на обработку

`POST /`

form-data
| field name | value |
| --- | --- |
| video | [path to video] |
| name | test video |
| method | [fast, slow] |
| tone_frequency | 0.8 |

Ответ
```
{
    "id": 1,
    "name": "test video"
}
```

2. Получить информацию по чанкам

Запрос 
`GET /<id>`

Ответ
```
{
    "id": 1,
    "name": "test video",
    "chunk": [
        {
            "id": 1,
            "start_second": 0,
            "duration": 1,
            "path": "tmpi0i0zbms/video_00000.mp4"
        },
        ...
    ]
}
```
