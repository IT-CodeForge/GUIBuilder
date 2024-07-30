from multiprocessing import freeze_support
from os import devnull, path
import sys
from traceback import format_exc
from exceptions import UserError
from steuerung import Steuerung
from jk.msgbox import MSGBoxStream

version = "2.0_pre-2"
dir_root: str  # path to root dir (project folder / folder of exe)
internal_dir_root: str  # path to internal root dir (project folder / folder of unpacked files)
additional_files_path: str


def generate_error(e: UserError):
    if not getattr(sys, "frozen", False):
        try:
            raise e
        except:
            print(format_exc(), file=sys.stderr)
            return
    print(f"en:\n{e.err_en}\n\ndt:\n{e.err_dt}", file=sys.stderr)


def __main():
    import main
    freeze_support()  # must be called to ensure that multiprocessing works correctly if packaged to exe (ignored when run as script)

    # fixes problem when application is ran without console (because then sys.stdout and sys.stderr are nonexisting and any print() etc. raises an Error)
    if sys.stdout is None:  # type:ignore
        sys.stdout = open(devnull, "w")  # redirects output to void
    if sys.stderr is None:  # type:ignore
        sys.stderr = MSGBoxStream()  # redirects errors to MSGBox

    # Überprüft ob es als exe oder als py-script vorliegt
    if not getattr(sys, "frozen", False):
        main.dir_root = path.abspath(path.join(path.split(path.abspath(__file__))[0], ".."))
        main.internal_dir_root = main.dir_root
    else:
        main.dir_root = path.split(path.abspath(sys.executable))[0]
        main.internal_dir_root = str(sys._MEIPASS)  # type:ignore
    main.additional_files_path = path.abspath(f"{main.internal_dir_root}\\additional_files")

    print("\n"*20)
    s = Steuerung()
    s.run()


if __name__ == "__main__":
    try:
        __main()
    except UserError as e:
        try:
            generate_error(e)
        finally:
            sys.exit()
