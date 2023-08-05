import os, sys

class Map:
    def __init__(self, columns, rows, *, empty=' ', clear_screen=False, pixel_size=None):
        self.pixel_size = pixel_size or 1
        self.clear_screen = clear_screen
        self.rows, self.columns = rows, columns
        self._map = [0]*rows
        self.empty = empty
        for row_n in range(rows):
            setattr(self, f'row{row_n+1}', [empty]*columns)
            self._map[row_n] = getattr(self, f'row{row_n+1}')
    
    def __getitem__(self, item):
        if isinstance(item, int):
            return getattr(self, f'row{item+1}')
        elif isinstance(item, tuple):
            return getattr(self, f'row{item[1]+1}')[item[0]]
    
    def __setitem__(self, item, value):
        if isinstance(item, int) and isinstance(value, list):
            setattr(self, f'row{item+1}', value)
        elif isinstance(item, tuple):
            _ = getattr(self, f'row{item[1]+1}')
            _[item[0]] = value
            setattr(self, f'row{item[1]+1}', _)
        self._update_map()
    
    def __str__(self):
        if self.clear_screen:
            os.system('cls' if sys.platform.startswith('win') else 'clear')
        return self.map
    
    def _update_map(self):
        for row_n in range(self.rows):
            self._map[row_n] = getattr(self, f'row{row_n+1}')
    
    def replace_row(self, row_n, new_row):
        setattr(self, f'row{row_n+1}', new_row)
        self._update_map()
    
    def replace_column(self, col_n, new_col):
        for row_n in self.rows:
            _ = getattr(self, f'row{row_n+1}')
            _[col_n] = new_col[row_n]
            setattr(self, f'row{row_n+1}', _)
        self._update_map()
    
    def set_pixel(self, x, y, full='#'):
        _ = getattr(self, f'row{y+1}')
        _[x] = full
        setattr(self, f'row{y+1}', _)
        self._update_map()
    
    @property
    def map(self):
        return '\n'.join([''.join([b*self.pixel_size for b in a]) for a in self._map])
