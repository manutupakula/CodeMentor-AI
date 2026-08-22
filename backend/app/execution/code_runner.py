import sys
import io
import traceback
import time
import ast
from typing import Dict, Any, List, Optional
from app.core.config import settings

class CodeExecutionResult:
    def __init__(
        self,
        success: bool,
        stdout: str = "",
        stderr: str = "",
        error_type: Optional[str] = None,
        test_results: Optional[List[Dict[str, Any]]] = None,
        passed_count: int = 0,
        total_count: int = 0,
        execution_time_ms: float = 0.0
    ):
        self.success = success
        self.stdout = stdout
        self.stderr = stderr
        self.error_type = error_type
        self.test_results = test_results or []
        self.passed_count = passed_count
        self.total_count = total_count
        self.execution_time_ms = execution_time_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "error_type": self.error_type,
            "test_results": self.test_results,
            "passed_count": self.passed_count,
            "total_count": self.total_count,
            "execution_time_ms": self.execution_time_ms
        }

class SafeCodeRunner:
    """Safe isolated sandbox execution engine."""

    @staticmethod
    def check_syntax(code: str) -> Optional[str]:
        try:
            ast.parse(code)
            return None
        except SyntaxError as e:
            return f"SyntaxError on line {e.lineno}: {e.msg}"
        except Exception as e:
            return f"Syntax Error: {str(e)}"

    @classmethod
    async def run_code(
        cls,
        code: str,
        test_cases: Optional[List[Dict[str, Any]]] = None,
        function_name: Optional[str] = None,
        timeout_seconds: float = 2.0
    ) -> CodeExecutionResult:
        syntax_err = cls.check_syntax(code)
        if syntax_err:
            return CodeExecutionResult(
                success=False,
                stderr=syntax_err,
                error_type="SYNTAX_ERROR",
                test_results=[],
                passed_count=0,
                total_count=len(test_cases) if test_cases else 0
            )

        return cls._run_isolated_tests(code, test_cases, function_name, timeout_seconds)

    @classmethod
    def _run_isolated_tests(
        cls,
        code: str,
        test_cases: Optional[List[Dict[str, Any]]] = None,
        function_name: Optional[str] = None,
        timeout_seconds: float = 2.0
    ) -> CodeExecutionResult:
        start_time = time.time()
        
        safe_builtins = {
            "abs": abs, "all": all, "any": any, "bin": bin, "bool": bool,
            "bytearray": bytearray, "bytes": bytes, "chr": chr, "complex": complex,
            "dict": dict, "divmod": divmod, "enumerate": enumerate, "filter": filter,
            "float": float, "format": format, "frozenset": frozenset, "hasattr": hasattr,
            "hash": hash, "hex": hex, "id": id, "int": int, "isinstance": isinstance,
            "issubclass": issubclass, "iter": iter, "len": len, "list": list,
            "map": map, "max": max, "min": min, "next": next, "object": object,
            "oct": oct, "ord": ord, "pow": pow, "print": print, "range": range,
            "repr": repr, "reversed": reversed, "round": round, "set": set,
            "slice": slice, "sorted": sorted, "str": str, "sum": sum,
            "tuple": tuple, "type": type, "zip": zip,
            "ValueError": ValueError, "TypeError": TypeError, "IndexError": IndexError,
            "KeyError": KeyError, "ZeroDivisionError": ZeroDivisionError,
            "RecursionError": RecursionError, "Exception": Exception,
            "True": True, "False": False, "None": None
        }
        
        import math, collections, heapq, itertools, functools, re
        exec_scope = {
            "__builtins__": safe_builtins,
            "math": math,
            "collections": collections,
            "defaultdict": collections.defaultdict,
            "Counter": collections.Counter,
            "deque": collections.deque,
            "heapq": heapq,
            "itertools": itertools,
            "functools": functools,
            "re": re
        }
        safe_globals_keys = list(exec_scope.keys())

        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        try:
            exec(code, exec_scope)
            stdout_text = redirected_output.getvalue()
        except RecursionError:
            sys.stdout = old_stdout
            return CodeExecutionResult(
                success=False,
                stderr="RecursionError: maximum recursion depth exceeded while calling a Python object. (Missing or invalid base case)",
                error_type="RUNTIME_ERROR",
                test_results=[],
                passed_count=0,
                total_count=len(test_cases) if test_cases else 0
            )
        except Exception as e:
            sys.stdout = old_stdout
            return CodeExecutionResult(
                success=False,
                stderr=traceback.format_exc(),
                error_type="RUNTIME_ERROR",
                test_results=[],
                passed_count=0,
                total_count=len(test_cases) if test_cases else 0
            )
        finally:
            sys.stdout = old_stdout

        if not test_cases:
            return CodeExecutionResult(
                success=True,
                stdout=stdout_text,
                error_type="CORRECT" if not stdout_text.startswith("Error") else "LOGICAL_ERROR",
                passed_count=1,
                total_count=1,
                execution_time_ms=(time.time() - start_time) * 1000
            )

        # Detect candidate student function or class
        func = None
        ignored_names = set(safe_globals_keys)
        
        if function_name and function_name in exec_scope and callable(exec_scope[function_name]):
            func = exec_scope[function_name]
        else:
            for k, val in exec_scope.items():
                if k not in ignored_names and not k.startswith("__") and callable(val) and not isinstance(val, type):
                    func = val
                    break

        # Check if OOP class
        oop_class = None
        for k, val in exec_scope.items():
            if k not in ignored_names and not k.startswith("__") and isinstance(val, type):
                oop_class = val
                break

        if not func and not oop_class and test_cases:
            return CodeExecutionResult(
                success=False,
                stdout=stdout_text,
                stderr="No callable function or class found in student code to evaluate.",
                error_type="LOGICAL_ERROR",
                test_results=[],
                passed_count=0,
                total_count=len(test_cases)
            )

        test_results = []
        passed = 0
        overall_error_type = "CORRECT"

        for idx, tc in enumerate(test_cases):
            input_args = tc.get("input_args", [])
            expected = tc.get("expected_output")
            is_hidden = tc.get("is_hidden", False)

            try:
                if oop_class and input_args == ["test_oop"]:
                    inst = oop_class(100)
                    inst.deposit(50)
                    inst.withdraw(30)
                    actual = inst.get_balance()
                elif func:
                    actual = func(*input_args)
                else:
                    actual = None

                is_match = (actual == expected)
                if is_match:
                    passed += 1
                else:
                    overall_error_type = "LOGICAL_ERROR"

                test_results.append({
                    "test_case_index": idx + 1,
                    "input_args": "[HIDDEN]" if is_hidden else input_args,
                    "expected_output": "[HIDDEN]" if is_hidden else expected,
                    "actual_output": "[HIDDEN]" if is_hidden and not is_match else actual,
                    "passed": is_match,
                    "is_hidden": is_hidden
                })
            except RecursionError:
                overall_error_type = "RUNTIME_ERROR"
                test_results.append({
                    "test_case_index": idx + 1,
                    "input_args": "[HIDDEN]" if is_hidden else input_args,
                    "expected_output": "[HIDDEN]" if is_hidden else expected,
                    "actual_output": "RecursionError (Maximum recursion depth exceeded)",
                    "passed": False,
                    "is_hidden": is_hidden
                })
            except Exception as e:
                overall_error_type = "RUNTIME_ERROR"
                test_results.append({
                    "test_case_index": idx + 1,
                    "input_args": "[HIDDEN]" if is_hidden else input_args,
                    "expected_output": "[HIDDEN]" if is_hidden else expected,
                    "actual_output": f"Error: {type(e).__name__}: {str(e)}",
                    "passed": False,
                    "is_hidden": is_hidden
                })

        success = (passed == len(test_cases))
        if success:
            overall_error_type = "CORRECT"

        return CodeExecutionResult(
            success=success,
            stdout=stdout_text,
            stderr="" if success else "Some test cases failed.",
            error_type=overall_error_type,
            test_results=test_results,
            passed_count=passed,
            total_count=len(test_cases),
            execution_time_ms=(time.time() - start_time) * 1000
        )
