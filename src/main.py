
import argparse
from github import Github
from github import GithubException


def get_argument_parser():
    """
    Prepares the argument parser. Command line arguments can be added in this method.
    :return: ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog='license-adder',
        description='Adds licenses to repositories that do not have licenses in a given organization in Github'
    )
    parser.add_argument(
        '-o',
        '--organization',
        action='store',
        dest='organization'
    )
    parser.add_argument(
        '-u',
        '--username',
        action='store',
        dest='username',
        default=None
    )
    parser.add_argument(
        '-p',
        '--password',
        action='store',
        dest='password',
        default=None
    )
    parser.add_argument(
        '-c',
        '--credentials',
        dest='credentials',
        default=None
    )
    parser.add_argument(
        '-l',
        '--license',
        action='store',
        dest='license',
        default='LICENSE'
    )
    parser.add_argument(
        '-b'
        '--base',
        action='store',
        dest='base',
        default='master'
    )
    parser.add_argument(
        '-n',
        '--new-branch',
        action='store',
        dest='head',
        default='license'
    )

    return parser


def get_license(path):
    """
    Consolidates the contents of the given file into a single string
    :param path: path to the license file
    :return: license_content
    """
    with open(path) as license_file:
        return license_file.read().replace('\n', '')


def get_credentials(path):
    """
    Parses the credentials file to get the username and password.
    The credentials file should have the username on the first line and password on the second. All other lines will
    be ignored.
    :param path: the path to the credentials file
    :return: username, password
    """
    with open(path) as credentials_file:
        for index, value in enumerate(credentials_file.readlines()):
            if index == 0:
                username = value.strip()
            if index == 1:
                password = value.strip()
        return username, password


def add_license(repo, license_contents, base, head):
    """
    Branches from base to head, adds the license file, and creates the pull request for the given repo.
    :param repo: the repo that needs a license added
    :param license_contents: the string contents of the license to add
    :param base: the base branch to branch from
    :param head: the new branch
    :return: None
    """
    base_branch = repo.get_branch(base)
    license_branch = repo.create_git_ref('refs/heads/' + head, sha=base_branch.commit.sha)
    repo.create_file("/LICENSE", "Adding License", license_contents, branch=head)
    repo.create_pull(title="License Added", body="Added a license to this repository.", base=base, head=head)


def main():
    """
    The main function of the process. Processes the command line arguments, gets the repos for the given organization,
    and collects the repos missing license. Branches the repo, adds the license, and creates a pull request.
    :return: None
    """
    argparser = get_argument_parser()
    args = argparser.parse_args()

    credentials = args.credentials
    username = args.username
    password = args.password
    base = args.base
    head = args.head
    license_path = args.license

    if credentials is None:
        if username is None or password is None:
            # username and password must both be provided if credentials is None
            pass
    else:
        username, password = get_credentials(credentials)
        if username is None or not username or password is None or not password:
            # username and password must both be provided in credentials file
            pass

    organization_name = args.organization
    if organization_name is None or not organization_name:
        # organization name must be provided
        pass

    if license_path is None or not license_path:
        # license path must be provided
        pass

    license_content = get_license(license_path)
    github_client = Github(username, password)
    organization = github_client.get_organization(organization_name)

    repos_without_licenses = []
    for repo in organization.get_repos():
        try:
            repo.get_license()
        except GithubException:
            repos_without_licenses.append(repo)

    for repo in repos_without_licenses:
        add_license(repo, license_content, base, head)


if __name__ == "__main__":
    main()
