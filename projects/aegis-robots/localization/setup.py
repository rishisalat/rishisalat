from setuptools import find_packages, setup

package_name = "localization"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Rishi Salat",
    maintainer_email="rishisalat1425@gmail.com",
    description="AEGIS localization component: pose subscriber/publisher",
    license="Apache-2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "localization_node = localization.localization_node:main",
        ],
    },
)
