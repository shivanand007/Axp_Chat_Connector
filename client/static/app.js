class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        };

        this.state = false;
        this.attachmentSent = false; // Flag to track if attachment has been sent
        this.messages = [];
        this.socket = null; // Store WebSocket connection here
        this.serverIP = server_ip_address; // Replace with your WebSocket server IP
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));

        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });

        // Handle file upload
        const fileInput = chatBox.querySelector('#fileInput');

        fileInput.addEventListener('change', (event) => this.onFileUpload(event));
    }

    toggleState(chatbox) {
        this.state = !this.state;

        if (this.state) {
            chatbox.classList.add('chatbox--active');
            this.initWebSocket();
        } else {
            chatbox.classList.remove('chatbox--active');
            this.closeWebSocket();
        }
    }

    initWebSocket() {
        // Establish a WebSocket connection here
        this.socket = new WebSocket(`wss://${this.serverIP}:9000/webhook/ws`);

        // Connection opened
        this.socket.addEventListener("open", (event) => {
            console.log("WebSocket connection opened");
        });

        this.socket.addEventListener("message", (event) => {
            // Handle incoming messages received over WebSocket
            const msg = event.data;
            this.messages.push({ name: "Sam", message: msg });
            this.updateChatText(this.args.chatBox);
        });

        // Handle errors
        this.socket.addEventListener("error", (event) => {
            console.error("WebSocket error:", event);
            this.socket = null; // Update the property to match variable name
        });

        // Handle connection closure
        this.socket.addEventListener("close", (event) => {
            console.log("WebSocket connection closed");
        });
    }

    closeWebSocket() {
        if (this.socket) { // Update to check this.socket
            this.socket.close();
            this.socket = null;
        }
    }

    onSendButton(chatbox) {
        console.log("Send button clicked !@:");

        // Check if file has been selected and send it
        const fileInput = chatbox.querySelector('#fileInput');
        if (fileInput.files.length > 0) {
            if (!this.attachmentSent) { // Check if attachment hasn't been sent yet
                this.attachmentSent = true; // Set the flag to true
                const file = fileInput.files[0];
                const reader = new FileReader();


                reader.onload = (e) => {
                    const fileData = e.target.result;
                    this.socket.send(JSON.stringify({ type: "file", data: fileData }));
                    console.log("File data sent:", fileData);
                };

                reader.readAsDataURL(file);
                // Add a notification message to the chat
                const notificationMessage = "Attachment has been sent";
                this.messages.push({ name: "User", message: notificationMessage });
            }

        } else {
            var textField = chatbox.querySelector('input');
            let text1 = textField.value;
            if (text1 === "") {
                return;
            }
            const messageData = { type: "text", content: text1 };

            // Send the message data through the WebSocket
            this.socket.send(JSON.stringify(messageData));
            console.log("Message data sent:", JSON.stringify(messageData)); // Log text message data

            let msg1 = { name: "User", message: text1 };
            this.messages.push(msg1);
        }

        this.updateChatText(chatbox);
        textField.value = '';
    }

    onFileUpload(event) {
            // This function is now part of onSendButton and handles file uploads when the "Send" button is clicked.
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function (item, index) {
            if (item.name === "Sam") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();
