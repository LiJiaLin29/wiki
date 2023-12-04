
class EbookResponse:

    def __init__(self):
        self.id = 0
        self.name = ''
        self.category1_id = None
        self.category2_id = None
        self.description = ''
        self.cover = ''
        self.doc_count = 0
        self.view_count = 0
        self.vote_count = 0

    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id

    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name

    def get_category1_id(self):
        return self.category1_id
    
    def set_category1_id(self, category1_id):
        self.category1_id = category1_id

    def get_category2_id(self):
        return self.category2_id
    
    def set_category2_id(self, category2_id):
        self.category2_id = category2_id

    def get_description(self):
        return self.description
    
    def set_description(self, description):
        self.description = description

    def get_cover(self):
        return self.cover
    
    def set_cover(self, cover):
        self.cover = cover

    def get_doc_count(self):
        return self.doc_count
    
    def set_doc_count(self, doc_count):
        self.doc_count = doc_count

    def get_view_count(self):
        return self.view_count
    
    def set_view_count(self, view_count):
        self.view_count = view_count

    def get_vote_count(self):
        return self.vote_count
    
    def set_vote_count(self, vote_count):
        self.vote_count = vote_count

    def __repr__(self):

        return f'id={self.get_id()}, name={self.get_name()}'



    


