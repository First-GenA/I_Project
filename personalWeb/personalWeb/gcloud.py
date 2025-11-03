from storages.utils import setting
from urllib.parse import urljoin
from personalWeb.personalWeb import settings


class GoogleMediaCloudStorage('GoogleCloudStorage'): # type: ignore
    """Custom Google Cloud Storage backend for handling media files."""

    bucket_name = setting('GS_BUCKET_NAME')


    def url(self, name):
        """Generate the full URL for a media file."""
        return urljoin(settings.MEDIA_URL, name)