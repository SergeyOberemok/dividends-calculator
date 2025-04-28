import glob

from .paths import resolveWithAbsolutePath


def findFilesPath(extension: str, path: str = '.') -> list[str]:
    absolutePath = resolveWithAbsolutePath(path)
    path = f'{absolutePath}/*.{extension}'

    existingPaths = glob.glob(path)

    return existingPaths


def findFirstFilePath(extension: str, path: str = '.') -> str:
    existingPaths = findFilesPath(extension, path)

    return existingPaths[0] if len(existingPaths) else None
