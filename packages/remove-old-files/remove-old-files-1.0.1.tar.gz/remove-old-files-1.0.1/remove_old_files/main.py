#! /usr/bin/python3

from argparse import ArgumentParser
import sys
import os
import logging
import re
import datetime


def setup_logging() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    _logger = logging.getLogger(__name__)
    formater = logging.Formatter('%(asctime)s /%(name)s/ [%(levelname)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formater)
    _logger.setLevel(logging.INFO)
    _logger.addHandler(handler)
    _logger.propagate = False
    return _logger


def get_cmd_options() -> object:
    parser = ArgumentParser()
    parser.description = "Removing files from folder which have modify file date older than X days."
    parser.add_argument("folder", type=str, help="Directory where are files to be removed located.")
    parser.add_argument("-x", "--older-than", dest="remove_older_than", type=str, required=True, help="Remove files older than X (s)econds/(m)inutes/(h)ours/(D)ays. Example: 3D for 3 days.")
    parser.add_argument("-o", "--only-if-newer", dest="only_if_newer", default=False, action="store_true", help="Remevove older files than X smhD only if there are any newer files found.")
    parser.add_argument("-m", "--file-mask", dest="file_mask", type=str, default=".*", help="Regexp matching filenames for removing. Example: \".*-db-dump-.*\"")
    parser.add_argument("-d", "--dry-run", dest="dry_run", default=False, action="store_true", help="Dry run, withouth removing files.")

    arguments = parser.parse_args()

    return arguments


class RemoveOldFiles:
    def __init__(self, options: object, logger: logging.Logger):
        self.options: object = options
        self.logger: logging.Logger = logger

    def run(self):
        file_list = self.get_file_list()
        if file_list is None:
            self.logger.error(f"Directory {self.options.folder} does not exist.")
            sys.exit(1)
        elif not file_list:
            self.logger.info(f"No matching '{self.options.file_mask}' files found in folder '{self.options.folder}'.")

        remove_file_list = self.get_file_list_to_remove(file_list)
        if self.options.only_if_newer:
            if len(file_list) == len(remove_file_list):
                remove_file_list = []

        for file in remove_file_list:
            if not self.options.dry_run:
                self.logger.info(f"Removing file '{file}'.")
                os.unlink(file)
            else:
                self.logger.info(f"Dry run ... skiping file '{file}'.")

    def get_file_list(self) -> list:
        if not os.path.exists(self.options.folder):
            return None
        file_list = os.listdir(self.options.folder)
        ret = []
        for file in file_list:
            try:
                if (self.options.file_mask and re.match(self.options.file_mask, file)) or not self.options.file_mask:
                    ret.append(file)
            except Exception as ex:
                self.logger.error(f"Invalid file mask '{self.options.file_mask}': {ex}")
        return ret

    def get_file_list_to_remove(self, file_list: list) -> list:
        ret = []
        older_file_date = self._get_older_file_date()
        for file in file_list:
            file_path = os.path.join(self.options.folder, file)
            file_date = os.path.getmtime(file_path)
            if file_date < older_file_date.timestamp():
                self.logger.info(f"Prepare file '{file}' for removing, it is older than {self.options.remove_older_than}")
                ret.append(file)
            else:
                self.logger.info(f"Skipping file '{file}' it is not older than {self.options.remove_older_than}")
        return ret

    def _get_older_file_date(self) -> tuple:
        find = re.findall(r"^(\d+)([hmsD])$", self.options.remove_older_than)
        if not find:
            self.logger.error("Error while parsing --older-then param. Use number and letter h, m, s or D to specify time period. Example: 3D for 3 days or 5h for 5 hours")
            sys.exit(1)

        time_period, delta_letter = (int(find[0][0]), find[0][1])

        if delta_letter == "h":
            return datetime.datetime.today() - datetime.timedelta(hours=time_period)
        elif delta_letter == "m":
            return datetime.datetime.today() - datetime.timedelta(minutes=time_period)
        elif delta_letter == "s":
            return datetime.datetime.today() - datetime.timedelta(seconds=time_period)
        elif delta_letter == "D":
            return datetime.datetime.today() - datetime.timedelta(days=time_period)

        self.logger.error("No h, m, s or D match to specify time period.")
        sys.exit(1)


def main():
    logger = setup_logging()
    arguments = get_cmd_options()
    remover = RemoveOldFiles(arguments, logger)
    remover.run()
    logger.info("Done.")


if __name__ == '__main__':
    main()
