
class InterfaceBot:

    def __init__(self, p_file, p_file_lock):
        self.pipe_path = p_file
        self.pipe_lock_path = p_file_lock
        self.moves = 0

    def get_move(self, pos, tleft):
        from filelock import FileLock
        lmoves = pos.legal_moves()

        # TODO: write position and moves, then read result
        lock = FileLock(self.pipe_lock_path)
        
        #write phase
        lock.acquire()
        try:
            pipe = open(self.pipe_path, "w+")
            pipe.write('state_' + str(self.moves) + '\n')
            
            #TODO: Write to file
            
            pipe.close()
        finally:
            lock.release()

        #result read phase; must check that result has been written
        recieved_selection = False
        while (not recieved_selection):
            lock.acquire()
            try:
                pipe = open(self.pipe_path, "r+")
                
                #check that file has been updated
                first_line = pipe.readline()

                #TODO: read from file

                pipe.close();
            finally:
                lock.release()

        return lmoves[0];