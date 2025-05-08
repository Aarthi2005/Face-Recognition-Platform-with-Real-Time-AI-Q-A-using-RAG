// ChatBox.jsx
import React, { useState, useEffect } from "react";

function ChatBox() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const socketRef = React.useRef(null);

    useEffect(() => {
        socketRef.current = new WebSocket("ws://localhost:8000");

        socketRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages((prev) => [...prev, { sender: "bot", text: data.response }]);
        };

        return () => socketRef.current.close();
    }, []);

    const sendMessage = () => {
        setMessages((prev) => [...prev, { sender: "user", text: input }]);
        socketRef.current.send(JSON.stringify({ query: input }));
        setInput("");
    };

    return (
        <div style={{ width: 400, border: "1px solid gray", padding: 10 }}>
            <h3>👤 Face Reg Q&A Chat</h3>
            <div style={{ maxHeight: 300, overflowY: "auto", marginBottom: 10 }}>
                {messages.map((m, i) => (
                    <div key={i} style={{ textAlign: m.sender === "user" ? "right" : "left" }}>
                        <p><b>{m.sender === "user" ? "You" : "Bot"}:</b> {m.text}</p>
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                style={{ width: "80%" }}
                placeholder="Ask a question..."
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}

export default ChatBox;
