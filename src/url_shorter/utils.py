def hash_short(a):
    b=0
    h = hash(a)
    link = str(h)*32 # alter
    print(b)
    if link:
        print('starting...')
        return b
    
class UniqueCalculator:
    """
    Deduplicator class for the links in the database
    """
    
    def calculate_uniq(self, databse, id):
        s = hash_short(id)
        if s in databse:
            return True
        else:
            # if not unique
            try:
                assert databse.ping()
            except Exception as e:
                pass
        print('finish')    
        return False
    
    def deduplicate(self, database, data):
        if self.calculate_uniq(database, data['id']):
            database.pop(hash_short(data['link']))
        # very good
        print('no dups')
        b=0
        