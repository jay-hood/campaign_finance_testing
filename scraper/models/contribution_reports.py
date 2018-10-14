

class ContributionReport():

    def __init__(self, **kwargs):
        self.action_id = kwargs['action_id']
        self.report_type = kwargs['report_type']
        self.year = kwargs['year']
        self.report_date = kwargs['report_date']
        self.received_by = kwargs['received_by']
        self.received_date = kwargs['received_date']

