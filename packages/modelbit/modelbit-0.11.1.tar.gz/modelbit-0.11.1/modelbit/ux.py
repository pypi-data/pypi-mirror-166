from typing import List, Tuple
import html, random

LIST_TITLES_WARNINGS = ("inconsistency", "inconsistencies")
LIST_TITLES_TIPS = ("tip", "tips")
LIST_TITLES_ERRORS = ("error", "errors")


def codeStyle():
  return "font-family: monospace; font-size: 0.95em; font-weight: medium; color: #714488;"


def errorStyle():
  return "font-weight: bold; color: #714488;"


def tipStyle():
  return "font-weight: bold; color: green;"


def textStyle():
  return "font-family: Roboto, Arial, sans-serif; padding: 5px;"


def linkStyle():
  return "color: #106ba3; text-decoration:none; cursor: pointer;"


def wrapStyle(text: str, style: str, escape: bool = True):
  if escape:
    return f'<span style="{style}">{html.escape(text)}</span>'
  else:
    return f'<span style="{style}">{text}</span>'


class TableHeader:
  LEFT = 'left'
  CENTER = 'center'
  RIGHT = 'right'

  def __init__(self, name: str, alignment: str = LEFT, skipEscaping: bool = False):
    self.name = name
    self.alignment = alignment
    self.skipEscaping = skipEscaping
    if self.alignment not in [self.LEFT, self.CENTER, self.RIGHT]:
      raise Exception(f'Unrecognized alignment: {self.alignment}')

  def alignStyle(self):
    return f'text-align:{self.alignment};'

  def maybeEscape(self, val: str):
    return (val if self.skipEscaping else html.escape(val))


def makeHtmlTable(headers: List[TableHeader], rows: List[List[str]]) -> str:
  lines: List[str] = []
  lines.append(f'<div style="{textStyle()}"><table>')

  lines.append('<thead>')
  for header in headers:
    lines.append(f'<th style="{header.alignStyle()}">{html.escape(header.name)}</th>')
  lines.append('</thead>')

  lines.append('<tbody>')
  for row in rows:
    lines.append('<tr>')
    for i in range(len(row)):
      lines.append(f'<td style="{headers[i].alignStyle()}">{headers[i].maybeEscape(row[i])}</td>')
    lines.append('</tr>')
  lines.append('</tbody>')

  lines.append('</table></div>')
  return "".join(lines)


def makeTitledList(title: str, titleStyle: str, listEls: List[str], moreNames: Tuple[str, str]):
  if len(listEls) == 0:
    return ""

  listEls = [
      f'<div style="{textStyle()} border-left: 1px solid #714488; margin-bottom: 10px;">{e}</div>'
      for e in listEls
  ]

  lines: List[str] = [f'<div style="margin-top: 10px;">{wrapStyle(title, titleStyle)}</div>', listEls[0]]

  restOfEls = listEls[1:]
  if len(restOfEls) > 0:
    moreBtn = f'mb-{random.randint(1, 999999999)}'
    moreEls = f'mb-{random.randint(1, 999999999)}'
    moreClick = f"document.getElementById('{moreEls}').style.display='block'; document.getElementById('{moreBtn}').style.display='none';"
    issuePl = f"There is 1 more {moreNames[0]}"
    if len(restOfEls) > 1:
      issuePl = f"There are {len(restOfEls)} more {moreNames[1]}."
    issuePl += f' <span style="{linkStyle()}" onClick="{moreClick}">View all</span>'
    lines.append(f'<div style="display: none;" id="{moreEls}">{"".join(restOfEls)}</div>')
    lines.append(f'<div id="{moreBtn}" style="margin-top: 5px;">{issuePl}</div>')

  return '<div style="margin-top: 0; margin-bottom: 10px;">' + "".join(lines) + '</div>'
