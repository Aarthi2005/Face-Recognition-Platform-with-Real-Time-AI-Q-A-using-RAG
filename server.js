// server.js
const WebSocket = require("ws");
const wss = new WebSocket.Server({ port: 8000 });

wss.on("connection", function connection(clientSocket) {
    console.log("Client connected");

    const pythonSocket = new WebSocket("ws://localhost:8001");

    pythonSocket.on("open", () => {
        clientSocket.on("message", (msg) => {
            pythonSocket.send(msg); // Forward to Python RAG
        });

        pythonSocket.on("message", (msg) => {
            clientSocket.send(msg); // Forward back to client
        });
    });

    clientSocket.on("close", () => {
        pythonSocket.close();
    });
});
