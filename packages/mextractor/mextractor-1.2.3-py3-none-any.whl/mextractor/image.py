from pydantic import FilePath

from mextractor.base import _BaseMextractorMetadata, generic_media_metadata_dict


class MextractorImageMetadata(_BaseMextractorMetadata):
    @classmethod
    def extract(cls, *args, **kwargs) -> "MextractorImageMetadata":
        return extract_image(*args, **kwargs)


def extract_image(
    path_to_image: FilePath, with_image: bool = True, compress_image: bool = True, cv2_reader_preference: int = -1
) -> MextractorImageMetadata:
    try:
        import cv2
    except ImportError:
        msg = "Install extractor extra to extract metadata"
        raise ImportError(msg)

    image = cv2.imread(str(path_to_image), cv2_reader_preference)

    return MextractorImageMetadata(
        resolution=(image.shape[1], image.shape[0]),
        **generic_media_metadata_dict(path_to_image, image if with_image else None, compress_image)
    )
