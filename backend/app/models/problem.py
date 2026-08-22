from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ProblemTestCase(BaseModel):
    input_args: List[Any]
    expected_output: Any
    is_hidden: bool = False
    explanation: Optional[str] = None

class ProblemExample(BaseModel):
    input_str: str
    output_str: str
    explanation: Optional[str] = None

class ProblemModel(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: str
    topic: str               # Recursion, Loops, Arrays, Strings, Dictionaries, Searching, Sorting, OOP, DP, etc.
    subconcept: str          # base_case, loop_boundary, hash_lookup, two_pointer, etc.
    difficulty: str         # beginner, intermediate, advanced (or easy, medium, hard)
    language: str = "python"
    type: str = "coding"
    examples: List[Dict[str, Any]] = []
    constraints: List[str] = []
    starter_code: str
    test_cases: List[Dict[str, Any]] = []
    tags: List[str] = []
    estimated_time: int = 15  # in minutes
    
    # Secure server-side fields (Never exposed before unlock)
    solution: str
    explanation: str
    better_approach: str
    time_complexity: str
    space_complexity: str

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
