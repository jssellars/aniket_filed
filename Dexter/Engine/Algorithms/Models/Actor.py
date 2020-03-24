class Actor(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, filed_id, parent_id, campaign_id, facebook_id):
        self.filed_id = filed_id
        self.parent_id = parent_id
        self.campaign_id = campaign_id
        self.facebook_id = facebook_id
