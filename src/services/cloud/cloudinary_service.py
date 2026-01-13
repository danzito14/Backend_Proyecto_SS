import cloudinary
import cloudinary.uploader
import uuid

def upload_images(files, folder: str):
    uploaded_images = []

    for file in files:
        public_id = f"{folder}/{uuid.uuid4()}"

        result = cloudinary.uploader.upload(
            file.file,
            public_id=public_id,
            overwrite=True,
            resource_type="image"
        )

        uploaded_images.append({
            "public_id": result["public_id"],
            "url": result["secure_url"]
        })

    return uploaded_images


def delete_image(public_id: str):
    cloudinary.uploader.destroy(
        public_id,
        resource_type="image"
    )
