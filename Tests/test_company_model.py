from src.models.company_model import CompanyModel

def test_add_company(session):
    company_name = "Test Company"
    company = CompanyModel.add_company(session, company_name)
    assert company.id is not None
    assert company.company_name == company_name
    company2 = CompanyModel.add_company(session, company_name, 0.1)
    assert company2.discount == 0.1

def test_get_company(session):
    company_name = "Test Company"
    created_company = CompanyModel.add_company(session, company_name)
    fetched_company = CompanyModel.get_by_id(session, created_company.id)
    assert fetched_company is not None
    assert fetched_company.id == created_company.id
    assert fetched_company.company_name == company_name


def test_get_companies(session):
    company_name_1 = "Test Company 1"
    company_name_2 = "Test Company 2"
    CompanyModel.add_company(session, company_name_1)
    CompanyModel.add_company(session, company_name_2)
    companies = CompanyModel.get_all(session)
    assert len(companies) == 2
    assert companies[0].company_name in [company_name_1, company_name_2]
    assert companies[1].company_name in [company_name_1, company_name_2]
    

def test_update_company(session):
    company_name = "Test Company"
    new_company_name = "Updated Company"
    created_company = CompanyModel.add_company(session, company_name)
    updated_company = CompanyModel.update_by_id(session, created_company.id, company_name=new_company_name)
    assert updated_company.company_name == new_company_name


def test_delete_company(session):
    company_name = "Test Company"
    created_company = CompanyModel.add_company(session, company_name)
    CompanyModel.delete_by_id(session, created_company.id)
    deleted_company = CompanyModel.get_by_id(session, created_company.id)
    assert deleted_company is None