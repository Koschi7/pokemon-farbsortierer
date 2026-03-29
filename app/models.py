from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


pokemon_types = Table(
    "pokemon_types",
    Base.metadata,
    Column("pokemon_id", Integer, ForeignKey("pokemon.id"), primary_key=True),
    Column("type_name", String, primary_key=True),
)


class Pokemon(Base):
    __tablename__ = "pokemon"

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

    @property
    def size_description(self) -> str:
        h = self.height
        if h < 0.3:
            return "So klein wie deine Hand!"
        elif h < 0.6:
            return "So groß wie eine Katze!"
        elif h < 1.2:
            return "So groß wie ein Hund!"
        elif h < 2.0:
            return "So groß wie Mama oder Papa!"
        else:
            return "Größer als ein Auto!"


class PokemonType(Base):
    __tablename__ = "pokemon_type_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    type_name = Column(String, nullable=False)
    pokemon = relationship("Pokemon", back_populates="types")


class Setting(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)
