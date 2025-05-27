from setuptools import setup, find_packages

def load_requirements(file_path):
    with open(file_path, "r") as f:
        return f.read().splitlines()
    
requirements_my_project = load_requirements("trending_on_netflix/requirements.txt")

setup(
    name="trending_on_netflix",  # A name for your combined package
    version="0.1",
    # Find all Python packages under the 'dags' folder
    packages=find_packages(include=["trending_on_netflix", "trending_on_netflix.*"]),
    # package_dir={"": "code"},
    # Combine the requirements from all projects
    install_requires=requirements_my_project,
)