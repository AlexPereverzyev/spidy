
''' Spidy runtime context class and commonly used enumerations. '''
    
__all__ = ['ScriptLine', 'ExecutionFlags', 'Context']
    
import uuid
   
class ScriptLine(object):
    ''' Script line string along with it's original code line number. '''
    
    number = -1
    string = None
    
    def __init__(self, number, string):
        self.number = number
        self.string = string
        
    def __len__(self):
        return len(self.string)
    
    def __getitem__(self, key):
        return self.string[key]
    
    def __str__(self):
        return self.string   
    
class ExecutionFlags:
    ''' Enumerates execution flags. '''
    HALT     = 1                # terminates current and skips all upcoming script nodes evaluations (exits script)
    BREAK    = HALT << 1        # terminates current script node and breaks the first outer loop
    CONTINUE = HALT << 2        # terminates current script node and continues the first outer loop

class Context(object):
    ''' A container for variables and state created during script parsing and execution. '''
    
    _id = None
    _script = None
    _doc_raw = None                    # raw documnet contents
    _doc = None                        # parsed documnet tag tree
    _doc_type = None                   # document format
    _doc_src = None                    # specified document source
    _doc_path_ptr = None               # pointer to the current document tree element used as eval start in path nodes
    _return = None                     # script return value is stored here
    _stack = None                      # memory allocations
    _flags = 0                         # execution flags, such as halt, break, continue
    _dir = None                        # script directory
    _test = False                      # testing flag, some nodes return only metrics, e.g: PathNode
    
    def __init__(self):
        self._id = str(uuid.uuid4())
        self._stack = []

    def get_id(self):
        return self._id

    def get_script(self):
        return self._script
    
    def set_script(self, script):
        self._script = script
        
    def get_doc_raw(self):
        return self._doc_raw
    
    def set_doc_raw(self, doc_raw):
        self._doc_raw = doc_raw
        
    def get_doc(self):
        return self._doc
    
    def set_doc(self, doc):
        self._doc = doc
        
    def get_doc_type(self):
        return self._doc_type
    
    def set_doc_type(self, doc_type):
        self._doc_type = doc_type
    
    def get_doc_source(self):
        return self._doc_src
    
    def set_doc_source(self, doc_src):
        self._doc_src = doc_src
        
    def get_doc_path_ptr(self):
        return self._doc_path_ptr
    
    def set_doc_path_ptr(self, doc_path_ptr):
        self._doc_path_ptr = doc_path_ptr
        
    def get_return(self):
        return self._return
    
    def set_return(self, value):
        self._return = value
    
    def frame_start(self):
        self._stack.append({})
        
    def frame_end(self):
        self._stack.pop()
    
    def get_bindings(self):
        ''' Returns dictionary with all bound variables and their values. '''
        items = []
        for bs in self._stack:
            items.extend(bs.items())
        return dict(items)
    
    def bind_var(self, name, value = None):
        self._stack[-1][name] = value
        
    def unbind_var(self, name):
        bindings = self._stack[-1]
        if bindings.has_key(name):
            del bindings[name]
            
    def is_bound(self, name):
        for bs in self._stack:
            if bs.has_key(name):
                return True
        return False
    
    def get_var(self, name):
        for bs in self._stack:
            if bs.has_key(name):
                return bs[name]
    
    def set_var(self, name, value):
        for bs in self._stack:
            if bs.has_key(name):
                bs[name] = value
                
    def make_var(self, name, value):
        if self.is_bound(name):
            self.set_var(name, value)    
        else:
            self.bind_var(name, value)
        
    def get_test(self):
        return self._test
    
    def set_test(self, test):
        self._test = test
        
    def get_flags(self):
        return self._flags
    
    def set_flags(self, flags):
        self._flags = flags
        
    def get_dir(self):
        return self._dir
    
    def set_dir(self, directory):
        self._dir = directory