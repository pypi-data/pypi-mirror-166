from pydantic import BaseModel, Field


class SeasonModel(BaseModel):
    season_id: int = Field(alias="season_id")
    season_name: str = Field(alias="season_name")
