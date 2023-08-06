from typing import Union, List, Dict, Any, Callable, Tuple
import inspect, re, html, json

from .environment import ALLOWED_PY_VERSIONS, getInstalledPythonVersion, listMissingPackages, mismatchedPackageWarning
from .utils import printHtml, printError, unindent
from .helpers import DeploymentTestDef, DeploymentTestError, RuntimeFile, RuntimePythonProps, RuntimeType, getJson, getJsonOrPrintError, isAuthenticated, getDefaultPythonVersion, getDefaultPythonPackages, getDefaultSystemPackages
from .ux import LIST_TITLES_TIPS, LIST_TITLES_WARNINGS, LIST_TITLES_ERRORS, errorStyle, makeHtmlTable, TableHeader, codeStyle, wrapStyle, tipStyle, makeTitledList, textStyle
from .secure_storage import uploadRuntimeObject


class RuntimeStatusNotes:

  def __init__(self, tips: List[str], warnings: List[str], errors: List[str]):
    self.tips = tips
    self.warnings = warnings
    self.errors = errors
    self.deployable = len(errors) == 0

  def statusMsg(self):
    if self.deployable:
      return 'Ready'
    return 'Not Ready'

  def statusStyle(self):
    if self.deployable:
      return "color:green; font-weight: bold;"
    return "color:gray; font-weight: bold;"


class NamespaceCollection:

  def __init__(self):
    self.functions: Dict[str, str] = {}
    self.vars: Dict[str, Any] = {}
    self.imports: Dict[str, str] = {}
    self.froms: Dict[str, str] = {"*": "typing"}


class Runtime:
  _runtimeTypeName = "runtime"

  MAX_REQUIREMENTS_TXT = 20_000
  LAMBDA_RAM_MAX_MB = 10_240
  LAMBDA_RAM_MIN_MB = 128

  def __init__(self,
               rtType: RuntimeType,
               name: Union[str, None] = None,
               main_function: Union[Callable[..., Any], None] = None,
               python_version: Union[str, None] = None,
               requirements_txt_filepath: Union[str, None] = None,
               requirements_txt_contents: Union[List[str], None] = None,
               python_packages: Union[List[str], None] = None,
               system_packages: Union[List[str], None] = None,
               docker_run: Union[str, None] = None,
               source_override: Union[str, None] = None):
    self._pythonPackages: Union[List[str], None] = None
    self._systemPackages: Union[List[str], None] = None
    self._dockerRun: Union[str, None] = None
    self._deployName: Union[str, None] = None
    self._deployFunc: Union[Callable[..., Any], None] = None
    self.rtType: RuntimeType = rtType
    self._sourceOverride = source_override
    self._testOutputs: List[Tuple[bool, str]] = []

    self._pythonVersion = getDefaultPythonVersion()
    self.set_python_packages(getDefaultPythonPackages())
    self.set_system_packages(getDefaultSystemPackages())

    if name:
      self.set_name(name)
    if main_function:
      self._set_main_function(main_function)
    if python_version:
      self.set_python_version(python_version)
    if requirements_txt_filepath:
      self.set_requirements_txt(filepath=requirements_txt_filepath)
    if requirements_txt_contents:
      self.set_requirements_txt(contents=requirements_txt_contents)
    if python_packages is not None:
      self.set_python_packages(python_packages)
    if system_packages is not None:
      self.set_system_packages(system_packages)
    if docker_run:
      self.set_docker_run(docker_run)
    self._prepEnvironment()

  def _repr_html_(self):
    return self._describeHtml()

  def set_name(self, name: str):
    if not re.match('^[a-zA-Z0-9_]+$', name):
      raise Exception("Names should be alphanumeric with underscores.")
    self._deployName = name
    return self

  def set_python_version(self, version: str):
    if version not in ALLOWED_PY_VERSIONS:
      return self._selfError(f'Python version should be one of {ALLOWED_PY_VERSIONS}.')
    self._pythonVersion = version
    return self

  def set_requirements_txt(self, filepath: Union[str, None] = None, contents: Union[List[str], None] = None):
    # if filepath == None and contents == None:
    # return self._filepicker_requirements_txt()
    lines: List[str] = []
    if filepath != None and type(filepath) == str:
      f = open(filepath, "r")
      lines = [n.strip() for n in f.readlines()]
      return self.set_python_packages(lines)
    elif contents != None:
      return self.set_python_packages(contents)
    return self

  def set_python_packages(self, packages: Union[List[str], None]):
    if packages is None:
      self._pythonPackages = None
      return
    if type(packages) != list:
      printError("The python_packages parameter must be a list of strings.")
      return
    for pkg in packages:
      if type(pkg) != str:
        printError("The python_packages parameters must be a list of strings.")
        return
      if "\n" in pkg or "\r" in pkg:
        printError("The python_packages parameters cannot contain newlines")
        return
    self._pythonPackages = packages

  def set_system_packages(self, packages: Union[List[str], None]):
    if packages is None:
      self._systemPackages = None
      return
    if type(packages) != list:
      printError("The system_packages parameter must be a list of strings.")
      return
    for pkg in packages:
      if type(pkg) != str:
        printError("The system_packages parameters must be a list of strings.")
        return
      if "\n" in pkg or "\r" in pkg:
        printError("The system_packages parameters cannot contain newlines")
        return
    self._systemPackages = packages

  def set_docker_run(self, commands: Union[str, None]):
    if commands is None:
      self._dockerRun = None
      return
    if type(commands) != str:
      printError("The docker_run parameter must be a string.")
      return
    if "\n" in commands or "\r" in commands:
      printError("The docker_run parameter cannot contain newlines.")
      return
    self._dockerRun = commands

  def _set_main_function(self, func: Callable[..., Any]):
    self._deployFunc = func
    if callable(func) and self._deployName == None:
      self.set_name(func.__name__)
    tests = self._getTests()
    if tests == None:
      self._testOutputs = []
    else:
      self._testOutputs = self._getTestOutputs(tests)
    return self

  def _getRequirementsTxt(self):
    if self._pythonPackages:
      return "\n".join(self._pythonPackages)
    else:
      return None

  def _prepEnvironment(self):
    getJson(
        "jupyter/v1/runtimes/prep_environment", {
            "environment": {
                "requirementsTxt": self._getRequirementsTxt(),
                "pythonVersion": self._pythonVersion,
                "systemPackages": self._systemPackages,
                "dockerRun": self._dockerRun,
            }
        })

  def deploy(self):
    status = self._getStatusNotes()
    rtProps, errors = self._getFuncProps()
    if not status.deployable or len(errors) > 0:
      printError("Unable to continue because errors are present.")
      return self

    notes: List[str] = []
    notes.append(makeTitledList("Errors", errorStyle(), status.errors, LIST_TITLES_ERRORS))
    notes.append(makeTitledList("Heads up!", errorStyle(), status.warnings, LIST_TITLES_WARNINGS))
    notes.append(makeTitledList("Tips", tipStyle(), status.tips, LIST_TITLES_TIPS))
    notes = [n for n in notes if n != ""]
    if len(notes) > 0:
      printHtml("".join(notes))

    printHtml(f'<div style="">{wrapStyle(f"Deploying {self._deployName}...", tipStyle())}</div>')
    printHtml(f"Uploading dependencies...")
    sourceFile = self._makeSourceFile(rtProps)
    valueFiles = self._makeAndUploadValueFiles(rtProps)
    resp = getJsonOrPrintError(
        "jupyter/v1/runtimes/create", {
            "runtime": {
                "name": self._deployName,
                "type": self.rtType.value,
                "pyState": {
                    "sourceFile": sourceFile.asDict(),
                    "valueFiles": valueFiles,
                    "name": rtProps.name,
                    "module": self._sourceFileName(),
                    "argNames": rtProps.argNames,
                    "argTypes": rtProps.argTypes,
                    "requirementsTxt": self._getRequirementsTxt(),
                    "pythonVersion": self._pythonVersion,
                    "systemPackages": self._systemPackages,
                    "dockerRun": self._dockerRun
                }
            }
        })
    if not isAuthenticated():
      return None
    if not resp:
      printHtml(f'Error processing request: no response from server.')
    elif resp.error:
      printHtml(f'Error processing request: {html.escape(resp.error)}')
    elif resp.runtimeOverviewUrl:
      printHtml("")  # line break after upload statements
      printHtml(f'<div style="">{wrapStyle(f"Success!", tipStyle())}</div>')
      if resp.message:
        printHtml(html.escape(resp.message))
      message = "View status and integration options."
      printHtml(f'<a href="{resp.runtimeOverviewUrl}" target="_blank">{message}</a>')
    else:
      printHtml(f"Unknown error while processing request (server response in unexpected format).")
    return None

  def _sourceFileName(self):
    return "source"

  def _makeSourceFile(self, pyProps: RuntimePythonProps):

    def addSpacer(strList: List[str]):
      if len(strList) > 0 and strList[-1] != "":
        strList.append("")

    sourceParts: List[str] = ["import modelbit, sys"]

    if pyProps.namespaceFroms:
      for iAs, iModule in pyProps.namespaceFroms.items():
        sourceParts.append(f"from {iModule} import {iAs}")
    if pyProps.namespaceImports:
      for iAs, iModule in pyProps.namespaceImports.items():
        sourceParts.append(f"import {iModule} as {iAs}")
    addSpacer(sourceParts)

    if pyProps.namespaceVars and pyProps.namespaceVarsDesc:
      for nName, _ in pyProps.namespaceVars.items():
        sourceParts.append(f'{nName} = modelbit.load_value("{nName}") # {pyProps.namespaceVarsDesc[nName]}')

    addSpacer(sourceParts)
    if pyProps.namespaceFunctions:
      for _, fSource in pyProps.namespaceFunctions.items():
        sourceParts.append(fSource)
        addSpacer(sourceParts)

    addSpacer(sourceParts)
    if pyProps.source:
      sourceParts.append("# main function")
      sourceParts.append(pyProps.source)

    sourceParts.append("# to run locally via git & terminal")
    sourceParts.append('if __name__ == "__main__":')
    sourceParts.append(f"  print({pyProps.name}(*sys.argv[1:]))")
    return RuntimeFile(f"{self._sourceFileName()}.py", "\n".join(sourceParts))

  def _makeAndUploadValueFiles(self, pyState: RuntimePythonProps):
    valueFiles: Dict[str, Dict[str, str]] = {}  # is a RuntimeDataMap
    if pyState.namespaceVars and pyState.namespaceVarsDesc:
      for nName, nVal in pyState.namespaceVars.items():
        valueFiles[nName] = {"contentHash": uploadRuntimeObject(nVal, nName)}
    return valueFiles

  def _selfError(self, txt: str):
    printError(txt)
    return None

  def _describeHtml(self):
    nonStr = '(None)'

    def codeWrap(txt: str):
      if txt == nonStr:
        return nonStr
      return wrapStyle(txt, codeStyle())

    status = self._getStatusNotes()
    statusWithStyle = wrapStyle(status.statusMsg(), status.statusStyle())
    funcProps, _ = self._getFuncProps()

    headerLines: List[str] = []
    if self._deployName != None:
      headerLines.append(
          f'<div style="font-weight: bold;">{html.escape(self._deployName)} is {statusWithStyle} to deploy.</div>'
      )

    headerLines.append(makeTitledList("Errors", errorStyle(), status.errors, LIST_TITLES_ERRORS))
    headerLines.append(makeTitledList("Warnings", errorStyle(), status.warnings, LIST_TITLES_WARNINGS))
    headerLines.append(makeTitledList("Tips", tipStyle(), status.tips, LIST_TITLES_TIPS))

    headers = [
        TableHeader("Property", TableHeader.LEFT),
        TableHeader("Value", TableHeader.LEFT, skipEscaping=True),
    ]
    rows: List[List[str]] = []

    funcSig = nonStr
    if funcProps.name and funcProps.argNames:
      funcSig = f"{funcProps.name}({', '.join(funcProps.argNames)})"
    rows.append(["Function", codeWrap(funcSig)])

    if funcProps.namespaceFunctions and len(funcProps.namespaceFunctions) > 0:
      nsFuncs = "<br/>".join([codeWrap(k) for k, _ in funcProps.namespaceFunctions.items()])
      rows.append(["Helpers", nsFuncs])

    if funcProps.namespaceVarsDesc and len(funcProps.namespaceVarsDesc) > 0:
      nsVars = "<br/>".join([codeWrap(f'{k}: {v}') for k, v in funcProps.namespaceVarsDesc.items()])
      rows.append(["Values", nsVars])

    nsImports: List[str] = []
    if funcProps.namespaceFroms and len(funcProps.namespaceFroms) > 0:
      for k, v in funcProps.namespaceFroms.items():
        nsImports.append(codeWrap(f'from {v} import {k}'))
    if funcProps.namespaceImports and len(funcProps.namespaceImports) > 0:
      for k, v in funcProps.namespaceImports.items():
        nsImports.append(codeWrap(f'import {v} as {k}'))
    if len(nsImports) > 0:
      rows.append(["Imports", '<br/>'.join(nsImports)])

    rows.append(["Python Version", codeWrap(self._pythonVersion)])

    if self._pythonPackages and len(self._pythonPackages) > 0:
      maxDepsShown = 7
      if len(self._pythonPackages) > maxDepsShown:
        deps = "<br/>".join([codeWrap(d) for d in self._pythonPackages[:maxDepsShown]])
        numLeft = len(self._pythonPackages) - maxDepsShown
        deps += f'<br/><span style="font-style: italic;">...and {numLeft} more.</span>'
      else:
        deps = "<br/>".join([codeWrap(d) for d in self._pythonPackages])
      rows.append(["requirements.txt", deps])

    if self._systemPackages:
      rows.append(["System Packages", codeWrap(", ".join(self._systemPackages))])

    if self._dockerRun:
      rows.append(["Docker RUN", codeWrap(self._dockerRun)])

    if len(self._testOutputs) > 0:
      testOutput: List[str] = [t[1] for t in self._testOutputs]
      rows.append(["Tests", f'<div style="font-family: monospace;">{"".join(testOutput)}</div>'])

    return f'<div style="{textStyle()}">' + "".join(headerLines) + '</div>' + makeHtmlTable(headers, rows)

  def _getFuncProps(self):
    errors: List[str] = []
    props: RuntimePythonProps = RuntimePythonProps()
    if not callable(self._deployFunc):
      errors.append('The main_function parameter does not appear to be a function.')
    else:
      props.name = self._deployFunc.__name__
      props.source = self.getFuncSource()
      props.argNames = self.getFuncArgNames()
      props.argTypes = self._annotationsToTypeStr(self._deployFunc.__annotations__)
      nsCollection = NamespaceCollection()
      self._collectNamespaceDeps(self._deployFunc, nsCollection)
      props.namespaceFunctions = nsCollection.functions
      props.namespaceVars = nsCollection.vars
      props.namespaceVarsDesc = self._strValues(nsCollection.vars)
      props.namespaceImports = nsCollection.imports
      props.namespaceFroms = nsCollection.froms
    return (props, errors)

  def getFuncSource(self):
    if self._sourceOverride:
      return self._sourceOverride
    if not callable(self._deployFunc):
      return None
    return unindent(inspect.getsource(self._deployFunc))

  def getFuncArgNames(self):
    argSpec = inspect.getfullargspec(self._deployFunc)
    if argSpec.varargs:
      return ['...']
    if argSpec.args:
      return argSpec.args
    noArgs: List[str] = []
    return noArgs

  def _annotationsToTypeStr(self, annotations: Dict[str, Any]):
    annoStrs: Dict[str, str] = {}
    for name, tClass in annotations.items():
      try:
        if tClass == Any:
          annoStrs[name] = "Any"
        else:
          annoStrs[name] = tClass.__name__
      except:
        pass
    return annoStrs

  def _collectNamespaceDeps(self, func: Callable[..., Any], collection: NamespaceCollection):
    if not callable(func):
      return collection
    globalsDict = func.__globals__  # type: ignore
    allNames = func.__code__.co_names + func.__code__.co_freevars
    for maybeFuncVarName in allNames:
      if maybeFuncVarName in globalsDict:
        maybeFuncVar = globalsDict[maybeFuncVarName]
        if "__module__" in dir(maybeFuncVar):
          if maybeFuncVar.__module__ == "__main__":  # the user's functions
            argNames = list(maybeFuncVar.__code__.co_varnames or [])
            funcSig = f"{maybeFuncVar.__name__}({', '.join(argNames)})"
            if funcSig not in collection.functions:
              collection.functions[funcSig] = inspect.getsource(maybeFuncVar)
              self._collectNamespaceDeps(maybeFuncVar, collection)
          else:  # functions imported by the user from elsewhere
            if inspect.isclass(maybeFuncVar):
              collection.froms[maybeFuncVarName] = maybeFuncVar.__module__
            elif callable(maybeFuncVar) and not self._hasState(maybeFuncVar):
              collection.froms[maybeFuncVarName] = maybeFuncVar.__module__
            elif isinstance(maybeFuncVar, object):
              collection.froms[maybeFuncVar.__class__.__name__] = maybeFuncVar.__module__
              collection.vars[maybeFuncVarName] = maybeFuncVar
            else:
              collection.froms[maybeFuncVarName] = f"NYI: {maybeFuncVar.__module__}"
        elif str(maybeFuncVar).startswith('<module'):
          collection.imports[maybeFuncVarName] = maybeFuncVar.__name__
        else:
          collection.vars[maybeFuncVarName] = maybeFuncVar

  def _hasState(self, obj: Any) -> bool:
    try:
      return len(obj.__dict__) > 0
    except:
      return False

  def _getStatusNotes(self):
    tips: List[str] = []
    warnings: List[str] = []
    errors: List[str] = []

    # Errors
    if not self._deployName:
      cmd = wrapStyle(".set_name('name')", codeStyle())
      errors.append(f'Run {cmd} to specify the {self._runtimeTypeName}\'s name.')
    if not self._deployFunc:
      funcName = "set_deploy_function"
      cmd = wrapStyle("." + funcName + "(func, args = {\"arg1\": value1, ...})", codeStyle())
      errors.append(f'Run {cmd} to specify the {self._runtimeTypeName}\'s runtime.')
    else:
      _, propErrors = self._getFuncProps()
      if len(propErrors) > 0:
        errors.extend(errors)
    for tOut in self._testOutputs:
      if tOut[0] == False:  # failed test
        errors.append("Some tests are failing.")
        break
    if not isAuthenticated():
      errors.append("You are not logged in to Modelbit.")

    # Tips
    if len(self._testOutputs) == 0:
      tips.append(
          'Add some <a href="https://doc.modelbit.com/#/deployments/unit-tests" target="_blank">unit tests</a> to improve this deployment.'
      )

    # Warnings
    missingPackages = listMissingPackages(getDefaultPythonPackages())
    if len(missingPackages) > 0:
      for mp in missingPackages:
        desiredPackage, similarPackage = mp
        if similarPackage is not None:
          warnings.append(mismatchedPackageWarning(desiredPackage, similarPackage))

    localPyVersion = getInstalledPythonVersion()
    if self._pythonVersion != localPyVersion:
      warnings.append(
          f"This deployment will use Python {wrapStyle(self._pythonVersion, codeStyle())} but the version installed locally is {wrapStyle(localPyVersion, codeStyle())}"
      )
    return RuntimeStatusNotes(tips, warnings, errors)

  def _strValues(self, args: Dict[str, Any]):
    newDict: Dict[str, str] = {}
    for k, v in args.items():
      strVal = re.sub(r'\s+', " ", str(v))
      if len(strVal) > 200:
        strVal = strVal[0:200] + "..."
      newDict[k] = strVal
    return newDict

  def _getTests(self):
    if not callable(self._deployFunc):
      return None
    funcName = self._deployFunc.__name__
    funcSource = self.getFuncSource()
    resp = getJsonOrPrintError("jupyter/v1/runtimes/parse_tests", {
        "funcName": funcName,
        "funcSource": funcSource,
    })
    if resp:
      return resp.tests
    return None

  def _runTest(self, test: DeploymentTestDef):
    if not callable(self._deployFunc):
      return False
    if test.args == None:
      return self._deployFunc()
    return self._deployFunc(*test.args)  # type: ignore

  def _getTestOutputs(self, tests: List[DeploymentTestDef]) -> List[Tuple[bool, str]]:
    return [self._getTestOutput(t) for t in tests]

  def _getTestOutput(self, test: DeploymentTestDef) -> Tuple[bool, str]:

    def testError(msg: str):
      return f'<div><span style="font-weight: bold; color: #E2548A; width: 45px; display: inline-block;">Error</span> {test.command}: <span style="color: #E2548A;">{msg}</span></div>'

    def testPass():
      return f'<div><span style="font-weight: bold; color: green; width: 45px; display: inline-block;">Pass</span> {test.command}: <span style="color: green;">{json.dumps(test.expectedOutput)}</span></div>'

    if test.error:
      errorMessage = "Unable to run test."
      if test.error == DeploymentTestError.UnknownFormat.value:
        errorMessage = "Unknown test format"
      if test.error == DeploymentTestError.ExpectedNotJson.value:
        errorMessage = "Expected value must be JSON serializeable"
      if test.error == DeploymentTestError.CannotParseArgs.value:
        errorMessage = "Unable to parse function arguments."
      return (False, testError(errorMessage))

    result = self._runTest(test)
    try:
      jResult = json.loads(json.dumps(result))  # dump+load helps clean up numbers like 2.00000000001
      if jResult != test.expectedOutput:
        return (False,
                testError(f"Expected: {json.dumps(test.expectedOutput)}. Received: {json.dumps(jResult)}."))
    except:
      return (False, testError(f"Output must be JSON serializeable. Received: {type(result).__name__}."))
    return (True, testPass())


class Deployment(Runtime):
  _runtimeTypeName = "deployment"

  def __init__(self,
               name: Union[str, None] = None,
               deploy_function: Union[Callable[..., Any], None] = None,
               python_version: Union[str, None] = None,
               requirements_txt_filepath: Union[str, None] = None,
               requirements_txt_contents: Union[List[str], None] = None,
               python_packages: Union[List[str], None] = None,
               system_packages: Union[List[str], None] = None,
               docker_run: Union[str, None] = None,
               source_override: Union[str, None] = None):
    Runtime.__init__(self,
                     RuntimeType.Deployment,
                     name=name,
                     main_function=deploy_function,
                     python_version=python_version,
                     requirements_txt_filepath=requirements_txt_filepath,
                     requirements_txt_contents=requirements_txt_contents,
                     python_packages=python_packages,
                     system_packages=system_packages,
                     docker_run=docker_run,
                     source_override=source_override)

  def set_deploy_function(self, func: Callable[..., Any]):
    self._set_main_function(func)
