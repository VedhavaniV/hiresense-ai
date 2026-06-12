import unittest

from app.matcher import analyze_match, extract_skills


class SkillExtractionTests(unittest.TestCase):
    def test_extracts_known_skills(self):
        text = "I built Python APIs with FastAPI, Docker, SQL, and MLflow."

        skills = extract_skills(text)

        self.assertIn("python", skills)
        self.assertIn("fastapi", skills)
        self.assertIn("docker", skills)
        self.assertIn("sql", skills)
        self.assertIn("mlflow", skills)


class MatchAnalysisTests(unittest.TestCase):
    def test_scores_resume_against_job_description(self):
        resume = "Python SQL Docker FastAPI machine learning"
        job = "We need Python, SQL, Docker, Kubernetes, MLflow, and AWS."

        report = analyze_match(resume, job)

        self.assertEqual(report.score, 50)
        self.assertEqual(report.matched_skills, ["docker", "python", "sql"])
        self.assertEqual(report.missing_skills, ["aws", "kubernetes", "mlflow"])
        self.assertTrue(report.roadmap)

    def test_handles_job_description_without_known_skills(self):
        report = analyze_match(
            "Python and SQL",
            "We need someone curious, responsible, and energetic.",
        )

        self.assertEqual(report.score, 0)
        self.assertEqual(report.job_skills, [])
        self.assertTrue(report.roadmap)


if __name__ == "__main__":
    unittest.main()

