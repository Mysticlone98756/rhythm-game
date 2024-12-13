def read_sm_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = file.readlines()
    
    parsed_data = {}
    notes_section = False
    notes = []
    
    for line in data:
        line = line.strip()
        if line.startswith('#') and ':' in line:
            # Metadata and timing data
            tag, value = line.split(':', 1)
            tag = tag.strip('#')
            value = value.strip(';')
            parsed_data[tag] = value
        elif line.startswith('#NOTES:'):
            # Start of notes section
            notes_section = True
            notes.append(line)
        elif notes_section:
            # Add to notes section
            notes.append(line)
            if line.endswith(';'):
                notes_section = False
    
    parsed_data['NOTES'] = ''.join(notes)
    return parsed_data

# Example Usage
file_path = "C:\\Users\\Mysticlone98756\\Desktop\\codin\\song.sm"
parsed_chart = read_sm_file(file_path)
print(parsed_chart)
