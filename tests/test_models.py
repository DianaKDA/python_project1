"""Test module for models."""
import pytest
from src.models import User, Product


def test_product_creation():
    """Test product creation and methods."""
    product_data = {
        'id': 1,
        'name': 'Test Product',
        'price': 100.0,
        'description': 'Test Description',
        'seller': 'test_seller'
    }
    
    product = Product(**product_data)
    assert product.to_dict() == product_data
    
    product_from_dict = Product.from_dict(product_data)
    assert product_from_dict == product


def test_user_creation():
    """Test user creation and methods."""
    user_data = {
        'username': 'test_user',
        'password': 'password',
        'user_type': 'buyer',
        'cart': []
    }
    
    user = User(**user_data)
    assert user.to_dict() == user_data
    assert user.is_buyer()
    assert not user.is_seller()
    
    user_from_dict = User.from_dict(user_data)
    assert user_from_dict == user


def test_user_types():
    """Test user type checking."""
    buyer = User('buyer', 'password', 'buyer', [])
    seller = User('seller', 'password', 'seller', [])
    
    assert buyer.is_buyer()
    assert not buyer.is_seller()
    assert seller.is_seller()
    assert not seller.is_buyer()