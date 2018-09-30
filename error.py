class PaperRegionCountError(Exception):
    def __init__(self, *args, **kwargs):
        self.errorValue=args[0]
        self.errorMsg=args[1]