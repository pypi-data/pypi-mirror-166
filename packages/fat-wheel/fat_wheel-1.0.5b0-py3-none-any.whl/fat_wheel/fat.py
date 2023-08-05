"""
Approach to build fat wheel
1.[x] find root dir and move to it
2.[x] find following config file
- [x] requirements.txt
- fat-wheel.yaml
- pyproject.toml
3. [x] read config and build list of remote and local project dependency
************************************************************************
4. create a env and (may not do ;-) 
4. install dependency with --upgrade

-> pip install -r requirements -t .
- understand above cmd
- use of venv
- use of pipenv
************************************************************************
5. move local project to fat-wheel folder
6. move dependency in fat-wheel-<version> folder
7. chdir in fat-wheel-<version> and write setup.py 
8. generate wheel file cmd
9. remove fat-wheel-<version> if asked
10. 
"""
import os
from fat_wheel.cmd.pip import download_wheel, build
from fat_wheel.fs import copy, copy2, create_dirs, move
from fat_wheel.gen import generate_setup_py, copy_installer, get_version
from fat_wheel.parse.config import get_include_files, get_ignore_files
from fat_wheel.project_model import ProjectBuilder
from fat_wheel.utils import now, joinpath

# ignored_files = ["venv", "src", ".idea", "build", ".git"]


def move_dist(project):
    src ="dist"
    dst = joinpath(project.root_dir, "dist", project.version)
    copy2(src, dst, dirs_exist_ok=True)


def process():
    project_dir = input(f"Root dir press enter if not Enter project path: ")
    project = ProjectBuilder.builder().build_by_path(project_dir=project_dir).build()
    options = ["build", "sdist", "bdist_wheel"]
    project.set_version(version=get_version(project.root_dir))
    print(project.__dict__)
    if project.is_root:
        fat_wheel_build = f"{project.name}-v{project.version}-{now()}"
        fat_wheel_build_path = os.path.join(project.root_dir, "build", fat_wheel_build)
        create_dirs(fat_wheel_build_path)
        ignored_files = get_ignore_files(project.fat_config_yml)
        print(f"Ignored files/folder {ignored_files}")
        required_files = list(os.scandir(project.root_dir))
        for file in required_files:
            if file.name not in ignored_files:
                print(file.path)
                if os.path.isdir(file.path):
                    dst = os.path.join(fat_wheel_build_path, file.name)
                    copy2(src=file.path, dst=dst)
                else:
                    copy(src=file.path, dst=fat_wheel_build_path)
        print(f"chdir: {fat_wheel_build_path}")
        os.chdir(fat_wheel_build_path)
        download_wheel(project.pkg_name)
        copy_installer(project.pkg_name)
        generate_setup_py(fat_wheel_build_path, project.root_dir, project.pkg_name)
        build(options)
        move_dist(project)


def main():
    process()


if __name__ == '__main__':
    main()
