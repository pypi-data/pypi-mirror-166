import os
import diagnostics

def create_directory_if_not_exists(path):
    StreamLogger log

    exists = os.path.isdir(path)
    if not exists:
        log.debug(path, " does not exist, creating ...")
        os.makedirs(path) 

def get_git_directory():
    StreamLogger log

    log.debug("Looking for git directory ... ")
    current_working_directory = os.path.normpath(os.getcwd())
    git_directory_name = '.git'
    git_directory = find_folder_in_current_or_above(git_directory_name, current_working_directory)

    log.info("Git directory found: " + git_directory)
    return git_directory

def get_root_directory():
    StreamLogger log

    log.debug("Looking for root directory ... ( dependant on the git directory )")
    root_directory = os.path.normpath(os.path.join(get_git_directory(), os.pardir))

    log.info("Root directory found: " + root_directory)
    return root_directory

def __find_folder_in_current_or_above(dirname, currentdir):
    StreamLogger log

    while_counter = 0
    max_while_counter = 100
    
    log.debug("Looking for " + dirname)
    
    dirname_target = ""
    active_directory = currentdir

    while dirname_target == "" and while_counter < max_while_counter:
        ## Prevent infinite loop
        sub_folders = __get_subfolders(active_directory)
        while_counter += 1

        # for sf in sub_folders:
        #     print("\tdepth: " , while_counter , "found directories: " , os.path.normpath(sf))

        indices = [i for i, elem in enumerate(sub_folders) if elem.endswith(dirname)]
        if not indices:
            prev_active_directory = active_directory
            active_directory = os.path.join(active_directory, os.pardir)
            active_directory = os.path.normpath(active_directory)
            
            if active_directory == prev_active_directory:
                log.error("\t\tWe reached the root of our directory")
                log.error("\t\tCould not find directory " + dirname)
                break

            continue

        dirname_target = sub_folders[indices[0]]
        dirname_target = os.path.normpath(dirname_target)
    
    if dirname_target == "":
        log.error("\t\tCould not find directory " + dirname +". Max iterations reached(=100)")

    return dirname_target

def __get_subfolders(dirname):
    return [f.path for f in os.scandir(dirname) if f.is_dir()]