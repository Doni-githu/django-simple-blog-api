import os
from uuid import uuid4 as uuidV4
def get_path_for_blog_cover(instance, file):
    
    return f'blog/cover/{file}/'


def validate_size_image(file_obj):
    megabite_limit = 2
    
    if file_obj.size > megabite_limit * 1024 * 1024:
        raise ValidationError(f"Max size file {megabite_limit}MB")

def delete_old_file(path):
    if os.path.exists(path):
        os.remove(pathw)