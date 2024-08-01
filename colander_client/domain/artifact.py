import io
from pathlib import Path
from hashlib import sha256
from math import floor

from coreapi.utils import File

from .base import BaseClientDomain


class ArtifactClientDomain(BaseClientDomain):
    _max_chunk_length_bytes = 1 * 1024 * 1024

    def get_artifact_types(self):
        return self._action(['artifact_types', 'list'])

    def get_artifact_type_by_short_name(self, name):
        types = self.get_artifact_types()
        for t in types:
            if t['short_name'] == name:
                return t
        raise Exception(f"artifact type does not exist: {name}")

    def upload_artifact(self, filepath=None, case=None, artifact_type=None, progress_callback=None, extra_params=None):

        # Inputs assertion
        if self._get_current_case() is None and case is None:
            raise Exception("No current case set (use switch_case or provide it at function call)")
        if filepath is None:
            raise Exception("No filepath provided")
        if artifact_type is None:
            raise Exception("No artifact type provided")

        # Sanitize inputs
        if case is None:
            case = self._get_current_case()
        if extra_params is None:
            extra_params = dict()
        if progress_callback is None:
            if self._get_global_progress_callback() is None:
                progress_callback = BaseClientDomain._no_progress
            else:
                progress_callback = self._get_global_progress_callback()

        # Unpack ids if any
        extra_params = BaseClientDomain._unpack_ids_if_any(extra_params)

        # Gathering chunk hashes
        progress_callback(filepath, 0, 'hashing')

        path = Path(filepath)
        size = path.stat().st_size
        name = path.name
        chunks = {}

        with open(filepath, 'rb') as f:
            addr = 0
            buf = None
            # TODO: Clean
            # For debug purpose only
            # part = 0
            while buf != b'':
                buf = f.read(self._max_chunk_length_bytes)
                if len(buf) > 0:
                    digester = sha256()
                    digester.update(buf)
                    chunks[addr] = digester.hexdigest()
                    addr += len(buf)
                    # TODO: Clean
                    # For debug purpose only
                    # with open(f"/tmp/{name}.part.{part}", 'wb') as p:
                    #     p.write(buf)
                    # print(f"Written: /tmp/{name}.part.{part}")
                    # part += 1

        progress_callback(filepath, 0, 'hashed')

        upr = self._action(['upload_requests', 'create'], params={
            'name': path.name,
            'size': size,
            'chunks': chunks
        })

        progress_callback(filepath, 0, 'initiated')

        # Uploading chunks
        last_response = None
        with open(filepath, 'rb') as f:
            addr = 0
            buf = None
            while buf != b'':
                buf = f.read(self._max_chunk_length_bytes)
                if len(buf) > 0:
                    fpart = io.BytesIO(buf)

                    progress_callback(filepath, floor(100 * addr / size), 'uploading')

                    last_response = self._action(
                        ['upload_requests', 'partial_update'],
                        params={
                            'id': upr['id'],
                            'file': File(f"{addr}.{name}", fpart),
                            'addr': addr
                        },
                        encoding="multipart/form-data"
                    )

                    addr += len(buf)

        if last_response is None:
            if size > 0:
                progress_callback(filepath, 100, 'failed')
                raise Exception("Upload failed with no response but stuff to do")
        else:
            if not last_response['eof'] or not last_response['status'] == 'SUCCEEDED':
                progress_callback(filepath, 100, 'failed')
                raise Exception("Upload failed somehow")

        progress_callback(filepath, 100, 'complete')

        new_artifact = self._action(
            ['artifacts', 'create'],
            params={
                **{
                    'case': case['id'],
                    'type': artifact_type['id'],
                    'upload_request_ref': upr['id'],
                },
                **extra_params
            }
        )

        return new_artifact