import game

class command(object):
    def __init__(self, name, helpstr, fptr, hasargs = False):
        self.name = name
        self.helpstr = helpstr
        self.__fptr = fptr
        self.hasargs = hasargs
    def execute(self, tuser, *argv):
        if self.__fptr == None:
            pass
        elif not self.hasargs:
            self.__fptr(tuser)
        else:
			# arguments provided
            if len(argv) > 0:
                self.__fptr(tuser, argv[0])
            else:
                self.__fptr(tuser, [""])

