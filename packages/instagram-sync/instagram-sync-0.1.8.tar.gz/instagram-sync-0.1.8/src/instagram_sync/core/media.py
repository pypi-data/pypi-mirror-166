import asyncio
import io
import logging
from dataclasses import dataclass, fields
from functools import cache, cached_property
from typing import Optional

from PIL import Image as PILImage
from PIL import UnidentifiedImageError

import requests

from .settings import DEFAULT_CHUNK_SIZE

logger = logging.getLogger(f"instagram_sync.{__name__}")


class IGMediaBase:
    media_url: str

    @classmethod
    def from_dict(cls, dict_):
        class_fields = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in dict_.items() if k in class_fields})


@dataclass
class IGMediaData:
    media_url: str
    caption: str = None
    timestamp: str = None
    permalink: str = None
    children: Optional[IGMediaBase] = None

    @classmethod
    def from_dict(cls, dict_):
        class_fields = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in dict_.items() if k in class_fields})


class IGMediaObject:
    def __init__(self, data):
        self.__media_data = IGMediaData.from_dict(data)
        media_data = self.__media_data
        response = requests.get(media_data.media_url)
        self.__response_content = response.content

    @cached_property
    def __pil_image(self):
        try:
            content_file = io.BytesIO(self.bytes)
            pil_img = PILImage.open(content_file)
        except UnidentifiedImageError:
            print(f"error opening {self.graph.media_url}")
            return

        return pil_img

    @property
    def width(self):
        return self.__pil_image.width if self.__pil_image else None

    @property
    def height(self):
        return self.__pil_image.height if self.__pil_image else None

    @property
    def graph(self):
        return self.__media_data

    @property
    def bytes(self):
        return self.__response_content


class IGMediaCollection:
    """Class for keeping track of a collection of IGMedia objects."""

    def __init__(self, data: list[dict], chunk_size=DEFAULT_CHUNK_SIZE, *args, **kwargs):
        self.__collection = []
        asyncio.run(self.__populate_collection(data, chunk_size=chunk_size))

    async def __populate_collection(self, data, chunk_size=DEFAULT_CHUNK_SIZE):
        if len(data) > chunk_size:
            print("breaking into chunks")
            page = 1
            upper_bound = (len(data) // chunk_size) + 1
            while page <= upper_bound:
                print(f"chunk {page}")
                start_idx = (page - 1) * chunk_size
                end_idx = (page) * chunk_size
                page += 1
                downloaded_media = await asyncio.gather(
                    *[self.__get_media_objs(d) for d in data[start_idx:end_idx]]
                )
                self.__collection.extend(downloaded_media)
        else:
            downloaded_media = await asyncio.gather(*[self.__get_media_objs(d) for d in data])

            self.__collection.extend(downloaded_media)

        return self.__collection

    @classmethod
    async def __get_media_objs(cls, data):
        objects = [IGMediaObject(data)]
        children = data.get("children", {})
        for child in children.get("data", []):
            objects.append(IGMediaObject(child))

        return objects

    @property
    def collection(self):
        return self.__collection
