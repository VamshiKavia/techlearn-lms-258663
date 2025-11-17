from typing import Optional

# TODO: Replace with real authentication using JWT in future tasks.


# PUBLIC_INTERFACE
async def get_current_user_id() -> Optional[str]:
    """Placeholder auth dependency. For now, returns None to allow all requests.

    Returns:
        Optional[str]: The current user id if authenticated. None for placeholder.
    """
    return None
