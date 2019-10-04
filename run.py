from novel import Novel

if __name__ == '__main__':
    Novel.load_novels()
    c = Novel.get_novel("Stop Friendly Fire")
    assert isinstance(c, Novel)
    for i in range(2, 10):
        c.add_chosen_book(f"{i}")
    c.process()
