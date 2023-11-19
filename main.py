import os
import sys
import shutil
import argparse
from loguru import logger
from soundtype import soundtype

# Arguments handling
parser = argparse.ArgumentParser(
    prog='SampleSorter',
    description='Sort audio samples thanks to key words defined in a Json file',
    epilog='https://github.com/mjarms/SampleSorter',
)
parser.add_argument('-s', '--src', type=str, default=None, help="Source folder path")
parser.add_argument('-d', '--dst', type=str, default=None, help="Chosen destination path")
parser.add_argument('-o', '--one-by-one', action='store_true', help="Ask for each file if you want to copy (can be long)")
parser.add_argument('-nl', '--no-log', action='store_true', help="Use this option to disable logging (not recommanded)")
args = parser.parse_args()


# Source & Destination folders set up
SrcFolder = args.src if args.src else input("Source Folder ? ")
DstFolder = args.dst if args.dst else input("Destination Folder ? ")

# Logger configuration
logger.remove(0)
logger.add(sys.stderr, format="[{level}] {message}", level="SUCCESS")
if not args.no_log:
    logger.add("SampleSorter.log", rotation="5MB", level="INFO")
logger.warning(f"Source folder = {SrcFolder}")
logger.warning(f"Destination Folder = {DstFolder}")


def checkfolders(src,dst) -> None:  # Exit program if folders are not valide 
    logger.info(f"Checking folders")
    if not os.path.exists(src):
        logger.error(f"The src folder '{src}' is not valid. Exit program")
        exit()
    try:
        parent = '\\'.join(dst.split("\\")[:-1])
    except Exception as e:
        logger.error(f"Error in the dst folder : {e}")
    if not os.path.exists(parent):
        logger.error(f"The dst folder '{dst}' is not valid. Exit program")
        exit()


def IsAudioFile(file) -> bool:  # Check if it's audio file
    _, ext = os.path.splitext(file)
    if ext in ['.wav', '.mp3']: return True


def sortsample(src, sorting, name):  # Sort the sample into the right directory
    dst = f"{DstFolder}\\{sorting}\\{name}"
    folder = f"{DstFolder}\\{sorting}"
    logger.info(f"Copy from {src} to {dst}")
    
    try:  # Make dst dir if not exists
        if not os.path.exists(folder):
            logger.info(f"Creating foler : {folder}")
            os.makedirs(folder)
    except Exception as e:
        logger.error(f"Cannot create directory {folder} : {e}")

    try:  # File copy
        shutil.copy2(src, dst)
    except Exception as e:
        logger.error(f"Cannot copy file : {e}")


if __name__ == "__main__":
    checkfolders(SrcFolder, DstFolder)
    if os.path.exists(DstFolder):
        logger.warning(f"The dst folder already exists")
        if input(f"The destination folder {DstFolder} already exists. Are you sure that you want to overwrite it ? You will loose all the files inside ! (y/n)") not in ["y","Y"]:
            logger.warning(f"User Exit")
            exit()
        logger.info(f"Deleting old dst folder")
        try:  # Delete previous dest folder if exist
            logger.warning(f"Removing previous sample folder {DstFolder}")
            shutil.rmtree(DstFolder)
        except Exception as e:
            logger.error(f"Old dst folder cannot be removed : {e}")
            exit()

    for root, dirs, files in os.walk(SrcFolder, topdown=False):  # Recursively read file
        for name in files:  # For each found file
            path = os.path.join(root, name)
            if IsAudioFile(name):  # Is it audio ?
                sample_obj = soundtype(name, path, logger)  # Sound type class call
                logger.info(f"File {sample_obj.path} classified as {sample_obj.type}")
                sortsample(sample_obj.path, sample_obj.sorting, sample_obj.name)  # Sorting
                # input("...")  # One by one
            else:
                logger.warning(f"{path} is not an audio file")
