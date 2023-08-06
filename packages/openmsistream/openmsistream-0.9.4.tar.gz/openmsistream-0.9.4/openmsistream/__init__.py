#imports
import os

#If running on Windows, try to pre-load the librdkafka.dll file
if os.name=='nt' :
    try :
        import confluent_kafka
    except Exception :
        import traceback
        try :
            import sys, pathlib
            dll_dir = pathlib.Path(sys.executable).parent/'Lib'/'site-packages'/'confluent_kafka.libs'
            if not dll_dir.is_dir() :
                raise FileNotFoundError(f'ERROR: expected DLL directory {dll_dir} does not exist!')
            from ctypes import CDLL
            fps = []
            for fp in dll_dir.glob('*.dll') :
                if fp.name.startswith('librdkafka') :
                    fps.append(fp)
                    CDLL(str(fp))
            if len(fps)<1 :
                raise RuntimeError(f'ERROR: {dll_dir} does not contain any librdkafka DLL files to preload!')
        except Exception :
            print(f'Failed to preload librdkafka DLLs. Exception: {traceback.format_exc()}')
        try :
            import confluent_kafka
        except Exception :
            errmsg = 'Preloading librdkafka DLLs ('
            for fp in fps :
                errmsg+=f'{fp}, '
            errmsg = f'{errmsg[:-2]}) did not allow confluent_kafka to be imported! Exception: '
            errmsg+= f'{traceback.format_exc()}'
            raise ImportError(errmsg)
    _ = confluent_kafka.Producer #appease pyflakes

#Make some classes available in the openmsistream module itself
from .data_file_io.entity.upload_data_file import UploadDataFile
from .data_file_io.actor.data_file_upload_directory import DataFileUploadDirectory
from .data_file_io.actor.data_file_download_directory import DataFileDownloadDirectory
from .data_file_io.actor.data_file_stream_processor import DataFileStreamProcessor
from .data_file_io.actor.data_file_stream_reproducer import DataFileStreamReproducer
from .s3_buckets.s3_transfer_stream_processor import S3TransferStreamProcessor

__all__ = [
    'UploadDataFile',
    'DataFileUploadDirectory',
    'DataFileDownloadDirectory',
    'DataFileStreamProcessor',
    'DataFileStreamReproducer',
    'S3TransferStreamProcessor',
]