import os, platform, sys
from git import Repo

# class lister:
#     def __init__(self, directory: str = os.getcwd()):
#         self.dir = directory
    
#     @property
#     def scan(self) -> list[str]:
#         entries = []

#         for dirpath, dirnames, filenames in os.walk(self.dir):
#             for dirname in dirnames:
#                 entries.append(os.path.join(dirpath, dirname))
#             for filename in filenames:
#                 entries.append(os.path.join(dirpath, filename))
        
#         return entries

#     def list(self, file: str = os.path.join(os.getcwd(), '__all_files__')):
#         with open(file, 'w+') as f_r:
#             for f in self.scan:
#                 f_r.write(f + "\n")

class sync:
    def __init__(self):
        token = os.environ['GITHUB_TOKEN']
        repo = Repo(os.getcwd())

        with open('pyproject.toml', 'r+') as tml:
            toml = tml.readlines()
        
        check = False
        for line in toml:
            line = line.replace('\n', '')
            if line.startswith('python-source'):
                ps = line.split('=')[-1].strip().replace('\"', '').replace('\'', '')
                check = True
                break
        
        if not check:
            print("python-source not defined in maturin config under pyproject.toml")
            sys.exit(1)
        else:
            with open('__all_files__', 'r+') as ref:
                oldpaths = ref.readlines()
                print("oldpaths:", oldpaths)
            
            os.system(f"python {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'presync.py')}")

            with open('__all_files__', 'r+') as ref:
                newpaths = ref.readlines()
                print("newpaths:", newpaths)
            
            os.unlink(os.path.join(os.getcwd(), '__all_files__'))

            to_add = []
            for path in newpaths:
                if ps in path and path not in oldpaths:
                    to_add.append(path.replace('\n', ''))
            
            print("files to add:", to_add)

            if repo.is_dirty(untracked_files=True):
                for path in to_add:
                    repo.index.add(path)
                repo.index.commit(f'mixed-bins added by [bot].')
                origin = repo.remote()
                origin.push()
                print("Updates pushed!")
            else:
                print("No change detected.")

sync()