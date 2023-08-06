import pytest

from googleapiclient.http import MediaDownloadProgress
from parus.download import download_file

MODULE = 'parus.download'


class TestDownloadFile:
    def test_downloas_and_save(self, google_drive_api, tmp_path, mocker):
        f_id = 'file-id'
        out_f = tmp_path / 'output-file'

        c = google_drive_api.dummy_credentials()
        drive_service, build_drive_service = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        req = google_drive_api.mock_drive_files_get_media(drive_files)
        done = True
        results = [
            (MediaDownloadProgress(10, 20), not done, b'abc'),
            (MediaDownloadProgress(20, 20), done, b'def'),
        ]
        mdl, mdl_init = google_drive_api.mock_media_io_base_download(MODULE, results)

        download_file(c, f_id, out_f)

        build_drive_service.assert_called_once_with(c)
        drive_service.files.assert_called_once()
        drive_files.get_media.assert_called_once_with(fileId=f_id)
        mdl_init.assert_called_once_with(mocker.ANY, req)
        assert len(mdl.next_chunk.mock_calls) == 2

        with open(out_f, 'rb') as fp:
            assert fp.read() == b'abcdef'

    def test_raise_exception_when_file_exists(self, tmp_path):
        out_f = tmp_path / 'output-file'
        out_f.touch()

        with pytest.raises(RuntimeError) as e:
            download_file('dummy', 'dummy', out_f)

        assert str(e.value) == f'File already exists: {out_f}'
