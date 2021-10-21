def merge_tables(*args) -> List[Dict]:
    """Merge lists of dicts from args (usually represent time series) into one sorted list
    
    Args:
        args (List): python lists with same format dicts, e.g. [{'time': datetime, 'value': Any, 'label': str}]
            It is important to use same keys in all lists of dicts in args.
            
    Returns:
        List[Dict]: list of merged dicts by time
    """
    # Search for the longest list in args
    longest_table = None
    longest_label = None
    for table, label in args:
        for row in table:
            row['label'] = label
        if longest_table is None or len(longest_table) < len(table):
            longest_table = table
            longest_label = label
    
    # Insert all other lists in longest, so we decrease inserts amount
    merged_table = copy(longest_table)
    for table, label in args:
        if label == longest_label:
            continue
        
        cursor_pos = 0
        for row in table:
            while merged_table[cursor_pos]['time'] < row['time'] and cursor_pos < len(merged_table):
                cursor_pos += 1
            merged_table.insert(cursor_pos, row)
    
    # Result list dicts contain keys from from initial lists labels
    all_labels = [tpl[1] for tpl in args]
    all_labels.append('time')
    
    slice_ = {label: None for label in all_labels}
    
    pretty_table = []
    for row in merged_table:
        curr_time = row['time']
        if slice_['time'] is not None and curr_time != slice_['time']:
            pretty_table.append(copy(slice_))
        
        curr_label = row['label']
        slice_[curr_label] = row['value']
        slice_['time'] = row['time']

    pretty_table.append(copy(slice_))
    
    return pretty_table
    
        

flow_ip = [
    {'time': 1, 'value': 111},
    {'time': 3, 'value': 222},
    {'time': 8, 'value': 333},
]

flow_canvas = [
    {'time': 12, 'value': 'canv1'},
    {'time': 60, 'value': 'canv2'},
]

flow_smth = [
    {'time': 0,  'value': 'aaa'},
    {'time': 11, 'value': 'bb'},
    {'time': 12, 'value': 'ccc'},
    {'time': 20, 'value': 'hhh'},
    {'time': 40, 'value': 'jjj'},
    {'time': 60, 'valuev': 'rr'},
]
      
merge_tables((flow_ip, 'ip'), (flow_canvas, 'canvas'), (flow_smth, 'smth'))
