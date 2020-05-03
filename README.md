## git-stats

[Git](https://git-scm.com/) is expected to be preinstalled and in `PATH`.

### Usage

Output CSV to `stdout`:
```
python gitstats.py [<path-to-git-repo> [<release-branch>]]
```
`<path-to-git-repo>` defaults to the current working directory;  
`<release-branch>` defaults to `origin/master`

Pipe the output to a CSV file:
```
python gitstats.py > stats.csv
```