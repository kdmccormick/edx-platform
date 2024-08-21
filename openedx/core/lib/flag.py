

@dataclass
class Scope:
    value: bool

    authenticated: bool | None = None
    superusers: bool | None = None
    staff: bool | None = None

    user_ids: list[int] | None = None
    group_id: list[int] | None = None
    languages: list[str] | None = None
    percent: float | None = None
    percent_ttl_ms: int | None = None

    org: str | None = None
    context: LearningContextKey | str | None = None


    @classmethod
    def from_database(cls, db_override: FlagDatabaseOverride) -> t.Self:
        return cls(
            ...
        )

    def includes(self, user: User | None, context: LearningContextKey | None) -> bool:

        ...


class FlagDatabaseOverride(models.Model):
    ...



class Flag:

    def __init__(self, global_default: bool, /)
        self.global_default = global_default
        self._code_overrides: list[tuple[Scope, bool]] = []

    @cached_property
    def name(self) -> str:
        for setting_name, setting_value in vars(settings).items():
            if setting_value is self:
                return setting_name
        raise

    def override(self, scope: Scope, value: bool, /) -> None:
        self._code_overrides.append(scope, value)

    @cached_property
    def _db_overrides(self) -> list[tuple[Scope, bool]]:
        if settings.ENABLE_FLAG_OVERRIDES_IN_DATABASE:
            return [
                Scope.from_database(db_override)
                for db_override in FlagDatabaseOverride.objects.get(name=self.name)
            ]
        return []

    def for_context(self, context_key: LearningContextKey | None):
        user = _get_user()
        for scope, value in reversed(self._code_overrides + self._db_overrides):
            if scope.includes(user, context_key):
                return value
        return self.default

    def __bool__(self) -> bool:
        return self.for_context(None)
