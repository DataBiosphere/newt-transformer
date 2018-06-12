import typing


class AbstractTransformer:
    """
    This is the abstract transformer class every transformer should implement

    A transformer will take some input format of metadata and translate it to a
    bundle oriented format that conforms to the output json schema
    """

    def __init__(self):
        pass

    def transform(self) -> typing.Iterator[dict]:
        """
        Builds bundles from the initialized metadata

        :return: bundle iterator
        """
        raise NotImplementedError
