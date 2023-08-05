## Cloud Github API

Github Rest API implementation.

## Installing

```shell
pip install cloud-github-api
```

## How To Use

Class Branches match [document branches](https://docs.github.com/en/rest/branches)

Class GitDatabase match [document git](https://docs.github.com/en/rest/git)

Class Pulls match [document git](https://docs.github.com/en/rest/pulls)

Class Repository match [document repository](https://docs.github.com/en/rest/repos)


## Code Example

```python
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from cloud_github.ghe import Branches, GithubUrl, GitDatabase, Pulls


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    url = "git.toolsfdg.net/cloud_github/v3"
    owner = "wilfred-y"
    repo = "cloud-android"
    username = "wilfred-y"
    password = "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"
    repo = GithubUrl(url, owner, repo, username, password)
    branches = Branches(repo)
    branch = branches.get_branch("developer")
    branch_sha = branch["commit"]["sha"]
    db = GitDatabase(repo)
    blob = db.create_blob("hello")
    new_tree = {"path": "test.txt", "mode": "100644", "type": "blob", "sha": blob["sha"]}
    tree = db.create_tree(branch_sha, [new_tree])
    commit = db.create_commit(branch_sha, tree["sha"], "test commit")

    branch = branches.get_branch("test")
    if "name" in branch:
        db.update_ref(commit["sha"], "refs/heads/test")
    else:
        db.create_ref(commit["sha"], "refs/heads/test")
    pull = Pulls(repo)
    pull.create_pr("test pr", "test pr", "test", "developer")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

```