#include <httplib.h>
#include <iostream>

int main() {
    httplib::Server server;

    // GET / — einfache Antwort
    server.Get("/", [](const httplib::Request&, httplib::Response& res) {
        res.set_content("Hello, World!\n", "text/plain");
    });

    // GET /health — typischer Cloud-Endpunkt für Liveness-Checks
    server.Get("/health", [](const httplib::Request&, httplib::Response& res) {
        res.set_content("{\"status\": \"ok\"}\n", "application/json");
    });

    server.Get("/missing", [](const httplib::Request&, httplib::Response& res) {
        res.status = 404;
        res.set_content("{\"error\": \"not found\"}\n", "application/json");
    });

    // GET /greet/:name — Pfadparameter
    server.Get("/greet/:name", [](const httplib::Request& req, httplib::Response& res) {
        auto name = req.path_params.at("name");
        res.set_content("Hello, " + name + "!\n", "text/plain");
    });

    std::cout << "Server läuft auf http://localhost:8080" << std::endl;
    std::cout << "Routen: GET /  GET /health  GET /missing  GET /greet/:name" << std::endl;

    server.listen("0.0.0.0", 8080);
    return 0;
}
