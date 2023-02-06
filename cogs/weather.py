import os
import logging
import discord

from discord import app_commands, ui, ButtonStyle
from discord.app_commands import locale_str as _T
from discord.ext import commands

from bot import BotCore

from typing import Optional, List

from utils.translator import Translator, TranslatorCallable
from utils.embed import Embed
from utils.types import WeatherData, WeatherAlert
from utils.views import EmbedPaginator


log = logging.getLogger(__name__)

WEATHER_API_BASE_URL = 'https://api.weatherapi.com/v1'


class ShowAlertsButton(ui.View):
    def __init__(
        self,
        t: TranslatorCallable,
        alerts: List[WeatherAlert],
        *,
        timeout: Optional[float] = 180
    ):
        super().__init__(timeout=timeout)

        self.alerts: List[WeatherAlert] = alerts

        self.show_alert.label = t('commands.weather.show_alert')

    @ui.button(emoji='⚠', style=ButtonStyle.blurple)
    async def show_alert(self, interaction: discord.Interaction, button: ui.Button) -> None:
        embeds = []
        for alert in self.alerts:
            embed = discord.Embed(
                title=alert.headline,
                description=alert.desc,
                color=discord.Colour.brand_red()
            )
            embeds.append(embed)

        if len(embeds) == 1:
            await interaction.response.edit_message(embed=embeds[0], view=None)
        else:
            view = EmbedPaginator(embeds, check=lambda i: i.user == interaction.user)
            await interaction.response.edit_message(embed=embeds[0], view=view)

        self.stop()


class Weather(commands.Cog):
    def __init__(self, bot: BotCore) -> None:
        self.bot: BotCore = bot

    def _classify_uv_index(self, t: TranslatorCallable, uv_index: int) -> str:
        match uv_index:
            case 0 | 1 | 2 | 3:
                return t('commands.weather.uv_index_rating.low')
            case 4 | 5 | 6:
                return t('commands.weather.uv_index_rating.moderate')
            case 7 | 8:
                return t('commands.weather.uv_index_rating.high')
            case 9 | 10 | 11:
                return t('commands.weather.uv_index_rating.very_high')
            case _:
                return t('commands.weather.uv_index_rating.extreme')

    weather = app_commands.Group(
        name=_T('weather', id='commands.weather.name'),
        description=_T('...', id='commands.weather.description'),
        guild_only=False
    )

    @weather.command(
        name=_T('current', id='commands.weather.current.name'),
        description=_T('...', id='commands.weather.current.description')
    )
    @app_commands.rename(
        city=_T('city', id='commands.weather.current.options.city.name')
    )
    @app_commands.describe(
        city=_T('...', id='commands.weather.current.options.city.description')
    )
    @app_commands.checks.cooldown(1, 5)
    async def weather_current(self, interaction: discord.Interaction, city: str):
        t = Translator(interaction.locale)
        await interaction.response.defer()
        url = (
            f'{WEATHER_API_BASE_URL}/forecast.json?' +
            f'key={os.environ.get("WEATHER_API_KEY")}&' +
            f'q={city}&days=1&alerts=yes'
        )

        try:
            async with self.bot.session.request('GET', url) as res:
                data = await res.json()
        except Exception as e:
            log.error('Request error', exc_info=e)
            embed = Embed.error(t('errors.request_error'))
            return await interaction.followup.send(embed=embed)

        if res.status != 200:
            #  City not found
            if data['error']['code'] == 1006:
                embed = Embed.error(t('errors.city_not_found'))
            else:
                embed = Embed.error(t('errors.request_error'))
                embed.set_footer(
                    text=t(
                        'errors.error_code', error_code=data['error']['code']
                    )
                )
            return await interaction.followup.send(embed=embed)

        data = WeatherData(data)

        day_or_night = 'day' if data.current.is_day else 'night'
        condition_text = t(f'commands.weather.codes.{data.current.condition_code}.{day_or_night}')

        embed = discord.Embed(
            title=f'{data.location.name}, {data.location.country}',
            description=condition_text,
            color=0x5ea3d8,
            timestamp=data.current.last_updated
        )

        embed.add_field(
            name='🌡 ' + t('commands.weather.temperature'),
            value=f'{data.current.temp_c}° C | {data.current.temp_f}° F',
            inline=False
        )

        embed.add_field(
            name='💧 ' + t('commands.weather.humidity'),
            value=f'{data.current.humidity}%',
            inline=False
        )

        embed.add_field(
            name='💨 ' + t('commands.weather.wind_speed'),
            value=f'{data.current.wind_kph} km/h',
            inline=False
        )

        embed.add_field(
            name='☀ ' + t('commands.weather.uv_index'),
            value=f'{self._classify_uv_index(t, int(data.current.uv))}',
            inline=False
        )

        embed.set_footer(
            text='https://www.weatherapi.com/' + ' | ' + t('commands.weather.last_updated')
        )

        embed.set_thumbnail(url='https:' + data.current.condition_icon)

        if len(data.alerts) > 0:
            alert_embed = discord.Embed(
                description=t('commands.weather.alert_available'),
                color=discord.Colour.brand_red()
            )

            embeds = [alert_embed, embed]

            view = ShowAlertsButton(t, data.alerts)

            await interaction.followup.send(embeds=embeds, view=view)
        else:
            await interaction.followup.send(embed=embed)

    @weather.command(
        name=_T('forecast', id='commands.weather.forecast.name'),
        description=_T('...', id='commands.weather.forecast.description')
    )
    @app_commands.rename(
        city=_T('city', id='commands.weather.forecast.options.city.name')
    )
    @app_commands.describe(
        city=_T('...', id='commands.weather.forecast.options.city.description')
    )
    @app_commands.checks.cooldown(1, 5)
    async def weather_forecast(self, interaction: discord.Interaction, city: str):
        t = Translator(interaction.locale)
        await interaction.response.defer()
        url = (
            f'{WEATHER_API_BASE_URL}/forecast.json?' +
            f'key={os.environ.get("WEATHER_API_KEY")}&' +
            f'q={city}&days=3&alerts=yes'
        )
        discord.Locale

        try:
            async with self.bot.session.request('GET', url) as res:
                data = await res.json()
        except Exception as e:
            log.error('Request error', exc_info=e)
            embed = Embed.error(t('errors.request_error'))
            return await interaction.followup.send(embed=embed)

        if res.status != 200:
            #  City not found
            if data['error']['code'] == 1006:
                embed = Embed.error(t('errors.city_not_found'))
            else:
                embed = Embed.error(t('errors.request_error'))
                embed.set_footer(
                    text=t(
                        'errors.error_code', error_code=data['error']['code']
                    )
                )
            return await interaction.followup.send(embed=embed)

        data = WeatherData(data)

        day_or_night = 'day' if data.current.is_day else 'night'

        embeds = []
        for i, day in enumerate(data.forecast, 1):
            condition_text = t(f'commands.weather.codes.{day.condition_code}.{day_or_night}')

            embed = discord.Embed(
                title=discord.utils.format_dt(day.date, 'd'),
                description=condition_text,
                color=0x5ea3d8
            )

            if i == 1:
                embed.set_author(
                    name=f'{data.location.name}, {data.location.country}'
                )

            embed.add_field(
                name='🌡 ' + t('commands.weather.temperature'),
                value=(
                    f'🔼 {day.maxtemp_c}° C | {day.maxtemp_f}° F\n'
                    f'🔽 {day.mintemp_c}° C | {day.mintemp_f}° F'
                )
            )
            if day.daily_chance_of_rain > 0:
                embed.add_field(
                    name='🌧 ' + t('commands.weather.chance_of_rain'),
                    value=f'{day.daily_chance_of_rain}%'
                )
            if day.daily_chance_of_snow > 0:
                embed.add_field(
                    name='❄ ' + t('commands.weather.chance_of_snow'),
                    value=f'{day.daily_chance_of_snow}%'
                )
            embed.set_thumbnail(url='https:' + data.current.condition_icon)

            if i == len(data.forecast):
                embed.set_footer(
                    text=(
                        'https://www.weatherapi.com/' + ' | ' +
                        t('commands.weather.last_updated')
                    )
                )
                embed.timestamp = data.current.last_updated

            embeds.append(embed)

        if len(data.alerts) > 0:
            alert_embed = discord.Embed(
                description=t('commands.weather.alert_available'),
                color=discord.Colour.brand_red()
            )
            embeds.insert(0, alert_embed)

            view = ShowAlertsButton(t, data.alerts)

            await interaction.followup.send(embeds=embeds, view=view)
        else:
            await interaction.followup.send(embeds=embeds)


async def setup(bot: BotCore) -> None:
    await bot.add_cog(Weather(bot))
