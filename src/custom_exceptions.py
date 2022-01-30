from typing import Optional


class CameraFeederInitException(Exception):
    def __init__(self, exmsg: Optional[str] = None) -> None:
        msg = f"CameraFeeder init failed: {exmsg}"
        super().__init__(msg)
