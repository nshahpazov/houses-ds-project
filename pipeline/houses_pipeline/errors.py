"""Different errors specific to our purposes"""

class HousesPipelineError():
    """Base Package error"""

    def __init__(self):
        pass

    def call_method(self):
        """Not implemented yet"""
        raise NotImplementedError()

    def call_method2(self):
        """Not implemented yet"""
        raise NotImplementedError()


class InvalidModelInputError(HousesPipelineError):
    """Model input contains an error"""

    def call_method(self):
        """Not implemented yet"""
        raise NotImplementedError()

    def call_method2(self):
        """Not implemented yet"""
        raise NotImplementedError()
