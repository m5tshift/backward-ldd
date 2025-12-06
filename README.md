```bash
git clone https://github.com/m5tshift/backward-ldd.git
cd backward-ldd
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Basic Usage
```bash
python3 bldd.py <library_name> [-d directory] [-a arch] [-o output_file]
```

### Command Line Options
- `libraries`: One or more shared library files to search for (e.g., libc.so.6)
- `-d, --directory`: Root directory to scan (default: /)
- `-a, --arch`: Target architectures (choices: x86, x86_64, armv7, aarch64). Default: all architectures
- `-o, --output`: Path to report file (supports .txt, .pdf). If not specified, output is printed to console.

### Examples

1. Find libc.so.6 in /usr/bin directory:
```bash
python3 bldd.py libc.so.6 -d /usr/bin
```

2. Find multiple libraries and save to PDF:
```bash
python3 bldd.py libssl.so libcrypto.so -o report.pdf
```

3. Search for ARMv7 libraries:
```bash
python3 bldd.py libc.so.6 --arch armv7
```
