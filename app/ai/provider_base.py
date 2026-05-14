from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ArticleSummary:
    """AI-generated text for one selected article."""

    final_summary: str
    why_it_matters:str


class AIProvider(ABC):
    """Interface for swappable AI summarisation providers."""

    @abstractmethod
    def summarize_article(self, article:dict[str, Any]) -> ArticleSummary:
        """Generate summary text and why-it-matters text for one article"""
        raise NotImplementedError
