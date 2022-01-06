from pathlib import PurePath

def get_basename_with_suffix(path, suffix):
    p = PurePath(path)
    return p.name.replace(p.suffix, f"_{suffix}{p.suffix}")
