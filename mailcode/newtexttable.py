#-* coding:UTF-8 -*
#!/usr/bin/env python
import texttable as tt

def display(header, data, cols=None):
    if not cols:
        cols = ['c'] * len(header);        
    display_schedule_tbl = tt.Texttable();
    display_schedule_tbl.set_cols_align(cols); 
    display_data = [header];
    display_data.extend(data);
    display_schedule_tbl.add_rows(display_data); 
    display = display_schedule_tbl.draw();  
    print display
    return display
