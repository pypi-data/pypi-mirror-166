import os, json
def is_replit():
    if ([k for k in os.environ.keys() if 'REPLIT_' in k]): # checks if there are env vars that have REPLIT_ in them
        return True
    else:
        return False

def load_json(file_name):
    return json.loads(open(str(file_name)).read()) # reads all json data from a file and loads it as dict or list

def save_json(file_name, data, indent:int=2):
    if indent > 0: # checks if there should be a indent
        with open(str(file_name), "w") as f: # if there should be then save it with one
            f.write(json.dumps(data, indent=indent))
    else: # otherwise save it without a indent
        with open(str(file_name), "w") as f:
            f.write(json.dumps(data))

