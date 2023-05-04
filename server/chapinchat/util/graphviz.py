from flask import current_app
import os
import subprocess


def to_one_table(table: str) -> str:
    upload_forlder = current_app.config["UPLOAD_FOLDER"]
    output_file = upload_forlder + "/out.pdf"
    input_file = upload_forlder + "/out.out"

    build = """digraph G {
    rankdir=TB;
    node [shape=plaintext];
    """

    build = "\n".join([build, "table1 [label=<"])

    build = "\n".join([build, table])

    build = "\n".join([build, ">];\n}"])

    # build = "\n".join([build, '"Nodo1" -> table1;'])

    with open(input_file, "w+") as f:
        f.write(build)

    os.system(f"dot -Tpdf {input_file} -o {output_file}")

    return output_file


def all_to_one_table(tables: list[str]) -> str:
    upload_forlder = current_app.config["UPLOAD_FOLDER"]
    output_file = upload_forlder + "/out.pdf"
    input_file = upload_forlder + "/out.out"

    build = """digraph G {
    rankdir=TB;
    node [shape=plaintext];
    """

    table_name = lambda x: f"tabla{x}"

    for i, table in enumerate(tables):
        build = "\n".join([build, f"{table_name(i)} [label=<"])
        build = "\n".join([build, table])
        build = "\n".join([build, ">];"])

    i = 0
    while i + 1 < len(tables):
        build = "\n".join([build, f"{table_name(i)} -> {table_name(i+1)}[style=invis]"])
        i += 1

    build = "\n".join([build, "}"])

    with open(input_file, "w+") as f:
        f.write(build)

    os.system(f"dot -Tpdf {input_file} -o {output_file}")

    return output_file
