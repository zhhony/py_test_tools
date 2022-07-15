from pathlib import Path
import pandas as pd

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def isNotIn(path: Path, ignorePathList: list) -> bool:
    for ignorePath in ignorePathList:
        if str(path).find(str(Path(ignorePath))) == 0:
            return False
    return True


def getFileSet(path: str, fileTypeList: list, ignoreFileList: list, ignorePathList: list) -> set:
    fileSet = set()
    for filetype in fileTypeList:
        # 获取路径下的文件
        fileiter = Path(path).glob('**/*' + filetype)
        # 将文件装入集合
        fileSet.update(set([i for i in fileiter]))

    if ignoreFileList:
        fileSet = set([i for i in fileSet if i.name not in ignoreFileList])

    if ignorePathList:
        fileSet = set(
            [i for i in fileSet if isNotIn(i.parent, ignorePathList)])

    return fileSet


def CodeStatistics(path, fileTypeList, ignoreFileList, ignorePathList):
    content = []

    PathDirsPYFiles = getFileSet(
        path, fileTypeList, ignoreFileList, ignorePathList)

    for PathDirsPYFile in PathDirsPYFiles:
        f = open(str(PathDirsPYFile), 'r', encoding='utf-8')
        cont = f.read()
        content.append([PathDirsPYFile, len(
            cont.encode('utf-8')), cont.count('\n')])

    df = pd.DataFrame(data=content, columns=['路径', '总字符数', '总行数'])
    df.sort_values(by='路径', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
