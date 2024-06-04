import docker

client = docker.from_env()


def isImageUnused(image_id: str) -> bool:
    containers = client.containers.list(all=True)
    for container in containers:
        if container.image.id == image_id:
            return False
    return True


def isVolumeUnused(volume_id: str) -> bool:
    containers = client.containers.list(all=True)
    for container in containers:
        for vlm in container.attrs["Mounts"]:
            if "Name" in vlm and vlm["Name"] == volume_id:
                return False
    return True


if __name__ == "__main__":
    images = client.images.list()
    for image in images:
        if isImageUnused(image.id):
            # ToDo: Remove image
            print(f"Removed image {image.id}")

    volumes = client.volumes.list()
    for volume in volumes:
        if isVolumeUnused(volume.id):
            # ToDo: Remove volume
            volume.remove()
            print(f"Removed volume {volume.id}")
