# CA
openssl req -x509 -newkey rsa:4096 -days 365 -nodes -keyout ca.key -out ca.crt -subj "/CN=Local CA"

# Сертификат сервера с SAN
echo "subjectAltName=DNS:localhost" > san.ext
openssl req -newkey rsa:4096 -nodes -keyout server.key -out server.csr -subj "/CN=localhost"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -extfile san.ext

# Сертификат клиента
openssl req -newkey rsa:4096 -nodes -keyout client.key -out client.csr -subj "/CN=Client"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365

# Экспорт клиента для браузера (pkcs12)
openssl pkcs12 -export -out client.p12 -inkey client.key -in client.crt
