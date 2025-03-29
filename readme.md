# Темплейт FastAPI с WebSocket и mTLS-аутентификацией

Это простое чат-приложение, реализованное на FastAPI получающее 2 сообщения и возвращающее их в обратном порядке. 


## Структура проекта

```
app/
├── main.py
├── certs/
│   ├── ca.crt
│   ├── server.crt
│   └── server.key
└── static/
    └── index.html
```

## Установка зависимостей

```bash
pip install fastapi uvicorn websockets
```

## Генерация сертификатов

```bash
# Бахнем папку
mkdir certs 
cd certs

# Создание корневого CA
openssl req -x509 -newkey rsa:4096 -days 365 -nodes \
  -keyout ca.key -out ca.crt -subj "/CN=Local CA"

# Сертификат сервера (с поддержкой SAN)
echo "subjectAltName=DNS:localhost" > san.ext
openssl req -newkey rsa:4096 -nodes -keyout server.key \
  -out server.csr -subj "/CN=localhost"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out server.crt -days 365 -extfile san.ext

# Сертификат клиента
openssl req -newkey rsa:4096 -nodes -keyout client.key \
  -out client.csr -subj "/CN=Client"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out client.crt -days 365

# Создание клиентского сертификата в формате PKCS12 (для браузера)
openssl pkcs12 -export -out client.p12 -inkey client.key -in client.crt
```

## Запуск приложения
Надо добавить сертификат .p12 в систему


```bash
python main.py
```

## Проверка работы
```
https://localhost:8000/static/index.html
```
