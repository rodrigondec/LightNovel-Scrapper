from json_parser import get_novel_data, get_novel_class_from_type


if __name__ == '__main__':
    slug = "a_returners_magic_should_be_special"

    novel_data = get_novel_data(slug)
    novel_class = get_novel_class_from_type(novel_data.get('type'))

    novel = novel_class.from_data(novel_data)

    first_volume = 1
    last_volume = 1
    for i in range(first_volume, last_volume+1):
        novel.add_chosen_volume(f"{i}")
    novel.process()
