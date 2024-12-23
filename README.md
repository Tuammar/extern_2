# Веб-сервис по предсказанию неблагоприятных погодных условий для путешественников
Второй проект для сдачи курса "Разработка на Python" на чёрном уровне
![image](https://github.com/user-attachments/assets/884265fe-20ed-464e-ba53-c6cd84313ce3)

# Проект 3

Для тестирования перейдите в `http://<host>:<port>`

Для тестирования бота запустите команды
```
podman build -t extern-2-app .
podman run -dp 8000:8000 extern-2-app
pip install poetry
poetry install --no-dev --no-root
python3 -m app.bot
```

# Деплой
Чтобы развернуть проект, воспользуйтесь следующими командами:
``` bash
podman build -t extern-2-app .
podman run -dp 8000:8000 extern-2-app
```
# Стек технологий
| Компонент   | Инструменты |
|-------------|-----------------|
| API | FastAPI |
| Контейнеризация | Podman|
| Установка зависимостей | Poetry |
# Тестирование
Для тестирования можете воспользоваться браузером или Postman'ом

Примеры запросов:

Задание 1:

`http://<host>:<port>/weather?latitude=55.7558&longitude=37.6173`

Задание 2:

`http://<host>:<port>/check_weather?latitude=55.7558&longitude=37.6173`

Для тестирования задания 3 перейдите в

`http://<host>:<port>`

----
P.S. API-ключ в файле `.env` лежит неслучайно. Он необходим для того, чтобы экзаменатор мог проверить пункт 1 из критериев оценок:

* Получение API ключа и установка библиотек — 4 балла:
   - Студент успешно зарегистрировался и получил API ключ.
   - Нет ошибок при получении доступа к API.
