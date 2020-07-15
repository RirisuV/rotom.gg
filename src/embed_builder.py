import discord
import pokeapi_manager

class EmbedBuilder:

    def __init__(self, config):
        self.config = config
        self.pokeapi = pokeapi_manager.PokeApiManager(config)
        
        self.icon_url = config['rotomgg']['icon_url']
        self.bot_name = "rotom.gg"


    def format_pokemon_message(self, pkmn_data, pkmn_desc):
        flavor_text = list(filter(lambda x:x['language']['name']=='en', pkmn_desc['flavor_text_entries']))

        embed=discord.Embed(title=f"#{pkmn_data['id']} {pkmn_data['species']['name']}", url="", description=flavor_text[0]['flavor_text'])
        embed.set_author(name=self.bot_name, icon_url=self.icon_url)
        embed.set_thumbnail(url=pkmn_data['sprites']['front_default'])
        embed.add_field(name='Basic', value=self.build_pokemon_default_data_text(pkmn_data, pkmn_desc), inline=False)
        embed.add_field(name='Stats', value=self.build_pokemon_basic_stats_text(pkmn_data), inline=False)

        for ability in pkmn_data['abilities']:
            ability_precisely_data = self.pokeapi.get_pokemon_abilities_from_url(ability['ability']['url'])
            effect_entries = list(filter(lambda x:x['language']['name']=='en', ability_precisely_data['effect_entries']))

            if ability['is_hidden']:
                ability_type = 'hidden ability'
            else:
                ability_type = 'ability'
            
            embed.add_field(name=f"[{ability_type}] {ability['ability']['name']}", value=effect_entries[0]['effect'], inline=False)

        return embed


    def build_pokemon_basic_stats_text(self, pkmn_data):
        pkmn_stats = pkmn_data['stats']
        
        return f"HP {pkmn_stats[0]['base_stat']} / Atk {pkmn_stats[1]['base_stat']} / Def {pkmn_stats[2]['base_stat']} / SpA {pkmn_stats[3]['base_stat']} / SpD {pkmn_stats[4]['base_stat']} / Spe {pkmn_stats[5]['base_stat']}"


    def build_pokemon_default_data_text(self, pkmn_data, pkmn_desc):
        if len(pkmn_data['types']) == 2:
            type_text = f"{pkmn_data['types'][0]['type']['name']} / {pkmn_data['types'][1]['type']['name']}"
        else:
            type_text = pkmn_data['types'][0]['type']['name'] 

        genra = list(filter(lambda x:x['language']['name']=='en', pkmn_desc['genera']))

        return f"{genra[0]['genus']} | {type_text} | Height: {pkmn_data['height']/10}m | Weight: {pkmn_data['weight']/10}kg"
