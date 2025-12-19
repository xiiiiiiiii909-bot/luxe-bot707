import discord
from discord.ext import commands
from discord.ui import Button, View
import requests
from flask import Flask
from threading import Thread
import asyncio
import os # ضروري لجلب البورت من ريندر

# --- نظام الـ Keep Alive المطور لـ Luxe Store ---
app = Flask('')

@app.route('/')
def home(): 
    return "Luxe Store Bot is Active and Running 24/7!"

def run():
    # جلب البورت تلقائياً من Render لضمان عدم حدوث خطأ 502
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات Luxe Store ---
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------TOKEN = "MTQ1MTI3MDc2NzQxNjQ0MzEyMw.GW8yIz.qIkxllONGnhHx32BEv5W9eEm8cwauFJvW7yQzM" 
SHOP_CHANNEL_ID = 1445513442826911764    
ORDERS_CHANNEL_ID = 1451158466407174229  

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- قاعدة بيانات المنتجات ---
PRODUCTS = {
    "product_1": {
        "name": "🔥 𝐋𝐮𝐱𝐞 𝐒𝐭𝐨𝐫𝐞 / Bot ادارة الدسكورد", 
        "price": 59.93, 
        "images": [
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451286010297323745/1619.png", 
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451286108980904014/1620.png"
        ]
    },
    "product_2": {
        "name": "✨ نظام تسجيل دخول المطور / 𝐋𝐮𝐱𝐞 𝐒𝐭𝐨𝐫𝐞", 
        "price": 45.00, 
        "images": [
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451287027763908739/1621.png", 
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451287123608080394/1622.png",
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451287259004272722/1623.png",
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451287335978139868/1624.png",
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451287422607425688/1625.png",
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451287519374213321/1628.png",
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451287586680213609/1629.png"
        ]
    },
    "product_3": {
        "name": "💎 Luxe Stroe Bot / توظيف اداره ديسكورد", 
        "price": 39.99, 
        "images": [
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451289254901711091/1630.png", 
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451289323453550602/1631.png",
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451289414931058800/1632.png"
        ]
    },
    "product_4": {
        "name": "📊 بوت إضافة نقاط الإدارة التلقائي", 
        "price": 65.00, 
        "images": [
            "https://cdn.discordapp.com/attachments/1420695671438180507/1451316295529140347/image0.jpg"
        ]
    },
    "product_5": {
        "name": "💎 نـظـام Luxe AI Llama 3.3 70B الـمـتـطـور", 
        "price": 99.00, 
        "images": [
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451293546723414016/1633.png", 
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451293509649825823/1635.png",
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451293592034349249/1613.png"
        ]
    },
    "product_6": {
        "name": "🛡️ طـلـب بـوت خـاص / 𝐂𝐮𝐬𝐭𝐨𝐦 𝐁𝐨𝐭", 
        "price": 150.00, 
        "images": [
            "https://cdn.discordapp.com/attachments/1425216723749044315/1451295048082784420/Gemini_Generated_Image_cqcdzcqcdzcqcdzc.png"
        ]
    }
}

class StoreMainView(View):
    def __init__(self, product_id):
        super().__init__(timeout=None)
        self.product_id = product_id

    @discord.ui.button(label="عرض التفاصيل والطلب 🔍", style=discord.ButtonStyle.primary)
    async def open_browser(self, interaction: discord.Interaction, button: Button):
        view = PersonalCarousel(self.product_id)
        await interaction.response.send_message(embed=view.create_embed(), view=view, ephemeral=True)

class PersonalCarousel(View):
    def __init__(self, product_id):
        super().__init__(timeout=120)
        self.product_id = product_id
        self.index = 0
        self.quantity = 1
        self.data = PRODUCTS[product_id]
        
        if product_id != "product_6":
            self.remove_item(self.minus_btn)
            self.remove_item(self.plus_btn)

    def create_embed(self):
        total_price = round(self.data['price'] * self.quantity, 2)
        desc = f"\n💰 **السعر:** `{self.data['price']}` **ريال**"
        
        if self.product_id == "product_4":
            desc += "\n✨ نظام ذكي يضيف نقاط للإدارة عند (سحب سبورت، استلام تذاكر، تفعيل) مع قائمة التوب."
            
        if self.product_id == "product_6":
            desc += f"\n📦 **الكمية:** `{self.quantity}`\n💵 **الإجمالي:** `{total_price}` **ريال**"
        
        embed = discord.Embed(title=f"🛒 متصفح Luxe: {self.data['name']}", description=desc, color=0x00FFFF)
        embed.set_image(url=self.data['images'][self.index])
        embed.set_footer(text=f"صورة {self.index + 1} من {len(self.data['images'])} | خاص بك")
        return embed

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.secondary)
    async def prev(self, interaction: discord.Interaction, button: Button):
        self.index = (self.index - 1) % len(self.data['images'])
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="➖", style=discord.ButtonStyle.danger)
    async def minus_btn(self, interaction: discord.Interaction, button: Button):
        if self.quantity > 1:
            self.quantity -= 1
            await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="إرسال الطلب ✅", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        channel = bot.get_channel(ORDERS_CHANNEL_ID)
        total = round(self.data['price'] * self.quantity, 2)
        
        order_embed = discord.Embed(title="📦 طلب جديد وارد!", color=0x00FFFF)
        order_embed.add_field(name="العميل:", value=interaction.user.mention, inline=True)
        order_embed.add_field(name="المنتج:", value=self.data['name'], inline=True)
        order_embed.add_field(name="الكمية:", value=f"`{self.quantity}`", inline=True)
        order_embed.add_field(name="المجموع:", value=f"`{total}` ريال", inline=False)
        order_embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        await channel.send(embed=order_embed)
        await interaction.response.edit_message(content="🚀 تم إرسال طلبك بنجاح! سيتم التواصل معك قريباً.", embed=None, view=None)

    @discord.ui.button(label="➕", style=discord.ButtonStyle.success)
    async def plus_btn(self, interaction: discord.Interaction, button: Button):
        self.quantity += 1
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: Button):
        self.index = (self.index + 1) % len(self.data['images'])
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

@bot.command()
async def setup_store(ctx):
    if ctx.channel.id != SHOP_CHANNEL_ID: return
    await ctx.message.delete()
    for pid in PRODUCTS:
        data = PRODUCTS[pid]
        embed = discord.Embed(title=f"**{data['name']}**", description="انقر على الزر بالأسفل لمشاهدة كافة الصور والطلب.", color=0x00FFFF)
        embed.set_image(url=data['images'][0])
        await ctx.send(embed=embed, view=StoreMainView(pid))

@bot.event
async def on_ready():
    print(f"✅ Luxe Store System is Online.")
    print(f"🔗 Keep Alive URL: https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'your-app-name.onrender.com')}")

if __name__ == "__main__":
    keep_alive() # تشغيل النبض المطور
    bot.run(TOKEN)


