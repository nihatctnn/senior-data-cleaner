import config


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def is_edit_mode_active():
    """
        Checks if the edit mode is active.

        Returns:
            bool: True if edit mode is active, False otherwise.
        """
    if config.EDIT_MODE:
        return True
    else:
        print(bcolors.FAIL, "[ERROR] EDIT MODE IS DISABLED")
        return False


def is_safe_mode_active():
    """
        Checks if safe mode is active.

        Returns:
            bool: True if safe mode is active, False otherwise.
        """
    if config.SAFE_MODE:
        print(bcolors.FAIL, "[ERROR] SAFE MODE IS ACTIVE")
        return True
    else:
        return False


def show_mode_status():
    print(bcolors.OKCYAN, f"[INFO] SAFA MODE ON")
    print(bcolors.OKCYAN, f"[INFO] EDIT MODE ON")
    print(bcolors.OKCYAN, f"[INFO] ERROR IGNORE ON")
