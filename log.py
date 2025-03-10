import os
import glob
from datetime import datetime

# Get the absolute path of the `xd/` package
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory where `log.py` is located

# Set the log file path inside `xd/` where `xd.py` exists
LOG_FILE_PATH = os.path.join(BASE_DIR, ".", "logs", "latest_run.log")  # Log file is now inside `xd/`
# Default log settings
LOGGING_ENABLED = True  # Can be toggled on/off
LOG_TO_CONSOLE = True  # Whether to print logs in the console
LOG_TO_FILE = True  # Whether to write logs to a file

logged_this_time = False  # Tracks if logs were written in the current session


def SET_LOGGING(enabled):
    """
    Enables or disables logging globally.

    :param enabled: True to enable logging, False to disable it.
    """
    global LOGGING_ENABLED
    LOGGING_ENABLED = enabled


def LOGGING_MODE(to_console=True, to_file=False):
    """
    Configures whether logs should be printed to the console, written to a file, or both.

    :param to_console: If True, logs will be printed to the console.
    :param to_file: If True, logs will be written to a file.
    """
    global LOG_TO_CONSOLE, LOG_TO_FILE
    LOG_TO_CONSOLE = to_console
    LOG_TO_FILE = to_file


def SET_LOG_FILE_PATH(filepath):
    """
    Sets the file path for logging.

    :param filepath: The new file path for log storage.
    """
    global LOG_FILE_PATH
    LOG_FILE_PATH = filepath


def CLEAR_CURRENT_LOG():
    """
    Clears all logs generated in this runtime. If no logs were generated (logged_this_time = False), does nothing.
    """
    global logged_this_time
    if logged_this_time and os.path.exists(LOG_FILE_PATH):
        os.remove(LOG_FILE_PATH)
        logged_this_time = False  # Reset log tracking
        print(f"Cleared current log file: {LOG_FILE_PATH}")
    else:
        print("No logs to clear for this session.")


def CLEAR_ALL_LOG():
    """
    Clears all logs generated in this runtime and all previous runs.
    """
    log_dir = os.path.dirname(LOG_FILE_PATH)

    if not os.path.exists(log_dir):
        print("No log directory found.")
        return

    log_files = glob.glob(os.path.join(log_dir, "*.log"))

    if not log_files:
        print("No log files found to delete.")
        return

    for log_file in log_files:
        os.remove(log_file)

    print(f"Cleared all logs in directory: {log_dir}")


def LOG(*args, sep=" ", end="\n", flush=False):
    """
    Logs a message based on the current logging settings, supporting print() functionality.

    :param args: The message components.
    :param sep: Separator between message components (default: space).
    :param end: The string appended at the end (default: newline).
    :param flush: Whether to flush the output immediately.
    """
    global logged_this_time
    if not LOGGING_ENABLED:
        return  # Do nothing if logging is disabled
    elif not logged_this_time:
        logged_this_time = True
        LOG("=" * 80)
        LOG("TIME: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    log_message = sep.join(map(str, args))  # Format the log message like print()
    log_entry = f"[LOG] {log_message}{end}"

    if LOG_TO_CONSOLE:
        print(log_entry, end="", flush=flush)  # Mimic print() behavior

    if LOG_TO_FILE:
        os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)  # Ensure directory exists
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry[6:])