from typing import List, Union, Tuple
import os, sys, re
from .ux import wrapStyle, codeStyle

ALLOWED_PY_VERSIONS = ['3.6', '3.7', '3.8', '3.9', '3.10']


def _listInstalledPackages():
  pkgList: List[str] = []
  pkgLines = os.popen("pip list").read().strip().split("\n")
  for pkgLine in pkgLines:
    parts = re.split(r'\s+', pkgLine)
    pkgList.append("==".join(parts).lower())
  return pkgList


# Returns List[(desiredPackage, installedPackage|None)]
def listMissingPackages(
    deploymentPythonPackages: Union[List[str], None]) -> List[Tuple[str, Union[str, None]]]:
  missingPackages: List[Tuple[str, Union[str, None]]] = []

  if deploymentPythonPackages is None or len(deploymentPythonPackages) == 0:
    return missingPackages

  installedPackages = _listInstalledPackages()
  for dpp in deploymentPythonPackages:
    if dpp not in installedPackages:
      similarPackage: Union[str, None] = None
      dppNoVersion = dpp.split("=")[0].lower()
      for ip in installedPackages:
        if ip.startswith(dppNoVersion):
          similarPackage = ip
      missingPackages.append((dpp, similarPackage))

  return missingPackages


def getInstalledPythonVersion():
  installedVer = f"{sys.version_info.major}.{sys.version_info.minor}"
  return installedVer


def mismatchedPackageWarning(desiredPackage: str, similarPackage: str):
  pipInstall = f"!pip install {desiredPackage}"
  deployPkg = f'mb.deploy(my_deploy_function, <b>python_packages=["{similarPackage}"]</b>)'
  lines: List[str] = [
      f'You chose {wrapStyle(desiredPackage, codeStyle())} for your production environment, but you have {wrapStyle(similarPackage, codeStyle())} locally.',
      f'To match your environment to production, run:',
      f'<div style="padding-left: 15px;">{wrapStyle(pipInstall, codeStyle())}</div>',
      f'To match production to your local environment, include this line in your deployment:',
      f'<div style="padding-left: 15px;">{wrapStyle(deployPkg, codeStyle(), False)}</div>',
  ]
  lines = [f'<div>{ln}</div>' for ln in lines]
  return "".join(lines)


def differentPythonVerWarning(desiredVersion: str, localVersion: str):
  deployVer = f'mb.deploy(my_deploy_function, <b>python_version=["{localVersion}"]</b>)'
  lines: List[str] = [
      f'You chose {wrapStyle("Python " + desiredVersion, codeStyle())} for your production environment, but you have {wrapStyle("Python " + localVersion, codeStyle())} locally.',
      f'To match production to your local environment, include this line in your deployment:',
      f'<div style="padding-left: 15px;">{wrapStyle(deployVer, codeStyle(), False)}</div>',
      f'To match your local environment to production, consider installing {wrapStyle("Python " + desiredVersion, codeStyle())} locally.'
  ]
  lines = [f'<div>{ln}</div>' for ln in lines]
  return "".join(lines)
