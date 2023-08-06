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

class Button:
    def __call__(self, text: str):
        parsed = urllib.parse.quote(text)
        # https://stackoverflow.com/questions/3303312/how-do-i-convert-a-string-to-a-valid-variable-name-in-python (re.sub, varStr -> text)
        setattr(self, re.sub('\W|^(?=\d)','_', text).lower(), f"[{text}]({links.docs}/{parsed})")
        def wrapper(func) -> None:
            def wr1(func):
                def wr2():
                    func()
                    return render_template('index.html', html = "<h1>you can now close this tab! Your request has been processed</h1>")
                wr2.__name__ = text
                return wr2
            _ = wr1(func)
            app.route(f'/{parsed}')(_)
        return wrapper     

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
        self.client = Client(token)
        self.logging = logging
        self.bio = bio
        self.alias = {}

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
            parsed["ping statement"] != self.client.user.username):
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
        html = f"""
<center><h1>Commands are as followed</h1></center>
<pre><code>@{self.client.user.username}
/command-here
param1:here
param2:here
</code>
</pre>
<hr>
<center><h1>Commands</h1></center>
<blockquote>{self.bio}</blockquote>
<hr>
        """.strip()
        for i in self.commands:
            data = self.commands[i]
            html += f"""
<center><h2>/{data['name']} parameters</h2></center>
<blockquote>{data['desc']}</blockquote>
<ul>
            """.strip()
            current_json = {}
            for j in data["params"]:
                _param = data['params'][j]
                current_json[j] = (_param.default if not _param.required else None)
                html += f"""
<li>{j}</li>
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
        self.client.once("ready", lambda: 0)
        self.create_docs()

        def _run(notif) -> None:
            """main runner code"""
            if (getattr(notif, "comment", False)):
                parsed_json = self.parse_command(notif.comment.body)
                if ("command" in parsed_json and (parsed_json["command"] in self.commands or parsed_json["command"] in self.alias)):
                    c = parsed_json["command"]
                    if (parsed_json["command"] in self.alias):
                        c = self.alias[c]
                    valid, kwargs = self.get_kwargs(self.commands[c], parsed_json['options'])
                    if (valid):
                        logging.success("successful command")
                        self.commands[c]["call"](notif.comment, **kwargs)
                    else:
                        logging.error("unsuccessful command")
                        notif.comment.reply(f"please include all required params. You can check the bot docs here {links.docs}")
                elif ("command" in parsed_json):
                    logging.error("unsuccessful command")
                    notif.comment.reply(f"That is not a valid command. You see the bot docs here {links.docs}")
        
        self.client.on("notification", _run)
        self.client.user.notifications.startEvents()
        serve(app, host="0.0.0.0", port=8080)

buttons = Button()