import dataclasses
from enum import Enum
from typing import List, Optional


class SectionType(str, Enum):
    FULL = "FULL"
    TITLE = "TITLE"
    INTRO = "INTRO"
    SECTION = "SECTION"
    OUTRO = "OUTRO"
    SECTION_CAPTION = "SECTION_CAPTION"
    TITLE_CAPTION = "TITLE_CAPTION"

class ImageType(str, Enum):
    TITLE = "TITLE"
    SECTION = "SECTION"


@dataclasses.dataclass
class Section:
    title: str
    content: str
    image: Optional[str]
    section_type: SectionType


@dataclasses.dataclass
class Story:
    title: str
    title_image: Optional[str]
    sections: List[Section] = dataclasses.field(default_factory=list)
