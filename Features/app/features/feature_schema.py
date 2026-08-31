from pydantic import BaseModel
from typing import Dict, Any

class ExtractedFeatures(BaseModel):
    loop_count: int = 0
    for_loop_count: int = 0
    while_loop_count: int = 0
    max_loop_depth: int = 0
    nested_loop_count: int = 0
    if_count: int = 0
    function_count: int = 0
    method_count: int = 0
    function_call_count: int = 0
    recursive: bool = False
    recursive_call_count: int = 0
    ast_depth: int = 0
    statement_count: int = 0
    condition_count: int = 0
    linear_loop_count: int = 0
    logarithmic_loop_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
