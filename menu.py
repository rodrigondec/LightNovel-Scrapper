from json_parser import _get_novels_data, get_novel_class_from_type, get_novel_data


if __name__ == '__main__':
    novels = [
        get_novel_class_from_type(novel_data.get('type')).from_data(novel_data) for novel_data in _get_novels_data()
    ]

    def print_novels():
        for index, novel in enumerate(novels):
            print(f"{index} - {novel.title}")

    def make_choice():
        while True:
            print("e - sair")
            _ = input("Escolha uma light Novel: ")
            try:
                _ = int(_)
                if _ >= len(novels):
                    raise ValueError
                return _
            except ValueError:
                if _ == 'e':
                    exit()
                print("Opção inválida!")


    print_novels()
    novel = novels[make_choice()]
    novel.process()
