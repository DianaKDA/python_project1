"""Test module for marketplace functionality."""
import pytest
from src.marketplace import Marketplace
from src.models import User, Product

@pytest.fixture
def marketplace():
    """Create marketplace instance for testing."""
    return Marketplace()

@pytest.fixture
def test_seller():
    """Create test seller user."""
    return User(
        username="test_seller",
        password="password",
        user_type="seller",
        cart=[]
    )

@pytest.fixture
def test_buyer():
    """Create test buyer user."""
    return User(
        username="test_buyer",
        password="password",
        user_type="buyer",
        cart=[]
    )

class TestMarketplace:
    """Test cases for Marketplace class."""

    def test_user_registration(self, marketplace):
        """Test user registration functionality."""
        # Test successful registration
        assert marketplace.register_user("new_user", "password", "buyer")
        
        # Test duplicate username
        assert not marketplace.register_user("new_user", "password", "buyer")
        
        # Test invalid user type
        with pytest.raises(ValueError):
            marketplace.register_user("another_user", "password", "invalid_type")

    def test_user_login(self, marketplace):
        """Test user login functionality."""
        # Register a test user
        marketplace.register_user("test_user", "password", "buyer")
        
        # Test successful login
        user = marketplace.login_user("test_user", "password")
        assert user is not None
        assert user.username == "test_user"
        
        # Test invalid credentials
        assert marketplace.login_user("test_user", "wrong_password") is None
        assert marketplace.login_user("nonexistent_user", "password") is None

    def test_product_management(self, marketplace, test_seller):
        """Test product management functionality."""
        # Test adding product
        marketplace.add_product(
            test_seller,
            "Test Product",
            100.0,
            "Test Description"
        )
        
        products = marketplace.list_products()
        assert len(products) == 1
        assert products[0].name == "Test Product"
        
        # Test editing product
        marketplace.edit_product(
            test_seller,
            1,  # product_id
            new_name="Updated Product",
            new_price=150.0
        )
        
        products = marketplace.list_products()
        assert products[0].name == "Updated Product"
        assert products[0].price == 150.0
        
        # Test deleting product
        marketplace.delete_product(test_seller, 1)
        assert len(marketplace.list_products()) == 0

    def test_cart_operations(self, marketplace, test_buyer):
        """Test shopping cart functionality."""
        # Add a product first
        seller = User("seller", "password", "seller", [])
        marketplace.add_product(seller, "Test Product", 100.0, "Description")
        
        # Test adding to cart
        marketplace.add_to_cart(test_buyer, 1)  # product_id = 1
        
        # Check cart contents
        cart_items = test_buyer.cart
        assert len(cart_items) == 1
        assert cart_items[0]['name'] == "Test Product"
        
        # Test checkout
        marketplace.checkout(test_buyer)
        assert len(test_buyer.cart) == 0

    def test_unauthorized_operations(self, marketplace, test_buyer, test_seller):
        """Test unauthorized operations are prevented."""
        # Buyer shouldn't be able to add products
        with pytest.raises(ValueError):
            marketplace.add_product(
                test_buyer,
                "Test Product",
                100.0,
                "Description"
            )
        
        # Seller shouldn't be able to add to cart
        marketplace.add_product(
            test_seller,
            "Test Product",
            100.0,
            "Description"
        )
        with pytest.raises(ValueError):
            marketplace.add_to_cart(test_seller, 1)

    def test_product_listing(self, marketplace, test_seller):
        """Test product listing functionality."""
        # Add multiple products
        marketplace.add_product(test_seller, "Product 1", 100.0, "Description 1")
        marketplace.add_product(test_seller, "Product 2", 200.0, "Description 2")
        
        # Test general product listing
        all_products = marketplace.list_products()
        assert len(all_products) == 2
        
        # Test seller-specific product listing
        seller_products = marketplace.list_seller_products(test_seller)
        assert len(seller_products) == 2
        assert all(p.seller == test_seller.username for p in seller_products)

    def test_data_persistence(self, marketplace):
        """Test data persistence between operations."""
        # Register user
        marketplace.register_user("test_user", "password", "buyer")
        
        # Verify user exists after registration
        user = marketplace.login_user("test_user", "password")
        assert user is not None
        
        # Add product and verify it persists
        seller = User("seller", "password", "seller", [])
        marketplace.register_user(seller.username, seller.password, seller.user_type)
        marketplace.add_product(seller, "Test Product", 100.0, "Description")
        
        products = marketplace.list_products()
        assert len(products) == 1
        assert products[0].name == "Test Product"

    @pytest.mark.parametrize("invalid_price", [-100, 0, "invalid"])
    def test_invalid_product_price(self, marketplace, test_seller, invalid_price):
        """Test handling of invalid product prices."""
        with pytest.raises(ValueError):
            marketplace.add_product(
                test_seller,
                "Test Product",
                invalid_price,
                "Description"
            )

    def test_empty_marketplace(self, marketplace):
        """Test behavior with empty marketplace."""
        assert len(marketplace.list_products()) == 0
        
        buyer = User("buyer", "password", "buyer", [])
        marketplace.view_cart(buyer)  # Should not raise error for empty cart
        marketplace.checkout(buyer)   # Should not raise error for empty cart 