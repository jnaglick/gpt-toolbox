from utils import console

def get_file_view(file_path, line_num=None):
    response = {
        'file_contents': [],
        'error': None,
    }

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        if line_num is not None:
          start = max(0, line_num - 11)  # 10 lines before, -1 because of 0-indexing
          end = min(len(lines), line_num + 10)  # 10 lines after
          lines = lines[start:end]

        for i in range(len(lines)):
            response['file_contents'].append([i+1, lines[i]])
    except Exception as e:
        console.error(f"get_file_view error: {e}")
        response['error'] = str(e)
    
    return response
