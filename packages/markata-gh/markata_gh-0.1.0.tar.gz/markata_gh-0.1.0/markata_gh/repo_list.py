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


def repo_list(topic=""):
    cmd = f"gh repo list --topic {topic} --json name --json url --json updatedAt --json url --json stargazerCount --json issues --json description --json pullRequests --json homepageUrl".split()
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        repos = json.loads(proc.stdout.read())
    proc.kill()
    proc.wait()
    repos.sort(key=lambda repo: repo.get("updatedAt", ""), reverse=True)
    return repos


def repo_html(topic=""):
    repos = repo_list(topic)
    repo_html = "\n".join([REPO_CARD.render(**repo) for repo in repos])
    return repo_html


class GhRepoListTopic(Extension):
    tags = {"gh_repo_list_topic"}

    def __init__(self, environment):
        super().__init__(environment)

    def parse(self, parser):
        line_number = next(parser.stream).lineno
        topic = [parser.parse_expression()]
        return nodes.CallBlock(self.call_method("brun", topic), [], [], "").set_lineno(
            line_number
        )

    def brun(self, topic, caller):
        return repo_html(topic=topic)


if __name__ == "__main__":
    print(repo_html("markata"))
