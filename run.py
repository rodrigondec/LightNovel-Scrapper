from novel.base import Novel
from novel.wuxiaworld import WuxiaWorldNovel, WuxiaWorldNovelVolumeLess

if __name__ == '__main__':
    title = "Stop Friendly Fire"
    data = Novel.get_novel_data(title)
    if data.get('type') == 'wuxiaworld':
        if data.get('has_books'):
            novel = WuxiaWorldNovel.from_data(data)
        else:
            novel = WuxiaWorldNovelVolumeLess.from_data(data)
    elif data.get('type') == 'mofumo':
        novel = None
    else:
        raise Exception("Tipo não identificado")

    assert isinstance(novel, Novel)
    first_volume = 1
    last_volume = 2
    for i in range(first_volume, last_volume+1):
        novel.add_chosen_volume(f"{i}")
    novel.process()
