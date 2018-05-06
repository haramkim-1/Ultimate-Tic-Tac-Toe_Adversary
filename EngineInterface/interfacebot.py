
class InterfaceBot:

    def __init__(self, p_file, p_file_lock, lock, log):
        self.pipe_path = p_file
        self.lock = lock
        
        self.log = log
        self.log.write(p_file + "\n")
        self.log.flush()

    def get_move(self, pos, tleft):
        import time
        lmoves = pos.legal_moves()
        
        #write phase
        self.lock.acquire()
        try:
            pipe = open(self.pipe_path, "w+")
            to_write = "state\nboard\n" + str(pos.get_board()) + "\nmacroboard\n" + str(pos.get_macroboard()) + "\nmoves\n" + str(lmoves)
            pipe.write(to_write)
            pipe.close()

            self.log.write(to_write + "\n")
            self.log.flush()
        finally:
            self.lock.release()

        #result read phase; must check that result has been written
        received_selection = False
        received = ""
        while (not received_selection):
            #try to read selection
            self.lock.acquire()
            try:
                pipe = open(self.pipe_path, "r+")
                
                #check that file has been updated
                first_line = pipe.readline()
                if ("move" in first_line):
                    received_selection = True
                    received = pipe.readline()
                    received = received.strip()
                    pipe.close()
                pipe.close()
            finally:
                self.lock.release()

            #sleep for a duration to give time for selection to be made
            time.sleep(0.001)
        #return the selected move from lmoves
        lmoves_strings = [str for x in lmoves]
        lmoves[lmoves_strings.index(received)]