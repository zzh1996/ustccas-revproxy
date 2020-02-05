from flask import Flask
from urllib.parse import urlencode
from flask import redirect, request, abort, session
from urllib.request import urlopen
from xml.etree import ElementTree
import os
import uuid


casURL = "https://passport.ustc.edu.cn/login"
validateURL = "https://passport.ustc.edu.cn/serviceValidate"
redirectURL = "http://home.ustc.edu.cn/~zzh1996/cas_redirect.html"
logoutURL = "https://passport.ustc.edu.cn/logout"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]


def check_ticket(ticket, service):
    validate = validateURL + "?" + urlencode({"service": service, "ticket": ticket})
    with urlopen(validate) as req:
        tree = ElementTree.fromstring(req.read())[0]
    cas = "{http://www.yale.edu/tp/cas}"
    if tree.tag != cas + "authenticationSuccess":
        return None
    gid = tree.find("attributes").find(cas + "gid").text.strip()
    user = tree.find(cas + "user").text.strip()
    return user


@app.route("/auth")
def auth():
    if "user" in session:
        return session["user"]
    else:
        return abort(401)


@app.route("/login")
def login():
    if "id" not in session:
        session["id"] = uuid.uuid4().hex
    jump = request.base_url + "?" + urlencode({"id": session["id"]})
    service = redirectURL + "?" + urlencode({"jump": jump})
    ticket = request.args.get("ticket")
    if not ticket:
        return redirect(casURL + "?" + urlencode({"service": service}))
    if request.args.get("id") != session["id"]:
        abort(401)
    user = check_ticket(ticket, service)
    if user:
        session["user"] = user
        return redirect("/")
    else:
        return abort(401)


@app.route("/logout")
def logout():
    if "user" in session:
        del session["user"]
    return redirect(logoutURL)
