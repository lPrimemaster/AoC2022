from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class File:
    def __init__(self, parent, name, size) -> None:
        self.name = name
        self.size = size
        self.parent = parent
        

@dataclass
class Directory:
    def __init__(self, parent, name) -> None:
        self.name = name
        self.parent = parent
        self.child_dirs = []
        self.child_files = []
        self.depth = 0
        
    def insert_child_dir(self, child) -> None:
        child.depth = self.depth + 1
        self.child_dirs.append(child)
        
    def insert_child_file(self, child) -> None:
        self.child_files.append(child)
        
    def find_child_dir(self, name) -> Directory:
        cdir = [x for x in self.child_dirs if x.name == name]
        if len(cdir) < 1:
            print(f'Dir {name} not found!')
        else:
            return cdir[0]
        
    def print(self) -> None:
        
        tab = '\t'*self.depth + '- '
        tabf = '\t'*(self.depth+1) + '- '
        
        print(f'{tab}Directory {self.name}')
        
        for f in self.child_files:
            print(f'{tabf}File {f.name} {f.size}')
        
        
        for f in self.child_dirs:
            f.print()
            
    def compute_size(self) -> int:
        size = 0
        for f in self.child_files:
            size += f.size
        
        for f in self.child_dirs:
            size += f.compute_size()
            
        return size
        

def Parse(inputs: list) -> Tuple[Directory, List[Directory]]:
    all_dirs = [] # Except Root
    root = Directory(None, '/')
    
    head = root
    for input in inputs:
        if input.startswith('$'):
            commands = input.split()
            if commands[1] == 'cd':
                if commands[2] == '..':
                    head = head.parent
                else:
                    head = head.find_child_dir(commands[2])
                    
                    # This could work if there weren't any empty dirs (might not be the case idk)
                    # head = Directory(head, commands[2])
            
            elif commands[1] == 'ls':
                continue
        elif input.startswith('dir'):
            directory = Directory(head, input.split()[1])
            head.insert_child_dir(directory)
            all_dirs.append(directory)
        else:
            size, name = input.split()
            head.insert_child_file(File(head, name, int(size)))
            
    return root, all_dirs

FS_SIZE = 70000000
UPDATE_REQ_SIZE = 30000000

with open('day7.txt') as f:
    root, all_dirs = Parse(f.readlines()[1:])
    root.print()
    
    total_size = 0
    for d in all_dirs:
        size = d.compute_size()
        if size <= 100000:
            # print(f'{d.name} - {size}')
            total_size += size
    print(f'Total polled size = {total_size}')
    
    
    missing_space = UPDATE_REQ_SIZE - (FS_SIZE - root.compute_size())
    print(f'FS used space = {root.compute_size()}/{FS_SIZE}')
    print(f'FS free space = {FS_SIZE - root.compute_size()}')
    print(f'FS spaced required to be freed = {missing_space}')
    
    best_dir_size = FS_SIZE
    for d in all_dirs:
        size = d.compute_size()
        if size >= missing_space and size < best_dir_size:
            best_dir_size = size
    print(f'Dir to delete size = {best_dir_size}')
            