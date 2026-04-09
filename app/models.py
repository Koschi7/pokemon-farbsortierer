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
    def display_name(self) -> str:
        return self.german_name.replace("♀", " Weiblich").replace("♂", " Männlich")

    @property
    def type_names(self) -> list[str]:
        return [t.type_name for t in self.types]

    @property
    def size_description(self) -> str:
        h = self.height
        # Format height as German: "1,7 m" for display, spoken version for TTS
        if h < 1.0:
            cm = round(h * 100)
            height_str = f"{cm} cm"
        else:
            height_str = f"{h:.1f} m".replace(".", ",")

        if h <= 0.2:
            return f"{height_str} – Passt in deine Hand!"
        elif h <= 0.3:
            return f"{height_str} – So groß wie ein Lineal!"
        elif h <= 0.5:
            return f"{height_str} – So groß wie ein Teddy!"
        elif h <= 0.7:
            return f"{height_str} – So groß wie ein Kissen!"
        elif h <= 0.9:
            return f"{height_str} – So groß wie ein Bobbycar!"
        elif h <= 1.1:
            return f"{height_str} – So groß wie du!"
        elif h <= 1.3:
            return f"{height_str} – So groß wie ein Fahrrad!"
        elif h <= 1.6:
            return f"{height_str} – So groß wie ein Schneemann!"
        elif h <= 2.0:
            return f"{height_str} – So groß wie Mama oder Papa!"
        elif h <= 3.0:
            return f"{height_str} – So groß wie eine Zimmerdecke!"
        elif h <= 5.0:
            return f"{height_str} – So groß wie eine Giraffe!"
        else:
            return f"{height_str} – So groß wie ein Haus!"

    @property
    def size_description_spoken(self) -> str:
        """German-phonetic version for TTS: '1 Meter siebzig' instead of '1,7 m'."""
        h = self.height
        if h < 1.0:
            cm = round(h * 100)
            spoken_height = f"{cm} Tsentimeter"
        else:
            m = int(h)
            cm = round((h - m) * 100)
            if cm == 0:
                spoken_height = f"{m} Meter"
            else:
                spoken_height = f"{m} Meter {cm}"

        if h <= 0.2:
            return f"{spoken_height}, Passt in deine Hand!"
        elif h <= 0.3:
            return f"{spoken_height}, So groß wie ein Lineal!"
        elif h <= 0.5:
            return f"{spoken_height}, So groß wie ein Teddy!"
        elif h <= 0.7:
            return f"{spoken_height}, So groß wie ein Kissen!"
        elif h <= 0.9:
            return f"{spoken_height}, So groß wie ein Bobbycar!"
        elif h <= 1.1:
            return f"{spoken_height}, So groß wie du!"
        elif h <= 1.3:
            return f"{spoken_height}, So groß wie ein Fahrrad!"
        elif h <= 1.6:
            return f"{spoken_height}, So groß wie ein Schneemann!"
        elif h <= 2.0:
            return f"{spoken_height}, So groß wie Mama oder Pappa!"
        elif h <= 3.0:
            return f"{spoken_height}, So groß wie eine Zimmerdecke!"
        elif h <= 5.0:
            return f"{spoken_height}, So groß wie eine Giraffe!"
        else:
            return f"{spoken_height}, So groß wie ein Haus!"


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
