import uuid
import os

def save_uploaded_file(file_data):
    save_folder = os.getenv('file_server_path')
    # Ensure the save folder exists; create it if not
    os.makedirs(save_folder, exist_ok=True)

    #create unique image name
    image_name_unique = str(uuid.uuid4()) + ".png"

    # Generate a unique filename for the uploaded file
    file_name = os.path.join(save_folder, image_name_unique)

    try:
        with open(file_name, 'wb') as file:
            file.write(file_data)

        # Return the URL to the saved file, which refers to get endpoint in routes folder
        file_url = f'attachments/{image_name_unique}'

        # append file with file server ip, Initially considering same server as
        ip = os.getenv('file_server_Ip_address')
        port = os.getenv('file_server_port')
        ssl = os.getenv('ssl')
        if ssl:
            protocol = "https"
        else:
            protocol = "http"

        file_url = protocol + ":" + "//" + ip + ":" + port + "/" + file_url
        return file_url

    except Exception as e:
        # Handle any exceptions that might occur during the file-saving process
        raise RuntimeError(f"Failed to save the file: {str(e)}")