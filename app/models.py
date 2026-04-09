from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index, Table
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


pokemon_types = Table(
    "pokemon_types",
    Base.metadata,
    Column("pokemon_id", Integer, ForeignKey("pokemon.id"), primary_key=True),
    Column("type_name", String, primary_key=True),
    Index("idx_pokemon_types_type_name", "type_name"),
)


class Pokemon(Base):
    __tablename__ = "pokemon"
    __table_args__ = (
        Index("idx_pokemon_generation", "generation"),
        Index("idx_pokemon_color", "color"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    german_name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    height = Column(Float, nullable=False)  # in meters
    weight = Column(Float, nullable=False)  # in kg
    generation = Column(Integer, nullable=False)
    sprite_url = Column(String, nullable=False)
    artwork_url = Column(String, nullable=False)
    types = relationship("PokemonType", back_populates="pokemon", cascade="all, delete-orphan")
    evolves_from_id = Column(Integer, ForeignKey("pokemon.id"), nullable=True)

    @property
    def type_names(self) -> list[str]:
        return [t.type_name for t in self.types]

    def display_name_for(self, lang: str = "de") -> str:
        name = self.german_name if lang == "de" else self.name.title()
        return name.replace("♀", " Weiblich" if lang == "de" else " Female").replace(
            "♂", " Männlich" if lang == "de" else " Male"
        )

    # Keep backwards compat for seed.py and existing code
    @property
    def display_name(self) -> str:
        return self.display_name_for("de")

    @property
    def size_description(self) -> str:
        from app.i18n import get_size_description
        return get_size_description(self.height, "de")

    @property
    def size_description_spoken(self) -> str:
        from app.i18n import get_size_description_spoken
        return get_size_description_spoken(self.height, "de")


class PokemonType(Base):
    __tablename__ = "pokemon_type_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    type_name = Column(String, nullable=False)
    pokemon = relationship("Pokemon", back_populates="types")


class Favorite(Base):
    __tablename__ = "favorites"

    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), primary_key=True)


class Setting(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)
