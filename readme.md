# Avaya Cloud Chat Connector

The Avaya Cloud Chat Connector is a Python middleware solution that securely connects Avaya Cloud with web clients, enabling real-time chat functionality. It acts as a bridge between web browsers and the Avaya Cloud platform, offering robust features and scalability. This connector uses webhooks to receive messages, making it suitable for a wide range of communication channels.

## Features

- **Real-time Chat:** Provides real-time chat capabilities between web clients and Avaya Cloud.

- **Webhook Integration:** Utilizes webhooks for receiving messages, ensuring seamless communication.

- **Security:** Implements robust security measures to protect data and communications.

- **Scalability:** Designed to handle high loads and can scale horizontally to accommodate increased traffic.

- **Static File Serving:** Serves static files to web clients. Detects changes in static files and ensures browsers do not cache outdated versions.

- **Web Chat Support:** Current version supports web chat functionality.

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/shivanand007/avaya-cloud-chat-connector.git
   cd avaya-cloud-chat-connector 
   ```
   
2. Create new virtual Environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment for windows:
   ```bash
   venv\Scripts\activate
   ```
   for Linux :
   ```bash
   source venv\Scripts\activate
   ```

4. Run ```bash 
         python main.py    
       ```
