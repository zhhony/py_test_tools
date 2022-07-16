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


def CodeStatistics(path, fileTypeList: list, ignoreFileList: list, ignorePathList: list) -> pd.DataFrame:
    '''本方法可以用来在给出指定路径下面，解析出指定类型文件的行数和字符数。本方法需要pandas环境，请提前安装。
    path:路径；
    fileTypeList：文件类型清单，可以把需要解析的文件对应的类型放入列表，方法会基于列表寻找文件。范例：fileTypeList = ['.py','.json']；
    ignoreFileList：需要排除的文件清单。如果存在不需要统计的文件，可以用这个参数指定。范例：['abc.py','123.json']
    ignorePathList：需要排除的路径清单。

    '''
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
