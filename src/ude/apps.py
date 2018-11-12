APP_PREFIX = "app_"
DEFAULT_APP_FILE = "default_app.txt"


def main():
    """ Scans main directory for "app_*" files and treat them as
    applications, i.e. something which can be imported executed via its main()
    method and cleaned after via its finish() method
    """

    import os

    prefix = "app_"
    default_app_file = "default_app.txt"

    dir_entries = os.listdir()

    apps = [app for app in os.listdir() if app.startswith(APP_PREFIX)]

    if len(apps) < 1:
        print("No applications found (files starting with {}) - so nothing to select".format(APP_PREFIX))
        return

    def show_apps():
        print("Found {} application(s):".format(len(apps)))

        for idx, name in enumerate(apps, 1):
            print("{} -> {}".format(idx, name))

        print("To make an app automatically started - save its name to {}".format(DEFAULT_APP_FILE))
        print("To turn off automatic start of an app - remove {}".format(DEFAULT_APP_FILE))

    show_apps()

    default_app_idx = None
    if default_app_file in dir_entries:
        try:
            f = open(DEFAULT_APP_FILE)
            default_app = f.read().strip()
            # find its index, add 1 (since we enumerate from 1) and convert to string, since it
            # will be injected as user input
            default_app_idx = str(apps.index(default_app) + 1) # we enumerate from 1
        except:
            default_app_idx = None
        finally:
            f.close()

    while True:
        print("Select application (by number) to run or 0 to skip:")
        try:
            if default_app_idx is not None:
                print("USING DEFAULT APP {}".format(default_app_idx))
                user_input = default_app_idx
                default_app_idx = None
            else:
                user_input = input("Your choice > ")
        except EOFError:
            show_apps()
            continue

        if user_input.isdigit():
            app_idx = int(user_input)
            if app_idx >= 0 and app_idx <= len(apps):
                break

    if app_idx == 0:
        print("OK - doing nothing")
    else:
        app_idx -= 1
        app_name = apps[app_idx].rstrip(".py")
        print("Loading module {} and running its main()".format(app_name))
        mod = __import__(app_name)
        try:
            mod.main()
        except KeyboardInterrupt:
            print("Interrupted")

        try:
            mod.finish()
        except:
            pass


def set_default(a_name):
    import os

    apps = [ n for n in os.listdir() if n.startswith(APP_PREFIX)]

    if a_name in apps:
        f = open(DEFAULT_APP_FILE, "w")
        f.write(a_name)
        f.close()
        print("Default app saved")
    else:
        print("App not found in: {}".format(" ".join(apps)))


def remove_default():
    import os

    try:
        os.remove(DEFAULT_APP_FILE)
        print("Default app starting - removed")
    except:
        pass


if __name__ == "__main__":
    main()
