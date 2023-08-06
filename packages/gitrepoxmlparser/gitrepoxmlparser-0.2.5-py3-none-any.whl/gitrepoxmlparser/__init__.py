__version__ = "0.2.5"
import os
import argparse
from rich.console import Console
from rich.table import Table
from rich.table import Column
from xml.dom.minidom import parse, parseString
from pywebio import start_server
from pywebio.output import *

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="manifest xml file", required=True)
parser.add_argument(
    "-c",
    help="Your company name (Should match with companies folder name in the stack)",
    required=True,
)
parser.add_argument(
    "-s",
    help="Supplier's Company name (just contrasts with only one vendor)",
    required=True,
)
parser.add_argument(
    "-x", "--html", action="store_true", default=False, help="For html report"
)
# print('Arguments offered are')
args = parser.parse_args()
xmlfile = args.f
company = args.c
supplier = args.s
ishtml = args.html
# print(args.p)

d = parse(xmlfile)
console = Console()

emptyattributes = []  # requierd!
empty_str = ""


def check_and_add(table, row, i):
    # console.print("Tuple > List section > check and add section")
    first_list = row[0]
    second_list = row[1]
    third_list = row[2]
    f_len = len(first_list)
    s_len = len(second_list)
    t_len = len(third_list)
    first_list_item = first_list[i] if i < len(first_list) else empty_str
    second_list_item = second_list[i] if i < len(second_list) else empty_str
    third_list_item = third_list[i] if i < len(third_list) else empty_str
    table.add_row(
        str(i + 1),
        first_list_item,
        second_list_item,
        third_list_item,
        style="bright_green",
    )


def rich_table(title, cols, rows, attributes):
    table = ""
    match len(cols):
        case 0:
            table = Table(Column(no_wrap=True, header="no"), title=title, expand=True)
        case 1:
            table = Table(
                Column(no_wrap=True, header="no"),
                Column(no_wrap=False, header=cols[0]),
                title=title,
                expand=True,
            )
        case 2:
            table = Table(
                Column(no_wrap=True, header="no"),
                Column(no_wrap=False, header=cols[0]),
                Column(no_wrap=False, header=cols[1]),
                title=title,
                expand=True,
            )
        case 3:
            table = Table(
                Column(no_wrap=True, header="no"),
                Column(no_wrap=False, header=cols[0]),
                Column(no_wrap=False, header=cols[1]),
                Column(no_wrap=False, header=cols[2]),
                title=title,
                expand=True,
            )
        case 4:
            table = Table(
                Column(no_wrap=True, header="no"),
                Column(no_wrap=False, header=cols[0]),
                Column(no_wrap=False, header=cols[1]),
                Column(no_wrap=False, header=cols[2]),
                Column(no_wrap=False, header=cols[3]),
                title=title,
                expand=True,
            )
        case 5:
            table = Table(
                Column(no_wrap=True, header="no"),
                Column(no_wrap=False, header=cols[0]),
                Column(no_wrap=False, header=cols[1]),
                Column(no_wrap=False, header=cols[2]),
                Column(no_wrap=False, header=cols[3]),
                Column(no_wrap=False, header=cols[4]),
                title=title,
                expand=True,
            )
        case 6:
            table = Table(
                Column(no_wrap=True, header="no"),
                Column(no_wrap=False, header=cols[0]),
                Column(no_wrap=False, header=cols[1]),
                Column(no_wrap=False, header=cols[2]),
                Column(no_wrap=False, header=cols[3]),
                Column(no_wrap=False, header=cols[4]),
                Column(no_wrap=False, header=cols[5]),
                title=title,
                expand=True,
            )
    # for col in cols:
    # table.add_column(col)
    if len(rows) > 0:
        if type(rows[0]) is tuple:  # check 1st element of list is tuple
            # console.print("Tuple section")
            for i, row in enumerate(rows):
                if len(row) == 1:
                    table.add_row(str(i + 1), str(row[0]), style="bright_green")
                if len(row) == 2:
                    table.add_row(
                        str(i + 1), str(row[0]), str(row[1]), style="bright_green"
                    )
                if len(row) == 3 and type(row[0]) is list:
                    # console.print("Tuple > List section")
                    maximumnolist = max(len(row[0]), len(row[1]), len(row[2]))
                    for i in range(maximumnolist):
                        check_and_add(table, row, i)
                elif len(row) == 3 and type(row[0]) is str:
                    table.add_row(
                        str(i + 1),
                        str(row[0]),
                        str(row[1]),
                        str(row[2]),
                        style="bright_green",
                    )
                if len(row) == 4 and type(row[0]) is str:
                    table.add_row(
                        str(i + 1),
                        str(row[0]),
                        str(row[1]),
                        str(row[2]),
                        str(row[3]),
                        style="bright_green",
                    )
                if len(row) == 5 and type(row[0]) is str:
                    table.add_row(
                        str(i + 1),
                        str(row[0]),
                        str(row[1]),
                        str(row[2]),
                        str(row[3]),
                        str(row[4]),
                        style="bright_green",
                    )
                if len(row) == 6 and type(row[0]) is str:
                    table.add_row(
                        str(i + 1),
                        str(row[0]),
                        str(row[1]),
                        str(row[2]),
                        str(row[3]),
                        str(row[4]),
                        str(row[5]),
                        style="bright_green",
                    )

        elif type(rows[0]) is str:
            # console.print("str section")
            for i, row in enumerate(rows):
                table.add_row(str(i + 1), row, style="bright_green")

        else:
            for i, row in enumerate(rows):
                if len(attributes) == 1:
                    table.add_row(
                        str(i + 1),
                        row.getAttribute(attributes[0]),
                        style="bright_green",
                    )
                if len(attributes) == 2:
                    table.add_row(
                        str(i + 1),
                        row.getAttribute(attributes[0]),
                        row.getAttribute(attributes[1]),
                        style="bright_green",
                    )
                if len(attributes) == 3:
                    table.add_row(
                        str(i + 1),
                        row.getAttribute(attributes[0]),
                        row.getAttribute(attributes[1]),
                        row.getAttribute(attributes[2]),
                        style="bright_green",
                    )
                if len(attributes) == 4:
                    table.add_row(
                        str(i + 1),
                        row.getAttribute(attributes[0]),
                        row.getAttribute(attributes[1]),
                        row.getAttribute(attributes[2]),
                        row.getAttribute(attributes[3]),
                        style="bright_green",
                    )
                if len(attributes) == 5:
                    table.add_row(
                        str(i + 1),
                        row.getAttribute(attributes[0]),
                        row.getAttribute(attributes[1]),
                        row.getAttribute(attributes[2]),
                        row.getAttribute(attributes[3]),
                        row.getAttribute(attributes[4]),
                        style="bright_green",
                    )
                if len(attributes) == 6:
                    table.add_row(
                        str(i + 1),
                        row.getAttribute(attributes[0]),
                        row.getAttribute(attributes[1]),
                        row.getAttribute(attributes[2]),
                        row.getAttribute(attributes[3]),
                        row.getAttribute(attributes[4]),
                        row.getAttribute(attributes[5]),
                        style="bright_green",
                    )
    else:
        console.print("No Data to add")

    console.print(table)


def html_table(title, cols, rows, attributes):
    style(put_html(f"<h1>{title}</h1>"), "color:green")
    table = []
    table.append(cols)
    if len(rows) > 0:
        if type(rows[0]) is tuple:  # check 1st element of list is tuple
            # console.print("Tuple section")
            for i, row in enumerate(rows):
                if type(row[0]) is str:  # check 1st element of tuple is str
                    table.append([style(put_text(i + 1), "color:green"), *row])
                if type(row[0]) is list:  # check 1st element of tuple is list
                    ll = [*row]
                    ll.sort(key=len)

                    smalllist = ll[0]
                    mediumlist = ll[1]
                    highlist = ll[2]
                    collectedlist = []
                    for i in range(len(highlist)):
                        highVal = highlist[i]
                        mediumVal = ""
                        smallVal = ""
                        if i < len(mediumlist):
                            mediumVal = mediumlist[i]
                        if i < len(smalllist):
                            smallVal = smalllist[i]
                        table.append(
                            [
                                style(put_text(i + 1), "color:green"),
                                highVal,
                                mediumVal,
                                smallVal,
                            ]
                        )

                    # table.append([*collectedlist])
        elif type(rows[0]) is str:
            for i, row in enumerate(rows):
                table.append([style(put_text(i + 1), "color:green"), row])
        elif type(rows[0]) is list:
            for i, row in enumerate(rows):
                table.append([style(put_text(i + 1), "color:green"), *row])
        else:
            for i, row in enumerate(rows):
                if len(attributes) == 1:
                    table.append(
                        [
                            style(put_text(i + 1), "color:green"),
                            row.getAttribute(attributes[0]),
                        ]
                    )
                if len(attributes) == 2:
                    table.append(
                        [
                            style(put_text(i + 1), "color:green"),
                            row.getAttribute(attributes[0]),
                            row.getAttribute(attributes[1]),
                        ]
                    )
                if len(attributes) == 3:
                    table.append(
                        [
                            style(put_text(i + 1), "color:green"),
                            row.getAttribute(attributes[0]),
                            row.getAttribute(attributes[1]),
                            row.getAttribute(attributes[2]),
                        ]
                    )
                if len(attributes) == 4:
                    table.append(
                        [
                            style(put_text(i + 1), "color:green"),
                            row.getAttribute(attributes[0]),
                            row.getAttribute(attributes[1]),
                            row.getAttribute(attributes[2]),
                            row.getAttribute(attributes[3]),
                        ]
                    )
                if len(attributes) == 5:
                    table.append(
                        [
                            style(put_text(i + 1), "color:green"),
                            row.getAttribute(attributes[0]),
                            row.getAttribute(attributes[1]),
                            row.getAttribute(attributes[2]),
                            row.getAttribute(attributes[3]),
                            row.getAttribute(attributes[4]),
                        ]
                    )
        put_table(table)
    else:
        console.print("No Data to add")


def main():
    # ================================================================================================
    remotetitle = "Remotes"
    remotecolumns = ["no.", "fetch url", "remote name"]
    remoterows = d.getElementsByTagName("remote")
    remoteattributes = ["fetch", "name"]
    if ishtml:
        html_table(remotetitle, remotecolumns, remoterows, remoteattributes)
    else:
        rich_table(remotetitle, remotecolumns, remoterows, remoteattributes)
    # ================================================================================================
    inctitle = "Includes"
    inccolumns = ["no.", "Name(xml manifest files)"]
    incrows = [p.getAttribute("name") for p in d.getElementsByTagName("include")]

    if ishtml:
        html_table(inctitle, inccolumns, incrows, emptyattributes)
    else:
        rich_table(inctitle, inccolumns, incrows, emptyattributes)
    # ================================================================================================
    removedprojects = [
        p.getAttribute("name") for p in d.getElementsByTagName("remove-project")
    ]

    rmtitle = "Removed projects"
    rmcolumns = ["no.", f"Name ({supplier} project repos)"]
    rmrows = removedprojects
    if ishtml:
        html_table(rmtitle, rmcolumns, rmrows, emptyattributes)
    else:
        rich_table(rmtitle, rmcolumns, rmrows, emptyattributes)
    # rich_table(rmtitle, rmcolumns, rmrows, emptyattributes)
    # ================================================================================================

    projectsall = [
        (
            p.getAttribute("name"),
            p.getAttribute("path"),
            p.getAttribute("revision"),
            p.getAttribute("remote"),
            p.getAttribute("upstream"),
        )
        for p in (d.getElementsByTagName("project"))
    ]

    replaced_rname_nname_npath = [
        (rp, p[0], p[1], p[2], p[3], p[4])
        for p in projectsall
        for rp in removedprojects
        if p[0].endswith(rp)
    ]

    reptitle = f"{company} Replaced projects with {supplier}(Modificatiosn may be small or big)"
    repcolumns = [
        "no.",
        f"({supplier})Removed Name",
        f"({company}) Replaced Project Name",
        f"({company}) Replaced Project Path",
        f"({company}) Replaced Project Revision",
        f"({company}) Replaced Project Remote",
        f"({company}) Replaced Project Upstream",
    ]
    reprows = replaced_rname_nname_npath

    if ishtml:
        html_table(reptitle, repcolumns, reprows, emptyattributes)
    else:
        rich_table(reptitle, repcolumns, reprows, emptyattributes)
    # ================================================================================================
    conewtitle = f"Newly added projects with {company} package names"
    cocolumns = [
        "no.",
        f"({company}) Project Name Tag",
        f"({company}) Project Path Tag",
        f"({company}) Project Revision",
        f"({company}) Project Remote",
        f"({company}) Project Upstream",
    ]
    replaced_names = [
        replaced_project[1] for replaced_project in replaced_rname_nname_npath
    ]

    conewRows = [
        p for p in projectsall if p[0] not in replaced_names and company.lower() in p[0]
    ]

    if ishtml:
        html_table(conewtitle, cocolumns, conewRows, emptyattributes)
    else:
        rich_table(conewtitle, cocolumns, conewRows, emptyattributes)
    # ================================================================================================
    noncotitle = f"Newly added ({company} & Other Vendors) Project repos "
    noncocolumns = [
        "no.",
        f"({company} & Other Vendors) Project Name Tag",
        f"({company} & Other Vendors) Project Path Tag",
        f"({company}) Project Revision",
        f"({company}) Project Remote",
        f"({company}) Project Upstream",
    ]
    nonconewRows = [
        p
        for p in projectsall
        if p[0] not in replaced_names and company.lower() not in p[0]
    ]

    if ishtml:
        html_table(noncotitle, noncocolumns, nonconewRows, emptyattributes)
    else:
        rich_table(noncotitle, noncocolumns, nonconewRows, emptyattributes)
    # ================================================================================================
    actualreplacedPaths = [rep[2] for rep in replaced_rname_nname_npath]
    conewprojectsPaths = [n[1] for n in conewRows]
    nonconewprojectsPaths = [n[1] for n in nonconewRows]

    allpathtitle = "All Paths for Build file processing"
    allpathscolumns = ["no.", "Paths"]
    allpathsRows = actualreplacedPaths + conewprojectsPaths + nonconewprojectsPaths
    if ishtml:
        html_table(allpathtitle, allpathscolumns, allpathsRows, emptyattributes)
    else:
        rich_table(allpathtitle, allpathscolumns, allpathsRows, emptyattributes)
    # ================================================================================================
    newlyad_title = f"All Newly added Paths for considerations in {company}"

    newlyad_columns = [
        "no.",
        f"{supplier} replaced paths",
        f"New {company} repo paths",
        f"{company} or other vendors paths",
    ]

    newlyad_Rows = [(actualreplacedPaths, conewprojectsPaths, nonconewprojectsPaths)]
    if ishtml:
        html_table(newlyad_title, newlyad_columns, newlyad_Rows, emptyattributes)
    else:
        rich_table(newlyad_title, newlyad_columns, newlyad_Rows, emptyattributes)
    # ================================================================================================
    totallength = (
        len(actualreplacedPaths) + len(conewprojectsPaths) + len(nonconewprojectsPaths)
    )
    if ishtml:
        style(
            put_text(f"Actual replaced paths = {len(actualreplacedPaths)}"), "color:red"
        )
        style(
            put_text(f"Total Company's new repos = {len(conewprojectsPaths)}"),
            "color:red",
        )
        style(
            put_text(f"Total non Company's new repos = {len(nonconewprojectsPaths)}"),
            "color:red",
        )
        style(put_text(f"Total repos = {totallength}"), "color:red")
    else:
        console.print(f"Actual replaced paths = {len(actualreplacedPaths)}")
        console.print(f"Total Company's new repos = {len(conewprojectsPaths)}")
        console.print(f"Total non Company's new repos = {len(nonconewprojectsPaths)}")
        console.print(f"Total non Company's new repos = {len(nonconewprojectsPaths)}")


if __name__ == "__main__":
    if ishtml:
        start_server(main, port=8080, debug=True)
    else:
        main()
