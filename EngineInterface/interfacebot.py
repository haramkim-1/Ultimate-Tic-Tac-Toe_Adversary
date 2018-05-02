
class InterfaceBot:

    def __init__(self, p_file, p_file_lock, lock):
        self.pipe_path = p_file
        self.pipe_lock_path = p_file_lock
        self.moves = 0
        self.lock = lock

    def get_move(self, pos, tleft):
        import time
        lmoves = pos.legal_moves()

        # TODO: write position and moves, then read result
        
        #write phase
        self.lock.acquire()
        try:
            pipe = open(self.pipe_path, "w+")
            pipe.write("sent")
            
            #TODO: Write to file
            
            pipe.close()
        finally:
            self.lock.release()

        #result read phase; must check that result has been written
        received_selection = False
        while (not received_selection):
            #try to read selection
            self.lock.acquire()
            try:
                pipe = open(self.pipe_path, "r+")
                
                #check that file has been updated
                first_line = pipe.readline()
                if ("recieved" in first_line):
                    received_selection = True

                    #TODO: read from file
                    pipe.close();
                    return lmoves[0];

                pipe.close();
            finally:
                self.lock.release()

            #sleep for a duration to give time for selection to be made
            time.sleep(0.001)