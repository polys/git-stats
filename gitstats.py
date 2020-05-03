import csv
import subprocess
import sys
import time


SEC_IN_DAY = 60 * 60 * 24


def get_list_from_stdout(cwd, args):
    # print(' '.join(args), file=sys.stderr)
    process = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE)
    stdout, _ = process.communicate()
    return [s for s in stdout.decode('utf8').split('\n') if len(s)]


def get_tags(cwd):
    return get_list_from_stdout(
        cwd,
        ['git', 'tag', '--list', '--sort=version:refname'])


def get_unmerged_remote_branches(cwd, release_branch):
    return get_list_from_stdout(
        cwd,
        ['git', 'branch', '--list', '--remotes',
         '--sort=-committerdate',
         f'--no-merged={release_branch}',
         '--format=%(refname)'])


def get_age_of_oldest_commit_between_tags(cwd, from_commit, to_commit):
    str_unix_times = get_list_from_stdout(
        cwd,
        ['git', 'log', f'{from_commit}..{to_commit}', '--format=tformat:%ct'])
    dates = [int(t) for t in str_unix_times if len(t) > 0]
    min_date = min(dates) if len(dates) else None
    max_date = max(dates) if len(dates) else None
    age_days = (max_date - min_date) / SEC_IN_DAY if min_date else 0
    return age_days, min_date, max_date


if __name__ == '__main__':
    RELEASE_BRANCH = 'origin/master'

    cwd = sys.argv[1] if len(sys.argv) > 1 else None
    release_branch = sys.argv[2] if len(sys.argv) > 2 else RELEASE_BRANCH

    csv_writer = csv.writer(sys.stdout, dialect='unix')
    csv_writer.writerow(['From', 'To', 'Age (days)'])

    tags = get_tags(cwd)
    for i in range(1, len(tags)-1):
        from_tag = tags[i-1]
        to_tag = tags[i]
        age_days, _, _ = get_age_of_oldest_commit_between_tags(
            cwd, from_tag, to_tag)
        csv_writer.writerow([from_tag, to_tag, round(age_days, 1)])

    csv_writer.writerow([])

    unmerged_branches = get_unmerged_remote_branches(cwd, release_branch)
    for branch in unmerged_branches:
        _, _, max_date = get_age_of_oldest_commit_between_tags(cwd, '', branch)
        date_now = time.time()
        age_days = (date_now - max_date) / SEC_IN_DAY if max_date else 0
        csv_writer.writerow([branch, '', round(age_days)])
