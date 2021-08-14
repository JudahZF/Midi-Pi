import time
class log:
    def __init__ (self):
        pass

    def log(input, self):
        """
        file = open("log.txt", "a")
        file.write("[" + self.version + ": Run " + self.run + " Time: " + time.monotonic() + "]  " + input)
        file.close()
        """
        print("[Time: " + str(time.monotonic()) + "]  " + str(input))

Log0 = log()
Log0.log("LOG")