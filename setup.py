import cx_Freeze

executables = [cx_Freeze.Executable("gof.py")]

cx_Freeze.setup(
    name="Game of flames",
    options={"build_exe": {"packages": ["pygame","screeninfo"],
                           "include_files": ["/assets/*"]}},
    executables=executables

)
