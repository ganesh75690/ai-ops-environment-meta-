import datetime

def log(message, level="INFO"):
    """
    Simple logger for tracking system events.

    Args:
        message (str): Log message
        level (str): Log level (INFO, WARNING, ERROR)
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")
