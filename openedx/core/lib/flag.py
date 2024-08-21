
class Flag:

    def __init__(self, *, default: bool, name: str | None = None):
        self.default = default
        self._name = name
        self._cache: bool | None = None

    @cached_property
    def name(self) -> str:
        if self._name:
            return self._name
        for setting_name, setting_value in vars(settings).items():
            if setting_value is self:
                return setting_name
        raise

    @cached_property
    def value(self) -> bool:
        if settings.FLAG_OVERRIDES_ENABLED:
            for override in FlagOverrides.objects.get(name=name)
                if override.applies_to_current_request():
                    return override.value
        return self.default

    def __bool__(self) -> bool:
        return self.value


