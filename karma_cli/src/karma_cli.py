#! /usr/bin/python3

import argparse
import datetime
import yaml
import getpass
import os
import requests


class COLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_error(error):
    print(COLORS.FAIL + COLORS.BOLD + error + COLORS.ENDC)


parser = argparse.ArgumentParser(description="Command Line Interface for 'Karma - Real Internet Points'")

subparsers = parser.add_subparsers(title="command", description="command which shall be performed", dest="command")

parser_add = subparsers.add_parser("add", help="add karma to your account")
parser_add.add_argument("points", type=int, help="number of karma points to add")
parser_add.add_argument("-p", "--project", default="", dest="project", help="project to which karma is added",
                        required=False)
parser_add.add_argument("-c", "--category", default="", dest="category", help="category to which karma is added",
                        required=False)
parser_add.add_argument("-t", "--time", default="", dest="time", help="time at which to add karma", required=False)
parser_add.add_argument("-d", "--description", default="", dest="description", help="description of what you have done",
                        required=False)

parser_get = subparsers.add_parser("get", help="get karma of an account or category over a duration")

parser_get.add_argument("-p", "--project", nargs="?", default="", dest="project", help="which project's karma score",
                        required=False)
parser_get.add_argument("-c", "--category", nargs="?", default="", dest="category", help="category of karma score",
                        required=False)
parser_get.add_argument("-d", "--days", nargs="?", default="", dest="days", help="days of karma score",
                        required=False)

parser_login = subparsers.add_parser("login",
                                     help="login to your account and create a token for authentication, do this first")

parser_config = subparsers.add_parser("config", help="configure defaults")
parser_config.add_argument("-p", "--project", default=False, action="store_true", help="set the default project",
                           required=False)
parser_config.add_argument("-c", "--category", default=False, action="store_true", help="set the default category",
                           required=False)
parser_config.add_argument("-d", "--delete", default=False, action="store_true",
                           help="delete default category and project", required=False)

parser_hs = subparsers.add_parser("highscore", help="get the highscore")
parser_hs.add_argument("days", type=int, help="days of the highscore")
parser_hs.add_argument("-p", "--project", nargs="?", default="", dest="project", help="which project's karma score",
                       required=False)
args = parser.parse_args()

base_url = "https://karma.bit-bots.de/api/"

config_dir = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
config_path = os.path.join(config_dir, "karma")
config = {}
try:
    f = open(config_path, mode='r')
    config = yaml.load(f, Loader=yaml.Loader)
    f.close()
except FileNotFoundError:
    if args.command != "login":
        print("Please login before any other command")
        exit(1)


def write_config():
    try:
        f = open(config_path, "w+")
        yaml.dump(config, f)
        f.close()
    except Exception as ex:
        print(ex)
        exit(1)


def check_projects_or_categories(user_selection, available_selections, name, check_default=True):
    available = False
    selected_name = None
    if user_selection in available_selections:
        available = True
        selected_name = args.project
    elif user_selection != "":
        print("The " + name + " you have chosen is not available.")

    if not available:
        if "default_" + name in config and check_default:
            return config["default_" + name]
        print("Available " + name + ":")
        for n, proj in enumerate(available_selections):
            print(COLORS.OKBLUE + COLORS.BOLD + "[{}] ".format(n) + COLORS.ENDC + proj)

        selected = input("Select a " + name + COLORS.OKBLUE
                         + COLORS.BOLD + " [0..{}]".format(len(available_selections) - 1)
                         + COLORS.ENDC + ": ")
        try:
            selected = int(selected)
        except ValueError as ex:
            print_error("Invalid input")
            exit(1)
        if not selected >= 0 or not selected < len(available_selections):
            print_error("Input out of range")
            exit(1)
        selected_name = available_selections[selected]

    return selected_name


def get_time():
    date_time_obj = None
    if args.time != "":
        try:
            date_time_obj = datetime.datetime.strptime(args.time, '%Y-%m-%d %H:%M')
        except ValueError:
            try:
                entered_time = datetime.datetime.strptime(args.time, '%d %H:%M')
                date_time_obj = datetime.datetime.now().replace(hour=entered_time.hour,
                                                                minute=entered_time.minute,
                                                                day=entered_time.day)
            except ValueError:
                try:
                    entered_time = datetime.datetime.strptime(args.time, '%H:%M')
                    date_time_obj = datetime.datetime.now().replace(hour=entered_time.hour,
                                                                    minute=entered_time.minute)
                except ValueError:
                    print_error("Datetime format not available \n"
                                + "available formats: '%Y-%m-%d %H:%M', '%H:%M', '%d %H:%M'")
                    exit(1)
    else:
        karma_min = datetime.timedelta(minutes=args.points)
        date_time_obj = datetime.datetime.now() - karma_min
    return date_time_obj


def get_available_projects_and_categories():
    resp = requests.get(base_url + "projects/",
                        headers={'Authorization': f"Token {config['token']}"})
    if resp.status_code == 200:
        d = resp.json()
        return {project['name']: project['categories'] for project in d}
    else:
        print_error("Failed to get projects for user")


if args.command == "login":
    user = input("Enter Username: ")
    password = getpass.unix_getpass("Enter Password: ")
    resp = requests.post(base_url + "auth/", data={"username": user, "password": password})
    if resp.status_code == 200:
        config['token'] = resp.json()['token']
        write_config()
        print(f"{COLORS.BOLD}{COLORS.OKGREEN}Login Successful{COLORS.ENDC}")
    else:
        print_error("Login not successful:")
        print_error(f"Server returned {resp.status_code}")
        print(COLORS.FAIL + resp.text + COLORS.ENDC)

elif args.command == "add":
    projects_and_categories = get_available_projects_and_categories()
    projects = list(projects_and_categories.keys())
    project = check_projects_or_categories(args.project, projects, "project")
    categories = projects_and_categories[project]
    category = check_projects_or_categories(args.category, categories, "category")
    time = get_time()
    if args.description == "":
        description = input("Enter a description of what you have done: ")
    else:
        description = args.description

    yes = input(f"Project: {project} || Category: {category} || Datetime: {time.strftime('%y-%m-%d %H:%M')} || "
                f" Karma: {args.points} || Description: {description} {COLORS.BOLD} {COLORS.OKBLUE}[Y/n] {COLORS.ENDC}")
    if yes == "" or yes == "y" or yes == "Y":

        resp = requests.post(base_url + "karma/",
                             headers={'Authorization': f"Token {config['token']}"},
                             data={"project": project, "category": category, "time": time.isoformat(),
                                   "description": description, "points": args.points})
        if resp.status_code == 201:
            print(f"{COLORS.OKGREEN}{COLORS.BOLD}Karma has been added successfully{COLORS.ENDC}")
        else:
            print_error("Failed to add karma")
            print_error(f"Server returned {resp.status_code}")
    else:
        print_error("Aborted adding karma")
elif args.command == "get":
    print_error("not implemented yet :D")
    """resp.json()
    project = check_projects_or_categories(args.project, get_available_projects(), "project")
    if args.category != "":
        category = check_projects_or_categories(args.category, get_available_categories(), "category")
    else:
        category = ""
    resp = requests.get("https://karma.bit-bots.de/api/karma/",
                        headers={'token': config['token']}, params={"project": project})
    """
elif args.command == "config":
    if args.delete:
        try:
            del config['default_project']
            print(f"{COLORS.BOLD}{COLORS.OKGREEN}Deleted default project settings.{COLORS.ENDC}")
        except KeyError:
            print("No default project setting found")
        try:
            del config['default_category']
            print(f"{COLORS.BOLD}{COLORS.OKGREEN}Deleted default project settings.{COLORS.ENDC}")
        except KeyError:
            print("No default category setting found")
        write_config()
        exit(0)
    projects_and_categories = get_available_projects_and_categories()
    if args.project:
        projects = list(projects_and_categories.keys())
        config["default_project"] = check_projects_or_categories(args.project, projects, "project",
                                                                 check_default=False)
        if args.category:
            categories = projects_and_categories[config["default_project"]]
            config["default_category"] = check_projects_or_categories(args.category, categories, "category",
                                                                      check_default=False)
    write_config()
elif args.command == "highscore":
    projects_and_categories = get_available_projects_and_categories()
    projects = list(projects_and_categories.keys())
    project = check_projects_or_categories(args.project, projects, "project")
    resp = requests.get(base_url + "highscore/",
                        headers={'Authorization': f"Token {config['token']}"},
                        params={"project": project, "days": args.days})
    resp_dict = resp.json()
    karma_sorted = [(k, resp_dict[k]) for k in sorted(resp_dict, key=resp_dict.get, reverse=True)]
    for name, value in karma_sorted:
        print("* " + name + " " * (15 - len(name) - len(str(value))) + str(value))
