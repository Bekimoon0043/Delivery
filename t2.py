from telethon import TelegramClient, events, Button

# Replace with your own values
API_ID = '21078554'
API_HASH = 'fca31798b27a1010122a0ab57e9fdf63'
BOT_TOKEN = '7960311644:AAHBp5NpmNnkmwB7wvqsv3YQkixwrK-aDYo'

# Creating the client
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Dictionary to track users who selected Telebirr and CBE Birr
telebirr_users = {}
cbe_birr_users = {}
user_cart = {}
current_item = {}
user_food_choice = {}  # Track user food choices
user_drink_choice = {}  # Track user drink choices

# Define a price dictionary for food items
food_prices = {
    'beyaynet': 100,
    'testye': 100,
    'dinich': 100,
    'firfir': 100,
    'inkulal_tibs': 100,
    'inkualal_bedinich': 120
}

# Define a price dictionary for drink items
drink_prices = {
    'water': 35,
    'coca cola': 50,
    'fanta': 50
}

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    # Define inline buttons
    buttons = [
        [Button.inline("Food", b'food'),
         Button.inline("Drinks", b'drinks')],
        [Button.inline("Clear cart", b'clear'),
         Button.inline("Refresh", b'main_menu'),
         Button.inline("Help", b'help')],
        [Button.inline("pay for all", b'payhere')]
        
    ]

    food_items = user_cart.get(event.sender_id, {}).get('food', [])
    drink_items = user_cart.get(event.sender_id, {}).get('drinks', [])
           # Concatenate all selected food and drink items
    food_item_list1 = ', '.join(food_items) if food_items else ""
    drink_item_list1 = ', '.join(drink_items) if drink_items else ""
    user_info = (f'**Welcome!** to **Dire Dawa University** food delivery. Please choose an option to buy: \n')
    user_info += f'food you chosed: **{food_item_list1}**\n'
    user_info += f'Drink Items you chosed: **{drink_item_list1}**\n'
    

    # Send a message with inline buttons
    await event.respond(user_info, buttons=buttons)

@client.on(events.CallbackQuery)
async def button_click_handler(event):
    user_id = event.sender_id

    if event.data == b'food':
        # Define an inline button for food items
        food_buttons = [
            [Button.inline("beyaynet", b'beyaynet')],
            [Button.inline("testye", b'testye')],
            [Button.inline("dinich", b'dinich')],
            [Button.inline("firfir", b'firfir')],
            [Button.inline("inkulal tibs", b'inkulal_tibs')],
            [Button.inline("inkualal bedinich", b'inkualal_bedinich')],
            [Button.inline("Back", b'main_menu')]
        ]
        food_items = user_cart.get(event.sender_id, {}).get('food', [])
        drink_items = user_cart.get(event.sender_id, {}).get('drinks', [])
            
            # Concatenate all selected food and drink items
        food_item_list = ', '.join(food_items) if food_items else "No food items selected"
        drink_item_list = ', '.join(drink_items) if drink_items else "No drink items selected"
        user_info = (f'Please choose a food item: \n')
        user_info += f'food you chosed: {food_item_list}\n'
        user_info += f'Drink Items you chosed: {drink_item_list}\n'
        # Send the image buttons to choose food items
        await event.respond(user_info, buttons=food_buttons)

    elif event.data == b'drinks':
        # Define an inline button for drink items
        drink_buttons = [
            [Button.inline("water", b'water')],
            [Button.inline("coca cola", b'coca cola')],
            [Button.inline("fanta", b'fanta')],
            [Button.inline("Back", b'main_menu')]
        ]
        food_items = user_cart.get(event.sender_id, {}).get('food', [])
        drink_items = user_cart.get(event.sender_id, {}).get('drinks', [])
           # Concatenate all selected food and drink items
        food_item_list = ', '.join(food_items) if food_items else "No food items selected"
        drink_item_list = ', '.join(drink_items) if drink_items else "No drink items selected"
        user_info = (f'Please choose a drinking item: \n')
        user_info += f'food you chosed: {food_item_list}\n'
        user_info += f'Drink Items you chosed: {drink_item_list}\n'
        # Send the image buttons to choose drink items
        await event.respond(user_info, buttons=drink_buttons)

    elif event.data in {b'beyaynet', b'testye', b'dinich', b'firfir', b'inkulal_tibs', b'inkualal_bedinich'}:
        # Store selected food item in current_item and user_food_choice
        food_item = event.data.decode('utf-8')
        current_item[user_id] = {'type': 'food', 'item': food_item}
        user_food_choice[user_id] = food_item  # Store the food choice

        # Define an inline button for payment
        image_buttons = [
                         [Button.inline("add to cart", b'add')],
                         [Button.inline("Main Menu", b'main_menu')]]
        
        # Send the image with a caption and buttons together based on the chosen food item
        food_images = {
            'beyaynet': 'beyaynet.jpg',
            'testye': 'testye.jpeg',
            'dinich': 'dinich.jpeg',
            'firfir': 'firfir.jpeg',
            'inkulal_tibs': 'inkulal_tibs.jpeg',
            'inkualal_bedinich': 'inkualal_bedinich.jpeg'
        }
        
        # Get the price for the selected food item
        price = food_prices[food_item]
        
        await client.send_file(
            event.chat_id,
            food_images[food_item],
            caption=f'{food_item}: with delivery only {price} birr',
            buttons=image_buttons
        )

    elif event.data in {b'water', b'coca cola', b'fanta'}:
        # Store selected drink item in current_item and user_drink_choice
        drink_item = event.data.decode('utf-8')
        current_item[user_id] = {'type': 'drink', 'item': drink_item}
        user_drink_choice[user_id] = drink_item  # Store the drink choice

        # Define an inline button for payment
        image_buttons = [
                         [Button.inline(" add to cart", b'add')],
                         [Button.inline("Main Menu", b'main_menu')]]
        
        # Send the image with a caption and buttons together based on the chosen drink item
        drink_images = {
            'water': 'water.png',
            'coca cola': 'coca cola.png',
            'fanta': 'fanta.jpeg'
        }
        
        # Get the price for the selected drink item
        price = drink_prices[drink_item]
        
        await client.send_file(
            event.chat_id,
            drink_images[drink_item],
            caption=f'{drink_item}: with delivery only {price} birr',
            buttons=image_buttons
        )

    elif event.data == b'add':
        # Add the current item to the user's cart
        if user_id in current_item:
            item_info = current_item[user_id]
            item_type = item_info['type']
            item_name = item_info['item']
            
            user_cart.setdefault(user_id, {'food': [], 'drinks': []})
            if item_type == 'food':
                user_cart[user_id]['food'].append(item_name)
            else:
                user_cart[user_id]['drinks'].append(item_name)

            await event.respond(f'Added {item_name} to your cart!')

    elif event.data == b'payhere':
        # Calculate total price for food items in the cart
        total_food_price = sum(food_prices[item] for item in user_cart.get(user_id, {}).get('food', []))
        total_drink_price = sum(drink_prices[item] for item in user_cart.get(user_id, {}).get('drinks', []))
        total_price = total_food_price + total_drink_price

        # Define payment options for food
        payment_buttons = [
            [Button.inline("anybank to Telebirr", b'telebirr')],
            [Button.inline("anybank to CBE", b'cbebirr')],
            [Button.inline("Cash on Delivery", b'cash_on_delivery')],
            [Button.inline("Main Menu", b'main_menu')]
        ]
        food_items = user_cart.get(event.sender_id, {}).get('food', [])
        drink_items = user_cart.get(event.sender_id, {}).get('drinks', [])
            
            # Concatenate all selected food and drink items
        food_item_list = ', '.join(food_items) if food_items else "No food items selected"
        drink_item_list = ', '.join(drink_items) if drink_items else "No drink items selected"
        user_info = (f'Which payment system do you want?\n')
        user_info += f'Total amount to pay: {total_price}\n'
        user_info += f'Food Items: **{food_item_list}**\n'
        user_info += f'Drinking items: {drink_item_list}\n'
        # Ask the user which payment system they want for food
        await event.respond(user_info, buttons=payment_buttons)

    elif event.data == b'payhere':
        # Calculate total price for drink items in the cart
        total_food_price = sum(food_prices[item] for item in user_cart.get(user_id, {}).get('food', []))
        total_drink_price = sum(drink_prices[item] for item in user_cart.get(user_id, {}).get('drinks', []))
        total_price = total_food_price + total_drink_price

        # Define payment options for drinks
        payment_buttons = [
            [Button.inline("anybank to Telebirr", b'telebirr_drink')],
            [Button.inline("anybank to CBE", b'cbebirr_drink')],
            [Button.inline("Cash on Delivery", b'cash_on_delivery_drink')],
            [Button.inline("Main Menu", b'main_menu')]
        ]
        
        # Ask the user which payment system they want for drinks
        await event.respond(f'Total amount to pay: {total_price} birr. Which payment system do you want?', buttons=payment_buttons)
        
    elif event.data == b'telebirr':
        # Handle Telebirr payment for food
        telebirr_users[event.sender_id] = True
        food_items = user_cart.get(event.sender_id, {}).get('food', [])
        
        if food_items:
                # Calculate total price for drink items in the cart
            total_food_price = sum(food_prices[item] for item in user_cart.get(user_id, {}).get('food', []))
            total_drink_price = sum(drink_prices[item] for item in user_cart.get(user_id, {}).get('drinks', []))
            total_price = total_food_price + total_drink_price
            food_items = user_cart.get(event.sender_id, {}).get('food', [])
            drink_items = user_cart.get(event.sender_id, {}).get('drinks', [])
            
            # Concatenate all selected food and drink items
            food_item_list = ', '.join(food_items) if food_items else "No food items selected"
            drink_item_list = ', '.join(drink_items) if drink_items else "No drink items selected"
            user_info = (f'Send **{total_price}** birr to this number **0978494843** and send a **SCREENSHOT** of the payment **your phone number should be together like the image above**\n')
            user_info += f'Total amount to pay: **{total_price}**\n'
            user_info += f'Food Items: **{food_item_list}**\n'
            user_info += f'Drinking items: **{drink_item_list}**\n'
            
            image_path = 'bb.jpg'  # Update this path
            buttons = [
            [Button.inline("Main Menu", b'main_menu')]
]
            
            await client.send_file(event.chat_id, image_path, caption=user_info, buttons=buttons, parse_mode='markdown')
        else:
            await event.respond('No food item selected. Please select a food item first.')
            
    elif event.data == b'cbebirr':
        # Handle CBE payment for food
        cbe_birr_users[event.sender_id] = True
        food_items = user_cart.get(event.sender_id, {}).get('food', [])
        
        if food_items:
                # Calculate total price for drink items in the cart
            total_food_price = sum(food_prices[item] for item in user_cart.get(user_id, {}).get('food', []))
            total_drink_price = sum(drink_prices[item] for item in user_cart.get(user_id, {}).get('drinks', []))
            total_price = total_food_price + total_drink_price
            food_items = user_cart.get(event.sender_id, {}).get('food', [])
            drink_items = user_cart.get(event.sender_id, {}).get('drinks', [])
            
            # Concatenate all selected food and drink items
            food_item_list = ', '.join(food_items) if food_items else "No food items selected"
            drink_item_list = ', '.join(drink_items) if drink_items else "No drink items selected"
            user_info = (f'Send **{total_price}** birr to this account number **1000474794978** and send a **SCREENSHOT** of the payment **your phone number should be together like the image above**\n')
            user_info += f'Total amount to pay: **{total_price}**\n'
            user_info += f'Food Items: **{food_item_list}**\n'
            user_info += f'Drinking items: **{drink_item_list}**\n'
            image_path = 'cbe.jpg' # Update this path
            buttons = [
            [Button.inline("Main Menu", b'main_menu')]
]          
            await client.send_file(event.chat_id, image_path, caption=user_info, buttons=buttons, parse_mode='markdown')
        else:
            await event.respond('No food item selected. Please select a food item first.') 

    elif event.data == b'main_menu':
        await start_handler(event)

    elif event.data == b'help':
        user_guide = (
            "📚 **DDU Food Delivery Bot User Guide**\n"
            "Welcome! Use this guide to navigate the Dire Dawa Food Delivery Bot easily.\n\n"
            "**Main Options**\n"
            "1. **Food**: Browse food items.\n"
            "2. **Drinks**: Browse drink items.\n"
            "3. **add to cart**: adding items to buy.\n"
            "4. **Clear Cart**: Remove all items from your cart.\n"
            "5. **Refresh**: Update the menu.\n"
            "6. **Help**: Get assistance.\n"
            "7. **Pay for All**: Proceed to payment.\n\n"
            "**Food & Drink Selection**\n"
            "1. Food: Click to see items like Beyaynet and Testye. View details and **add to cart**.\n"
            "2. Drinks: Click to see items like Water and Coca Cola. View details and **add to cart**.\n\n"
            "**Managing Your Cart**\n"
            "View your cart anytime.\n"
            "Use Clear Cart to empty it.\n"
            "Use Refresh to update the menu.\n\n"
            "**Payment Process**\n"
            "Click Pay for All to choose a payment method:\n"
            "Telebirr: Send payments to Telebirr. this means you can send money from **anybank**(anywhere) to telebirr\n"
            "CBE: Send payments to CBE.this means you can send money from **anybank**(anywhere) to CBE\n"
            "Follow the instructions for payment and send a **screenshot** with your **phone** on the caption of your confirmation to the bot.\n\n"
        )
        buttons = [
            [Button.inline("Main Menu", b'main_menu')]
]         
        await event.respond(user_guide, buttons=buttons)

    elif event.data == b'clear':
        # Clear the user's cart
        user_cart[user_id] = {'food': [], 'drinks': []}
        await event.respond('Your cart has been cleared! know click Refresh')

@client.on(events.NewMessage)
async def handler(event):
    # Check if the user has selected Telebirr or CBE Birr
    if event.sender_id in telebirr_users or event.sender_id in cbe_birr_users:
        if event.media and event.media.photo:
            user = await event.get_sender()
            username = user.username if user.username else "No username"
            print(f' New image from {event.sender_id} ({username})')
            await event.respond('The admin will respond to you soon! 👍')
            caption = event.message.message if event.message.message else "No caption provided"
            user_id_admin = 6546621672  # Replace with your user ID
            
            food_items = user_cart.get(event.sender_id, {}).get('food', [])
            drink_items = user_cart.get(event.sender_id, {}).get('drinks', [])
            
            # Concatenate all selected food and drink items
            food_item_list = ', '.join(food_items) if food_items else "No food items selected"
            drink_item_list = ', '.join(drink_items) if drink_items else "No drink items selected"

            # Get the total prices for the selected food and drink items
            food_price = sum(food_prices[item] for item in food_items)
            drink_price = sum(drink_prices[item] for item in drink_items)

            user_info = (f'New image from {event.sender_id}\n')
            user_info += f'username: @{username}\n'
            user_info += f'Food Items: {food_item_list}\n'
            user_info += f'Food Total Price: {food_price}\n'
            user_info += f'Drink Items: {drink_item_list}\n'
            user_info += f'Drink Total Price: {drink_price}\n'
            user_info += f'Payment Amount: {food_price + drink_price}\n'
            user_info += f'phone or accountno: {caption}\n'
            
            await client.send_file(user_id_admin, event.message.media, caption=user_info)
            await client.send_message(user_id_admin, "Please reply to this message:")
        else:
            # Avoid sending an empty message
            await event.respond('')
    else:
        await event.respond('')

@client.on(events.NewMessage(pattern='/send (.+)'))
async def send_message_handler(event):
    try:
        command_parts = event.message.message.split(' ', 2)
        if len(command_parts) < 3:
            await event.respond('Usage: /send <user_id> <message>')
            return
        
        user_id = int(command_parts[1])
        message = command_parts[2]

        await client.send_message(user_id, message)
        await event.respond(f'Message sent to user {user_id}: "{message}"')
    except ValueError:
        await event.respond('Invalid user ID. Please enter a valid numeric user ID.')
    except Exception as e:
        await event.respond(f'An error occurred: {str(e)}')

# Start the client
print("bot is running.....")
client.run_until_disconnected()