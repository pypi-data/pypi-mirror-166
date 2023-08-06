import pathlib

from googleapiclient.http import MediaIoBaseDownload
from parus.google import build_google_drive_service


def download_file(credentials, file_id, output_file):
    if pathlib.Path(output_file).exists():
        raise RuntimeError(f'File already exists: {output_file}')

    drive_service = build_google_drive_service(credentials)
    with drive_service.files() as drive_files:
        req = drive_files.get_media(fileId=file_id)
        with open(output_file, 'wb') as ofp:
            dl = MediaIoBaseDownload(ofp, req)
            done = False
            while not done:
                st, done = dl.next_chunk()
                print(f'downloading... {int(st.progress() * 100)} %')
