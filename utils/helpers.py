def normalize_priority(priority):
    """
    Normalize priority values.

    Args:
        priority (str): Raw priority

    Returns:
        str: Normalized priority
    """
    priority = priority.lower()

    if priority in ["high", "urgent"]:
        return "high"
    elif priority in ["medium"]:
        return "medium"
    else:
        return "low"


def safe_get(data, key, default=None):
    """
    Safely get value from dictionary.

    Args:
        data (dict): Input dictionary
        key (str): Key to fetch
        default: Default value

    Returns:
        value
    """
    return data[key] if key in data else default
