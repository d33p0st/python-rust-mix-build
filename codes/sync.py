import os
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

        if repo.is_dirty(untracked_files=True):
            repo.index.add('')
            repo.index.commit(f'mixed-bins added by [bot].')
            origin = repo.remote()
            origin.push()
            print("Updates pushed!")
        else:
            print("No change detected.")

sync()