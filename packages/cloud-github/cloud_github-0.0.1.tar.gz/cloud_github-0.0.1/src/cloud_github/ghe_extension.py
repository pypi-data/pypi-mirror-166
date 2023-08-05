import base64

from ghe import Pulls, GithubUrl, GitDatabase


class PRFileFetcher:
    def __init__(self, url: GithubUrl):
        """
        :param url:
        """
        self.pulls = Pulls(url)
        self.gd = GitDatabase(url)

    def get_pr_files_path_content(self, pull_num, file_name):
        pr_files = self.pulls.list_pr_files(pull_num)
        path_content_list = []
        for pr_file in pr_files:
            fn = pr_file["filename"]
            if fn.__contains__(file_name):
                path = fn
                file_sha = pr_file["sha"]
                blob = self.gd.get_blob(file_sha)
                b64_content = blob["content"]
                content = base64.b64decode(b64_content).decode("utf-8")
                path_content_list.append([path, content])
        return path_content_list
