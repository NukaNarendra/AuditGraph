import difflib


class EntityResolver:


    @staticmethod
    def normalize_name(name: str) -> str:

        return name.strip().lower()

    @staticmethod
    def is_match(name1: str, name2: str, threshold=0.85) -> bool:
        n1 = EntityResolver.normalize_name(name1)
        n2 = EntityResolver.normalize_name(name2)


        if n1 == n2:
            return True

        matcher = difflib.SequenceMatcher(None, n1, n2)
        return matcher.ratio() > threshold

    @staticmethod
    def resolve_entity_id(candidate_name: str, existing_names: list) -> str:

        for existing in existing_names:
            if EntityResolver.is_match(candidate_name, existing):
                return existing  # Reuse the old ID (Merge)
        return candidate_name  # Create new ID