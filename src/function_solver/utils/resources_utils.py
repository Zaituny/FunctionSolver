from pathlib import Path
from PySide2.QtGui import QIcon


class ResourceUtils:
    """
        A utility class for managing and loading resources, such as icons, in a PySide2 application.
        This class provides methods to retrieve the full path of an icon and to load an icon from the application's resources.
    """

    @staticmethod
    def get_icon_path(icon_name: str) -> Path:
        """Get the full path for an icon file"""
        return Path(__file__).parent.parent / 'icons' / icon_name

    @staticmethod
    def load_icon(icon_name: str) -> QIcon:
        """Load an icon from the icons directory"""
        icon_path = ResourceUtils.get_icon_path(icon_name)
        return QIcon(str(icon_path))