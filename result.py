from dataclasses import dataclass


@dataclass
class Result:
  code: int
  message: str = None

class ResultError(Exception):

  def __init__(self, result: Result, *args) -> None:
    super().__init__(result.message, *args)
    self.result = result
  
  def makeWithResult(code, message):
    return ResultError(Result(code, message))