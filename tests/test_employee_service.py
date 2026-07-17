import pytest

from app.services import employee_service


def test_insert_employee_success(mocker):
    mock_collection = mocker.MagicMock()
    mock_collection.insert_one.return_value = mocker.MagicMock(inserted_id="mocked-id-1")

    mocker.patch.object(employee_service, "employee_collection", mock_collection)

    payload = {"name": "Alice"}
    result = employee_service.insert_employee(payload)

    mock_collection.insert_one.assert_called_once_with(payload)
    assert result["message"] == "Employee Added"
    assert result["id"] == "mocked-id-1"


def test_insert_employee_exception(mocker):
    mock_collection = mocker.MagicMock()
    mock_collection.insert_one.side_effect = Exception("insert failed")
    mocker.patch.object(employee_service, "employee_collection", mock_collection)

    with pytest.raises(Exception):
        employee_service.insert_employee({"name": "Bob"})


def test_get_all_employees_success_and_department_filter(mocker):
    sample_docs = [{"_id": "id1", "name": "A"}, {"_id": "id2", "name": "B"}]

    # create a fake cursor that supports chaining skip().limit()
    mock_cursor = mocker.MagicMock()
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = sample_docs

    mock_collection = mocker.MagicMock()
    mock_collection.count_documents.return_value = 2
    mock_collection.find.return_value = mock_cursor

    mocker.patch.object(employee_service, "employee_collection", mock_collection)

    # without department
    res = employee_service.get_all_employees(page=1, limit=10)
    mock_collection.count_documents.assert_called_once_with({})
    mock_collection.find.assert_called_once()
    assert res["total"] == 2
    assert len(res["data"]) == 2
    assert res["data"][0]["_id"] == "id1"

    # with department filter
    mock_collection.reset_mock()
    mock_collection.count_documents.return_value = 1
    mock_collection.find.return_value = mock_cursor

    res2 = employee_service.get_all_employees(page=2, limit=1, department="HR")
    mock_collection.count_documents.assert_called_once_with({"department": "HR"})
    mock_collection.find.assert_called_once()
    assert res2["page"] == 2
    assert res2["limit"] == 1


def test_get_all_employees_exception(mocker):
    mock_collection = mocker.MagicMock()
    mock_collection.count_documents.side_effect = Exception("count failed")
    mocker.patch.object(employee_service, "employee_collection", mock_collection)

    with pytest.raises(Exception):
        employee_service.get_all_employees()


def test_get_employee_found_and_not_found_and_exception(mocker):
    # Mock ObjectId conversion to a predictable value
    mocker.patch("app.services.employee_service.ObjectId", side_effect=lambda x: f"mocked-{x}")

    mock_collection = mocker.MagicMock()
    mock_collection.find_one.return_value = {"_id": "mocked-123", "name": "Charlie"}
    mocker.patch.object(employee_service, "employee_collection", mock_collection)

    found = employee_service.get_employee("123")
    mock_collection.find_one.assert_called_once_with({"_id": "mocked-123"})
    assert found["name"] == "Charlie"
    assert found["_id"] == "mocked-123"

    # not found
    mock_collection.find_one.return_value = None
    not_found = employee_service.get_employee("999")
    assert not_found == {"message": "Employee Not Found"}

    # exception path
    mock_collection.find_one.side_effect = Exception("find failed")
    with pytest.raises(Exception):
        employee_service.get_employee("err")


def test_update_employee_success_and_exception(mocker):
    mocker.patch("app.services.employee_service.ObjectId", side_effect=lambda x: f"mocked-{x}")

    mock_collection = mocker.MagicMock()
    mock_collection.update_one.return_value = mocker.MagicMock()
    mocker.patch.object(employee_service, "employee_collection", mock_collection)

    payload = {"name": "Delta"}
    res = employee_service.update_employee("123", payload)
    mock_collection.update_one.assert_called_once_with({"_id": "mocked-123"}, {"$set": payload})
    assert res["message"] == "Employee Updated"

    # exception
    mock_collection.update_one.side_effect = Exception("update failed")
    with pytest.raises(Exception):
        employee_service.update_employee("err", payload)


def test_delete_employee_success_and_exception(mocker):
    mocker.patch("app.services.employee_service.ObjectId", side_effect=lambda x: f"mocked-{x}")

    mock_collection = mocker.MagicMock()
    mock_collection.delete_one.return_value = mocker.MagicMock()
    mocker.patch.object(employee_service, "employee_collection", mock_collection)

    res = employee_service.delete_employee("123")
    mock_collection.delete_one.assert_called_once_with({"_id": "mocked-123"})
    assert res["message"] == "Employee Deleted"

    mock_collection.delete_one.side_effect = Exception("delete failed")
    with pytest.raises(Exception):
        employee_service.delete_employee("err")
