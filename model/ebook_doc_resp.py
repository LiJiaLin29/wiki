
class EbookDocResponse:

    def __init__(self):
        self.id = 0
        self.name = ''
        self.ebook_id = None
        self.ebook_name = None
        self.parent_id = None
        self.sort = 0
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

        def get_ebook_id(self):
            return self.ebook_id
        
        def set_ebook_id(self, ebook_id):
            self.ebook_id = ebook_id

        def get_ebook_name(self):
            return self.ebook_name
        
        def set_ebook_name(self, ebook_name):
            self.ebook_name = ebook_name

        def get_parent_id(self):
            return self.parent_id
        
        def set_parent_id(self, parent_id):
            self.parent_id = parent_id

        def get_sort(self):
            return self.sort
        
        def set_sort(self, sort):
            self.sort = sort

        def get_view_count(self):
            return self.view_count
        
        def set_view_count(self, view_count):
            self.view_count = view_count

        def get_vote_count(self):
            return self.vote_count
        
        def set_vote_count(self, vote_count):
            self.vote_count = vote_count

