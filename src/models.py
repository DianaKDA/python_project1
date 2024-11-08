"""Models module for marketplace application."""
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Product:
    """Product model representing marketplace item.
    
    Attributes:
        id (int): Unique identifier of the product
        name (str): Name of the product
        price (float): Price of the product
        description (str): Description of the product
        seller (str): Username of the seller
    """
    id: int
    name: str
    price: float
    description: str
    seller: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert product to dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the product
        """
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'seller': self.seller
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create product from dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary with product data
            
        Returns:
            Product: New product instance
        """
        return cls(**data)

@dataclass
class User:
    """User model representing marketplace user.
    
    Attributes:
        username (str): Unique username
        password (str): User's password
        user_type (str): Type of user ('buyer' or 'seller')
        cart (List[Dict]): List of products in user's cart
    """
    username: str
    password: str
    user_type: str
    cart: List[Dict] = field(default_factory=list)

    def is_buyer(self) -> bool:
        """Check if user is a buyer.
        
        Returns:
            bool: True if user is a buyer, False otherwise
        """
        return self.user_type == 'buyer'

    def is_seller(self) -> bool:
        """Check if user is a seller.
        
        Returns:
            bool: True if user is a seller, False otherwise
        """
        return self.user_type == 'seller'

    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the user
        """
        return {
            'username': self.username,
            'password': self.password,
            'user_type': self.user_type,
            'cart': self.cart
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create user from dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary with user data
            
        Returns:
            User: New user instance
        """
        return cls(**data)