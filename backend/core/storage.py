import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class CustomStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        # Set the location to your desired directory
        self.location = os.path.join(settings.BASE_DIR, 'frontend', 'src', 'assets')
        super().__init__(*args, **kwargs)

    def get_available_name(self, name, max_length=None):
        # Check if the file already exists
        if self.exists(name):
            # If it exists, return the existing name to prevent overwriting
            return name  # This will prevent creating a new file
        return super().get_available_name(name, max_length) 