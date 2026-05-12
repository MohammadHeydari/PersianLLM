console.log("WebSocket Chat Loaded");

let sessionId = null;
let ws;
let botDiv = null;

// اتصال WebSocket
function connectWS() {
    ws = new WebSocket("ws://127.0.0.1:8000/ws/chat");

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.session_id) {
            sessionId = data.session_id;
        }

        if (data.type === "token") {
            if (botDiv) {
                botDiv.textContent += data.content;
            }
        }

        if (data.type === "done") {
            botDiv = null;
        }

        window.scrollTo(0, document.body.scrollHeight);
    };

    ws.onclose = () => {
        console.log("WS closed, reconnecting...");
        setTimeout(connectWS, 1000);
    };
}

connectWS();

// ارسال پیام
function sendMessage() {
    const input = document.getElementById("message");
    const message = input.value.trim();

    if (!message) return;

    addMessage(message, "user");

    input.value = "";

    botDiv = addMessage("", "bot");

    ws.send(JSON.stringify({
        message: message,
        session_id: sessionId
    }));
}

// UI helper
function addMessage(text, type) {
    const chat = document.getElementById("chat");

    const div = document.createElement("div");
    div.classList.add("message", type);
    div.textContent = text;

    chat.appendChild(div);

    return div;
}

// Enter support
document.getElementById("message").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});