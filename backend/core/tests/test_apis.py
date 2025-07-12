import pytest
from rest_framework.test import APIClient
from core.models import User, Product

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def buyer_user(db):
    return User.objects.create_user(username='buyer', password='pass123', role='buyer')

@pytest.fixture
def seller_user(db):
    return User.objects.create_user(username='seller', password='pass123', role='seller')

@pytest.fixture
def buyer_client(api_client, buyer_user):
    api_client.force_authenticate(user=buyer_user)
    return api_client

@pytest.fixture
def seller_client(api_client, seller_user):
    api_client.force_authenticate(user=seller_user)
    return api_client

@pytest.fixture
def product(seller_user):
    return Product.objects.create(
        seller=seller_user,
        product_name='Water',
        cost=50,
        amount_available=10
    )

def test_deposit_valid_coin(buyer_client):
    response = buyer_client.post('/core/users/deposit/', {'amount': 50})
    assert response.status_code == 200
    assert response.data['deposit'] == 50

def test_deposit_invalid_coin(buyer_client):
    response = buyer_client.post('/core/users/deposit/', {'amount': 3})
    assert response.status_code == 400
    assert 'amount' in response.data
    assert 'Deposit amount must be divisible by 5.' in response.data['amount'][0]

def test_reset_deposit(buyer_client):
    buyer_client.post('/core/users/deposit/', {'amount': 50})
    response = buyer_client.post('/core/users/reset/')
    assert response.status_code == 200
    assert response.data['deposit'] == 0

def test_buy_product_success(buyer_client, product):
    buyer_client.post('/core/users/deposit/', {'amount': 100})
    response = buyer_client.post('/core/users/buy/', {'product_id': product.id, 'quantity': 1})
    assert response.status_code == 200
    assert response.data['product'] == 'Water'
    assert response.data['total_spent'] == 50
    assert isinstance(response.data['change'], dict)

def test_buy_insufficient_deposit(buyer_client, product):
    buyer_client.post('/core/users/deposit/', {'amount': 10})
    response = buyer_client.post('/core/users/buy/', {'product_id': product.id, 'quantity': 1})
    assert response.status_code == 400
    assert 'error' in response.data

def test_buy_product_not_found(buyer_client):
    response = buyer_client.post('/core/users/buy/', {'product_id': 9999, 'quantity': 1})
    assert response.status_code == 400
    assert 'error' in response.data or 'detail' in response.data


def test_buy_not_enough_stock(buyer_client, product):
    buyer_client.post('/core/users/deposit/', {'amount': 500})
    response = buyer_client.post('/core/users/buy/', {'product_id': product.id, 'quantity': 99})
    assert response.status_code == 400
    assert 'error' in response.data


def test_create_product_by_seller(seller_client):
    response = seller_client.post('/core/products/', {
        'product_name': 'Soda',
        'cost': 100,
        'amount_available': 20
    })
    assert response.status_code == 201
    assert response.data['product_name'] == 'Soda'

def test_create_product_by_buyer_fails(buyer_client):
    response = buyer_client.post('/core/products/', {
        'product_name': 'Juice',
        'cost': 100,
        'amount_available': 5
    })
    assert response.status_code == 403
