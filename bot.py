import discord
import os
import pytesseract
from PIL import Image, ImageEnhance

print("★★★ BOT起動 ★★★")

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"ログイン成功: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith((".png", ".jpg", ".jpeg")):
                os.makedirs("images", exist_ok=True)

                file_path = os.path.join("images", attachment.filename)
                await attachment.save(file_path)

                print(f"保存完了: {file_path}")

                img = Image.open(file_path)
                width, height = img.size

                right_area = img.crop((
                    int(width * 0.35),
                    int(height * 0.13),
                    int(width * 0.9),
                    int(height * 0.9)
                ))

                right_area_path = "images/test_right.png"
                right_area.save(right_area_path)

                rank_height = right_area.height // 4

                for i in range(4):
                     top = i * rank_height
                     bottom = (i + 1) * rank_height
                     
                     rank_block = right_area.crop((0, top, right_area.width, bottom))
                     
                     # ===== 名前エリア（上半分中央） =====
                     name_area = rank_block.crop((
                          int(rank_block.width * 0.2),
                          int(rank_block.height * 0.1),
                          int(rank_block.width * 0.8),
                          int(rank_block.height * 0.55)
                    ))
                     
                     # ===== 数字エリア（下半分中央） =====
                     number_area = rank_block.crop((
                           int(rank_block.width * 0.3),
                           int(rank_block.height * 0.55),
                           int(rank_block.width * 0.8),
                           int(rank_block.height * 0.9)
                    ))
                     
                     # ----- 前処理 -----
                     name_gray = name_area.convert("L")
                     number_gray = number_area.convert("L")
                     
                     # OCR（名前）
                     name_text = pytesseract.image_to_string(
                          name_gray,
                          lang="jpn",
                          config="--psm 7"
                    )
                     
                     # OCR（数字だけ）
                     number_text = pytesseract.image_to_string(
                          number_gray,
                          config="--psm 7 -c tessedit_char_whitelist=0123456789"
                    )
                     
                     print(f"{i+1}位 名前: {name_text.strip()}")
                     print(f"{i+1}位 数字: {number_text.strip()}")
                
                await message.channel.send("すべての処理が完了しました")

                print("処理終了")

client.run(TOKEN)