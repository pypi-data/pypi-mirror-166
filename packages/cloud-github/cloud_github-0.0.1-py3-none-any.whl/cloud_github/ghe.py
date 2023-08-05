import requests
import json

from . import logger


class GithubUrl:
    def __init__(self, url: str, owner: str, repo: str, username: str, token: str):
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        self.repo_url = f"https://{username}:{token}@{url}/repos/{owner}/{repo}"


class GithubCore:

    def __init__(self, url: GithubUrl):
        """
        :param url:
        """
        self.repo_url = url.repo_url
        self.headers = url.headers


class Branches(GithubCore):

    def get_branch(self, branch_name: str):
        """
        :param branch_name:
        :return:
        https://docs.github.com/en/rest/branches/branches#get-a-branch
        """
        url = f"{self.repo_url}/branches/{branch_name}"
        logger.p(f"get_branch: {url}")
        response = requests.get(url, headers=self.headers)
        logger.p(response.json())
        return response.json()

    def merge_upstream(self, branch_name: str):
        """
        Sync a branch of a forked repository to keep it up-to-date with the upstream repository.
        :return:
        https://docs.github.com/en/rest/branches/branches#sync-a-fork-branch-with-the-upstream-repository
        """
        url = f"{self.repo_url}/merge-upstream"
        merge_upstream = {
            "branch": branch_name
        }
        logger.p(f"merge_upstream: {url} \n {json.dumps(merge_upstream)}")
        response = requests.post(url, data=json.dumps(merge_upstream), headers=self.headers)
        logger.p(response.json())
        return response.json()


class GitDatabase(GithubCore):

    def create_blob(self, content: str, encoding: str = "utf-8"):
        """
        :return:
        https://docs.github.com/en/rest/git/blobs#create-a-blob
        """
        logger.p("create_blob: " + content)
        response = requests.post(f"{self.repo_url}/git/blobs",
                                 data=json.dumps({"content": content, "encoding": encoding}),
                                 headers=self.headers)
        logger.p(response.json())
        return response.json()

    def get_blob(self, file_sha):
        """
        :param file_sha:
        :return:
        https://docs.github.com/en/rest/git/blobs#get-a-blob
        """
        url = f"{self.repo_url}/git/blobs/{file_sha}"
        logger.p(f"get_blob: {url} \n {file_sha}")
        response = requests.get(url, headers=self.headers)
        logger.p(response.json())
        return response.json()

    def get_tree(self, tree_sha: str):
        """
        :param tree_sha:
        :return:
        https://docs.github.com/en/rest/git/trees#get-a-tree
        """
        url = f"{self.repo_url}/git/trees/{tree_sha}"
        logger.p(f"get_tree: {url} \n {tree_sha}")
        response = requests.get(url, headers=self.headers)

        logger.p(json.dumps(response.json()))
        return response.json()

    def create_tree(self, base_tree: str, tree: list):
        """
        :param base_tree:
        :param tree:
        :return:
        https://docs.github.com/en/rest/git/trees#create-a-tree
        """
        url = f"{self.repo_url}/git/trees"
        new_tree = {"base_tree": base_tree,
                    "tree": tree}
        logger.p(f"create_tree: {url} \n {json.dumps(new_tree)}")
        response = requests.post(f"{self.repo_url}/git/trees",
                                 data=json.dumps(new_tree),
                                 headers=self.headers)
        logger.p(response.json())
        return response.json()

    def get_commit(self, commit_sha=""):
        """
        :param commit_sha:
        :return:
        https://docs.github.com/en/rest/git/commits#get-a-commit
        """
        url = f"{self.repo_url}/git/commits/{commit_sha}"
        logger.p(f"get_commit: {url} \n {commit_sha}" + commit_sha)
        response = requests.get(url, headers=self.headers)
        logger.p(response.json())
        return response.json()

    def create_commit(self, parent_sha, tree_sha, msg):
        """
        :param parent_sha:
        :param tree_sha:
        :param msg:
        :return:
        https://docs.github.com/en/rest/git/commits#create-a-commit
        """
        commit = {
            "parents": [parent_sha],
            "tree": tree_sha,
            "message": msg
        }
        url = f"{self.repo_url}/git/commits"
        logger.p(f"create_commit: {url} \n {json.dumps(commit)}")
        response = requests.post(url, data=json.dumps(commit), headers=self.headers)
        logger.p(response.json())
        return response.json()

    def get_ref(self, ref_name="heads/developer"):
        """
        :param ref_name:
        :return:
        https://docs.github.com/en/rest/git/refs#get-a-reference
        """
        url = f"{self.repo_url}/git/ref/{ref_name}"
        logger.p(f"get_ref: {url} \n {ref_name}")
        response = requests.get(url, headers=self.headers)
        logger.p(response.json())
        return response.json()

    def create_ref(self, commit_sha: str, ref_name: str):
        """
        :param ref_name:
        :param commit_sha:
        :return:
        https://docs.github.com/en/rest/git/refs#create-a-reference
        """
        url = f"{self.repo_url}/git/refs"
        ref = {
            "sha": commit_sha,
            "ref": ref_name
        }
        logger.p(f"creat_ref: {url} \n {json.dumps(ref)}")
        response = requests.post(url, data=json.dumps(ref), headers=self.headers)
        logger.p(response.json())
        return response.json()

    def update_ref(self,
                   commit_sha="",
                   ref_name="",
                   force=True):
        """
        :param force:
        :param ref_name:
        :param commit_sha:
        :return:
        https://docs.github.com/en/rest/git/refs#update-a-reference
        """
        url = f"{self.repo_url}/git/{ref_name}"
        ref = {
            "force": force,
            "sha": commit_sha
        }
        logger.p(f"update_ref: {url} \n {json.dumps(ref)}")
        response = requests.post(url, data=json.dumps(ref), headers=self.headers)
        logger.p(response.json())
        return response.json()


class Pulls(GithubCore):

    def list_pr(self, head: str = None):
        """
        :return:
        https://docs.github.com/en/rest/pulls/pulls#list-pull-requests
        """
        url = f"{self.repo_url}/pulls"
        logger.p("list_pr: ")
        params = None
        if head is not None:
            params = {"head": head}
        response = requests.get(url, params=params, headers=self.headers)
        logger.p(response.json())
        return response.json()

    def create_pr(self,
                  title,
                  body,
                  head_branch_name,
                  base_branch_name):
        """
        :param title:
        :param body:
        :param head_branch_name:
        :param base_branch_name:
        :return:
        https://docs.github.com/en/enterprise-server@3.5/rest/pulls/pulls#create-a-pull-request
        """
        url = f"{self.repo_url}/pulls"
        pull = {
            "title": title,
            "body": body,
            "head": head_branch_name,
            "base": base_branch_name
        }
        logger.p(f"create_pr: {url} \n {json.dumps(pull)}")
        response = requests.post(url,
                                 data=json.dumps(pull),
                                 headers=self.headers)
        logger.p(response.json())
        return response.json()

    def list_pr_files(self, pull_num):
        """
        :param pull_num:
        :return:
        https://docs.github.com/en/rest/pulls/pulls#list-pull-requests-files
        """
        url = f"{self.repo_url}/pulls/{pull_num}"
        logger.p(f"list_pr_files: {url}")
        response = requests.get(url, headers=self.headers)
        logger.p(response.json())
        return response.json()

    def create_review(self, pull_number: str, commit_id: str = None, body: str = None, event: str = "COMMENT",
                      comments: list = None):
        """
        :param pull_number:
        :param commit_id:
        :param body:
        :param event:
        :param comments:
        :return:
        https://docs.github.com/en/rest/pulls/reviews#create-a-review-for-a-pull-request
        """
        url = f"{self.repo_url}/pulls/{pull_number}/reviews"
        pr_review = {
            "body": body,
            "event": event
        }
        if commit_id is not None:
            pr_review["commit_id"] = commit_id
        if comments is not None and comments.__len__() > 0:
            pr_review["comments"] = comments
        print(f"create_pr_review: {url} \n {json.dumps(pr_review)}")
        response = requests.post(url, data=json.dumps(pr_review), headers=self.headers)
        print(response.json())
        return response.json()

    def request_reviewers(self, pr_num: str, reviewers: list, team_reviewers: list):
        """
        :param pr_num:
        :param reviewers:
        :param team_reviewers:
        :return:
        https://docs.github.com/en/rest/pulls/review-requests#request-reviewers-for-a-pull-request
        """
        url = f"{self.repo_url}/pulls/{pr_num}/requested_reviewers"
        request_reviewers = {
            "reviewers": reviewers,
            "team_reviewers": team_reviewers
        }
        logger.p(f"request_reviewers: {url} \n {json.dumps(request_reviewers)}")
        response = requests.post(url, data=json.dumps(request_reviewers), headers=self.headers)
        logger.p(response.json())
        return response.json()


class Repository(GithubCore):

    def get_repository(self):
        """
        :return:
        https://docs.github.com/en/rest/repos/repos#get-a-repository
        """
        url = f"{self.repo_url}"
        logger.p(f"get_repository: {url}")
        response = requests.get(url, headers=self.headers)
        logger.p(response.json())
        return response.json()

    def exist_repository(self):
        logger.p("exist_repository: ")
        if "node_id" in self.get_repository():
            logger.p("Yes")
            return True
        else:
            logger.p("No")
            return False

    def create_fork(self):
        """
        :return:
        https://docs.github.com/en/rest/repos/forks#create-a-fork
        """
        url = f"{self.repo_url}/forks"
        logger.p(f"create_fork: {url}")
        response = requests.post(url, headers=self.headers)
        logger.p(response.json())
        return response.json()
