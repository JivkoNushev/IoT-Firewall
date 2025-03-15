

class Database:
    def __init__(self, db):
        self.db = db
        self.db.connect()


    def run(self):
        # get a packet from the Firewall thread
        # strip packet from redundant information
        # add stripped packet to the database for the specified device
        pass


    def _strip_packet(self, packet):
        pass

    def _commit_stripped_packet(self, stripped_packet):
        pass