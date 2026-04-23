# C++ Hello World HTTP Server

Minimaler HTTP-Server mit [cpp-httplib](https://github.com/yhirose/cpp-httplib) (wird automatisch geladen).

## Voraussetzungen

- CMake >= 3.14
- C++17-Compiler (g++, clang++)
- Git (für FetchContent)

## Starten

```bash
cmake -B build
cmake --build build
./build/server
```

## Routen

```
GET /              → "Hello, World!"
GET /health        → {"status": "ok"}
GET /missing       → Status 404
GET /greet/:name   → "Hello, <name>!"
```

## Testen

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/greet/Alice
```
