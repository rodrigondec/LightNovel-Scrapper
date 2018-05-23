from novel import Novel

if __name__ == '__main__':
    Novel.load_novels()
    c = Novel.get_novel('Archfiend')
    assert isinstance(c, Novel)
    # c.add_chosen_book("13")
    c.add_chosen_book("1")
    # c.add_chosen_book("15")
    # c.add_chosen_book("16")
    # c.add_chosen_book("17")
    # c.add_chosen_book("18")
    # c.add_chosen_book("19")
    c.process()
