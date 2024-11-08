"""Main module for marketplace application."""
from src.marketplace import Marketplace
from src.models import User
from typing import Optional


def main() -> None:
    """Run the marketplace application."""
    marketplace = Marketplace()
    print("Добро пожаловать в мини-маркетплейс!")
    
    current_user = None
    
    while True:
        try:
            if not current_user:
                current_user = handle_auth_menu(marketplace)
                continue
                
            print("\n1. Выйти")
            if current_user.is_seller():
                print("2. Добавить товар")
                print("3. Редактировать товар")
                print("4. Удалить товар")
                print("5. Посмотреть свои товары")
            elif current_user.is_buyer():
                print("2. Посмотреть все товары")
                print("3. Добавить товар в корзину")
                print("4. Просмотреть корзину")
                print("5. Оформить покупку")

            choice = input("Выберите действие: ")
            
            if choice == '1':
                current_user = None
                print("Вы вышли из аккаунта.")
            elif current_user.is_seller():
                handle_seller_choice(marketplace, current_user, choice)
            elif current_user.is_buyer():
                handle_buyer_choice(marketplace, current_user, choice)
                
        except ValueError as error:
            print(f"Ошибка: {error}")
        except Exception as error:
            print(f"Произошла ошибка: {error}")


def handle_seller_choice(marketplace: Marketplace, seller: User, choice: str) -> None:
    """Handle seller menu choices."""
    if choice == '2':
        name = input("Название товара: ")
        price = float(input("Цена товара: "))
        description = input("Описание товара: ")
        marketplace.add_product(seller, name, price, description)
    elif choice == '3':
        product_id = int(input("ID товара для редактирования: "))
        new_name = input("Новое название (или Enter для пропуска): ")
        new_price_str = input("Новая цена (или Enter для пропуска): ")
        new_description = input("Новое описание (или Enter для пропуска): ")
        
        new_price = float(new_price_str) if new_price_str else None
        marketplace.edit_product(seller, product_id, new_name, new_price, new_description)
    elif choice == '4':
        product_id = int(input("ID товара для удаления: "))
        marketplace.delete_product(seller, product_id)
    elif choice == '5':
        marketplace.list_seller_products(seller)


def handle_buyer_choice(marketplace: Marketplace, buyer: User, choice: str) -> None:
    """Handle buyer menu choices."""
    if choice == '2':
        marketplace.list_products()
    elif choice == '3':
        product_id = int(input("ID товара для добавления в корзину: "))
        marketplace.add_to_cart(buyer, product_id)
    elif choice == '4':
        marketplace.view_cart(buyer)
    elif choice == '5':
        marketplace.checkout(buyer)


def handle_auth_menu(marketplace: Marketplace) -> Optional[User]:
    """Handle authentication menu.
    
    Args:
        marketplace (Marketplace): Marketplace instance
        
    Returns:
        Optional[User]: Authenticated user or None
    """
    print("\n1. Вход")
    print("2. Регистрация")
    action = input("Выберите действие: ")

    if action == '1':
        username = input("Имя пользователя: ")
        password = input("Пароль: ")
        return marketplace.login_user(username, password)
    elif action == '2':
        username = input("Имя пользователя: ")
        password = input("Пароль: ")
        user_type = input("Выберите тип пользователя (buyer/seller): ")
        if user_type in ['buyer', 'seller']:
            if marketplace.register_user(username, password, user_type):
                return marketplace.login_user(username, password)
        else:
            print("Неверный тип пользователя.")
    return None


if __name__ == "__main__":
    main()