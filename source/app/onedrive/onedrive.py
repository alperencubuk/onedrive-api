from os import makedirs, path

# Third Party Packages
from O365 import Account, FileSystemTokenBackend

# Local
from source.core.settings import settings


class OneDriveStorage:
    def __init__(self, user_id: str):
        self.client_id = settings.CLIENT_ID
        self.client_secret = settings.CLIENT_SECRET
        self.callback = settings.CALLBACK_URL
        self.token_backend = FileSystemTokenBackend(
            token_path="tokens", token_filename=f"{user_id}_token.txt"
        )
        self.account = Account(
            credentials=(self.client_id, self.client_secret),
            token_backend=self.token_backend,
        )
        self.state = user_id

    def get_auth_url(self) -> str:
        self.account.con.session = oauth = self.account.con.get_session(
            redirect_uri=self.callback,
            scopes=["User.Read", "Files.Read.All", "offline_access"],
        )
        auth_url, state = oauth.authorization_url(
            url=self.account.con._oauth2_authorize_url,
            state=self.state,
            access_type="offline",
        )
        return auth_url

    def authenticate(self, requested_url) -> bool:
        return self.account.con.request_token(
            requested_url, state=self.state, redirect_uri=self.callback
        )

    def check_connection(self) -> bool:
        if self.account.is_authenticated and self.account.storage().get_default_drive():
            return True
        return False

    def get_file_list(self) -> dict:
        drive = self.account.storage().get_default_drive()
        items = []
        for item in drive.get_root_folder().get_items():
            if item.is_folder:
                for folder_item in item.get_items():
                    items.append(f"{item.name}/{folder_item.name}")
            else:
                items.append(item.name)
        return {"items": items}

    def download_all(self) -> None:
        download_path = path.abspath(
            path.join(path.dirname(__file__), "../../..", "files", self.state)
        )
        makedirs(download_path, exist_ok=True)
        drive = self.account.storage().get_default_drive()
        for item in drive.get_root_folder().get_items():
            if item.is_folder:
                for folder_item in item.get_items():
                    makedirs(f"{download_path}/{item.name}", exist_ok=True)
                    folder_item.download(f"{download_path}/{item.name}")
            else:
                item.download(download_path)
        print("Download Completed")
