import unittest

from app.matcher import analyze_match, extract_skills
from app.semantic_similarity import semantic_similarity_score


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

        self.assertEqual(report.skill_score, 50)
        self.assertGreater(report.semantic_score, 0)
        self.assertEqual(report.score, round((report.skill_score * 0.7) + (report.semantic_score * 0.3)))
        self.assertEqual(report.scoring_method, "hybrid_skill_overlap_70_semantic_30")
        self.assertEqual(report.matched_skills, ["docker", "python", "sql"])
        self.assertEqual(report.missing_skills, ["aws", "kubernetes", "mlflow"])
        self.assertTrue(report.roadmap)

    def test_handles_job_description_without_known_skills(self):
        report = analyze_match(
            "Python and SQL",
            "We need someone curious, responsible, and energetic.",
        )

        self.assertEqual(report.skill_score, 0)
        self.assertEqual(report.score, report.semantic_score)
        self.assertEqual(report.scoring_method, "semantic_only_no_known_job_skills")
        self.assertEqual(report.job_skills, [])
        self.assertTrue(report.roadmap)


class SemanticSimilarityTests(unittest.TestCase):
    def test_scores_related_text_higher_than_unrelated_text(self):
        related = semantic_similarity_score(
            "Python SQL machine learning model evaluation",
            "Python SQL machine learning model evaluation",
        )
        unrelated = semantic_similarity_score(
            "Python SQL machine learning model evaluation",
            "customer support sales communication",
        )

        self.assertGreater(related, unrelated)
        self.assertEqual(related, 100)


if __name__ == "__main__":
    unittest.main()
