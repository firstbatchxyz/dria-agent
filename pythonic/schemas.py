from string import printable

from pydantic import BaseModel
from typing import Dict, Any, List
import json

FLOAT_TOLERANCE = 1e-6


class FunctionResults(BaseModel):
    """Results from executing functions, including return values, variables and errors."""

    results: Dict[str, Any]
    data: Dict[str, Any]
    errors: List[str]

    def check_score(self, values_list: List[Any], functions_list: List[str]) -> float:
        """
        Calculate a score based on presence of values and functions in results.
        Max score is 1.0, split between values (0.5) and functions (0.5) proportionally.

        Args:
            values_list: The values to search for
            functions_list: The functions to search for

        Returns:
            float: Score between 0 and 1, where 1 means all values and functions present
        """

        def values_match(value1: Any, value2: Any) -> bool:
            """Check if two values match, considering tolerance for floats."""
            if isinstance(value1, float) and isinstance(value2, float):
                return abs(value1 - value2) <= FLOAT_TOLERANCE
            return value1 == value2

        # Count matching values
        matching_values = sum(
            1
            for value in values_list
            if any(
                values_match(value, var_value) for var_value in self.variables.values()
            )
        )
        values_score = 0.5 * (
            matching_values / len(values_list) if values_list else 1.0
        )

        # Count matching functions
        matching_functions = sum(
            1 for function in functions_list if function in self.function_results.keys()
        )
        functions_score = 0.5 * (
            matching_functions / len(functions_list) if functions_list else 1.0
        )

        return values_score + functions_score


class ExecutionResults(BaseModel):
    results: Dict[str, Any]
    data: Dict[str, Any]
    errors: List[str]
    content: str
    is_dry: bool

    def dict(self, *args, **kwargs):
        if self.is_dry:
            return {"content": self.content}
        return super().model_dump_json(
            *args, **kwargs, exclude_none=True, exclude_defaults=True
        )

    def __str__(self):
        if self.is_dry:
            return json.dumps({"content": self.content})
        return json.dumps({k: self.data[v] for k, v in self.results.items()})

    def final_answer(self):
        if self.is_dry:
            return self.content
        if not self.data or (len(self.data) == 1 and "re" in self.data):
            raise ValueError("No final value")
        return list(self.data.values())[-1]
