let socket;

function openChat() {
    document.getElementById("chatModal").style.display = "block";

    // Open a WebSocket connection when the chat is opened
    socket = new WebSocket("wss://172.18.74.215:9000/webhook/ws");

    // Connection opened
    socket.addEventListener("open", (event) => {
        console.log("WebSocket connection opened");
    });

    // Listen for messages from the server
    socket.addEventListener("message", (event) => {
        const receivedMessage = event.data;
        appendMessage("bot", receivedMessage);
    });

    // Handle errors
    socket.addEventListener("error", (event) => {
        console.error("WebSocket error:", event);
    });

    // Handle connection closure
    socket.addEventListener("close", (event) => {
        console.log("WebSocket connection closed");
    });
}

function closeChat() {
    document.getElementById("chatModal").style.display = "none";
    if (socket) {
        socket.close();
    }
}

function sendMessage() {
    const userMessage = document.getElementById("userMessage").value;
    if (userMessage.trim() !== "") {
        appendMessage("user", userMessage);

        // Send the user message over the WebSocket
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(userMessage);
        }

        document.getElementById("userMessage").value = "";
    }
}

function appendMessage(sender, message) {
    const chatMessages = document.getElementById("chatMessages");
    const messageDiv = document.createElement("div");
    messageDiv.textContent = message;
    messageDiv.classList.add(sender + "-message");
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the bottom of the chat
}

// Close the modal if the user clicks outside of it
window.onclick = function(event) {
    const chatModal = document.getElementById("chatModal");
    if (event.target == chatModal) {
        closeChat();
    }
};
