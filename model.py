from pydantic import BaseModel, Field
from typing import Optional, Literal, List

class BugItem(BaseModel):

    line_number: Optional[int] = Field(
        None,
        description=("Estimated line number or section where the issue occurs.")
    )
    description: str = Field(
        ...,
        description=("Explanation of the bug, anti-pattern, or performance bottleneck.")
    )
    fix_suggestion: str = Field(
        ...,
        description=("Recommended fix or best practice implementation.")
    )

class CodeReviewReport(BaseModel):

        summary: str = Field(
            ...,
            description=("A concise 1-sentence executive summary of the code quality.")
        )
        severity_score: int = Field(
            ...,
            ge=1,
            le=10,
            description=("Overall severity score from 1 (clean code) to 10 (critical bugs/errors).")
        )
        bug_identification: List[BugItem] = Field(
            ...,
            description=("List of identified bugs, security risks, or anti-patterns.")
        )
        refactored_code: str = Field(
            ...,
            description=("The cleaned-up, production-ready refactored version of the code.")
        )
        suggestion_test: str = Field(
            ...,
            description=("A PyTest or Jest unit test skeleton verifying the core logic.")
        )
    
