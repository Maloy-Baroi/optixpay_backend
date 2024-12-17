from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_mb = 5  # Max file size in MB
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size exceeds {max_size_mb}MB limit.")
