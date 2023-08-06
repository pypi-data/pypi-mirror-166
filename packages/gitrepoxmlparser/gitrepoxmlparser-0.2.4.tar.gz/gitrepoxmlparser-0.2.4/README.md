# GitRepoXMLParser

## _Capable of processing the AOSP repo's manifest file differentiating from the supplier_

GitRepoXMLParser helps you visualize your AOSP manifest files that is fed for [repo](https://source.android.com/docs/setup/develop/repo) tool
[Rich](https://pypi.org/project/rich/)-powered visualization.

## Manifest file example

```sh
<manifest >
    <remote fetch = "url" name = "pj-gerrit" review = "" / >
    <include name = "supplier.xml" / >
    <include name = "pj_apps.xml" / >
    <remove-project name = "pathto/projec" / >
    <project name = "supplier/pathto/projectrepo" path = "company/pathto/projectrepo" remote = "pj-gerrit" revision = "branch_name" / >
    <project name = "PJ/pathto/projectrepo1" path = "vendor/pathto/projectrepo1" remote = "pj-gerrit" revision = "branch_name" / >
    <project name = "PJ/pathto/projectrepo2" path = "vendor/pathto/projectrepo2" remote = "pj-gerrit" revision = "branch_name" / >
</manifest >
```

## Features

- Visualize your manifest.xml files visually
- The table size depends on the screensize of the command line utility that you are running the script

## Installation

gitrepoxmlparser requires [Rich](https://pypi.org/project/rich/) 12.5.1+.

```sh
pip install gitrepoxmlparser
```

## Usage

```sh
cmd>gitrepoxmlparser -h
usage: -m [-h] -f F -c C -s S [-x]

options:
  -h, --help  show this help message and exit
  -f F        manifest xml file
  -c C        Your company name (Should match with companies folder name in the stack)
  -s S        Supplier's Company name (just contrasts with only one vendor)
  -x, --html  For html report
```

#### Building the source

To activate the virtual env

```sh
poetry shell
```

Installing dependencies only

```sh
poetry install --no-root
```

To install the dependencies and install the package (reads the poetry.lock or pyproject.toml file )

```sh
poetry install
```

## License

MIT

**Free Software, Hell Yeah!**
