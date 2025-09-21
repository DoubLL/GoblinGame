init -900 python in cardgame:
    from enum import Enum, IntFlag
    from typing import Callable, Optional
    import random

    cards = {} # Cards add themselves to this dictionary on creation

    class CardType(Enum):
        Stance = "Stance"
        Action = "Action"
        WinCon = "WinCon"
        Player = "Player"

    class Keywords(IntFlag):
        None_ = 0

    def build_card_image(image_path: str, type: CardType, name: str, desc: str, flavor: str, keywords: Keywords) -> renpy.display.core.Displayable:
        name_size = 50
        vw, vh = renpy.store.Text(name, size=name_size).size()
        if vw > 415:
            name_size = int(50 * (415 / vw))
        return renpy.store.Composite(
            (600, 900),
            (33, 127), renpy.store.Image(image_path),
            (0, 0), renpy.store.Image(
                "gui/cardgame/card neutral.png" # Add logic to use actor-specific background
                ),
            (50, 37), renpy.store.Text(name, size=name_size, color="#000"),
            (535, 65), renpy.store.Fixed(renpy.store.Text(type.value[0:2], size=65, color="#000", xanchor=0.5, yanchor=0.5)),
            (300, 445), renpy.store.Fixed(renpy.store.Text(f"{type.value}", size=28, color="#000", xanchor=0.5)),
            (15, 490), renpy.store.VBox(
                renpy.store.Text(desc, size=34, color="#000", xalign=0.5, textalign=0.5),
                renpy.store.Text(f"{{i}}{flavor}{{/i}}", size=32, color="#333", xalign=0.5, textalign=0.5),
                xsize=570,
                spacing=15,
            ),
            (0, 855), renpy.store.Fixed(
                renpy.store.Text(
                    ", ".join(tag.name for tag in keywords if tag != keywords.None_ and tag in keywords),
                    size=28, color="#000", xalign=0.5
                ) if keywords != keywords.None_
                else renpy.store.Fixed()
            )
        )

    class HookType(Enum):
        ON_PLAY = "on_play"
        ON_OTHER_CARD_PLAYED = "on_other_card_played"
        ON_START_ROUND = "on_start_round"
        ON_END_ROUND = "on_end_round"
        ON_LOSE_HEALTH = "on_lose_health"
        ON_GAIN_HEALTH = "on_gain_health"
        ON_LOSE_ARMOR = "on_lose_armor"
        ON_GAIN_ARMOR = "on_gain_armor"
        ON_ENEMY_LOSE_HEALTH = "on_enemy_lose_health"
        ON_ENEMY_GAIN_HEALTH = "on_enemy_gain_health"
        ON_ENEMY_LOSE_ARMOR = "on_enemy_lose_armor"
        ON_ENEMY_GAIN_ARMOR = "on_enemy_gain_armor"
        ON_HEALTH_ADJUSTED = "on_health_adjusted"
        ON_ENEMY_HEALTH_ADJUSTED = "on_enemy_health_adjusted"
        ON_GAIN_STANCE = "on_gain_stance"
        ON_LOSE_STANCE = "on_lose_stance"
        ON_ATTEMPT_WIN = "on_attempt_win"

    
    class CardEvent:
        def __init__(self, card_owner: 'CardActor', opponent: 'CardActor', card: 'Card'):
            self.card = card
            self.card_owner = card_owner
            self.opponent = opponent

    class Card:

        def __init__(
            self,
            name: str,
            type_: CardType,
            keywords: Keywords = Keywords.None_,
            description: str = "Description missing.",
            flavor: str = "Flavor text missing.",
            image: str = "gui/cardgame/images/default image.png",
            conditions: list[tuple[Callable, str]] = [],
            hooks: Optional[dict[HookType, Callable]] = None,
            register: bool = True
        ):
            self.name = name
            self.type_ = type_
            self.keywords = keywords
            self.description = description
            self.flavor = flavor
            self.conditions = conditions
            self.image_path = image
            self.image = build_card_image(image, type_, name, description, flavor, keywords)
            # Normalize hook keys to stable strings (enum values) to survive reloads
            normalized_hooks: dict[Any, Callable] = {}
            if hooks:
                for k, v in hooks.items():
                    key = k.value if isinstance(k, HookType) else (k.name if isinstance(k, Enum) else k)
                    normalized_hooks[key] = v
            self.hooks = normalized_hooks
            if register:
                cards[self.name] = self

        def copy(self) -> 'Card':
            return Card(
                name=self.name,
                type_=self.type_,
                keywords=self.keywords,
                description=self.description,
                flavor=self.flavor,
                image=self.image_path,
                condition=self.condition,
                hooks=self.hooks,
                register=False
            )

        ON_PLAY_TYPE = Callable[['Card', CardEvent], 'Card']
        def _get_hook(self, hook_type: HookType):
            # Accept both enum and string keys, and match across reloads by enum.value
            try_key = hook_type.value if isinstance(hook_type, HookType) else hook_type
            fn = self.hooks.get(try_key) or self.hooks.get(hook_type)
            if fn:
                return fn
            # Fallback: scan for Enum keys with the same value string (handles hot-reload identity mismatches)
            target_val = hook_type.value if isinstance(hook_type, HookType) else str(hook_type)
            for k, v in self.hooks.items():
                if isinstance(k, Enum) and getattr(k, 'value', None) == target_val:
                    return v
            return None
        def call_on_play(self, event: CardEvent) -> 'Card':
            fn = self._get_hook(HookType.ON_PLAY)
            if fn:
                result = fn(self, event)
                return result if result and isinstance(result, Card) else self
            return self

        ON_OTHER_CARD_PLAYED_TYPE = Callable[['Card', CardEvent, bool], 'Card']
        def call_on_other_card_played(self, event: CardEvent, is_mine: bool) -> 'Card':
            fn = self._get_hook(HookType.ON_OTHER_CARD_PLAYED)
            if fn:
                result = fn(self, event, is_mine)
                return result if result and isinstance(result, Card) else event.card
            return event.card

        ON_START_ROUND_TYPE = \
        ON_END_ROUND_TYPE = Callable[[CardEvent], None]
        def call_on_start_round(self, event: CardEvent) -> None:
            fn = self._get_hook(HookType.ON_START_ROUND)
            if fn:
                fn(self, event)
        def call_on_end_round(self, event: CardEvent) -> None:
            fn = self._get_hook(HookType.ON_END_ROUND)
            if fn:
                fn(self, event)

        ON_LOSE_HEALTH_TYPE = \
        ON_GAIN_HEALTH_TYPE = \
        ON_ENEMY_LOSE_HEALTH_TYPE = \
        ON_ENEMY_GAIN_HEALTH_TYPE = \
        ON_LOSE_ARMOR_TYPE = \
        ON_GAIN_ARMOR_TYPE = \
        ON_ENEMY_LOSE_ARMOR_TYPE = \
        ON_ENEMY_GAIN_ARMOR_TYPE = Callable[['Card', CardEvent, int], int]
        def _manipulate_value(self, hook_type: HookType, event: CardEvent, amount: int) -> int:
            fn = self._get_hook(hook_type)
            if fn:
                result = fn(self, event, amount)
                return result if result and isinstance(result, int) else amount
            return amount

        def call_on_lose_health(self, event: CardEvent, amount: int) -> int:
            return self._manipulate_value(HookType.ON_LOSE_HEALTH, event, amount)
        def call_on_gain_health(self, event: CardEvent, amount: int) -> int:
            return self._manipulate_value(HookType.ON_GAIN_HEALTH, event, amount)
        def call_on_lose_armor(self, event: CardEvent, amount: int) -> int:
            return self._manipulate_value(HookType.ON_LOSE_ARMOR, event, amount)
        def call_on_gain_armor(self, event: CardEvent, amount: int) -> int:
            return self._manipulate_value(HookType.ON_GAIN_ARMOR, event, amount)
        def call_on_enemy_lose_health(self, event: CardEvent, amount: int) -> int:
            return self._manipulate_value(HookType.ON_ENEMY_LOSE_HEALTH, event, amount)
        def call_on_enemy_gain_health(self, event: CardEvent, amount: int) -> int:
            return self._manipulate_value(HookType.ON_ENEMY_GAIN_HEALTH, event, amount)
        def call_on_enemy_lose_armor(self, event: CardEvent, amount: int) -> int:
            return self._manipulate_value(HookType.ON_ENEMY_LOSE_ARMOR, event, amount)
        def call_on_enemy_gain_armor(self, event: CardEvent, amount: int) -> int:
            return self._manipulate_value(HookType.ON_ENEMY_GAIN_ARMOR, event, amount)

        ON_HEALTH_ADJUSTED_TYPE = \
        ON_ENEMY_HEALTH_ADJUSTED_TYPE = Callable[['Card', CardEvent], None]
        def call_on_health_adjusted(self, event: CardEvent) -> None:
            fn = self._get_hook(HookType.ON_HEALTH_ADJUSTED)
            if fn:
                fn(self, event)
        def call_on_enemy_health_adjusted(self, event: CardEvent) -> None:
            fn = self._get_hook(HookType.ON_ENEMY_HEALTH_ADJUSTED)
            if fn:
                fn(self, event)

        ON_GAIN_STANCE_TYPE = Callable[['Card', CardEvent, bool], None]
        ON_LOSE_STANCE_TYPE = Callable[['Card', CardEvent, bool], None]
        def call_on_gain_stance(self, event: CardEvent, is_forced: bool) -> None:
            fn = self._get_hook(HookType.ON_GAIN_STANCE)
            if fn:
                fn(self, event, is_forced)
        def call_on_lose_stance(self, event: CardEvent, is_forced: bool) -> None:
            fn = self._get_hook(HookType.ON_LOSE_STANCE)
            if fn:
                fn(self, event, is_forced)

        ON_ATTEMPT_WIN_TYPE = Callable[['Card', CardEvent], None]
        def call_on_attempt_win(self, event: CardEvent) -> None:
            fn = self._get_hook(HookType.ON_ATTEMPT_WIN)
            if fn:
                fn(self, event)

        def __str__(self):
            return f"{self.name} ({self.type_.value}) - {self.hooks}"
