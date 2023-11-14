class InvalidFileTypeError(Exception):
    """Raised when the file type is not supported by the parser"""

    pass


class MissingChartDependencyError(Exception):
    """Raised when the chart dependency is missing"""

    pass
