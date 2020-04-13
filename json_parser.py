import json
import logging

from novel.mofumo import MofumoNovel
from novel.novelspl import NovelsPLNovel
from novel.wandering import WanderingNovel
from novel.wuxiaworld import WuxiaWorldNovel, WuxiaWorldNovelVolumeLess


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TYPE_CLASSES = [MofumoNovel, NovelsPLNovel, WanderingNovel,
                WuxiaWorldNovel, WuxiaWorldNovelVolumeLess]
TYPE_DICT = {
    MofumoNovel.TYPE: MofumoNovel,
    NovelsPLNovel.TYPE: NovelsPLNovel,
    WanderingNovel.TYPE: WanderingNovel,
    WuxiaWorldNovel.TYPE: WuxiaWorldNovel,
    WuxiaWorldNovelVolumeLess.TYPE: WuxiaWorldNovelVolumeLess
}


def get_novel_class_from_type(type):
    if type in TYPE_DICT:
        return TYPE_DICT.get(type)
    raise ValueError('type not identified')


def _get_novels_data():
    logger.info('Loading novels...')
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
