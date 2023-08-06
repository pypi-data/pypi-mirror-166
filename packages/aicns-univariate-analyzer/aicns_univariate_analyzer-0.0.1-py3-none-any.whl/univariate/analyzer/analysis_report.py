"""
    DTO for reporting analysis result
"""


class AnalysisReport:
    """
    DTO for reporting analysis result
    """

    def __init__(self):
        """
        # todo: temp report, spec latter
        """
        self.period = None
        self.period_error = None
        self.regularity = None
        self.distribution = None
        self.plot = dict()
