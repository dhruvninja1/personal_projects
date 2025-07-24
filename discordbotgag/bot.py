import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import websockets
import json
import asyncio
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger('discord_bot_seeds')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

GAGAPI_WEBSOCKET_URL = "ws://localhost:8000/ws"
REST_API_BASE_URL = "http://localhost:8000" 

NOTIFICATION_CHANNEL_ID = 1397784869756604560
TARGET_GUILD_ID = 1397784868808560640 

SEED_ROLE_MAP = {} 

ALL_SEED_NAMES = [
    "Carrot", "Strawberry", "Blueberry", "Tomato", "Cauliflower",
    "Watermelon", "Rafflesia", "Green Apple", "Avocado", "Banana",
    "Pineapple", "Kiwi", "Bell Pepper", "Prickly Pear", "Loquat",
    "Feijoa", "Pitcher Plant", "Sugar Apple", "Burning Bud", "Giant Pinecone",
    "Pumpkin", "Beanstalk", "Ember Lily", "Apple", "Pear",
    "Raspberry", "Daffodil", "Corn", "Coconut", "Cactus",
    "Dragon Fruit", "Mango", "Rose", "Orange Tulip", "Lavender",
    "Foxglove", "Lilac", "Sunflower", "Nectarine", "Hive Fruit",
    "Mushroom", "Cacao", "Bamboo", "Purple Dahlia", "Pink Lily",
    "Lemon", "Zenflare", "Soft Sunshine", "Spiked Mango", "Monoblooma",
    "Serenity", "Taro Flower", "Zen Rocks", "Hinomai", "Maple Apple",
    "Wild Carrot", "Cantaloupe", "Parasol Flower", "Rosy Delight",
    "Elephant Ears", "Crocus", "Succulent", "Violet Corn", "Bendboo",
    "Cocovine", "Dragon Pepper", "Bone Blossom", "Stonebite",
    "Paradise Petal", "Horned Dinoshroom", "Boneboo", "Firefly Fern",
    "Fossilight", "Chocolate Carrot", "Red Lollipop", "Candy Sunflower",
    "Easter Egg", "Candy Blossom", "Durian", "Cranberry", "Eggplant",
    "Lotus", "Venus Flytrap", "Papaya", "Passionfruit", "Cursed Fruit",
    "Soul Fruit", "Nightshade", "Glowshroom", "Mint", "Moonflower",
    "Starfruit", "Moonglow", "Moon Blossom", "Blood Banana", "Moon Melon",
    "Moon Mango", "Celestiberry", "Manuka Flower", "Dandelion", "Lumira",
    "Honeysuckle", "Nectarshade", "Tiger Lily", "Chili", "Lime"
]
# --- End Seed Role List ---

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

last_known_seed_stock = {}


def transform_seed_list_to_dict(seed_list):
    """
    Transforms a list of seed dictionaries (from FastAPI) into a
    dictionary keyed by seed name for easier lookup and comparison.
    """
    if not isinstance(seed_list, list):
        # If it's not a list, it might be an empty dict or None, handle gracefully
        logger.warning(f"Expected a list of seeds, but got type: {type(seed_list)}. Data: {seed_list}")
        return {} # Return an empty dict to prevent further errors
        
    transformed_dict = {}
    for seed_item in seed_list:
        if isinstance(seed_item, dict) and "name" in seed_item:
            transformed_dict[seed_item["name"]] = seed_item
        else:
            logger.warning(f"Skipping malformed seed item: {seed_item}")
    return transformed_dict

# --- WebSocket Listener Task ---
@tasks.loop(seconds=1)
async def websocket_listener_task():
    global last_known_seed_stock
    while not bot.is_closed():
        try:
            logger.info(f"Attempting to connect to WebSocket at {GAGAPI_WEBSOCKET_URL}...")
            async with websockets.connect(GAGAPI_WEBSOCKET_URL) as websocket:
                logger.info("WebSocket connected. Listening for updates...")
                notification_channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
                if not notification_channel:
                    logger.warning(f"Notification channel with ID {NOTIFICATION_CHANNEL_ID} not found!")

                # Initialize last_known_seed_stock correctly when bot first connects
                # This ensures format_seed_changes has a valid dict from the start
                initial_data_received = False

                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        logger.info(f"Received WebSocket data: {data}")

                        if "type" in data and data["type"] == "stock_update" and "data" in data:
                            # The incoming data["data"] holds all categories (weather, gear, seeds, etc.)
                            current_all_stock_data = data["data"]

                            # Safely get the 'seeds' list and transform it into a dictionary
                            # This is the crucial change
                            current_seed_list = current_all_stock_data.get("seeds", [])
                            current_seed_stock_dict = transform_seed_list_to_dict(current_seed_list)

                            if not initial_data_received:
                                last_known_seed_stock = current_seed_stock_dict.copy()
                                initial_data_received = True
                                logger.info("Initial seed stock state captured.")
                                # Don't send a message on initial capture unless you want one
                                # continue # uncomment to skip initial message

                            seed_changes_message = await format_seed_changes(last_known_seed_stock, current_seed_stock_dict, notification_channel)

                            if seed_changes_message and notification_channel:
                                await notification_channel.send(f"🌱 **Grow A Garden Seed Stock Update!** 🌱\n{seed_changes_message}")
                                logger.info("Sent seed update message to Discord.")

                            last_known_seed_stock = current_seed_stock_dict.copy()

                    except websockets.exceptions.ConnectionClosed as e:
                        logger.warning(f"WebSocket connection closed unexpectedly: {e}. Reconnecting in 5 seconds...")
                        await asyncio.sleep(5)
                        break
                    except json.JSONDecodeError:
                        logger.error(f"Received non-JSON message from WebSocket: {message}")
                    except Exception as e:
                        logger.error(f"Error processing WebSocket message: {e}", exc_info=True)
                        await asyncio.sleep(5)

        except websockets.exceptions.InvalidURI:
            logger.error(f"Invalid WebSocket URI: {GAGAPI_WEBSOCKET_URL}. Please check the URL.")
            await asyncio.sleep(60)
        except ConnectionRefusedError:
            logger.error(f"WebSocket connection refused. Is the GAGAPI server running and accessible at {GAGAPI_WEBSOCKET_URL}?")
            await asyncio.sleep(10)
        except Exception as e:
            logger.error(f"Unhandled WebSocket connection error: {e}", exc_info=True)
            await asyncio.sleep(10)



async def format_seed_changes(old_seeds, new_seeds, channel):
    changes = []

    all_seed_names = sorted(list(set(old_seeds.keys()) | set(new_seeds.keys())))

    for seed_name in all_seed_names:
        old_details = old_seeds.get(seed_name, {})
        new_details = new_seeds.get(seed_name, {})

        old_quantity = old_details.get('quantity')
        new_quantity = new_details.get('quantity')

        # Check for changes in quantity, or if a seed appeared/disappeared
        if old_quantity != new_quantity or (seed_name not in old_seeds and seed_name in new_seeds) or (seed_name in old_seeds and seed_name not in new_seeds):
            role_mention = ""
            role_id = SEED_ROLE_MAP.get(seed_name)
            if role_id and channel:
                guild = channel.guild
                if guild:
                    role = guild.get_role(role_id)
                    if role:
                        role_mention = role.mention
                    else:
                        logger.warning(f"Role with ID {role_id} for {seed_name} not found in guild {guild.name}.")

            change_str = f"{role_mention} is in stock!" if role_mention else ""
            change_str += f"**{seed_name}:** "

            if old_details == {} and new_details != {}: # New seed appeared
                change_str += f"**NEW!** Quantity: `{new_quantity}`"
            elif new_details == {} and old_details != {}: # Seed removed
                change_str += f"**REMOVED!** (Was Quantity: `{old_quantity}`)"
            else: # Existing seed changed quantity
                if old_quantity is not None and new_quantity is not None:
                    change_str += f"Quantity: `{old_quantity}` -> `{new_quantity}`"
                elif new_quantity is not None: # Changed from non-existent/None to a quantity
                    change_str += f"Quantity: `{new_quantity}`"
                elif old_quantity is not None: # Changed from a quantity to non-existent/None
                    change_str += f"Quantity: `{old_quantity}` -> `N/A`" # Should be covered by removed case, but kept as a fallback

            changes.append(change_str)

    return "\n".join(changes) if changes else None


# --- Discord Bot Events ---
@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info('Starting WebSocket listener task...')
    websocket_listener_task.start()
    
    await populate_seed_role_map()

@bot.event
async def on_disconnect():
    logger.warning("Bot disconnected from Discord. Stopping WebSocket listener.")
    websocket_listener_task.stop()

@bot.event
async def on_resumed():
    logger.info("Bot reconnected to Discord. Restarting WebSocket listener if necessary.")
    if not websocket_listener_task.is_running():
        websocket_listener_task.start()
    await populate_seed_role_map() 


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the necessary permissions to run this command.")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("This command cannot be used in private messages.")
    else:
        logger.error(f"Error in command {ctx.command}: {error}", exc_info=True)
        await ctx.send("An unexpected error occurred while executing the command.")


# --- Function to populate SEED_ROLE_MAP ---
async def populate_seed_role_map():
    global SEED_ROLE_MAP
    guild = bot.get_guild(TARGET_GUILD_ID)
    if not guild:
        logger.error(f"Guild with ID {TARGET_GUILD_ID} not found. Cannot populate SEED_ROLE_MAP.")
        return

    SEED_ROLE_MAP.clear() 

    found_count = 0
    for seed_name in ALL_SEED_NAMES:
        role = discord.utils.get(guild.roles, name=seed_name)
        if role:
            SEED_ROLE_MAP[seed_name] = role.id
            found_count += 1
            logger.debug(f"Found existing role for {seed_name}: ID {role.id}")
        else:
            logger.debug(f"No existing role found for {seed_name}.")
    logger.info(f"Populated SEED_ROLE_MAP with {found_count} existing roles out of {len(ALL_SEED_NAMES)}.")


# --- Command to create all seed roles ---
@bot.command(name='createseedroles')
@commands.has_permissions(manage_roles=True) 
@commands.guild_only()
async def create_seed_roles(ctx):
    """
    Creates all specified seed roles in the server.
    Requires 'Manage Roles' permission for the bot and the user.
    """
    guild = ctx.guild
    if not guild: 
        await ctx.send("This command must be used in a server.")
        return

    await ctx.send(f"Attempting to create {len(ALL_SEED_NAMES)} seed roles. This may take a moment...")
    
    created_count = 0
    skipped_count = 0
    failed_count = 0

    for seed_name in ALL_SEED_NAMES:
       
        existing_role = discord.utils.get(guild.roles, name=seed_name)
        if existing_role:
            skipped_count += 1
            logger.info(f"Role '{seed_name}' already exists. Skipping creation.")
            continue

        try:
            # Create the role
            new_role = await guild.create_role(
                name=seed_name,
                mentionable=True,
                permissions=discord.Permissions.none(),
                color=discord.Color.green()
            )
            SEED_ROLE_MAP[seed_name] = new_role.id 
            created_count += 1
            logger.info(f"Successfully created role: {seed_name} (ID: {new_role.id})")
            await asyncio.sleep(0.5)
        except discord.Forbidden:
            failed_count += 1
            logger.error(f"Bot lacks permissions to create role '{seed_name}'. Make sure bot role is high enough and has 'Manage Roles' permission.")
            await ctx.send(f"Error: Bot lacks permissions to create role `{seed_name}`. Please check bot's permissions and role hierarchy.")
        except discord.HTTPException as e:
            failed_count += 1
            logger.error(f"HTTP error creating role '{seed_name}': {e}")
            await ctx.send(f"Error creating role `{seed_name}`: {e.text}")
        except Exception as e:
            failed_count += 1
            logger.error(f"An unexpected error occurred while creating role '{seed_name}': {e}", exc_info=True)
            await ctx.send(f"An unexpected error occurred while creating role `{seed_name}`.")
            
    await ctx.send(
        f"Role creation complete!\n"
        f"✅ Created: {created_count}\n"
        f"⏭️ Skipped (already existed): {skipped_count}\n"
        f"❌ Failed: {failed_count}"
    )
    await populate_seed_role_map()


# --- Manual check command for seeds ---
@bot.command(name='checkseeds')
async def check_seeds(ctx):
    """Manually checks and displays the current seeds stock."""
    if not REST_API_BASE_URL:
        await ctx.send("GAGAPI REST API base URL is not configured.")
        return

    try:
        response = requests.get(f"{REST_API_BASE_URL}/seeds")
        response.raise_for_status()
        data = response.json()

        if data:
            stock_message = "🌱 **Current Grow A Garden Seed Stock:** 🌱\n"
            seed_stock_dict = transform_seed_list_to_dict(data)

            if seed_stock_dict:
                for item_name, details in seed_stock_dict.items():
                    role_mention = ""
                    role_id = SEED_ROLE_MAP.get(item_name)
                    if role_id and ctx.guild:
                        role = ctx.guild.get_role(role_id)
                        if role:
                            role_mention = role.mention

                    # Only display quantity
                    quantity = details.get('quantity', 'N/A')
                    stock_message += f"{role_mention} **{item_name}:** Quantity: `{quantity}`\n"
            else:
                stock_message = "No seed stock data available."
        else:
            stock_message = "Could not retrieve seed stock data from API (empty response)."

        await ctx.send(stock_message)

    except requests.exceptions.RequestException as e:
        await ctx.send(f"Error fetching seed stock data from API: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")


bot.run(TOKEN)