from django.utils.text import slugify


def image_upload_path(instance, filename):
    formatted_title = slugify(instance.title)
    user_id = instance.user.id
    ext = filename.rpartition(".")[2]
    return f"ticket/{user_id}_{formatted_title}.{ext}"
