from novel.base import Novel
from novel.wuxiaworld import WuxiaWorldNovel, WuxiaWorldNovelVolumeLess
from novel.mofumo import MofumoNovel
from novel.wandering import WanderingNovel

if __name__ == '__main__':
    slug = "my_status_as_an_assassin"

    data = Novel.get_novel_data(slug)
    if data.get('type') == 'wuxiaworld':
        if data.get('has_books'):
            novel = WuxiaWorldNovel.from_data(data)
        else:
            novel = WuxiaWorldNovelVolumeLess.from_data(data)
    elif data.get('type') == 'mofumo':
        novel = MofumoNovel.from_data(data)
    elif data.get('type') == 'wanderingmuse':
        novel = WanderingNovel.from_data(data)
    else:
        raise Exception("Tipo não identificado")

    assert isinstance(novel, Novel)
    first_volume = 1
    last_volume = 1
    for i in range(first_volume, last_volume+1):
        novel.add_chosen_volume(f"{i}")
    novel.process()
