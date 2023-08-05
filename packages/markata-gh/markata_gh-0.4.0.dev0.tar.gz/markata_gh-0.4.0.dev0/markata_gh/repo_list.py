import json
import subprocess

import jinja2
from jinja2 import nodes
from jinja2.ext import Extension

REPO_CARD = jinja2.Template(
    """
## [{{ name }}]({{ url }}) ⭐{{ stargazerCount }}
_Last Updated: {{ updatedAt }}_

{{ description }}
"""
)


def repo_list(username=None, topic=None):
    """
    Gets list of repo data within a username and topic from the gh cli.
    """
    if topic:
        cmd = f"gh repo list {username} --topic {topic} --json name --json url --json updatedAt --json url --json stargazerCount --json issues --json description --json pullRequests --json homepageUrl".split()
    else:
        cmd = f"gh repo list {username} --json name --json url --json updatedAt --json url --json stargazerCount --json issues --json description --json pullRequests --json homepageUrl".split()
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        repos = json.loads(proc.stdout.read())
    proc.kill()
    proc.wait()
    repos.sort(key=lambda repo: repo.get("updatedAt", ""), reverse=True)
    return repos


def repo_md(username=None, topic=None):
    """
    Get's markdown for repos within a github username and topic.
    """
    repos = repo_list(username, topic)
    repo_html = "\n".join([REPO_CARD.render(**repo) for repo in repos])
    return repo_html


def get_value_from_arg(arg):
    if isinstance(arg, jinja2.nodes.Name):
        return arg.name
    if isinstance(arg, jinja2.nodes.Const):
        return arg.value
    if isinstance(arg, jinja2.nodes.Sub):
        return get_value_from_arg(arg.left) + "-" + get_value_from_arg(arg.right)


class GhRepoListTopic(Extension):
    tags = {"gh_repo_list_topic"}

    def __init__(self, environment):
        super().__init__(environment)

    def parse(self, parser):
        line_number = next(parser.stream).lineno
        try:
            args = parser.parse_tuple().items
        except AttributeError:
            raise AttributeError(
                "Invalid Syntax gh_repo_list_topic expects <username>, or <username>,<topic> both must have the comma"
            )
        if len(args) == 1:
            self.username = get_value_from_arg(args[0])
            self.topic = ""
        elif len(args) == 2:
            self.username = get_value_from_arg(args[0])
            self.topic = get_value_from_arg(args[1])
        return nodes.CallBlock(self.call_method("run", []), [], [], "").set_lineno(
            line_number
        )

    def run(self, caller):
        "get's markdown to inject into post"
        return repo_md(username=self.username, topic=self.topic)


if __name__ == "__main__":
    print(repo_md("markata"))
