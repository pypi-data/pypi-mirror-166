import os
import jinja2
import pkginfo

from fat_wheel.parse.py_file import get_py_file_meta_data

TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), "template")
TEMPLATE_FILE = "setup.py"


def generator(options, extra_options, build_path=""):
    try:
        template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_FOLDER)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(TEMPLATE_FILE)
        print(options)
        output_text = template.render(options=options,
                                      extra_options=extra_options)  # this is where to put args to the template renderer
        with open(os.path.join(build_path, "setup.py"), mode="w") as s:
            s.write(output_text)
    except Exception as e:
        raise e


def generate_setup_py(fat_wheel_build_path, root_dir, pkg_name):
    meta_data = get_py_file_meta_data(os.path.join(root_dir, "setup.py"))
    # meta_data.append(__data_files())
    extra_options = [[[pkg_name, '"deps/*"']], [f"{pkg_name} = {pkg_name}.runner:install"]]
    generator(meta_data, extra_options, build_path=fat_wheel_build_path)


def __data_files():
    all_deps = os.scandir("test_project/deps")
    all_wheel = [f'deps/{dep.name}' for dep in all_deps]
    data_files = ["data_files", f'[("deps", ({str(all_wheel)[1:-1]}))]', object]
    return data_files


def get_version(root_dir):
    """refactor it please"""
    meta_data = get_py_file_meta_data(os.path.join(root_dir, "setup.py"))
    for key in meta_data:
        if "version" in key:
            return key[1]


def copy_installer(dest):
    try:
        template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_FOLDER)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template("runner.py")
        dest_list = []
        for i in os.scandir(os.path.join(dest, "deps")):
            dest_list.append(pkginfo.get_metadata(i.path).name)
        output_text = template.render(dep_list=str(dest_list))  # this is where to put args to the template renderer
        with open(os.path.join(dest, "runner.py"), mode="w") as s:
            s.write(output_text)
    except Exception as e:
        raise e