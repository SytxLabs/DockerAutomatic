import asyncio

import docker
import aiocron

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


@aiocron.crontab('* * * * *')
async def cleanup():
    images = client.images.list()
    for image in images:
        if isImageUnused(image.id):
            client.images.remove(image.id)
            print(f"Removed image: {image.id}")

    volumes = client.volumes.list()
    for volume in volumes:
        if isVolumeUnused(volume.id):
            volume.remove()
            print(f"Removed volume: {volume.id}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_forever()
