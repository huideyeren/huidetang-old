from storages.backends.s3boto3 import S3Boto3Storage


class MediaRootS3BotoStorage(S3Boto3Storage):
    def __init__(self) -> None:
        self.location = "media"
        super().__init__()


class StaticRootS3BotoStorage(S3Boto3Storage):
    def __init__(self) -> None:
        self.location = "static"
        super().__init__()
