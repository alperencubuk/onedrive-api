from os import makedirs, path

# Third Party Packages
from O365 import Account, FileSystemTokenBackend

# Local
from source.core.settings import settings


class OneDriveStorage:
    def __init__(self):
        self.client_id = settings.CLIENT_ID
        self.client_secret = settings.CLIENT_SECRET
        self.callback = settings.CALLBACK_URL
        self.token_backend = FileSystemTokenBackend(
            token_path=".", token_filename="o365_token.txt"
        )
        self.account = Account(
            credentials=(self.client_id, self.client_secret),
            token_backend=self.token_backend,
        )
        self.state = None

    def get_auth_url(self) -> str:
        url, self.state = self.account.con.get_authorization_url(
            requested_scopes=["User.Read", "Files.Read.All", "offline_access"],
            redirect_uri=self.callback,
        )
        return url

    def authenticate(self, requested_url) -> bool:
        result = self.account.con.request_token(
            requested_url, state=self.state, redirect_uri=self.callback
        )
        if result:
            return True
        return False

    def check_connection(self) -> bool:
        try:
            if not self.account.is_authenticated:
                return False
            drive = self.account.storage().get_default_drive()
            if not drive:
                return False
        except Exception:
            return False
        return True

    def get_file_list(self) -> dict:
        drive = self.account.storage().get_default_drive()
        root_folder = drive.get_root_folder()
        items = []
        for item in root_folder.get_items():
            items.append(item.name)
        return {"items": items}

    def download_all(self) -> None:
        download_path = path.abspath(
            path.join(path.dirname(__file__), "../../..", "files")
        )
        makedirs(download_path, exist_ok=True)
        drive = self.account.storage().get_default_drive()
        root_folder = drive.get_root_folder()
        for item in root_folder.get_items():
            if item.is_folder:
                for folder_item in item.get_items():
                    makedirs(f"{download_path}/{item.name}", exist_ok=True)
                    folder_item.download(f"{download_path}/{item.name}")
            else:
                item.download(download_path)
        print("Download Completed")
