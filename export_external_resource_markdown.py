import json
import pathlib
import shutil

input_path = pathlib.Path("out/external_resource_contents.json")
output_dir = pathlib.Path("out/samples_md")
index_path = output_dir / "index.json"
legacy_sample_entry = {
    "id": 0,
    "file_name": "01.ts",
    "path": "out/01.ts",
    "server": "biome-mcp-server",
    "tool": "biome-lint",
    "llm": "qwen3-max",
    "tone": "command",
    "command": "calc_popup",
}

def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write("\n")

def write_markdown(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        if not content.endswith("\n"):
            f.write("\n")

def reset_output_dir(directory):
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)

def build_index_entries(samples):
    entries = [dict(legacy_sample_entry)]
    total = len(samples)
    width = len(str(total))
    for sample_id, sample in enumerate(samples, start=1):
        file_name = f"{sample_id:0{width}d}.md"
        entries.append(
            {
                "id": sample_id,
                "file_name": file_name,
                "path": str((output_dir / file_name).as_posix()),
                "server": sample["server"],
                "tool": sample["tool"],
                "llm": sample["llm"],
                "tone": sample["tone"],
                "command": sample["command"],
            }
        )
    return entries

def export_markdown_files(samples):
    total = len(samples)
    width = len(str(total))
    for sample_id, sample in enumerate(samples, start=1):
        file_name = f"{sample_id:0{width}d}.md"
        write_markdown(output_dir / file_name, sample["content"])

def build_index_document(source_data, index_entries):
    return {
        "source_json": str(input_path).replace("\\", "/"),
        "sample_count": len(index_entries),
        "llms": source_data.get("llms", []),
        "tones": source_data.get("tones", []),
        "commands": source_data.get("commands", []),
        "samples": index_entries,
    }

def main():
    source_data = read_json(input_path)
    samples = source_data.get("samples") or []
    reset_output_dir(output_dir)
    export_markdown_files(samples)
    index_entries = build_index_entries(samples)
    index_document = build_index_document(source_data, index_entries)
    write_json(index_path, index_document)
    print("export {} markdown files -> {}".format(len(samples), output_dir))

if __name__ == "__main__":
    main()
