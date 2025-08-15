import pytest
@pytest.fixture(scope="module")
def resource_module():
    print("\n[module setup]")
    yield {}
    print("[module teardown]")

@pytest.fixture(scope="function")
def fx_function():
    print("\n[function setup]")
    yield {}
    print("[function teardown]")

@pytest.fixture(scope="class")
def fx_class():
    print("\n[class setup]")
    yield {}
    print("[class teardown]")

class TestExample:
    def test_a(self, fx_function, fx_class, resource_module):
        pass

    def test_b(self, fx_function, fx_class, resource_module):
        pass
