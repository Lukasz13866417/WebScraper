class LangMetadata:
    def __init__(self, name, popularity, change, changeType, rank2025, rank2024):
        self.name = name
        self.popularity = popularity
        self.change = change
        self.changeType = changeType
        self.rank2025 = rank2025
        self.rank2024 = rank2024

    def __str__(self):
        return f"{self.name}, {self.popularity}, {self.rank2025}, {self.rank2024}, {self.change}, {self.changeType}"


class LangInfo:
    def __init__(self, metadata, short_description, long_description):
        self.metadata = metadata
        self.short_description = short_description
        self.long_description = long_description

    def __str__(self):
        """
        Returns a structured string representation of LangInfo.
        Format:
        LangMetadata(name, popularity, rank2025, rank2024, change, changeType) | short_description | long_description
        """
        return f"{self.metadata} \n {self.short_description} \n {self.long_description}"

    @classmethod
    def from_string(cls, lang_str):
        """
        Parses a LangInfo object from its string representation.
        """
        try:
            # Split metadata and descriptions
            metadata_part, short_desc, long_desc = lang_str.split(" \n ", 2)

            # Extract metadata fields from its string representation
            metadata_values = metadata_part.split(", ")
            if len(metadata_values) != 6:
                raise ValueError("Invalid metadata format")

            name, popularity, rank2025, rank2024, change, changeType = metadata_values

            # Convert numeric fields
            rank2025, rank2024 = int(rank2025), int(rank2024)

            # Reconstruct LangMetadata
            metadata = LangMetadata(name, popularity, change, changeType, rank2025, rank2024)

            # Return the reconstructed LangInfo object
            return cls(metadata, short_desc, long_desc)

        except Exception as e:
            raise ValueError(f"Error parsing LangInfo from string: {e}")