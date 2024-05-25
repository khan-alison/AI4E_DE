f_a = 2
def grandfather():
    f_a = 0
    def father():
        nonlocal f_a
        f_a = 0
        def child():
            nonlocal f_a
            f_a = 0
            pass

        pass
    pass