import re
import subprocess

def get_current_branch():
    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
    return branch

def get_branch_versions(current_branch):
    branches = subprocess.check_output(['git', 'branch', '-r']).decode()
    versions = []
    for b in branches.split():
        if current_branch not in b:  
            match = re.search(r'release/(\d+\.\d+\.\d+)', b)
            if match:
                versions.append(match.group(1))
    return versions

def compare_versions(version1, version2):
    major1, minor1, patch1 = map(int, version1.split('.'))
    major2, minor2, patch2 = map(int, version2.split('.'))
    return (major1 > major2) or (major1 == major2 and minor1 > minor2) or (major1 == major2 and minor1 == minor2 and patch1 > patch2)

def check_version_increment(new_version, versions):
    # Check if the new version is greater than all existing versions
    if not all(compare_versions(new_version, v) for v in versions):
        raise ValueError(f"Version {new_version} must be greater than all existing versions")

if __name__ == "__main__":
    current_branch = get_current_branch()
    match = re.search(r'release/(\d+\.\d+\.\d+)', current_branch)
    if not match:
        raise ValueError("Current branch name does not follow the 'release/x.y.z' format")
    
    new_version = match.group(1)
    existing_versions = get_branch_versions(current_branch)
    if existing_versions:
        check_version_increment(new_version, existing_versions)
    else:
        print("No previous versions found. Proceeding with the first release.")
