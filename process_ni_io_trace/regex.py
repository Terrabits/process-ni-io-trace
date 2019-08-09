
action_regex = r'(\d+)\.\s+(Completing\s+)?{method}'
method_regex = action_regex.format(method=r'vi{name}\s+\((.*)\)')
status_regex = r'Status: 0(?:x[0-9A-F]+)\s+\((.*)\)'
