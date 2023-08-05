from setuptools import setup, find_packages



setup(
        name="wct",
        version="1.0",
        license="GNU",
        author="b4b4 and AntoineB24",
        packages=find_packages("src"),
        package_dir={'':'src'},
        url="https://github.com/b4-b4/wct",
        keyword="Wizard for the Computer Tree",
)

