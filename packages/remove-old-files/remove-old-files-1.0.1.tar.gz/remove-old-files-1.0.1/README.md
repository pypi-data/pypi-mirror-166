# Remove old files

`remove-old-files` is simple utility to clear folder for example with daily database dumps and leave only 3 newest.

```bash
remove-old-files --help
```
```
usage: remove-old-files [-h] -x REMOVE_OLDER_THAN [-o] [-m FILE_MASK] [-d] folder

Removing files from folder which have modify file date older than X days.

positional arguments:
  folder                Directory where are files to be removed located.

optional arguments:
  -h, --help            show this help message and exit
  -x REMOVE_OLDER_THAN, --older-than REMOVE_OLDER_THAN
                        Remove files older than X (s)econds/(m)inutes/(h)ours/(D)ays. Example: 3D for 3 days.
  -o, --only-if-newer   Remevove older files than X smhD only if there are any newer files found.
  -m FILE_MASK, --file-mask FILE_MASK
                        Regexp matching filenames for removing. Example: ".*-db-dump-.*"
  -d, --dry-run         Dry run, withouth removing files.

```

Example how to leave only 3 days old dumps
```bash
remove-old-files -x 3D -o /dumps
```