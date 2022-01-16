import platform, subprocess, tempfile, os, shutil

def get_platform():
    return platform.system()

def is_windows():
    return get_platform().upper() == 'Windows'.upper()


def get_office_cli_path():
    if is_windows():
        if not os.path.exists('C:\Program Files\LibreOffice\program\soffice.exe'):
            raise Exception(f'Could not find LibreOffice. Is it installed?')
        return 'C:\Program Files\LibreOffice\program\soffice'
    else:
        raise Exception('Unsupported platform')


def convert(in_file, out_file=None):
    if not out_file:
        outdir = os.path.dirname(in_file)
    else:
        outdir = tempfile.gettempdir()

    command_line = get_office_cli_path()
    subprocess.call([
        command_line,
        '--headless',
        '--convert-to',
        'pdf',
        '--outdir',
        outdir,
        in_file
    ])

    if out_file:
        out_temp_file_arr = os.path.splitext(in_file)
        out_temp_file_name = f'{os.path.basename(out_temp_file_arr[0])}.pdf'
        out_file = f'{os.path.splitext(out_file)[0]}.pdf'
        shutil.move(os.path.join(outdir, out_temp_file_name), out_file)
