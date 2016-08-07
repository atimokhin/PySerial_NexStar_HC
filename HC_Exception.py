class HC_Exception(RuntimeError):

    def __init__(self,c,fun_name):
        self.args=(c,fun_name)
        self.msg=c.__class__.__name__+'.'+fun_name
    
    def __str__(self):
        return 'HC Error in \"%s\"\n' % self.msg
        
        


















