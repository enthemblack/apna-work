import logging
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8523181326:AAGqYXjhXlw73carr3ldM0Ye6xqgXnGm9PA"

logging.basicConfig(level=logging.INFO)

# Extract JSON safely (supports nested JSON)
def extract_json(text):
    decoder = json.JSONDecoder()
    idx = 0
    results = []

    while idx < len(text):
        try:
            obj, end = decoder.raw_decode(text[idx:])
            results.append(obj)
            idx += end
        except json.JSONDecodeError:
            idx += 1

    return results

# Merge all JSON blocks including nested vehicle_details
def merge_data(json_list):
    merged = {}

    for item in json_list:
        if isinstance(item, list):
            for sub in item:
                merged.update(sub)
        elif isinstance(item, dict):
            merged.update(item)
            if "vehicle_details" in item and isinstance(item["vehicle_details"], dict):
                merged.update(item["vehicle_details"])

    return merged

# Build FINAL TEXT MESSAGE (YOUR FORMAT)
def build_message(d):
    mobile = d.get("mobileNo", "N/A")
    vehicle_no = d.get("vehicleNumber") or d.get("regNo") or d.get("vehicle_number", "N/A")
    vehicle_name = d.get("vehicle") or d.get("make_model") or d.get("model_name2") or d.get("model_name", "N/A")
    vehicle_type = d.get("vehicleType") or d.get("vehicle_type", "N/A")
    reg_date = d.get("regDate") or d.get("registration_date", "N/A")
    reg_auth = d.get("regAuthority") or d.get("registration_address", "N/A")
    engine = d.get("engine") or d.get("engine_number", "N/A")
    chassis = d.get("chassis") or d.get("chassis_number", "N/A")

    return f"""
Mobile number - {mobile}

Your Challan No. 384915784195624 for vehicle {vehicle_no} having total challan ammount Rs 8000.

𝐃𝐮𝐞 𝐭𝐨 - 𝚃𝚛𝚊𝚏𝚏𝚒𝚌 𝚟𝚒𝚘𝚕𝚎𝚗𝚌𝚎 𝚋𝚢 𝚢𝚘𝚞𝚛 𝚟𝚎𝚑𝚒𝚌𝚕𝚎 𝚗𝚎𝚊𝚛 𝙲𝚋𝚒 𝚏𝚊𝚝𝚊𝚔 (𝚓𝚊𝚐𝚊𝚝𝚙𝚞𝚛𝚊 𝚛𝚘𝚊𝚍)

𝐓𝐨 𝐜𝐡𝐞𝐜𝐤 𝐨𝐟 𝐜𝐡𝐚𝐥𝐥𝐚𝐧 𝐯𝐢𝐬𝐢𝐭 𝗠𝗽𝗮𝗿𝗶𝘃𝗮𝗵𝗮𝗻.𝗮𝗽𝗸 𝐭𝐨 𝐜𝐡𝐞𝐜𝐤 𝐅𝐢𝐧𝐞 / 𝐩𝐚𝐲

Vehicle details -

𝐑𝐞𝐠𝐢𝐬𝐭𝐫𝐚𝐭𝐢𝐨𝐧 𝐧𝐨 - {vehicle_no}

𝐕𝐞𝐡𝐢𝐜𝐥𝐞 𝐧𝐚𝐦𝐞 -  {vehicle_name}
𝐕𝐞𝐡𝐢𝐜𝐥𝐞 𝐭𝐲𝐩𝐞 - {vehicle_type}
𝐑𝐞𝐠𝐢𝐬𝐭𝐫𝐚𝐭𝐢𝐨𝐧 𝐝𝐚𝐭𝐞 - {reg_date}
𝐑𝐞𝐠𝐢𝐬𝐭𝐫𝐚𝐭𝐢𝐨𝐧 𝐚𝐝𝐝𝐫𝐞𝐬𝐬 -  {reg_auth}

𝐄𝐧𝐠𝐢𝐧𝐞 𝐧𝐨 - {engine}
𝐂𝐡𝐚𝐬𝐬𝐢𝐬 𝐧𝐨 - {chassis}
""".strip()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send vehicle JSON and I will format the message.")

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    json_data = extract_json(update.message.text)

    if not json_data:
        await update.message.reply_text("❌ No valid JSON found.")
        return

    merged = merge_data(json_data)
    message = build_message(merged)

    await update.message.reply_text(message, parse_mode="Markdown")

# Main
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running...")
app.run_polling()
