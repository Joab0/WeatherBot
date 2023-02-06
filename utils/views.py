import discord

from discord import ui, ButtonStyle

from typing import Optional, List, Callable


class EmbedPaginator(ui.View):
    def __init__(
        self,
        embeds: List[discord.Embed],
        *,
        check: Optional[Callable[[discord.Interaction], bool]] = None,
        timeout: Optional[float] = 180
    ):
        super().__init__(timeout=timeout)

        assert len(embeds) > 1
        self.embeds = embeds

        self.check = check
        if self.check is None:
            self.check = lambda i: True

        self.index = 0

        self.current_page.disabled = True
        self._update_state()

    def _update_state(self) -> None:
        self.previous_page.disabled = self.index == 0
        self.next_page.disabled = self.index + 1 == len(self.embeds)
        self.current_page.label = f'{self.index + 1}/{len(self.embeds)}'

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not self.check(interaction):
            await interaction.response.defer()
            return False
        return True

    @ui.button(emoji='◀', style=ButtonStyle.gray)
    async def previous_page(self, interaction: discord.Interaction, button: ui.Button) -> None:
        self.index -= 1
        self._update_state()

        embed = self.embeds[self.index]
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button()
    async def current_page(self, interaction: discord.Interaction, button: ui.Button) -> None:
        pass

    @ui.button(emoji='▶', style=ButtonStyle.gray)
    async def next_page(self, interaction: discord.Interaction, button: ui.Button) -> None:
        self.index += 1
        self._update_state()

        embed = self.embeds[self.index]
        await interaction.response.edit_message(embed=embed, view=self)
