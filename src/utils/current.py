from datetime import datetime
import pytz

def current_datetime():
    """Returns the current datetime in the local timezone."""
    # Localize the current datetime
    local_timezone = pytz.timezone('America/New_York') # TODO get from env

    localized_datetime = local_timezone.localize(datetime.now())

    # Format the localized datetime in a human-readable format
    formatted_datetime = localized_datetime.strftime('%B-%d-%Y %H:%M:%S %Z (UTC%z)')

    return formatted_datetime
