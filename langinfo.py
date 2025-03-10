class LangMetadata:
    def __init__(self, name, popularity, change, rank2025, rank2024):
        self.name = name
        self.popularity = popularity
        self.change = change
        self.rank2025 = rank2025
        self.rank2024 = rank2024

    def __str__(self):
        return f"{self.name}, {self.popularity}, {self.rank2025}, {self.rank2024}, {self.change}"


class LangInfo:
    def __init__(self, metadata, short_description, long_description):
        self.metadata = metadata
        self.short_description = short_description
        self.long_description = long_description

    def __str__(self):
        return f"{self.metadata} \n {self.short_description} \n {self.long_description}"

    @classmethod
    def from_string(cls, lang_str):
        try:
            metadata_part, short_desc, long_desc = lang_str.split(" \n ", 2)

            metadata_values = metadata_part.split(", ")
            if len(metadata_values) != 6:
                raise ValueError("Invalid metadata format")

            name, popularity, rank2025, rank2024, change = metadata_values

            rank2025, rank2024 = int(rank2025), int(rank2024)

            metadata = LangMetadata(name, popularity, change, rank2025, rank2024)

            return cls(metadata, short_desc, long_desc)

        except Exception as e:
            raise ValueError(f"Error parsing LangInfo from string: {e}")