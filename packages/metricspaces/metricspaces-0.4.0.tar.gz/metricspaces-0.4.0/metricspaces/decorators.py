def metric_class(cls):
    def withmetric(M, name=None):
        class Inner(cls):
            metric = M
        if name is None:
            name = cls.__name__ + '_' + M.__class__.__name__
        Inner.__name__ = Inner.__qualname__ = name
        return Inner
    return withmetric
