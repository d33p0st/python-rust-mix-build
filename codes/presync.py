import os

class Lister(list):
    def __init__(self, directory: str = os.getcwd()):
        self.dir = directory
    
    @property
    def fill_paths(self) -> list[str]:
        paths = []
        for root, dirs, files in os.walk(self.dir):
            for dir_name in dirs:
                paths.append(os.path.join(root, dir_name))
            for file in files:
                paths.append(os.path.join(root, file))
        return paths

if __name__ == "__main__":
    paths = Lister().fill_paths
    with open('__all_files__', 'w+') as ref:
        for path in paths:
            ref.write(path + "\n")
