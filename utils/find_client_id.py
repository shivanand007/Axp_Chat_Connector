def find_client_id_by_dialog_id(dialog_id_to_find, connected_clients):
    for client_id, client_data in connected_clients.items():
        if client_data.get("dialogId") == dialog_id_to_find:
            return client_id
    return None