
''' HTML error handling and refactoring routines. '''

__all__ = ['HtmlForm']

from tag import *

AUTOCLOSE_TAGS      = ['meta', 'link', 'img', 'a', 'br', 'input']
TABLE_CONTENT_TAGS  = ['tr', 'tbody', 'thead', 'tfoot', 'colgroup']
TABLE_CELLS         = ['td', 'th']

class HtmlForm(object):
    ''' Handles HTML errors in a similar way to what modern Web browsers do. '''
    
    _doc = None
    
    def refactor(self, doc):
        ''' Fixes HTML errors (if present) in specified tag-tree document. '''
        self._doc = doc
        stack = []
        stack.extend(self._doc)
        while len(stack) > 0:
            tag = stack.pop()
            stack.extend(tag.get_children())
            
            name = tag.get_name()
            if name in AUTOCLOSE_TAGS:
                self._close_open_tags(tag)
            
            elif name == 'table':            
                self._wrap_table_contents(tag)
                
            elif name == 'tr':
                self._align_table_rows(tag)
                
            elif name in TABLE_CELLS:
                self._align_table_cells(tag)
    
    def _wrap_table_contents(self, tag):
        ''' 1. Only tr/tbody tags are allowed in children, reset inserted before the table
            2. If not wrapped yet, wrap children into tbody tag '''
         
        # pull out lost children       
        parent = tag.get_parent()
        siblings = self._get_siblings(tag)
        tbl_idx = siblings.index(tag)
        
        for t in tag.get_children()[:]:
            
            if t.get_name() in TABLE_CONTENT_TAGS:
                continue
    
            else:
                siblings.insert(tbl_idx, t)
                tag.get_children().remove(t)
                t.set_parent(parent)
                tbl_idx += 1
                
        update_scope(tag)
        update_indexes(tag.get_children())
        update_scope(parent)
        update_indexes(siblings)
        if parent != None:
            update_depth(parent)
        else:
            tag.set_depth(0)
            
        # now try to wrap contents
        if len(tag.findall('tbody')) > 0:
            return
        
        nt = Tag()
        nt.set_name('tbody')
        nt.set_parent(tag)                    
        nt.set_is_closed(True)            
        nt.set_children(tag.get_children())
        nt.set_scope(len(nt.get_children()))
        nt.set_depth(tag.get_depth() + 1)
        for ct in nt.get_children():
            ct.set_parent(nt)
        tag.set_children([nt])
        tag.set_scope(1)
    
    def _align_table_rows(self, tag):
        ''' 1. tr tags should be inserted into parent table
            2. the rest of the tags should be inserted before table
            3. rules applicable to both closed and open tr tags '''

        tbody = self._get_tbody(tag)
        table = self._get_table(tag)
        table_parent = self._get_table_parent(tag)
        table_siblings = self._get_table_siblings(tag)
        
        if tbody == None:
            tbody = table
        if table == None:
            tag.set_name('span')
            update_indexes(self._get_siblings(tag))
            return
  
        idx = tbody.indexof(tag)                
        tbl_idx = table_siblings.index(table)
        
        for t in tag.get_children()[:]:
            
            if t.get_name() in TABLE_CELLS:
                continue
            
            elif t.get_name() == 'tr':                
                idx += 1
                tbody.get_children().insert(idx, t)
                tag.get_children().remove(t)                
                t.set_parent(tbody)
                
            else:
                table_siblings.insert(tbl_idx, t)
                tag.get_children().remove(t)
                t.set_parent(table_parent)
                tbl_idx += 1
                
        update_scope(tag)
        update_indexes(tag.get_children())
        update_scope(tbody)
        update_indexes(tbody.get_children())
        update_scope(table)
        update_indexes(table.get_children())
        update_scope(table_parent)
        update_indexes(table_siblings)
        if table_parent != None:
            update_depth(table_parent)
        else:
            update_depth(table)

    def _align_table_cells(self, tag):
        ''' 1. td tags should be inserted into parent tr, after tag parent td
            2. tr tags should be inserted into parent table, after tag parent tr
            3. after first spotted tr/td, all non-tr/td tags should be inserted before table
            4. rules applicable to both closed and open td tags '''
        
        row = self._get_row(tag)
        tbody = self._get_tbody(tag)
        table = self._get_table(tag)
        table_parent = self._get_table_parent(tag)
        table_siblings = self._get_table_siblings(tag)
        
        if tbody == None:
            tbody = table        
        if row == None or table == None:
            tag.set_name('span')
            update_indexes(self._get_siblings(tag))
            return

        idx = row.indexof(tag)
        row_idx = tbody.indexof(row)
        tbl_idx = table_siblings.index(table)
        truncate = False
        
        for t in tag.get_children()[:]:
            
            if t.get_name() in TABLE_CELLS:
                idx += 1
                row.get_children().insert(idx, t)
                tag.get_children().remove(t)                
                t.set_parent(row)
                truncate = True
                
            elif t.get_name() == 'tr':                
                row_idx += 1
                tbody.get_children().insert(row_idx, t)
                tag.get_children().remove(t)                
                t.set_parent(tbody)
                truncate = True
                
            elif truncate:
                table_siblings.insert(tbl_idx, t)
                tag.get_children().remove(t)
                t.set_parent(table_parent)
                tbl_idx += 1
                
        update_scope(tag)
        update_indexes(tag.get_children())
        update_scope(row)
        update_indexes(row.get_children())
        update_scope(tbody)
        update_indexes(tbody.get_children())
        update_scope(table)
        update_indexes(table.get_children())
        update_scope(table_parent)
        update_indexes(table_siblings)
        if table_parent != None:
            update_depth(table_parent)
        else:
            update_depth(table)

    def _close_open_tags(self, tag):
        ''' 1. Open inline tags are treated as closed w/o children. '''
        
        if tag.is_closed():
            return
            
        # get tag child index
        parent = tag.get_parent()
        siblings = self._get_siblings(tag)
        idx = siblings.index(tag)        
        
        # attach tag's children to parent
        for t in tag.get_children()[:]:            
            idx += 1
            siblings.insert(idx, t)
            tag.get_children().remove(t)        
            t.set_parent(parent)            
        
        update_scope(tag)        
        update_scope(parent)
        update_indexes(siblings)
        if parent != None:
            update_depth(parent)
        else:
            tag.set_depth(0)

    def _get_siblings(self, tag):
        parent = tag.get_parent()
        if parent != None:
            return parent.get_children()
        return self._doc
        
    def _get_row(self, tag):
        row = tag.get_parent()
        if row != None and row.get_name() == 'tr':
            return row
        return None
        
    def _get_tbody(self, tag):
        row = self._get_row(tag)
        if row != None:
            tag = row        
        tbody = tag.get_parent()
        if tbody != None and tbody.get_name() == 'tbody':
            return tbody
        return None
    
    def _get_table(self, tag):             
        table = None
        tbody = self._get_tbody(tag)
        if tbody != None:
            table = tbody.get_parent()
        if table != None and table.get_name() == 'table':
            return table
        return None

    def _get_table_parent(self, tag):
        table = self._get_table(tag)
        if table == None:
            return None  
        parent = table.get_parent()
        return parent

    def _get_table_siblings(self, tag):
        parent = self._get_table_parent(tag)
        if parent != None:
            siblings = parent.get_children()
        else:
            siblings = self._doc
        return siblings