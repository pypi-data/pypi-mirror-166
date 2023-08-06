"""file that stores the main bot runner code"""

import urllib.parse
import re
from .client import Client
from .links import links
from typing import (Callable as Function,
                    Any,
                    Dict,
                    Tuple,
                    get_type_hints,
                    List)
from flask import Flask, render_template
from waitress import serve
from .logging import logging

app = Flask(__name__)
_started_buttons = {}

@app.route('/<command>/<user>/<choice>')
def _parse_button_commands(command, user, choice):
    global _started_buttons
    _started_buttons[command][user] = choice
    return render_template("index.html", html="<h1>your request has been processed, you can close this tab</h1>")

class Button:
    def __init__(self, user: str, command: str):
        self.choice = None
        self.user = user
        self.command = command
        self.cache = {}

    def __getattr__(self, key: str):
        global _started_buttons
        if (self.command not in _started_buttons): _started_buttons[self.command] = {}
        _started_buttons[self.command].update({
            self.user: None
        })
        parsed = f"{self.command}/{self.user}/{urllib.parse.quote(key)}"
        # https://stackoverflow.com/questions/3303312/how-do-i-convert-a-string-to-a-valid-variable-name-in-python (re.sub, varStr -> text)
        var_name = re.sub('\W|^(?=\d)','_', key).lower()
        self.cache[var_name] = f"[{key}]({links.docs}/{parsed})"

        return self.cache[var_name]

    def get_choice(self):
        while (_started_buttons[self.command][self.user] is None): pass
        return _started_buttons[self.command][self.user]

class Bot(Client):
    """main bot object"""
    def __init__(self, token: str, bio: str = "") -> None:
        super()
        super().__init__(token)
        """init, please include name of bot (the username)"""
        self.commands = {
            "help": {
                "call": lambda ctx: ctx.reply(f"the docs are here {links.docs}"),
                "desc": "See commands",
                "name": "help",
                "params": {}
            }
        }
        self.token = token
        self.logging = logging
        self.bio = bio
        self.alias = {}
        self._call_when_followed = lambda ctx, person_who_followed: None

    def command(self, name: str, desc: str = None, alias: List[str] = []):
        """takes in args"""
        def wrapper(func: Function[..., Any]) -> Function[..., Any]:
            """adds to command list"""
            self.commands[name] = {
                "call": func,
                "desc": desc,
                "name": name,
                "params": get_type_hints(func)
            }
            for i in alias:
                self.alias[i] = name
        return wrapper

    def follower(self, func):
        self._call_when_followed = func
    
    def parse_command(self, command: str) -> Dict[str, Any]:
        """parses command

        ```@Example-Bot
        /hello
        message:hi!
        ```
        ->
        {
            "options": {
                "message": "hi!"
            },
            "ping statement": "@Example-Bot",
            "command": "hello"
        }
        
        """
        splited = command.split('\n')
        if (len(splited) < 2):
            return {}
            
        output = {
            "options": {},
            "ping statement": splited[0],
            "command": splited[1].lstrip("/"),
        }
        for i in splited[2:]:
            option, value = i.split(":")
            output["options"][option.strip(" ")] = value.strip(" ")
        return output

    def valid_command(self, resp: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """validates command. Returns true if is valid `(True, parsed_json)` or false if not `(False, {'None': None})"""
        if (resp == {} or resp["comment"] == None):
            return (False, {"None": None})
        parsed = self.parse_command(resp["comment"]["body"])
        if (parsed != {} or
            parsed["ping statement"] != self.user.username):
                return (False, {"None": None})
        return (True, parsed)

    def get_kwargs(self, resp: Dict[str, Any], given_params: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        """get arguements based on type hints of function"""
        params = resp["params"]
        output = {}
        for i in params:
            if (i in given_params):
                output[i] = given_params[i]
            elif (not params[i].required):
                output[i] = params[i].default
            else:
                return (False, {"None": None})
        return (True, output)

    def create_docs(self) -> None:
        html = f"""<center><h1>Commands are as followed</h1></center>
<pre><code>@{self.user.username}
/command-here
param1:here
param2:here
</code>
</pre>
<hr><center><h1>Commands</h1></center><blockquote>{self.bio}</blockquote><hr>""".strip()
        for i in self.commands:
            data = self.commands[i]
            html += f"""<center><h2>/{data['name']} parameters</h2></center><blockquote>{data['desc']}</blockquote>""".strip()
            current_json = {}
            for j in data["params"]:
                _param = data['params'][j]
                current_json[j] = (_param.default if not _param.required else None)
                html += f"""<li>{j}</li>
<ul>
    <li>Description:<pre class = "tab">    {_param.desc.strip()}</pre></li>
    <li>required = {_param.required}</li>
    <li>default = {_param.default}</li>
</ul>""".strip()
            
        @app.route('/')
        def _() -> None:
            return render_template("index.html", html=html)

    def run(self) -> None:
        """mainest runner code"""
        self.once("ready", lambda: None)
        self.create_docs()

        def _run(notif) -> None:
            """main runner code"""
            if (getattr(notif, "comment", False)):
                notif.comment.author = notif.comment.user
                notif.comment.author.mention = "@" + notif.comment.author.username
                parsed_json = self.parse_command(notif.comment.body)
                if ("command" in parsed_json and (parsed_json["command"] in self.commands or parsed_json["command"] in self.alias)):
                    c = parsed_json["command"]
                    if (parsed_json["command"] in self.alias):
                        c = self.alias[c]
                    valid, kwargs = self.get_kwargs(self.commands[c], parsed_json['options'])
                    if (valid):
                        notif.comment.button = Button(notif.comment.user.username, c)
                        
                        logging.success("successful command")
                        self.commands[c]["call"](notif.comment, **kwargs)
                    else:
                        logging.error("unsuccessful command")
                        notif.comment.reply(f"please include all required params. You can check the bot docs here {links.docs}")
                elif ("command" in parsed_json):
                    logging.error("unsuccessful command")
                    notif.comment.reply(f"That is not a valid command. You can see the bot docs here {links.docs}")
        
        self.on("notification", _run)
        self.user.notifications.startEvents()
        serve(app, host="0.0.0.0", port=8080)