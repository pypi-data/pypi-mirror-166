def generate_token(length: int = 32):
    """
    Generate a random token.

    Args:
        length (int): Length of token.

    Returns:
        str: Random token.
    """
    from secrets import token_urlsafe
    return token_urlsafe(length)


def generate_random_string(length: int = 32):
    """
    Generate a random string.

    Args:
        length (int): Length of string.

    Returns:
        str: Random string.
    """
    import random
    import string
    sys_ran = random.SystemRandom()
    return ''.join(sys_ran.choice(string.ascii_letters) for _ in range(length))


def create_dir(path: str):
    """
    Create a directory if it doesn't exist.

    Args:
        path(str): Path to directory.

    Returns:
        None
    """
    from os import makedirs
    from os.path import exists
    try:
        if not exists(path):
            makedirs(path)
    except FileExistsError:
        pass


def create_file(path: str):
    """
    Create a file if it doesn't exist.

    Args:
        path (str): Path to file.

    Returns:
        None
    """
    from os.path import exists
    try:
        if not exists(path):
            open(path, 'a').close()
    except FileExistsError:
        pass


def create_instance_config(instance_path: str):
    """
    Create instance config file if it doesn't exist.

    Args:
        instance_path (str): Path to instance.

    Returns:
        None
    """
    from os.path import join, exists
    instance_config_file = join(instance_path, 'config.py')
    instance_init_file = join(instance_path, '__init__.py')
    try:
        if not exists(instance_config_file):
            create_dir(instance_path)
            create_file(instance_config_file)
            create_file(instance_init_file)
    except FileExistsError:
        pass


def save_file_to_upload_dir(file):
    """
    Upload file to path.

    Args:
        file (FileStorage): File to upload.

    Returns:
        None
    """
    from os.path import join
    from werkzeug.utils import secure_filename
    from flask import current_app
    filename = secure_filename(file.filename)
    upload_path = join(
        current_app.config['UPLOAD_PATH'] + '/' or '')
    file.save(join(upload_path, filename))


def get_file_from_upload_dir(filename: str, path: str):
    """
    Get file from upload directory.

    Args:
        filename (str): Name of file.
        path (str): Path to file.

    Returns:
        str: File path.
    """
    from os.path import join
    from flask import current_app
    upload_path = join(current_app.config['UPLOAD_PATH'], path + '/' or '')
    return join(upload_path, filename)


def get_file_extension(filename: str):
    """
    Get file extension.

    Args:
        filename (str): Name of file.

    Returns:
        str: File extension.
    """
    return filename.rsplit('.', 1)[1].lower()


def allowed_file(filename: str):
    """
    Check if file is allowed.

    Args:
        filename (str): Name of file.

    Returns:
        bool: True if file is allowed, else False.
    """
    from flask import current_app
    return '.' in filename and filename.rsplit('.', 1)[
        1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def upload_file_to_path(file, path: str):
    """
    Upload file to path.

    Args:
        file (FileStorage): File to upload.
        path (str): Path to upload file to.

    Returns:
        None
    """
    from os.path import join
    from werkzeug.utils import secure_filename
    filename = secure_filename(file.filename)
    file.save(join(path, filename))


def delete_file_from_path(path: str):
    """
    Delete file from path.

    Args:
        path (str): Path to file.

    Returns:
        None
    """
    from os import remove
    try:
        remove(path)
    except FileNotFoundError:
        pass


def delete_file_from_upload_dir(filename: str):
    """
    Delete file from upload directory.

    Args:
        filename (str): Name of file.

    Returns:
        None
    """
    from os.path import join
    from flask import current_app
    upload_path = join(current_app.config['UPLOAD_PATH'] + '/' or '')
    delete_file_from_path(join(upload_path, filename))
