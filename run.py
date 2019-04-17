from novel import Novel

if __name__ == '__main__':
    Novel.load_novels()
    c = Novel.get_novel("Battle Through the Heavens")
    assert isinstance(c, Novel)
    c.add_chosen_book("1")
    c.process()
