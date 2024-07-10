from src.models.billing_model import BillingModel
def test_add_billing_data(session):
    # Adding a new billing record
    billing_data = BillingModel.add_billing_data(
        session,
        reservation_id=1,
        license_plate='ABC123',
        name='John Doe',
        address='123 Elm Street',
        email='john.doe@example.com',
        company_name='Doe Inc.',
        tax_ID='123456789',
        user_id=1
    )

    assert billing_data is not None
    assert billing_data.id is not None
    assert billing_data.name == 'John Doe'
    assert billing_data.company_name == 'Doe Inc.'

def test_get_last_by_user_id(session):
    # Adding multiple billing records for the same user
    BillingModel.add_billing_data(
        session,
        reservation_id=2,
        license_plate='XYZ789',
        name='Jane Doe',
        address='456 Oak Street',
        email='jane.doe@example.com',
        user_id=1
    )

    BillingModel.add_billing_data(
        session,
        reservation_id=3,
        license_plate='LMN456',
        name='John Smith',
        address='789 Pine Street',
        email='john.smith@example.com',
        user_id=1
    )

    # Retrieve the last billing record for user_id=1
    last_billing_data = BillingModel.get_last_by_user_id(session, 1)

    assert last_billing_data is not None
    assert last_billing_data.name == 'John Smith'
    assert last_billing_data.license_plate == 'LMN456'

def test_get_last_by_user_id_no_data(session):
    # Retrieve the last billing record for a user_id with no data
    last_billing_data = BillingModel.get_last_by_user_id(session, 2)

    assert last_billing_data is None