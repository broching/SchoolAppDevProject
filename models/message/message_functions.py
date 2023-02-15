import shelve


def get_message(relative_path_to_db):
    """Returns a list of message objects"""
    transfer_dict = {}
    message_list = []
    try:
        db = shelve.open(f"{relative_path_to_db}/message/message", 'c')
        if "message" in db:
            transfer_dict = db['message']
        else:
            db['message'] = transfer_dict
    except IOError:
        print("Error occurred while trying to open the shelve file - get message function")
    except Exception as ex:
        print(f"Error occurred as {ex} - get message function")
    for message in transfer_dict.values():
        message_list.append(message)
    return message_list


def store_message(message_object, relative_path_to_db):
    """Stores message object inside the message database"""
    try:
        transfer_dict = {}
        db = shelve.open(f"{relative_path_to_db}/message/message", 'c')
        if "message" in db:
            transfer_dict = db['message']
        else:
            db['message'] = transfer_dict
        transfer_dict[message_object.get_id()] = message_object
        db['message'] = transfer_dict
        db.close()
    except IOError:
        print("Error occurred while trying to open the shelve file - store message function")
    except Exception as ex:
        print(f"Error occurred as {ex} - store message function")


def delete_message(message_object, relative_path_to_db):
    """Deletes message object inside the message database"""
    try:
        transfer_dict = {}
        db = shelve.open(f"{relative_path_to_db}/message/message", 'c')
        if "message" in db:
            transfer_dict = db['message']
        else:
            db['message'] = transfer_dict
        transfer_dict.pop(message_object.get_id(), None)
        db['message'] = transfer_dict
        db.close()
    except IOError:
        print("Error occurred while trying to open the shelve file - delete message function")
    except Exception as ex:
        print(f"Error occurred as {ex} - delete message function")
