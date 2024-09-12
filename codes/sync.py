import os, sys, subprocess
from git import Repo

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
            
            print("Old Paths:")
            for path in oldpaths:
                path = path.replace('\n', '')
                print(path if len(path) <= 25 else "..."+path[-25:])
            
            os.system(f"python {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'presync.py')}")

            with open('__all_files__', 'r+') as ref:
                new = ref.readlines()

            os.unlink(os.path.join(os.getcwd(), '__all_files__'))

            newpaths: list[str] = []
            for path in new:
                if path not in oldpaths and 'target' not in path and 'Cargo' not in path:
                    newpaths.append(path)

            if len(newpaths) > 0:
                print("\nNew Paths:")
                for path in newpaths:
                    path = path.replace('\n', '')
                    print(path if len(path) <= 25 else "..."+path[-25:])
            else:
                print("\nNo New Paths.")

            try:
                result = subprocess.run(
                    ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
                    capture_output=True, text=True, check=True
                )

                mod = result.stdout.splitlines()
                modified: list[str] = []
                for i in range(len(mod)):
                    if mod[i].endswith('.rs'):
                        modified.append(mod[i])
                if len(modified) > 0:
                    print("Modified Rust Files:", modified)
                else:
                    print("No Modified Rust Files Present in the last commit.")
            except subprocess.CalledProcessError:
                print("Error Checking last commit.")
                sys.exit(1)

            to_add: list[str] = []
            for path in newpaths:
                path = path.replace('\n', '')
                if ps in path and path not in oldpaths:
                    to_add.append(path)
                elif ps in path and path.endswith('.so') and len(modified)>0:
                    to_add.append(path)
                elif ps in path and path.endswith('.so'):
                    diff = repo.git.diff(path)
                    if diff:
                        to_add.append(path)
            
            # also check all files under ps
            all_files_under_pysrc = Lister(os.path.join(os.getcwd(), ps)).fill_paths
            for path in all_files_under_pysrc:
                if not os.path.isdir(path):
                    diff = repo.git.diff(path)
                    if diff:
                        to_add.append(path)
            
            if len(to_add) > 0:
                print("\nFiles to be added At this time:")
                for path in to_add:
                    path = path.replace('\n', '')
                    print(path if len(path) <= 25 else "..."+path[-25:])
            else:
                print("\nNo Files to Add.")
                sys.exit(0)


            if repo.is_dirty(untracked_files=True):
                for path in to_add:
                    repo.index.add(path)
                repo.index.commit(f'mixed-bins added by [bot].')
                origin = repo.remote()
                origin.push()
                print("Change Detected: Push success.")
            else:
                print("No change detected at this time. Ok")

sync()