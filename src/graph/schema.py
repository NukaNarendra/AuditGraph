from typing import List, Optional
from pydantic import BaseModel, Field

class Entity(BaseModel):
    id: str = Field(description="Unique identifier (e.g., 'Company_A', 'Bob_Smith')")
    type: str = Field(description="Type of entity: Person, Company, Document, Asset")
    properties: dict = Field(default_factory=dict, description="Attributes like 'date', 'amount', 'title'")

class Relationship(BaseModel):
    source: str = Field(description="ID of the source entity")
    target: str = Field(description="ID of the target entity")
    type: str = Field(description="Relation type: SIGNED, OWNS, TRANSFERRED_TO, MENTIONS")
    properties: dict = Field(default_factory=dict)

class GraphData(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]