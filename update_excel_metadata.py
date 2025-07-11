import os
import shutil
import xml.etree.ElementTree as ET
import zipfile
from typing import Optional


def assignMetadataToExcel(input_file: str, commit_hash: str, release_tag: str):
    tmp_dir = "tmp_unzipped"
    infos = _customUnzip(input_file, tmp_dir)
    _infuseMetadata(commit_hash, release_tag)
    _customZip(input_file, tmp_dir, infos)


def _customZip(output_file, tmp_dir, infos):
    with zipfile.ZipFile(output_file, "w") as zip_out:
        for info in infos:
            filepath = os.path.join(tmp_dir, info.filename)
            with open(filepath, "rb") as f:
                data = f.read()
            zip_out.writestr(info, data)
    # Clean up
    shutil.rmtree(tmp_dir)


def _customUnzip(input_excel, tmp_dir):
    with zipfile.ZipFile(input_excel, "r") as zip_ref:
        infos = zip_ref.infolist()
        zip_ref.extractall(tmp_dir)
    return infos


def _infuseMetadata(
    commit_hash: Optional[str] = None, release_tag: Optional[str] = None
):
    # Register namespaces so ElementTree uses the desired prefixes.
    ET.register_namespace(
        "cp", "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
    )
    ET.register_namespace("dc", "http://purl.org/dc/elements/1.1/")
    ET.register_namespace("dcterms", "http://purl.org/dc/terms/")
    ET.register_namespace("dcmitype", "http://purl.org/dc/dcmitype/")

    core_xml_path = os.path.join("tmp_unzipped", "docProps", "core.xml")
    with open(core_xml_path, "r", encoding="utf-8", errors="replace") as file:
        core_xml = file.read()

    # Parse the XML
    root = ET.fromstring(core_xml)
    ns = {
        "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
    }

    # Update or create the <cp:version> element.
    version_elem = root.find("cp:version", ns)
    if version_elem is None:
        version_elem = ET.Element(
            "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}version"
        )
        root.append(version_elem)
    version_elem.text = release_tag

    # Add/update the "Tags" field as the "Keywords" property.
    keywords_elem = root.find("cp:keywords", ns)
    # If found, remove it so we can append it at the end.
    if keywords_elem is not None:
        root.remove(keywords_elem)
    else:
        keywords_elem = ET.Element(
            "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}keywords"
        )
    keywords_elem.text = commit_hash
    # Append the keywords element so it appears as the last child.
    root.append(keywords_elem)

    # Serialize with the desired encoding and declaration.
    updated_xml = ET.tostring(root, encoding="UTF-8", xml_declaration=True).decode(
        "UTF-8"
    )
    # Ensure standalone="yes" is present in the declaration.
    if "standalone" not in updated_xml:
        updated_xml = updated_xml.replace("?>", ' standalone="yes"?>', 1)

    # Write back the updated XML.
    with open(core_xml_path, "w", encoding="utf-8") as file:
        file.write(updated_xml)


def main():
    input_file = os.environ.get("EXCEL_FILE")
    commit_hash = os.environ.get("COMMIT_HASH", "unknown")
    release_tag = os.environ.get("RELEASE_TAG", "unknown")
    assignMetadataToExcel(input_file, commit_hash, release_tag)
    print(f"Metadata updated: version={release_tag}, tags={commit_hash}")


if __name__ == "__main__":
    main()
