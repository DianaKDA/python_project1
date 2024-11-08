"""Marketplace module containing main business logic."""
import json
import os
from typing import List, Optional, Dict, Any
from .models import User, Product


class Marketplace:
    """Main marketplace class handling all business logic."""

    def __init__(self) -> None:
        """Initialize marketplace with storage paths."""
        self.USERS_FILE = 'assets/users.json'
        self.PRODUCTS_FILE = 'assets/products.json'
        self._initialize_storage()

    def _initialize_storage(self) -> None:
        """Initialize storage files if they don't exist."""
        for filename in [self.USERS_FILE, self.PRODUCTS_FILE]:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            if not os.path.exists(filename):
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump([], file)

    def _load_data(self, filename: str) -> List[Dict[str, Any]]:
        """Load data from JSON file.
        
        Args:
            filename (str): Path to JSON file
            
        Returns:
            List[Dict[str, Any]]: Loaded data
        """
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _save_data(self, filename: str, data: List[Dict[str, Any]]) -> None:
        """Save data to JSON file.
        
        Args:
            filename (str): Path to JSON file
            data (List[Dict[str, Any]]): Data to save
        """
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def register_user(self, username: str, password: str, user_type: str) -> bool:
        """Register new user.
        
        Args:
            username (str): Username
            password (str): Password
            user_type (str): User type ('buyer' or 'seller')
            
        Returns:
            bool: True if registration successful, False otherwise
        """
        if user_type not in ['buyer', 'seller']:
            raise ValueError("Неверный тип пользователя")
            
        users = self._load_data(self.USERS_FILE)
        if any(user['username'] == username for user in users):
            print("Пользователь с таким именем уже существует.")
            return False
            
        user = User(
            username=username,
            password=password,
            user_type=user_type,
            cart=[]
        )
        users.append(user.to_dict())
        self._save_data(self.USERS_FILE, users)
        print(f"Пользователь {username} успешно зарегистрирован!")
        return True

    def login_user(self, username: str, password: str) -> Optional[User]:
        """Login user with given credentials.
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            Optional[User]: User instance if credentials are valid, None otherwise
        """
        users = self._load_data(self.USERS_FILE)
        user_dict = next(
            (user for user in users 
             if user['username'] == username and user['password'] == password),
            None
        )
        
        if user_dict:
            print(f"Добро пожаловать, {username}!")
            return User.from_dict(user_dict)
        print("Неверное имя пользователя или пароль.")
        return None

    def list_products(self) -> List[Product]:
        products = self._load_data(self.PRODUCTS_FILE)
        if not products:
            print("Нет доступных товаров.")
            return []
            
        product_list = [Product(**p) for p in products]
        for product in product_list:
            print(f"ID: {product.id}, Название: {product.name}, "
                  f"Цена: {product.price}, Продавец: {product.seller}")
        return product_list

    def add_product(self, seller: User, name: str, price: float, description: str) -> None:
        if not seller.is_seller():
            print("Только продавцы могут добавлять товары.")
            return

        products = self._load_data(self.PRODUCTS_FILE)
        product_id = len(products) + 1
        product = Product(
            id=product_id,
            name=name,
            price=price,
            description=description,
            seller=seller.username
        ).__dict__
        
        products.append(product)
        self._save_data(self.PRODUCTS_FILE, products)
        print(f"Товар {name} добавлен в маркетплейс.")

    def add_to_cart(self, user: User, product_id: int) -> None:
        if not user.is_buyer():
            print("Только покупатели могут добавлять товары в корзину.")
            return

        products = self._load_data(self.PRODUCTS_FILE)
        product = next((p for p in products if p['id'] == product_id), None)
        
        if product:
            users = self._load_data(self.USERS_FILE)
            user_idx = next(i for i, u in enumerate(users) 
                          if u['username'] == user.username)
            
            users[user_idx]['cart'].append(product)
            self._save_data(self.USERS_FILE, users)
            print(f"Товар {product['name']} добавлен в вашу корзину.")
        else:
            print("Товар не найден.")

    def view_cart(self, user: User) -> None:
        if not user.is_buyer():
            print("Только покупатели могут просматривать корзину.")
            return
        
        if not user.cart:
            print("Ваша корзина пуста.")
            return
            
        print("Ваши товары в корзине:")
        total = 0
        for idx, item in enumerate(user.cart, 1):
            print(f"{idx}. {item['name']} - {item['price']} руб.")
            total += item['price']
        print(f"\nОбщая сумма: {total} руб.")

    def checkout(self, user: User) -> None:
        if not user.is_buyer():
            print("Только покупатели могут оформлять покупку.")
            return
        
        if not user.cart:
            print("Ваша корзина пуста.")
            return
        
        total = sum(item['price'] for item in user.cart)
        print(f"Сумма вашей покупки: {total} руб.")
        confirm = input("Подтвердить покупку? (да/нет): ").lower()
        
        if confirm == 'да':
            users = self._load_data(self.USERS_FILE)
            user_idx = next(i for i, u in enumerate(users) 
                          if u['username'] == user.username)
            
            users[user_idx]['cart'] = []
            self._save_data(self.USERS_FILE, users)
            print("Покупка успешно оформлена. Спасибо за ваш заказ!")
        else:
            print("Оформление покупки отменено.")

    def edit_product(self, seller: User, product_id: int, 
                    new_name: Optional[str] = None,
                    new_price: Optional[float] = None,
                    new_description: Optional[str] = None) -> None:
        if not seller.is_seller():
            print("Только продавцы могут редактировать товары.")
            return

        products = self._load_data(self.PRODUCTS_FILE)
        product_idx = next((i for i, p in enumerate(products) 
                          if p['id'] == product_id and p['seller'] == seller.username), None)
        
        if product_idx is not None:
            if new_name:
                products[product_idx]['name'] = new_name
            if new_price:
                products[product_idx]['price'] = new_price
            if new_description:
                products[product_idx]['description'] = new_description
                
            self._save_data(self.PRODUCTS_FILE, products)
            print(f"Товар {products[product_idx]['name']} успешно обновлен.")
        else:
            print("Товар не найден или вы не являетесь его владельцем.")

    def delete_product(self, seller: User, product_id: int) -> None:
        if not seller.is_seller():
            print("Только продавцы могут удалять товары.")
            return

        products = self._load_data(self.PRODUCTS_FILE)
        product = next((p for p in products 
                       if p['id'] == product_id and p['seller'] == seller.username), None)

        if product:
            products.remove(product)
            self._save_data(self.PRODUCTS_FILE, products)
            print(f"Товар {product['name']} удален.")
        else:
            print("Товар не найден или вы не являетесь его владельцем.")

    def list_seller_products(self, seller: User) -> List[Product]:
        if not seller.is_seller():
            print("Только продавцы могут просматривать свои товары.")
            return []

        products = self._load_data(self.PRODUCTS_FILE)
        seller_products = [Product(**p) for p in products 
                         if p['seller'] == seller.username]
        
        if seller_products:
            print(f"Ваши товары, продавец {seller.username}:")
            for product in seller_products:
                print(f"ID: {product.id} | Название: {product.name} | "
                      f"Цена: {product.price} руб. | "
                      f"Описание: {product.description}")
        else:
            print("У вас нет добавленных товаров.")
            
        return seller_products