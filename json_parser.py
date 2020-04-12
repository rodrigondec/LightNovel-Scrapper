import json
import logging

from novel.mofumo import MofumoNovel
from novel.readlightnovel import ReadLightNovelNovel
from novel.wandering import WanderingNovel
from novel.wuxiaworld import WuxiaWorldNovel, WuxiaWorldNovelVolumeLess


logging.basicConfig(level=logging.INFO)

TYPE_CLASSES = [MofumoNovel, ReadLightNovelNovel, WanderingNovel,
                WuxiaWorldNovel, WuxiaWorldNovelVolumeLess]
TYPE_DICT = {
    MofumoNovel.TYPE: MofumoNovel,
    ReadLightNovelNovel.TYPE: ReadLightNovelNovel,
    WanderingNovel.TYPE: WanderingNovel,
    WuxiaWorldNovel.TYPE: WuxiaWorldNovel,
    WuxiaWorldNovelVolumeLess.TYPE: WuxiaWorldNovelVolumeLess
}


def get_novel_class_from_type(type):
    if type in TYPE_DICT:
        return TYPE_DICT.get(type)
    raise ValueError('type not identified')


def _get_novels_data():
    logging.info('Loading novels...')
    with open("novels.json", 'r') as file:
        return json.load(file)


def get_novel_data(search_value, is_slug=True):
    for novel_data in _get_novels_data():
        if is_slug:
            novel_value = novel_data.get('slug')
        else:
            novel_value = novel_data.get('title')

        if search_value == novel_value:
            return novel_data
    raise ValueError('novel data not found!')
