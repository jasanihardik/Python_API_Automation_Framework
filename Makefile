.PHONY: install test smoke regression negative html-report allure-results clean

install:
	pip install -r requirements.txt

test:
	pytest

smoke:
	pytest -m smoke

regression:
	pytest -m regression

negative:
	pytest -m negative

html-report:
	pytest --html=reports/api_test_report.html --self-contained-html

allure-results:
	pytest --alluredir=reports/allure-results

clean:
	rm -rf .pytest_cache reports/* allure-results allure-report
	touch reports/.gitkeep
