from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Offer:
    id: int
    source: str
    url: str
    job_position: str
    company: str
    category: str
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None
    currency: Optional[str] = None
    skills: Optional[List[str]] = None
    seniority: Optional[str] = None

    def __init__(self, id: int, source: str, url: str):
        self.id = id
        self.source = source
        self.url = url
    
    def set_job_basic_info(self, category,job_position, company, seniority: str):
        self.category = category
        self.job_position = job_position
        self.company = company
        self.seniority = seniority

    def set_salary(self, min_salary: float, max_salary: float, currency: str):
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.currency = currency

    def set_skills(self, skills: List[str]):
        self.skills = skills