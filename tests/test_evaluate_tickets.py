import unittest
from unittest.mock import patch
import pandas as pd
from evaluate_tickets import evaluate_tickets


class TestEvaluateTickets(unittest.TestCase):
    def setUp(self):
        self.sample_data = pd.DataFrame(
            {
                'ticket': ['Order status?', 'Refund request.'],
                'reply': ['Your order will arrive tomorrow.', 'Please provide a photo for refund.'],
            }
        )

    @patch('evaluate_tickets.get_evaluation_from_model')
    def test_evaluate_tickets(self, mock_get_eval):
        mock_get_eval.return_value = {
            'content_score': 5,
            'content_explanation': 'Good content.',
            'format_score': 5,
            'format_explanation': 'Well formatted.',
        }

        result_df = evaluate_tickets(self.sample_data)

        self.assertIn('content_score', result_df.columns)
        self.assertIn('content_explanation', result_df.columns)
        self.assertIn('format_score', result_df.columns)
        self.assertIn('format_explanation', result_df.columns)

        self.assertEqual(mock_get_eval.call_count, len(self.sample_data))

        self.assertTrue((result_df['content_score'] == 5).all())
        self.assertTrue((result_df['format_score'] == 5).all())


if __name__ == '__main__':
    unittest.main()
