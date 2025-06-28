import os
import chainlit as cl
from openai import OpenAI
from chainlit.types import AskFileResponse

# Set up OpenAI API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

system_message = """
คุณคือ OrderBot ระบบอัตโนมัติสำหรับรับออเดอร์ของร้านพิซซ่า
เริ่มต้นด้วยการทักทายลูกค้า จากนั้นรับออเดอร์
แล้วถามว่าลูกค้าจะรับเองหรือให้จัดส่ง
คุณจะรอจนกว่าจะได้รับออเดอร์ครบทั้งหมด จากนั้นสรุปออเดอร์และตรวจสอบครั้งสุดท้าย
ว่าลูกค้าต้องการเพิ่มอะไรอีกหรือไม่
หากเป็นการจัดส่ง คุณจะขอที่อยู่
สุดท้ายคุณจะดำเนินการเก็บเงิน
อย่าลืมอธิบายตัวเลือกทั้งหมด เช่น ท็อปปิ้ง ขนาด และรายละเอียดอื่น ๆ ให้ชัดเจน
เพื่อระบุรายการอาหารจากเมนูได้อย่างถูกต้อง
ตอบโต้ด้วยสไตล์ที่เป็นกันเอง สั้น และกระชับ
เมนูมีดังนี้:
พิซซ่าเปปเปอโรนี 12.95, 10.00, 7.00
พิซซ่าชีส 10.95, 9.25, 6.50
พิซซ่ามะเขือม่วง 11.95, 9.75, 6.75
เฟรนช์ฟรายส์ 4.50, 3.50
สลัดกรีก 7.25
ท็อปปิ้ง:
ชีสเพิ่ม 2.00
เห็ด 1.50
ไส้กรอก 3.00
เบคอนแคนาดา 3.50
ซอส AI 1.50
พริกหยวก 1.00
เครื่องดื่ม:
โค้ก 3.00, 2.00, 1.00
สไปรท์ 3.00, 2.00, 1.00
น้ำเปล่าขวด 5.00
"""

# Initialize conversation history
conversation_history = []

@cl.on_chat_start
async def start():
    # Initialize the conversation with the system message
    conversation_history.append({"role": "system", "content": system_message})
    # Send welcome message
    await cl.Message(content="ยินดีต้อนรับสู่ร้านพิซซ่า! ต้องการอะไรครับ?").send()

@cl.on_message
async def main(message: cl.Message):
    try:
        # Add user message to conversation history
        conversation_history.append({"role": "user", "content": message.content})
        
        # Get response from OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        
        # Get the assistant's message
        assistant_message = completion.choices[0].message.content
        
        # Add assistant's response to conversation history
        conversation_history.append({"role": "assistant", "content": assistant_message})
        
        # Send the response back to the user
        await cl.Message(content=str(assistant_message)).send()
        
    except Exception as e:
        await cl.Message(content=f"An error occurred: {str(e)}").send()