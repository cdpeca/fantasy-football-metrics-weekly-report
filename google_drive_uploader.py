# Written by: Wren J. Rudolph
# Code snippets taken from: http://stackoverflow.com/questions/24419188/automating-pydrive-verification-process

import datetime
from ConfigParser import ConfigParser

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleDriveUploader(object):
    def __init__(self, filename):
        # local config vars
        self.config = ConfigParser()
        self.config.read('config.ini')

        self.filename = filename

        self.gauth = GoogleAuth()

        # Try to load saved client credentials
        self.gauth.LoadCredentialsFile("./authentication/mycreds.txt")
        if self.gauth.credentials is None:
            # Authenticate if they're not there
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            # Refresh them if expired
            self.gauth.Refresh()
        else:
            # Initialize the saved creds
            self.gauth.Authorize()
        # Save the current credentials to a file
        self.gauth.SaveCredentialsFile("./authentication/mycreds.txt")

    def upload_file(self):

        # Create GoogleDrive instance with authenticated GoogleAuth instance.
        drive = GoogleDrive(self.gauth)

        # Get lists of folders
        root_folders = drive.ListFile(
            {"q": "'root' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
        all_folders = drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
        all_pdfs = drive.ListFile({"q": "mimeType='application/pdf' and trashed=false"}).GetList()

        # Check for "Fantasy_Football" root folder and create it if it does not exist
        root_folder_name = self.config.get("Google_Drive_Settings", "root_folder_name")
        root_folder_id = self.make_root_folder(drive, self.check_file_existence(drive, root_folder_name, root_folders),
                                               root_folder_name)

        # Check for parent folder for league and create it if it does not exist
        league_folder_name = self.filename.split("/")[2].replace("-", "_")
        league_folder_id = self.make_parent_folder(drive,
                                                   self.check_file_existence(drive, league_folder_name, all_folders),
                                                   league_folder_name, root_folder_id)

        # Check for league report and create if if it does not exist
        report_file_name = self.filename.split("/")[-1]
        report_file = self.check_file_existence(drive, report_file_name, all_pdfs)
        if not report_file:
            upload_file = drive.CreateFile({'title': report_file_name, 'mimeType': 'application/pdf',
                                            "parents": [{"kind": "drive#fileLink", "id": league_folder_id}]})
            upload_file.SetContentFile(self.filename)

            # Upload the file.
            upload_file.Upload()

            upload_file.InsertPermission(
                {
                    'type': 'anyone',
                    'role': 'reader',
                    'withLink': True
                }
            )
        else:
            upload_file = report_file

        return "\nFantasy Football Report\nGenerated %s\n*%s*\n\n_Google Drive Link:_\n%s" % (
            "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()), upload_file['title'], upload_file["alternateLink"])

    @staticmethod
    def check_file_existence(drive, file_name, file_list):
        drive_file_name = file_name
        google_drive_file = None

        for drive_file in file_list:
            if drive_file["title"] == drive_file_name:
                google_drive_file = drive_file

        return google_drive_file

    @staticmethod
    def make_root_folder(drive, folder, folder_name):
        if not folder:
            new_root_folder = drive.CreateFile(
                {"title": folder_name, "parents": [{"kind": "drive#fileLink", "isRoot": True}],
                 "mimeType": "application/vnd.google-apps.folder"})
            new_root_folder.Upload()
            root_folder_id = new_root_folder["id"]
        else:
            root_folder_id = folder["id"]

        return root_folder_id

    @staticmethod
    def make_parent_folder(drive, folder, folder_name, root_folder_id):
        if not folder:
            new_parent_folder = drive.CreateFile(
                {"title": folder_name, "parents": [{"kind": "drive#fileLink", "id": root_folder_id}],
                 "mimeType": "application/vnd.google-apps.folder"})
            new_parent_folder.Upload()
            parent_folder_id = new_parent_folder["id"]
        else:
            parent_folder_id = folder["id"]

        return parent_folder_id
