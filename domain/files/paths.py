from pathlib import Path


def resolveWithAbsolutePath(path: str = '.') -> str:
    relativePath = Path(path)
    absolutePath = relativePath.resolve()

    return str(absolutePath)
