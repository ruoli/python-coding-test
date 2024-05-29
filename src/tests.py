import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def upload_pdf(self, file_path, company_name):
        with open(file_path, "rb") as pdf_file:
            files = {
                "file": (os.path.basename(file_path), pdf_file, "application/pdf")
            }
            data = {"company_name": company_name}
            response = self.client.post("/upload/", files=files, data=data)
        return response

    @patch("pdf_service.PdfService.extract")
    def test_upload_healthinc_pdf(self, mock_extract):
        mock_extract.return_value = {
            'Company Name': 'HealthInc',
            'Industry': 'Healthcare',
            'Market Capitalization': 3000,
            'Revenue (in millions)': 1000,
            'EBITDA (in millions)': 250,
            'Net Income (in millions)': 80,
            'Debt (in millions)': 150,
            'Equity (in millions)': 666,
            'Enterprise Value (in millions)': 3150,
            'P/E Ratio': 15,
            'Revenue Growth Rate (%)': 12,
            'EBITDA Margin (%)': 40,
            'Net Income Margin (%)': 8,
            'ROE (Return on Equity) (%)': 13.33,
            'ROA (Return on Assets) (%)': 10,
            'Debt to Equity Ratio': 0.25,
            'Location': 'New York, NY',
            'CEO': 'Jane Smith',
            'Number of Employees': 3000,
        }
        file_path = os.path.abspath(os.path.dirname(__file__) + "/../assets/healthinc.pdf")
        response = self.upload_pdf(file_path, "HealthInc")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Company Name", data)
        self.assertTrue(data["Company Name"]["match"])

    @patch("pdf_service.PdfService.extract")
    def test_upload_retailco_pdf(self, mock_extract):
        mock_extract.return_value = {
            'Company Name': 'RetailCo',
            'Industry': 'Retail',
            'Market Capitalization': 2000,
            'Revenue (in millions)': 800,
            'EBITDA (in millions)': 150,
            'Net Income (in millions)': 40,
            'Debt (in millions)': 110,
            'Equity (in millions)': 400,
            'Enterprise Value (in millions)': 2100,
            'P/E Ratio': 20,
            'Revenue Growth Rate (%)': 8,
            'EBITDA Margin (%)': 18.75,
            'ROE (Return on Equity) (%)': 10,
            'ROA (Return on Assets) (%)': 6.5,
            'Current Ratio': 1.8,
            'Debt to Equity Ratio': 0.25,
            'Location': 'Chicago, IL',
            'CEO': 'Bob Johnson',
            'Number of Employees': 2000,
        }
        file_path = os.path.join(os.path.dirname(__file__), "../assets/retailco.pdf")
        response = self.upload_pdf(file_path, "RetailCo")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Company Name", data)
        self.assertTrue(data["Company Name"]["match"])

    @patch("pdf_service.PdfService.extract")
    def test_upload_financellc_pdf(self, mock_extract):
        mock_extract.return_value = {
            'Company Name': 'FinanceLLC',
            'Industry': 'Financial Services',
            'Market Capitalization': 4500,
            'Revenue (in millions)': 1200,
            'EBITDA (in millions)': 400,
            'Net Income (in millions)': 150,
            'Debt (in millions)': 300,
            'Equity (in millions)': 1000,
            'Enterprise Value (in millions)': 4400,
            'P/E Ratio': 18,
            'Revenue Growth Rate (%)': 15,
            'EBITDA Margin (%)': 33.33,
            'ROE (Return on Equity) (%)': 20,
            'ROA (Return on Assets) (%)': 12,
            'Current Ratio': 3,
            'Debt to Equity Ratio': 0.3,
            'Location': 'Boston, MA',
            'CEO': 'Alice Brown',
            'Number of Employees': 1500,
        }
        file_path = os.path.join(os.path.dirname(__file__), "../assets/financellc.pdf")
        response = self.upload_pdf(file_path, "FinanceLLC")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Company Name", data)
        self.assertTrue(data["Company Name"]["match"])

    @patch("pdf_service.PdfService.extract")
    def test_upload_techcorp_pdf(self, mock_extract):
        mock_extract.return_value = {
            'Company Name': 'TechCorp',
            'Industry': 'Technology',
            'Market Capitalization': 5000,
            'Revenue (in millions)': 1500,
            'EBITDA (in millions)': 300,
            'Net Income (in millions)': 100,
            'Debt (in millions)': 200,
            'Enterprise Value (in millions)': 5400,
            'P/E Ratio': 25,
            'Revenue Growth Rate (%)': 10,
            'EBITDA Margin (%)': 20,
            'Net Income Margin (%)': 6.67,
            'ROE (Return on Equity) (%)': 12.5,
            'ROA (Return on Assets) (%)': 7.5,
            'Current Ratio': 2.5,
            'Debt to Equity Ratio': 0.25,
            'Location': 'San Francisco, CA',
            'CEO': 'John Doe',
            'Number of Employees': 5000,
        }
        file_path = os.path.join(os.path.dirname(__file__), "../assets/techcorp.pdf")
        response = self.upload_pdf(file_path, "TechCorp")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Company Name", data)
        self.assertTrue(data["Company Name"]["match"])

if __name__ == '__main__':
    unittest.main()
