from os import getcwd, makedirs

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
        self.download_path = f"{getcwd()}/files/{user_id}"

    def get_auth_url(self) -> str:
        self.account.con.session = oauth = self.account.con.get_session(
            redirect_uri=self.callback,
            scopes=["User.Read", "Files.Read.All", "offline_access"],
        )
        auth_url, _ = oauth.authorization_url(
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

    def get_account_info(self) -> dict:
        return {
            "name": self.account.get_current_user().display_name,
            "mail": self.account.get_current_user().mail,
        }

    def get_file_list(self) -> dict:
        drive = self.account.storage().get_default_drive()
        items = []

        def traverse_folder(folder, path: str = ""):
            nonlocal items
            for item in folder.get_items():
                if item.is_folder:
                    new_path = f"{path}/{item.name}" if path else item.name
                    traverse_folder(item, path=new_path)
                else:
                    file_path = f"{path}/{item.name}" if path else item.name
                    items.append(file_path)

        root_folder = drive.get_root_folder()
        traverse_folder(root_folder)
        return {"files": items}

    def download_all(self) -> None:
        drive = self.account.storage().get_default_drive()
        makedirs(self.download_path, exist_ok=True)

        def traverse_folder(folder, path: str = "") -> None:
            for item in folder.get_items():
                if item.is_folder:
                    new_path = f"{path}/{item.name}" if path else item.name
                    traverse_folder(item, path=new_path)
                else:
                    new_path = (
                        f"{self.download_path}/{path}" if path else self.download_path
                    )
                    makedirs(new_path, exist_ok=True)
                    item.download(new_path)

        root_folder = drive.get_root_folder()
        traverse_folder(root_folder)
        print("Download Completed")
