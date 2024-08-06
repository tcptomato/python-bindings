# #!/usr/bin/env python3
#!/usr/bin/env python3
import os
import subprocess
import cffi
import argparse

def preprocess(source, header_path):
    """
    Function returning a preprocessed header file.
    """
    command = ["gcc", "-DLIB_PYCPARSER", "-E", "-P", "-D__extension__="]
    for header in header_path:
        command.append("-I" + header)
    command.append("-")

    try:
        return subprocess.run(command, input=source, stdout=subprocess.PIPE, universal_newlines=True, check=True).stdout
    except subprocess.CalledProcessError:
        print("Error during GCC preprocessing.")
        exit(1)

def create_bindings(include_path, library_path, output_name, header_file_name, path):
    ffi = cffi.FFI()

    with open(header_file_name, encoding="UTF-8") as h_file:
        ffi.cdef(preprocess(h_file.read(), include_path))

    print("Preprocess done")
    ffi.set_source(
        output_name,
        '#include "library.h"',
        include_dirs=include_path,
        libraries=["library"],
        library_dirs=library_path,
        extra_link_args=["-Wl,-rpath,."],
    )

    ffi.compile(target=output_name, verbose=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--include_path", help="Header include path to use", action='append', default=["."])
    parser.add_argument("-l", "--library_path", help="Library path to use", action='append', default=["."])
    parser.add_argument("-n", "--name", help="Name of the output object", action='store', default="libraryPYC")
    parser.add_argument("-p", "--path", help="Base path to use", action='store', default=".")
    parser.add_argument("-f", "--header_file", help="Name of the header file", action='store', default="library.h")

    args = parser.parse_args()

    include_path = [os.path.join(args.path, p) for p in args.include_path]
    library_path = args.library_path
    output_name = args.name
    header_file_name = os.path.join(args.path, args.header_file)

    try:
        create_bindings(include_path, library_path, output_name, header_file_name, args.path)
    except Exception as e:
        print(f"Error: {e}")
