from setuptools import Extension, setup

ext = Extension(
    name='mollia_window',
    include_dirs=[
        './deps/imgui',
        './deps/imgui/backends',
        './deps/SDL2/include',
    ],
    library_dirs=[
        './deps/SDL2/lib/x64',
    ],
    sources=[
        './mollia_window.cpp',
        './deps/imgui/imgui.cpp',
        './deps/imgui/imgui_draw.cpp',
        './deps/imgui/imgui_demo.cpp',
        './deps/imgui/imgui_tables.cpp',
        './deps/imgui/imgui_widgets.cpp',
        './deps/imgui/backends/imgui_impl_sdl.cpp',
        './deps/imgui/backends/imgui_impl_opengl3.cpp',
    ],
    libraries=['User32', 'Gdi32', 'Shell32', 'OpenGL32', 'SDL2'],
    # extra_compile_args=['/Z7'],
    # extra_link_args=['/DEBUG:FULL'],
)

data_files = ['mollia_window.pyi']

data_files.append('SDL2.dll')

setup(
    name='mollia_window',
    version='2.0.0',
    author='Mollia Zrt.',
    license='MIT',
    ext_modules=[ext],
    data_files=[('.', data_files)],
)
