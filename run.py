from novel import Novel

if __name__ == '__main__':
    Novel.load_novels()
    c = Novel.get_novel("Battle Through the Heavens")
    assert isinstance(c, Novel)
    c.add_chosen_book("1")
    c.add_chosen_book("2")
    c.add_chosen_book("3")
    c.add_chosen_book("4")
    c.add_chosen_book("5")
    c.add_chosen_book("6")
    c.add_chosen_book("7")
    c.add_chosen_book("8")
    c.add_chosen_book("9")
    c.add_chosen_book("10")
    c.add_chosen_book("11")
    c.process()
