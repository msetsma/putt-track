import os
import fnmatch

class FolderVisualizer:
    def __init__(self, root_path=None):
        self.root_path = root_path or os.getcwd()
        self.ignored_patterns = ['.pytest_cache', '__pycache__']
        self.load_gitignore()

    def load_gitignore(self):
        gitignore_path = os.path.join(self.root_path, '.gitignore')
        
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as file:
                for line in file:
                    pattern = line.strip()
                    if pattern and not pattern.startswith('#'):
                        self.ignored_patterns.append(pattern)

    def is_ignored(self, path):
        rel_path = os.path.relpath(path, self.root_path)
        for pattern in self.ignored_patterns:
            if fnmatch.fnmatch(rel_path, pattern):
                return True
        return False

    def build_structure(self, path=None, indent=0):
        structure_str = ""
        
        if path is None:
            path = self.root_path

        structure_str += ' ' * indent + f'+-- {os.path.basename(path)}/\n'
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if self.is_ignored(item_path):
                continue

            if os.path.isdir(item_path):
                structure_str += self.build_structure(item_path, indent + 4)
            else:
                structure_str += ' ' * (indent + 4) + f'--- {item}\n'
        
        return structure_str

    def save_structure(self, output_path='folder_structure.txt'):
        structure_str = self.build_structure()
        with open(output_path, 'w') as file:
            file.write(structure_str)
        print(f'Structure saved to {output_path}')

# Example usage
visualizer = FolderVisualizer()
visualizer.save_structure()
