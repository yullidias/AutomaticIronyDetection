import src.utils.constants as cns
import os
import json
import pandas as pd
import pickle


def create_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def read_sample(path, extension='.txt'):
    with open(get_filename(path, extension), 'r') as f:
        data_list = f.read().split('\n')
    return data_list[:-1] if data_list[-1] == '' else data_list


def read_json(path, extension='.json'):
    with open(get_filename(path, extension), 'r') as f:
        return json.loads(f.read())


def write_json(path, obj):
    create_if_not_exists(os.path.dirname(path))
    with open(path, 'w') as f:
        f.write(json.dumps(obj, indent=2))


def write_list(path, obj):
    with open(path, 'w') as f:
        f.write("\n".join([str(x) for x in obj]))


def get_filename(name, extension):
    return name if name.endswith(extension) else name + extension


def remove_extension(name, extension):
    return name.split(extension)[0] if name.endswith(extension) else name


def get_paths(collect_file):
    """
    Get full path of jsons files.

    Args:
        collect_file (str): filename to list of collected jsons

    Returns:
        list: full path to jsons
    """
    with open(collect_file) as f:
        paths = []
        line = f.readline()
        while line:
            paths.append(os.path.dirname(collect_file) + "/" +
                         line.split("\n")[0] + '.json')
            line = f.readline()
    return paths


def read_excel(paths, suffle=False):
    if type(paths) is list:
        df = pd.read_excel(paths[0], index_col=0)
        for path in paths[1:]:
            df = df.append(pd.read_excel(path, index_col=0))
    else:
        df = pd.read_excel(paths, index_col=0)
    if suffle:
        return df.sample(frac=1, random_state=cns.SEED)
    return df


def to_excel(path, dfs, sheet_name='Sheet1'):
    create_if_not_exists(os.path.dirname(path))
    with pd.ExcelWriter(path, engine='xlsxwriter',
                        options={'strings_to_urls': False}) as writer:
        if type(dfs) is list:
            if type(sheet_name) is not list:
                raise Exception("Expected a list in sheet_name.")
            for n, df in enumerate(dfs):
                df.to_excel(writer, sheet_name=sheet_name[n])
        else:
            dfs.to_excel(writer, sheet_name=sheet_name)
    writer.close()


def to_markdown(path, dfs, file_name='Sheet1'):
    create_if_not_exists(os.path.dirname(path))
    if type(dfs) is list:
        if type(file_name) is not list:
            raise Exception("Expected a list in file_name.")
        for n, df in enumerate(dfs):
            with open(get_filename(path + file_name[n], '.md'), 'w') as f:
                f.write(df.to_markdown())
    else:
        with open(get_filename(path + file_name, '.md'), 'w') as f:
            f.write(df.to_markdown())


def write_obj(filename, obj):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)


def read_obj(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
