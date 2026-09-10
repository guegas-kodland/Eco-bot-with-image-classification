import discord
from discord.ext import commands
import os
from visao_computacional import detect_image

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

token = os.getenv('TOKEN_DO_DISCORD')

@bot.event
async def on_ready():
    print(f'Estamos logados como {bot.user}')

@bot.command()
async def hello(ctx):
    """Eu simplesmente te cumprimento :)"""
    await ctx.send(f'Olá! eu sou um bot {bot.user}!')

@bot.command()
async def ajuda(ctx):
    """Mostra todos os comandos disponíveis automaticamente"""
    embed = discord.Embed(
        title="Menu do EcoAmigo 🌿", 
        description="Confira tudo o que eu posso fazer por você e pelo planeta:", 
        color=0x2ecc71
    )

    for comando in bot.commands:
        descricao = comando.help if comando.help else "Comando disponível."
        embed.add_field(
            name=f"!{comando.name}", 
            value=descricao, 
            inline=False
        )
    
    await ctx.send(embed=embed)
@bot.command()
async def eco_produtos(ctx):
    """Mostra ideias de produtos mais sustentáveis"""
    produtos = [
        "Garrafa reutilizável (em vez de plástico descartável)",
        "Escova de dente de bambu",
        "Sacolas reutilizáveis",
        "Canudos de inox ou bambu",
        "Sabão e shampoo em barra",
        "Copos reutilizáveis"
    ]
    
    resposta = "🌱 Sugestões de produtos ecológicos:\n"
    for p in produtos:
        resposta += f"- {p}\n"
    
    await ctx.send(resposta)

@bot.command()
async def pegada(ctx):
    """Você poderá fazer um pequeno quiz para calcular sua pegada ecológica"""
    await ctx.send(
        "🌍 **Quiz de Pegada Ecológica** 🌍\n\n"
        "Responda com A, B ou C:\n\n"
        "1️⃣ Como você se locomove?\n"
        "A) Carro 🚗\n"
        "B) Transporte público 🚌\n"
        "C) Bicicleta ou a pé 🚶\n\n"
        "Digite sua resposta (ex: A):"
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg1 = await bot.wait_for("message", check=check, timeout=30)
        r1 = msg1.content.upper()

        await ctx.send(
            "2️⃣ Quanto tempo dura seu banho?\n"
            "A) Mais de 20 min 🚿\n"
            "B) 10–20 min\n"
            "C) Menos de 10 min\n"
        )

        msg2 = await bot.wait_for("message", check=check, timeout=30)
        r2 = msg2.content.upper()

        await ctx.send(
            "3️⃣ Você usa muito plástico?\n"
            "A) Sim 😬\n"
            "B) Às vezes\n"
            "C) Quase nunca ♻️\n"
        )

        msg3 = await bot.wait_for("message", check=check, timeout=30)
        r3 = msg3.content.upper()

        # pontuação
        pontos = 0

        respostas = [r1, r2, r3]
        for r in respostas:
            if r == "A":
                pontos += 2
            elif r == "B":
                pontos += 1
            elif r == "C":
                pontos += 0

        # resultado
        if pontos >= 5:
            resultado = "😬 Pegada ecológica ALTA! Tente reduzir seu impacto."
        elif pontos >= 3:
            resultado = "⚠️ Pegada MÉDIA. Dá pra melhorar!"
        else:
            resultado = "🌱 Pegada BAIXA! Mandou bem!"

        await ctx.send(f"Resultado:\n{resultado}")

    except:
        await ctx.send("⏰ Tempo esgotado! Tente novamente.")

@bot.command()
async def sustentavel(ctx, *, material):
    """Digite esse comando mais o nome do material (tudo minusculo e sem acentos) que eu vou falar se é sustentável ou não"""
    materiais = {
        "plastico": "❌ Não é sustentável. Demora centenas de anos para se decompor.",
        "vidro": "✅ Sustentável! Pode ser reciclado várias vezes.",
        "papel": "⚠️ Depende. É sustentável se for reciclado ou de fonte responsável.",
        "metal": "✅ Sustentável! Pode ser reciclado muitas vezes.",
        "aluminio": "✅ Muito sustentável! Reciclagem eficiente.",
        "bambu": "✅ Sustentável! Cresce rápido e é renovável.",
        "madeira": "⚠️ Depende. Sustentável se for de reflorestamento."
    }

    material = material.lower()

    if material in materiais:
        await ctx.send(f"{material.capitalize()}: {materiais[material]}")
    else:
        await ctx.send("🤔 Não tenho informação sobre esse material ainda.")

@bot.command()
async def dica(ctx):
    """Mostra uma dica aleatória de como ser mais ecológico"""
    dicas = [
        "💡 Apague as luzes ao sair de um cômodo.",
        "🚿 Tome banhos mais curtos.",
        "♻️ Separe o lixo reciclável.",
        "🛒 Evite produtos com muito plástico.",
        "🚲 Use bicicleta ou transporte público quando possível."
    ]

    import random
    await ctx.send(random.choice(dicas))

@bot.command()
async def imagem(ctx):
    """Verifica se uma imagem está na mensagem e salva-a na pasta"""
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_path = f"./{file_name}"
            await attachment.save(f"./{attachment.filename}")
            await ctx.send(f"Recebi a imagem {attachment.filename}! Agora, deixa eu pensar...")

        try:
            class_name, confidence_score = detect_image(file_path)
            percentage = confidence_score * 100
            await ctx.send(f"Isso deve ser um **{class_name}** (Certeza: {percentage :.2f})")

        except Exception as e:
            await ctx.send("Vixi! Parece que houve um erro ao classificar a imagem...")
            print(e)
    else:
        await ctx.send("Mas nem tem imagem aqui.")


bot.run("IT'S A SECRET FOR EVERYONE")