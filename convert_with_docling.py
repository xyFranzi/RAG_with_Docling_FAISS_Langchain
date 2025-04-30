import os
import subprocess

PDF_DIR = "./test_doc"
OUTPUT_DIR = "./test_result"

os.makedirs(OUTPUT_DIR, exist_ok=True)

pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]

if not pdf_files:
    print("没有 PDF 文件")
else:
    print(f"共找到 {len(pdf_files)} 个 PDF 文件，开始处理...\n")

    for pdf in pdf_files:
        input_path = os.path.join(PDF_DIR, pdf)
        print(f"正在处理：{input_path}")

        command = [
            "docling",
            input_path,
            "--from", "pdf",
            "--to", "json",
            "--to", "md",
            "--output", OUTPUT_DIR
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(f"完成：{pdf}")
        except subprocess.CalledProcessError as e:
            print(f"错误处理文件 {pdf}:")
            print(e.stderr)

    print("\n所有文件处理完成。输出路径：", OUTPUT_DIR)
