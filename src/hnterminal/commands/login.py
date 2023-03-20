import argparse
from http.client import HTTPSConnection
from urllib import parse
from replbuilder import ReplCommand


def login_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", type=str, help="Your user name")
    parser.add_argument("password", type=str, help="Your password")
    return parser


def login(args, context):
    if context.user_cookie is not None:
        curr_user = context.user_cookie.split("=")[1].split("&")[0]
        if curr_user == args.username:
            print("You are already logged in, nothing to do")
            return
    login_data = parse.urlencode({
        "acct": args.username,
        "pw": args.password
    }).encode()
    try:
        conn = HTTPSConnection("news.ycombinator.com")
        conn.request("POST", "/login", login_data)
        resp = conn.getresponse()
        login_cookie = resp.info().get_all("Set-Cookie")[0]
        user_cookie = login_cookie.split("; ")[0]
        context.store_user_cookie(user_cookie)
        print("Successfully logged in as {}".format(args.username))
    except Exception as e:
        print("Login failed: {}".format(e))
    finally:
        conn.close()


def logout(args, context):
    if context.user_cookie is not None:
        curr_user = context.user_cookie.split("=")[1].split("&")[0]
        print("Logging out as {}".format(curr_user))
        context.store_user_cookie(None)
    else:
        print("Not logged in, nothing to do")


login_command = ReplCommand("login", login_parser(), login, "Login with username and password, this requests a user cookie which is destroyed when the cli exits", use_context=True)
logout_command = ReplCommand("logout", argparse.ArgumentParser(), logout, "Logout, wipes the user cookie", use_context=True)
