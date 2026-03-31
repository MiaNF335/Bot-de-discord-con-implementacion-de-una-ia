import discord
import os
from discord.ext import commands
import random
from Colorimetry import analizar_colorimetria

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def dado(ctx):
    n = random.randint(1,6)
    await ctx.send(f"tu dado: {n}")

@bot.command()
async def moneda(ctx):
    y = random.randint (1,2)
    if y == 1:
        await ctx.send(f"tu moneda salio cara")
    else:
        await ctx.send(f"tu moneda salio cruz")

@bot.command()
async def check(ctx):
    if ctx.message.attachments:#verifica si hay imagenes
        for attachment in ctx.message.attachments: #ctx.message.attachments es una lista, de archivos y con el for se pasa una por uno.
            await attachment.save(f"images/{attachment.filename}")#permite continuar el codigo si se llega a tardar la carga de la imagen el otro comando del inicio hace q la imagen se guarde en una carpeta
            await ctx.send(f"Tiene un archivo llamado{attachment.filename} y su url es {attachment.url}")#filename es para sacar el nombre de la imagen y el url la url de la imagen

    else:
        await ctx.send("No tiene un archivo")


@bot.command()
async def color(ctx):
# 1. Verificamos si el usuario subió una imagen
    if not ctx.message.attachments:
        await ctx.send("¡Hola! Para analizar tu colorimetría, por favor adjunta una foto tuya al comando.")
        return

    attachment = ctx.message.attachments[0]
    
    # 2. Validamos que sea un formato de imagen soportado
    formatos_validos = ('.png', '.jpg', '.jpeg', '.webp')
    if any(attachment.filename.lower().endswith(ext) for ext in formatos_validos):
        
        await ctx.send("🎨 **Analizando tu imagen... esto puede tardar unos segundos.**")
        
        # 3. Guardamos la imagen temporalmente en tu PC
        path_temporal = f"temp_{attachment.filename}"
        await attachment.save(path_temporal)
        
        try:
            # 4. LLAMADA A LA IA
            # Ahora recibimos: resultado (str), confianza (float) e info_extra (str)
            resultado, confianza, info_extra = analizar_colorimetria(path_temporal)
            
            # 5. ARMADO DEL MENSAJE FINAL
            # Usamos formato de Discord (### para títulos, ** para negritas)
            respuesta = (
                f"### ✨ Análisis de Colorimetría ✨\n"
                f"Tu estación es: **{resultado}**\n"
                f"Nivel de certeza: `{confianza}%`"
                f"{info_extra}" # Aquí ya vienen los consejos y famosos
            )
            
            await ctx.send(respuesta)

        except Exception as e:
            await ctx.send("❌ Hubo un error técnico al procesar la imagen.")
            print(f"Error en el servidor: {e}")
            
        finally:
            # 6. LIMPIEZA
            # Borramos la foto de tu carpeta para que no se llene de archivos temporales
            if os.path.exists(path_temporal):
                os.remove(path_temporal)
    else:
        await ctx.send("Por favor, sube un archivo de imagen válido (.jpg o .png).")


bot.run("TOKEN HERE")